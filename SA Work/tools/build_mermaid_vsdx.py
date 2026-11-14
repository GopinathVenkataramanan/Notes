"""Converts the Mermaid flowcharts in diagrams/mermaids/*.txt into Visio (.vsdx) files.

Run:  python tools\\build_mermaid_vsdx.py        (stdlib only, Python 3.12+)

Writes to diagrams/mermaid-visio/:
  <diagram name>.vsdx           one single-page file per Mermaid diagram
  Mermaid_Diagrams_All.vsdx     every diagram as a page in one file
  preview/<diagram name>.svg    SVG previews of the same layout

Supported Mermaid subset: flowchart/graph TB|TD|BT|LR|RL, node shapes [] () ([]) [[]] [()] (()) {} {{}} >],
subgraphs (nested), links --> --- <--> -.-> -.- ==> with |label| or inline "label" text, chains (A --> B --> C),
'&' node lists and 'style' fill/stroke/color. Layout is a layered (Sugiyama-style) layout per subgraph.
"""
import glob
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reuse the package skeleton that already passes validate_vsdx.py and opens in Visio.
from build_vsdx import CT, REL, VR, NS, DOC_XML, STYLE, app_xml  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "diagrams", "mermaids")
OUT = os.path.join(ROOT, "diagrams", "mermaid-visio")

# Logical reading order for the combined file; any other diagrams are appended alphabetically.
ORDER = [
    "current-state-system-context", "Current-State Application Landscape", "Target SaaS Solution Context",
    "Target SaaS Integration Architecture", "Identity and Security Architecture", "Data Migration Architecture",
    "Environment and Deployment Architecture", "Non-Functional Requirements Architecture",
    "SaaS Shared Responsibility Architecture", "Legacy Decommissioning and Transition Architecture",
    "Revised cost estimation model", "costEstimationTraceablityDiagram", "Backtracking diagram",
    "updatedE2EBacktracking",
]
PAGE_NAMES = {  # Visio page tabs (kept to 31 characters or fewer)
    "current-state-system-context": "Current-State Context",
    "Current-State Application Landscape": "Current-State Landscape",
    "Target SaaS Integration Architecture": "Target SaaS Integration",
    "Identity and Security Architecture": "Identity and Security",
    "Environment and Deployment Architecture": "Environment and Deployment",
    "Non-Functional Requirements Architecture": "Non-Functional Requirements",
    "SaaS Shared Responsibility Architecture": "SaaS Shared Responsibility",
    "Legacy Decommissioning and Transition Architecture": "Legacy Decommissioning",
    "Revised cost estimation model": "Revised Cost Estimation Model",
    "costEstimationTraceablityDiagram": "Cost Estimation Traceability",
    "Backtracking diagram": "Backtracking Diagram",
    "updatedE2EBacktracking": "Updated E2E Backtracking",
}
TITLES = {  # friendlier page titles for camelCase file names
    "current-state-system-context": "Current-State System Context",
    "costEstimationTraceablityDiagram": "Cost Estimation Traceability",
    "updatedE2EBacktracking": "Updated End-to-End Backtracking",
    "Backtracking diagram": "Backtracking Diagram",
    "Revised cost estimation model": "Revised Cost Estimation Model",
}

# ----------------------------------------------------------------- styling (inches)
FONT = 0.125            # node text size (9 pt)
LABEL_FONT = 0.105      # edge label size
CLUSTER_FONT = 0.13
NODE_FILL, NODE_LINE, NODE_TEXT = "#DDEBF7", "#2E75B6", "#000000"
DATA_FILL, DATA_LINE = "#FFF2CC", "#BF9000"
CLUSTER_FILL = ["#F4F7FB", "#FBFBF3", "#F7F4FA"]
CLUSTER_LINE, CLUSTER_TEXT = "#8EA9C1", "#1F3864"
EDGE_COLOR = "#404040"
PAD, HEADER = 0.22, 0.34   # cluster inner padding and title band
MARGIN, TITLE_H = 0.5, 0.85
MIN_PW, MIN_PH = 11.0, 8.5


# ----------------------------------------------------------------- parsing
SHAPES = [("[(", ")]", "cyl"), ("([", "])", "stadium"), ("[[", "]]", "sub"), ("((", "))", "circle"),
          ("{{", "}}", "hex"), ("[", "]", "rect"), ("(", ")", "round"), ("{", "}", "diamond"), (">", "]", "flag")]
ARROWS = [(re.compile(p), s, h) for p, s, h in [
    (r'<-\.+->', "dot", "both"), (r'<={2,}>', "thick", "both"), (r'<-{2,}>', "solid", "both"),
    (r'-\.\s*"([^"]*)"\s*\.+->', "dot", "end"), (r'-\.\s+([^"]+?)\s+\.+->', "dot", "end"),
    (r'==\s*"([^"]*)"\s*={2,}>', "thick", "end"), (r'==\s+([^"]+?)\s+={2,}>', "thick", "end"),
    (r'--\s*"([^"]*)"\s*-{2,}>', "solid", "end"), (r'--\s+([^"]+?)\s+-{2,}>', "solid", "end"),
    (r'-\.+->', "dot", "end"), (r'-\.+-', "dot", "none"), (r'={2,}>', "thick", "end"),
    (r'={3,}', "thick", "none"), (r'-{2,}>', "solid", "end"), (r'-{3,}', "solid", "none")]]
ID_RE = re.compile(r"[A-Za-z0-9_]+")
PIPE_RE = re.compile(r'\|\s*"?([^|"]*)"?\s*\|')


def clean_text(t):
    t = re.sub(r"<br\s*/?>", "\n", t.strip().strip('"'), flags=re.I)
    return t.replace("#quot;", '"').replace("&amp;", "&")


class Diagram:
    def __init__(self, name, text):
        self.name = name
        self.direction = "TB"
        self.nodes = {}       # id -> dict(label, shape, parent, fill, stroke, color)
        self.subs = {}        # id -> dict(label, parent)
        self.children = {None: []}
        self.edges = []       # dict(a, b, label, style, head)
        self._stack = []
        self._parse(text)

    # --- helpers
    def _add_child(self, parent, item):
        self.children.setdefault(parent, []).append(item)

    def _node(self, nid, label=None, shape=None):
        if nid in self.subs:
            return
        if nid not in self.nodes:
            parent = self._stack[-1] if self._stack else None
            self.nodes[nid] = dict(label=nid, shape="rect", parent=parent, fill=None, stroke=None, color=None)
            self._add_child(parent, nid)
        if label is not None:
            self.nodes[nid]["label"] = clean_text(label)
        if shape:
            self.nodes[nid]["shape"] = shape

    def _parse_node(self, line, pos):
        m = ID_RE.match(line, pos)
        if not m:
            return None, pos
        nid, pos = m.group(0), m.end()
        label = shape = None
        for op, cl, kind in SHAPES:
            if line.startswith(op, pos):
                j = pos + len(op)
                if j < len(line) and line[j] == '"':
                    k = line.index('"', j + 1)
                    label, end = line[j + 1:k], line.index(cl, k + 1)
                else:
                    end = line.index(cl, j)
                    label = line[j:end]
                pos, shape = end + len(cl), kind
                break
        m = re.compile(r":::[\w-]+").match(line, pos)
        if m:
            pos = m.end()
        self._node(nid, label, shape)
        return nid, pos

    def _parse_group(self, line, pos):
        ids = []
        while True:
            pos = _ws(line, pos)
            nid, pos = self._parse_node(line, pos)
            if nid is None:
                break
            ids.append(nid)
            p2 = _ws(line, pos)
            if p2 < len(line) and line[p2] == "&":
                pos = p2 + 1
                continue
            break
        return ids, pos

    def _statement(self, line):
        groups, ops, pos = [], [], 0
        while True:
            ids, pos = self._parse_group(line, pos)
            if not ids:
                break
            groups.append(ids)
            pos = _ws(line, pos)
            for rx, style, head in ARROWS:
                m = rx.match(line, pos)
                if m:
                    break
            else:
                break
            label = m.group(1) if m.groups() else ""
            pos = _ws(line, m.end())
            pm = PIPE_RE.match(line, pos)
            if pm:
                label, pos = pm.group(1), pm.end()
            ops.append((style, head, clean_text(label or "")))
        for i, (style, head, label) in enumerate(ops[:len(groups) - 1]):
            for a in groups[i]:
                for b in groups[i + 1]:
                    self.edges.append(dict(a=a, b=b, label=label, style=style, head=head))

    def _parse(self, text):
        for raw in text.splitlines():
            line = raw.strip().rstrip(";")
            if not line or line.startswith("%%"):
                continue
            m = re.match(r"(?:flowchart|graph)\s+(TB|TD|BT|LR|RL)\b", line)
            if m:
                self.direction = "TB" if m.group(1) == "TD" else m.group(1)
                continue
            m = re.match(r'subgraph\s+(.*)$', line)
            if m:
                body = m.group(1).strip()
                mm = re.match(r'([\w-]+)\s*\[\s*"?(.*?)"?\s*\]$', body)
                sid, label = (mm.group(1), mm.group(2)) if mm else (
                    (body, body) if ID_RE.fullmatch(body) else (f"sg{len(self.subs)}", clean_text(body)))
                parent = self._stack[-1] if self._stack else None
                self.subs[sid] = dict(label=clean_text(label), parent=parent)
                self.children.setdefault(sid, [])
                self._add_child(parent, sid)
                self._stack.append(sid)
                continue
            if line == "end":
                if self._stack:
                    self._stack.pop()
                continue
            m = re.match(r"style\s+([\w-]+)\s+(.*)$", line)
            if m:
                if m.group(1) in self.nodes:
                    for kv in m.group(2).split(","):
                        k, _, v = kv.partition(":")
                        k, v = k.strip(), v.strip()
                        if k in ("fill", "stroke", "color") and re.fullmatch(r"#[0-9A-Fa-f]{3,6}", v):
                            self.nodes[m.group(1)][k] = _hex6(v)
                continue
            if re.match(r"(classDef|class|linkStyle|direction|click)\b", line):
                continue
            self._statement(line)

    def parent(self, item):
        return self.nodes[item]["parent"] if item in self.nodes else self.subs[item]["parent"]


def _ws(line, pos):
    while pos < len(line) and line[pos] in " \t":
        pos += 1
    return pos


def _hex6(v):
    v = v.upper()
    return "#" + "".join(c * 2 for c in v[1:]) if len(v) == 4 else v


def _darken(hexc, f=0.6):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))


# ----------------------------------------------------------------- text metrics
def text_w(s, size, bold=False):
    w = 0.0
    for ch in s:
        w += 0.64 if ch.isupper() or ch.isdigit() else 0.27 if ch in " .,;:'|!il/" else 0.52
    return w * size * (1.07 if bold else 1.0)


def wrap(text, maxc=24):
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            if line and len(line) + 1 + len(word) > maxc:
                out.append(line)
                line = word
            else:
                line = f"{line} {word}" if line else word
        out.append(line)
    return out


def node_size(n):
    lines = wrap(n["label"])
    bold = n["label"].isupper()
    w = max(1.25, max(text_w(ln, FONT, bold) for ln in lines) + 0.38)
    h = max(0.55, len(lines) * FONT * 1.3 + 0.3)
    if n["shape"] == "cyl":
        h += 0.22
    elif n["shape"] in ("diamond", "hex"):
        w, h = w * 1.35, h * 1.35
    elif n["shape"] == "circle":
        w = h = max(w, h)
    return w, h, lines, bold


# ----------------------------------------------------------------- layout
def _reaches(adj, s, t):
    stack, seen = [s], {s}
    while stack:
        u = stack.pop()
        if u == t:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


def _pav(desired, sizes, gap):
    """Closest positions to `desired` (least squares) that keep order and minimum spacing."""
    off = [0.0]
    for i in range(1, len(sizes)):
        off.append(off[-1] + sizes[i - 1] / 2 + gap + sizes[i] / 2)
    blocks = []
    for v in (d - o for d, o in zip(desired, off)):
        blocks.append([v, 1])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            s, c = blocks.pop()
            blocks[-1][0] += s
            blocks[-1][1] += c
    res = []
    for s, c in blocks:
        res += [s / c] * c
    return [r + o for r, o in zip(res, off)]


class Layout:
    def __init__(self, d: Diagram):
        self.d = d
        self.m = 1 if d.direction in ("TB", "BT") else 0     # main (rank) axis: 1 = y, 0 = x
        self.flip = d.direction in ("BT", "RL")
        self.size, self.rel, self.info = {}, {}, {}
        for nid, n in d.nodes.items():
            w, h, lines, bold = node_size(n)
            self.size[nid] = (w, h)
            self.info[nid] = (lines, bold)
        self.no_edges = not d.edges
        self._group(None)
        self.abs = {}
        self._place(None, 0.0, 0.0)

    def _level_item(self, x, gid):
        while x is not None and self.d.parent(x) != gid:
            x = self.d.parent(x)
        return x

    def _group(self, gid):
        d, m = self.d, self.m
        items = d.children.get(gid, [])
        for it in items:
            if it in d.subs:
                self._group(it)
        # Aggregate links per item pair: one-way links vote with weight 1, two-way links only break ties,
        # remaining ties follow definition order (so a subgraph declared later sits further down-stream).
        idx = {it: k for k, it in enumerate(items)}
        votes, labelled = {}, False
        for e in d.edges:
            a, b = self._level_item(e["a"], gid), self._level_item(e["b"], gid)
            if a is None or b is None or a == b:
                continue
            labelled |= bool(e["label"])
            key = (a, b) if idx[a] < idx[b] else (b, a)
            sign = 1 if key == (a, b) else -1
            v = votes.setdefault(key, [0.0, 0.0, len(votes)])
            v[0 if e["head"] != "both" else 1] += sign
        pairs = []
        for (a, b), (uv, bv, first) in votes.items():
            fwd = uv > 0 or (uv == 0 and bv >= 0)
            pairs.append((-abs(uv), first, (a, b) if fwd else (b, a)))
        adj = {i: [] for i in items}
        for _, _, (a, b) in sorted(pairs):  # strongest pairs first, so weak ones never force a cycle
            if _reaches(adj, b, a):
                adj[b].append(a)
            else:
                adj[a].append(b)
        preds = {i: [] for i in items}
        for a in items:
            for b in adj[a]:
                preds[b].append(a)
        # longest-path ranking on the DAG
        indeg = {i: len(preds[i]) for i in items}
        topo, queue = [], [i for i in items if indeg[i] == 0]
        while queue:
            u = queue.pop(0)
            topo.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)
        rank = {i: 0 for i in items}
        for u in topo:
            for v in adj[u]:
                rank[v] = max(rank[v], rank[u] + 1)
        for u in reversed(topo):  # pull sources next to their first successor
            if not preds[u] and adj[u]:
                rank[u] = min(rank[v] for v in adj[u]) - 1
        if self.no_edges and gid is not None and all(i in d.nodes for i in items):
            rank = {it: k for k, it in enumerate(items)}  # edge-less list: stack along the main axis
        if items:
            lo = min(rank.values())
            rank = {k: v - lo for k, v in rank.items()}
        nbrs = {i: [] for i in items}
        for a in items:
            for b in adj[a]:
                nbrs[a].append(b)
                nbrs[b].append(a)
        R = max(rank.values()) + 1 if items else 0
        layers = [[i for i in items if rank[i] == r] for r in range(R)]
        pos = {i: k for L in layers for k, i in enumerate(L)}
        # barycentre crossing reduction
        for sweep in range(8):
            down = sweep % 2 == 0
            for r in (range(1, R) if down else range(R - 2, -1, -1)):
                def key(n, r=r, down=down):
                    nb = [pos[v] for v in nbrs[n] if (rank[v] < r if down else rank[v] > r)]
                    return sum(nb) / len(nb) if nb else pos[n]
                layers[r].sort(key=key)
                for k, i in enumerate(layers[r]):
                    pos[i] = k
        c = 1 - m
        gap_c = 0.32 if m == 1 else 0.26
        gap_m = (0.6 if m == 1 else 0.7) + (0.3 if labelled else 0)
        sc = {i: self.size[i][c] for i in items}
        smain = {i: self.size[i][m] for i in items}
        cpos = {}
        for L in layers:
            p = _pav([0.0] * len(L), [sc[i] for i in L], gap_c)
            shift = (p[0] + p[-1]) / 2 if p else 0
            for i, v in zip(L, p):
                cpos[i] = v - shift
        for it in range(16):
            order = range(R) if it % 2 == 0 else range(R - 1, -1, -1)
            for r in order:
                L = layers[r]
                desired = []
                for n in L:
                    nb = [cpos[v] for v in nbrs[n] if rank[v] != r]
                    desired.append(sum(nb) / len(nb) if nb else cpos[n])
                for n, v in zip(L, _pav(desired, [sc[i] for i in L], gap_c)):
                    cpos[n] = v
        thick = [max((smain[i] for i in L), default=0) for L in layers]
        mpos, acc = [], 0.0
        for t in thick:
            mpos.append(acc + t / 2)
            acc += t + gap_m
        total_m = acc - gap_m if layers else 0
        if items:
            cmin = min(cpos[i] - sc[i] / 2 for i in items)
            cmax = max(cpos[i] + sc[i] / 2 for i in items)
        else:
            cmin = cmax = 0
        for i in items:
            mv = mpos[rank[i]]
            if self.flip:
                mv = total_m - mv
            cv = cpos[i] - cmin
            self.rel[i] = (cv, mv) if m == 1 else (mv, cv)
        cw, chh = (cmax - cmin, total_m) if m == 1 else (total_m, cmax - cmin)
        if gid is not None:
            label_w = text_w(d.subs[gid]["label"], CLUSTER_FONT, True) + 0.3
            w = max(cw, label_w) + 2 * PAD
            h = chh + 2 * PAD + HEADER
            self.size[gid] = (w, h)
            self.content = None
            self.subs_inner = getattr(self, "subs_inner", {})
            self.subs_inner[gid] = (PAD + (w - 2 * PAD - cw) / 2, PAD + HEADER)
        else:
            self.root_size = (cw, chh)

    def _place(self, gid, ox, oy):
        for it in self.d.children.get(gid, []):
            cx, cy = self.rel[it]
            w, h = self.size[it]
            x0, y0 = ox + cx - w / 2, oy + cy - h / 2
            self.abs[it] = (x0, y0, x0 + w, y0 + h)
            if it in self.d.subs:
                ix, iy = self.subs_inner[it]
                self._place(it, x0 + ix, y0 + iy)


# ----------------------------------------------------------------- edge routing
def _seg_hits(p, q, box, eps=0.03):
    x0, y0, x1, y1 = box[0] + eps, box[1] + eps, box[2] - eps, box[3] - eps
    sx0, sx1 = sorted((p[0], q[0]))
    sy0, sy1 = sorted((p[1], q[1]))
    return sx1 > x0 and sx0 < x1 and sy1 > y0 and sy0 < y1


def route(S, T, obstacles, m):
    """Orthogonal route between boxes S and T avoiding obstacle boxes where possible."""
    lo = lambda B, a: B[a]
    hi = lambda B, a: B[a + 2]
    mid = lambda B, a: (B[a] + B[a + 2]) / 2
    cands = []
    main_sep = hi(S, m) <= lo(T, m) + 1e-6 or hi(T, m) <= lo(S, m) + 1e-6
    for ax in (m, 1 - m):
        ox = 1 - ax

        def Q(av, ov, ax=ax, ox=ox):
            p = [0.0, 0.0]
            p[ax], p[ox] = av, ov
            return tuple(p)
        if ax != m and main_sep:
            continue  # boxes in different ranks always connect through their rank-facing sides
        fwd, back = hi(S, ax) <= lo(T, ax) + 1e-6, hi(T, ax) <= lo(S, ax) + 1e-6
        if fwd or back:
            sf, tf = (hi(S, ax), lo(T, ax)) if fwd else (lo(S, ax), hi(T, ax))
            olo, ohi = max(lo(S, ox), lo(T, ox)), min(hi(S, ox), hi(T, ox))
            if ohi - olo > 0.15:
                v = (olo + ohi) / 2
                cands.append(([Q(sf, v), Q(tf, v)], 0))
            ms, mt = mid(S, ox), mid(T, ox)
            if abs(ms - mt) > 0.01:
                dirn = 1 if fwd else -1
                g = min(0.3, abs(tf - sf) / 2)
                for b in ((sf + tf) / 2, sf + dirn * g, tf - dirn * g):
                    cands.append(([Q(sf, ms), Q(b, ms), Q(b, mt), Q(tf, mt)], 0.15))
            else:
                dirn = 1 if fwd else -1
                g = min(0.3, abs(tf - sf) / 2)
            # channel routes: step out of the source, run along a free lane between obstacles, step into the target
            span0, span1 = sorted((sf, tf))
            lanes = {ms, mt}
            for o in obstacles:
                if o[ax + 2] > span0 and o[ax] < span1:
                    lanes.update((o[ox] - 0.14, o[ox + 2] + 0.14))
            for b1 in (sf + dirn * g, (sf + tf) / 2):
                for b2 in (tf - dirn * g,):
                    if (b2 - b1) * dirn <= 0:
                        continue
                    for X in lanes:
                        pts = [Q(sf, ms), Q(b1, ms), Q(b1, X), Q(b2, X), Q(b2, mt), Q(tf, mt)]
                        pts = [p for k, p in enumerate(pts) if k == 0 or p != pts[k - 1]]
                        cands.append((pts, 0.3))
    # U-shaped detours around everything between the two boxes
    for ax in (1 - m, m):
        ox = 1 - ax

        def Q(av, ov, ax=ax, ox=ox):
            p = [0.0, 0.0]
            p[ax], p[ox] = av, ov
            return tuple(p)
        ms, mt = mid(S, ox), mid(T, ox)
        a0, a1 = min(lo(S, ox), lo(T, ox)), max(hi(S, ox), hi(T, ox))
        between = [o for o in obstacles if o[ox + 2] > a0 and o[ox] < a1] + [S, T]
        for side in (1, -1):
            X = (max(hi(o, ax) for o in between) + 0.28) if side > 0 else (min(lo(o, ax) for o in between) - 0.28)
            fs, ft = (hi(S, ax), hi(T, ax)) if side > 0 else (lo(S, ax), lo(T, ax))
            cands.append(([Q(fs, ms), Q(X, ms), Q(X, mt), Q(ft, mt)], 0.6))
    best = None
    for pts, pen in cands:
        hits = sum(1 for o in obstacles for p, q in zip(pts, pts[1:]) if _seg_hits(p, q, o))
        length = sum(abs(p[0] - q[0]) + abs(p[1] - q[1]) for p, q in zip(pts, pts[1:]))
        score = hits * 100 + length + 0.2 * (len(pts) - 2) + pen
        if best is None or score < best[0]:
            best = (score, pts)
    return best[1]


# ----------------------------------------------------------------- page model
class Page:
    def __init__(self, stem, d: Diagram):
        self.name = PAGE_NAMES.get(stem, stem)[:31]
        self.title = TITLES.get(stem, stem)
        lay = Layout(d)
        cw, ch = lay.root_size
        self.PW = max(MIN_PW, cw + 2 * MARGIN)
        self.PH = max(MIN_PH, ch + 2 * MARGIN + TITLE_H + 0.3)
        ox = (self.PW - cw) / 2
        oy = MARGIN + TITLE_H + (self.PH - 2 * MARGIN - TITLE_H - 0.3 - ch) / 2
        boxes = {k: (b[0] + ox, b[1] + oy, b[2] + ox, b[3] + oy) for k, b in lay.abs.items()}
        self.items = []
        self.text(MARGIN, 0.3, self.PW - 2 * MARGIN, 0.4, self.title, 0.22, True, "l", "#1F3864")
        self.text(MARGIN, 0.68, self.PW - 2 * MARGIN, 0.25,
                  f"{d.direction} flowchart converted from diagrams/mermaids/{stem}.txt",
                  0.1, False, "l", "#7F7F7F")

        def depth(s):
            k = 0
            while d.subs[s]["parent"] is not None:
                s, k = d.subs[s]["parent"], k + 1
            return k
        for sid in sorted(d.subs, key=depth):  # outer clusters first so inner ones sit on top
            x0, y0, x1, y1 = boxes[sid]
            self.items.append(dict(t="box", x=x0, y=y0, w=x1 - x0, h=y1 - y0, geom="rect", round=0.06,
                                   fill=CLUSTER_FILL[depth(sid) % len(CLUSTER_FILL)], line=CLUSTER_LINE,
                                   text=d.subs[sid]["label"], size=CLUSTER_FONT, bold=True, color=CLUSTER_TEXT,
                                   ha="l", va="t", lw=0.0125))
        node_boxes = {k: boxes[k] for k in d.nodes}
        for e in d.edges:
            S, T = boxes[e["a"]], boxes[e["b"]]
            obst = [b for k, b in node_boxes.items() if k not in (e["a"], e["b"])]
            pts = route(S, T, obst, lay.m)
            self.items.append(dict(t="line", pts=pts, style=e["style"], head=e["head"]))
            if e["label"]:
                segs = list(zip(pts, pts[1:]))
                p, q = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
                lines = wrap(e["label"], 22)
                w = max(text_w(ln, LABEL_FONT) for ln in lines) + 0.16
                h = len(lines) * LABEL_FONT * 1.3 + 0.08
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                self.text(mx - w / 2, my - h / 2, w, h, "\n".join(lines), LABEL_FONT, False, "c", "#404040",
                          fill="#FFFFFF")
        for nid, n in d.nodes.items():
            x0, y0, x1, y1 = boxes[nid]
            lines, bold = lay.info[nid]
            fill = n["fill"] or (DATA_FILL if n["shape"] == "cyl" else NODE_FILL)
            line = n["stroke"] or (_darken(n["fill"]) if n["fill"] else (DATA_LINE if n["shape"] == "cyl" else NODE_LINE))
            rnd = {"round": 0.12, "stadium": (y1 - y0) / 2}.get(n["shape"], 0.05)
            geom = {"cyl": "cyl", "diamond": "diamond", "circle": "ellipse", "hex": "hex"}.get(n["shape"], "rect")
            self.items.append(dict(t="box", x=x0, y=y0, w=x1 - x0, h=y1 - y0, geom=geom, round=rnd, fill=fill,
                                   line=line, text="\n".join(lines), size=FONT, bold=bold,
                                   color=n["color"] or NODE_TEXT, ha="c", va="m", lw=0.0139))

    def text(self, x, y, w, h, t, size, bold, ha, color, fill=None):
        self.items.append(dict(t="box", x=x, y=y, w=w, h=h, geom="rect", round=0, fill=fill, line=None, text=t,
                               size=size, bold=bold, color=color, ha=ha, va="m", lw=0.01))

    # --- Visio
    def vsdx_xml(self):
        PH, out = self.PH, []
        for sid, it in enumerate(self.items, 1):
            if it["t"] == "line":
                xs = [p[0] for p in it["pts"]]
                ys = [PH - p[1] for p in it["pts"]]
                minx, miny = min(xs), min(ys)
                w, h = max(max(xs) - minx, 0.01), max(max(ys) - miny, 0.01)
                rows = "".join(
                    f'<Row T="{"MoveTo" if i == 0 else "LineTo"}" IX="{i + 1}">'
                    f'<Cell N="X" V="{px - minx:.4f}"/><Cell N="Y" V="{py - miny:.4f}"/></Row>'
                    for i, (px, py) in enumerate(zip(xs, ys)))
                pattern = {"solid": 1, "thick": 1, "dot": 3}[it["style"]]
                weight = 0.025 if it["style"] == "thick" else 0.0139
                arrows = ""
                if it["head"] in ("end", "both"):
                    arrows += '<Cell N="EndArrow" V="4"/><Cell N="EndArrowSize" V="2"/>'
                if it["head"] == "both":
                    arrows += '<Cell N="BeginArrow" V="4"/><Cell N="BeginArrowSize" V="2"/>'
                out.append(
                    f'<Shape ID="{sid}" Type="Shape" LineStyle="{STYLE}" FillStyle="{STYLE}" TextStyle="{STYLE}">'
                    f'<Cell N="PinX" V="{minx + w / 2:.4f}"/><Cell N="PinY" V="{miny + h / 2:.4f}"/>'
                    f'<Cell N="Width" V="{w:.4f}"/><Cell N="Height" V="{h:.4f}"/>'
                    f'<Cell N="LocPinX" V="{w / 2:.4f}"/><Cell N="LocPinY" V="{h / 2:.4f}"/>'
                    f'<Cell N="LineColor" V="{EDGE_COLOR}"/><Cell N="LineWeight" V="{weight}"/>'
                    f'<Cell N="LinePattern" V="{pattern}"/><Cell N="FillPattern" V="0"/>{arrows}'
                    f'<Section N="Geometry" IX="0"><Cell N="NoFill" V="1"/>{rows}</Section></Shape>')
                continue
            x, w, h = it["x"], it["w"], it["h"]
            y = PH - it["y"] - h
            fill = it["fill"]
            out.append(
                f'<Shape ID="{sid}" Type="Shape" LineStyle="{STYLE}" FillStyle="{STYLE}" TextStyle="{STYLE}">'
                f'<Cell N="PinX" V="{x + w / 2:.4f}"/><Cell N="PinY" V="{y + h / 2:.4f}"/>'
                f'<Cell N="Width" V="{w:.4f}"/><Cell N="Height" V="{h:.4f}"/>'
                f'<Cell N="LocPinX" V="{w / 2:.4f}"/><Cell N="LocPinY" V="{h / 2:.4f}"/>'
                f'<Cell N="FillForegnd" V="{fill or "#FFFFFF"}"/><Cell N="FillPattern" V="{1 if fill else 0}"/>'
                f'<Cell N="LineColor" V="{it["line"] or "#000000"}"/><Cell N="LineWeight" V="{it["lw"]}"/>'
                f'<Cell N="LinePattern" V="{1 if it["line"] else 0}"/>'
                f'<Cell N="Rounding" V="{it["round"] if it["geom"] == "rect" else 0:.4f}"/>'
                f'<Cell N="VerticalAlign" V="{0 if it["va"] == "t" else 1}"/>'
                f'<Cell N="LeftMargin" V="{0.1 if it["ha"] == "l" else 0.06}"/><Cell N="RightMargin" V="0.06"/>'
                f'<Cell N="TopMargin" V="{0.24 if it["geom"] == "cyl" else 0.06}"/><Cell N="BottomMargin" V="0.05"/>'
                f'{_geometry(it["geom"], w, h, bool(fill), bool(it["line"]))}'
                f'<Section N="Character"><Row IX="0"><Cell N="Size" V="{it["size"]}"/>'
                f'<Cell N="Color" V="{it["color"]}"/><Cell N="Style" V="{1 if it["bold"] else 0}"/></Row></Section>'
                f'<Section N="Paragraph"><Row IX="0"><Cell N="HorzAlign" V="{0 if it["ha"] == "l" else 1}"/></Row></Section>'
                f'<Text>{escape(it["text"])}</Text></Shape>')
        return ('<?xml version="1.0" encoding="utf-8"?>'
                f'<PageContents {NS} xml:space="preserve"><Shapes>{"".join(out)}</Shapes></PageContents>')

    # --- SVG preview
    def svg(self):
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.PW:.3f} {self.PH:.3f}" '
             f'width="{self.PW * 100:.0f}" height="{self.PH * 100:.0f}" font-family="Calibri,Segoe UI,Arial">'
             '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse">'
             f'<path d="M0,0 L8,4 L0,8 z" fill="{EDGE_COLOR}"/></marker></defs>'
             f'<rect width="{self.PW}" height="{self.PH}" fill="#fff"/>']
        for it in self.items:
            if it["t"] == "line":
                p = " ".join(f"{x:.3f},{y:.3f}" for x, y in it["pts"])
                dash = 'stroke-dasharray="0.04 0.04"' if it["style"] == "dot" else ""
                sw = 0.025 if it["style"] == "thick" else 0.0139
                me = 'marker-end="url(#a)"' if it["head"] in ("end", "both") else ""
                ms = 'marker-start="url(#a)"' if it["head"] == "both" else ""
                s.append(f'<polyline points="{p}" fill="none" stroke="{EDGE_COLOR}" stroke-width="{sw}" {dash} {me} {ms}/>')
                continue
            x, y, w, h = it["x"], it["y"], it["w"], it["h"]
            fill, line = it["fill"] or "none", it["line"] or "none"
            st = f'fill="{fill}" stroke="{line}" stroke-width="{it["lw"]}"'
            if it["geom"] == "cyl":
                ry = 0.1
                s.append(f'<path d="M{x},{y + ry} a{w / 2},{ry} 0 0 0 {w},0 v{h - 2 * ry} a{w / 2},{ry} 0 0 1 {-w},0 z" {st}/>'
                         f'<ellipse cx="{x + w / 2}" cy="{y + ry}" rx="{w / 2}" ry="{ry}" {st}/>')
            elif it["geom"] == "diamond":
                s.append(f'<polygon points="{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}" {st}/>')
            elif it["geom"] == "ellipse":
                s.append(f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" {st}/>')
            elif it["fill"] or it["line"]:
                s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{it["round"]}" {st}/>')
            lines = it["text"].split("\n")
            lh = it["size"] * 1.2
            if it["va"] == "t":
                ty = y + 0.08 + it["size"]
            else:
                off = 0.12 if it["geom"] == "cyl" else 0
                ty = y + off + (h - off) / 2 - (len(lines) - 1) * lh / 2 + it["size"] * 0.35
            tx, anc = (x + 0.1, "start") if it["ha"] == "l" else (x + w / 2, "middle")
            for i, ln in enumerate(lines):
                s.append(f'<text x="{tx:.3f}" y="{ty + i * lh:.3f}" font-size="{it["size"]}" text-anchor="{anc}" '
                         f'fill="{it["color"]}" font-weight="{"bold" if it["bold"] else "normal"}">{escape(ln)}</text>')
        s.append("</svg>")
        return "".join(s)


def _geometry(kind, w, h, filled, lined):
    head = f'<Cell N="NoFill" V="{0 if filled else 1}"/><Cell N="NoLine" V="{0 if lined else 1}"/>'

    def poly(pts, ix=0, nofill=None):
        hd = head if nofill is None else f'<Cell N="NoFill" V="{nofill}"/><Cell N="NoLine" V="0"/>'
        rows = "".join(f'<Row T="{"MoveTo" if i == 0 else "LineTo"}" IX="{i + 1}">'
                       f'<Cell N="X" V="{px:.4f}"/><Cell N="Y" V="{py:.4f}"/></Row>' for i, (px, py) in enumerate(pts))
        return f'<Section N="Geometry" IX="{ix}">{hd}{rows}</Section>'
    if kind == "diamond":
        return poly([(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2), (w / 2, 0)])
    if kind == "hex":
        k = min(0.2, w / 4)
        return poly([(k, 0), (w - k, 0), (w, h / 2), (w - k, h), (k, h), (0, h / 2), (k, 0)])
    if kind == "ellipse":
        return (f'<Section N="Geometry" IX="0">{head}<Row T="Ellipse" IX="1"><Cell N="X" V="{w / 2:.4f}"/>'
                f'<Cell N="Y" V="{h / 2:.4f}"/><Cell N="A" V="{w:.4f}"/><Cell N="B" V="{h / 2:.4f}"/>'
                f'<Cell N="C" V="{w / 2:.4f}"/><Cell N="D" V="{h:.4f}"/></Row></Section>')
    if kind == "cyl":
        ry = 0.1
        dr = (w / 2) / ry  # ellipse major/minor ratio for EllipticalArcTo

        def arc(ix, x, y, a, b):
            return (f'<Row T="EllipticalArcTo" IX="{ix}"><Cell N="X" V="{x:.4f}"/><Cell N="Y" V="{y:.4f}"/>'
                    f'<Cell N="A" V="{a:.4f}"/><Cell N="B" V="{b:.4f}"/><Cell N="C" V="0"/><Cell N="D" V="{dr:.4f}"/></Row>')
        body = (f'<Section N="Geometry" IX="0">{head}'
                f'<Row T="MoveTo" IX="1"><Cell N="X" V="0"/><Cell N="Y" V="{ry:.4f}"/></Row>'
                + arc(2, w, ry, w / 2, 0)
                + f'<Row T="LineTo" IX="3"><Cell N="X" V="{w:.4f}"/><Cell N="Y" V="{h - ry:.4f}"/></Row>'
                + arc(4, 0, h - ry, w / 2, h)
                + f'<Row T="LineTo" IX="5"><Cell N="X" V="0"/><Cell N="Y" V="{ry:.4f}"/></Row></Section>')
        lid = (f'<Section N="Geometry" IX="1"><Cell N="NoFill" V="1"/><Cell N="NoLine" V="0"/>'
               f'<Row T="MoveTo" IX="1"><Cell N="X" V="0"/><Cell N="Y" V="{h - ry:.4f}"/></Row>'
               + arc(2, w, h - ry, w / 2, h - 2 * ry) + '</Section>')
        return body + lid
    return poly([(0, 0), (w, 0), (w, h), (0, h), (0, 0)])


# ----------------------------------------------------------------- packaging
def core_xml(title):
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(title)}</dc:title><dc:creator>build_mermaid_vsdx.py</dc:creator>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
            '<dc:language>en-US</dc:language></cp:coreProperties>')


def windows_xml(p):
    return ('<?xml version="1.0" encoding="utf-8"?>'
            f'<Windows ClientWidth="1600" ClientHeight="900" {NS} xml:space="preserve">'
            '<Window ID="0" WindowType="Drawing" WindowState="1073741824" WindowLeft="0" WindowTop="0" '
            'WindowWidth="1600" WindowHeight="900" ContainerType="Page" Page="0" ViewScale="-1" '
            f'ViewCenterX="{p.PW / 2:.4f}" ViewCenterY="{p.PH / 2:.4f}">'
            '<ShowRulers>1</ShowRulers><ShowGrid>1</ShowGrid><ShowPageBreaks>0</ShowPageBreaks><ShowGuides>1</ShowGuides>'
            '<ShowConnectionPoints>1</ShowConnectionPoints><GlueSettings>9</GlueSettings><SnapSettings>65847</SnapSettings>'
            '<SnapExtensions>34</SnapExtensions><SnapAngles/><DynamicGridEnabled>1</DynamicGridEnabled>'
            '<TabSplitterPos>0.5</TabSplitterPos></Window></Windows>')


def write_vsdx(pages, path, title):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT.format(pages="".join(
            f'<Override PartName="/visio/pages/page{i + 1}.xml" ContentType="application/vnd.ms-visio.page+xml"/>'
            for i in range(len(pages)))))
        z.writestr("_rels/.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL}">'
                                  f'<Relationship Id="rId1" Type="{VR}/document" Target="visio/document.xml"/>'
                                  f'<Relationship Id="rId2" Type="{REL}/metadata/core-properties" Target="docProps/core.xml"/>'
                                  '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                                  '</Relationships>')
        z.writestr("docProps/core.xml", core_xml(title))
        z.writestr("docProps/app.xml", app_xml(pages))
        z.writestr("visio/document.xml", DOC_XML)
        z.writestr("visio/_rels/document.xml.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL}">'
                                                    f'<Relationship Id="rId1" Type="{VR}/pages" Target="pages/pages.xml"/>'
                                                    f'<Relationship Id="rId2" Type="{VR}/windows" Target="windows.xml"/></Relationships>')
        z.writestr("visio/windows.xml", windows_xml(pages[0]))
        pg = "".join(
            f'<Page ID="{i}" NameU="{escape(p.name)}" Name="{escape(p.name)}" ViewScale="-1" '
            f'ViewCenterX="{p.PW / 2:.4f}" ViewCenterY="{p.PH / 2:.4f}">'
            '<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">'
            f'<Cell N="PageWidth" V="{p.PW:.4f}"/><Cell N="PageHeight" V="{p.PH:.4f}"/>'
            '<Cell N="ShdwOffsetX" V="0.125"/><Cell N="ShdwOffsetY" V="-0.125"/>'
            '<Cell N="PageScale" V="1" U="IN_F"/><Cell N="DrawingScale" V="1" U="IN_F"/>'
            '<Cell N="DrawingSizeType" V="0"/><Cell N="DrawingScaleType" V="0"/><Cell N="InhibitSnap" V="0"/>'
            '<Cell N="UIVisibility" V="0"/><Cell N="ShdwType" V="0"/><Cell N="ShdwObliqueAngle" V="0"/>'
            '<Cell N="PageLockReplace" V="0" U="BOOL"/><Cell N="PageLockDuplicate" V="0" U="BOOL"/>'
            '<Cell N="ShdwScaleFactor" V="1"/><Cell N="DrawingResizeType" V="1"/><Cell N="RouteStyle" V="0"/>'
            '<Cell N="PageShapeSplit" V="1"/>'
            '<Cell N="XRulerOrigin" V="0"/><Cell N="YRulerOrigin" V="0"/><Cell N="XGridOrigin" V="0"/><Cell N="YGridOrigin" V="0"/>'
            f'</PageSheet><Rel r:id="rId{i + 1}"/></Page>'
            for i, p in enumerate(pages))
        z.writestr("visio/pages/pages.xml", f'<?xml version="1.0" encoding="utf-8"?><Pages {NS} xml:space="preserve">{pg}</Pages>')
        z.writestr("visio/pages/_rels/pages.xml.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL}">'
                   + "".join(f'<Relationship Id="rId{i + 1}" Type="{VR}/page" Target="page{i + 1}.xml"/>' for i in range(len(pages)))
                   + "</Relationships>")
        for i, p in enumerate(pages):
            z.writestr(f"visio/pages/page{i + 1}.xml", p.vsdx_xml())


def main():
    os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
    stems = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(SRC, "*.txt"))]
    stems = [s for s in ORDER if s in stems] + sorted(s for s in stems if s not in ORDER)
    pages = []
    for stem in stems:
        with open(os.path.join(SRC, stem + ".txt"), encoding="utf-8-sig") as f:
            d = Diagram(stem, f.read())
        p = Page(stem, d)
        pages.append(p)
        write_vsdx([p], os.path.join(OUT, stem + ".vsdx"), p.title)
        with open(os.path.join(OUT, "preview", stem + ".svg"), "w", encoding="utf-8") as f:
            f.write(p.svg())
        print(f"{stem:55} {d.direction}  nodes={len(d.nodes):2} edges={len(d.edges):2} "
              f"subgraphs={len(d.subs)}  page={p.PW:.1f}x{p.PH:.1f} in")
    write_vsdx(pages, os.path.join(OUT, "Mermaid_Diagrams_All.vsdx"), "SaaS Replacement - Mermaid Diagrams")
    print(f"done: {len(pages)} diagrams -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
