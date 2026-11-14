"""Structural validator for .vsdx (OPC + Visio XML). Stdlib only.
Usage: python validate_vsdx.py [file.vsdx]   Exit code 1 if any ERROR is found."""
import sys, os, re, zipfile, posixpath
import xml.etree.ElementTree as ET

VNS = "http://schemas.microsoft.com/office/visio/2012/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
VREL = "http://schemas.microsoft.com/visio/2010/relationships"
CT_DOC = "application/vnd.ms-visio.drawing.main+xml"
CT_PAGES = "application/vnd.ms-visio.pages+xml"
CT_PAGE = "application/vnd.ms-visio.page+xml"
CT_RELS = "application/vnd.openxmlformats-package.relationships+xml"

NUMERIC = {"PinX", "PinY", "Width", "Height", "LocPinX", "LocPinY", "LineWeight", "LinePattern",
           "FillPattern", "Rounding", "VerticalAlign", "LeftMargin", "RightMargin", "TopMargin",
           "BottomMargin", "BeginArrow", "EndArrow", "BeginArrowSize", "EndArrowSize", "X", "Y",
           "Size", "Style", "HorzAlign", "NoFill", "NoLine", "PageWidth", "PageHeight"}
COLOR = {"FillForegnd", "LineColor", "Color"}
# element order required by the Visio schema inside Shape
SHAPE_ORDER = ["Cell", "Section", "Text", "Data1", "Data2", "Data3", "ForeignData", "Shapes"]


def q(tag, ns=VNS):
    return f"{{{ns}}}{tag}"


def local(el):
    return el.tag.rsplit("}", 1)[-1]


def ns(el):
    return el.tag[1:].split("}")[0] if el.tag.startswith("{") else ""


class Report:
    def __init__(self):
        self.items = []

    def err(self, where, msg):
        self.items.append(("ERROR", where, msg))

    def warn(self, where, msg):
        self.items.append(("WARN", where, msg))

    @property
    def errors(self):
        return [i for i in self.items if i[0] == "ERROR"]


def parse(z, name, r):
    try:
        data = z.read(name)
    except KeyError:
        r.err(name, "part missing from package")
        return None
    if data.startswith(b"\xef\xbb\xbf"):
        r.warn(name, "UTF-8 BOM present")
    if re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", data):
        r.err(name, "illegal control characters in XML")
    try:
        return ET.fromstring(data)
    except ET.ParseError as e:
        r.err(name, f"XML not well-formed: {e}")
        return None


def check_rels(z, rels_name, r, source_dir, expect=None):
    """Returns {rId: (type, resolved_target)}"""
    root = parse(z, rels_name, r)
    out = {}
    if root is None:
        return out
    if root.tag != q("Relationships", PKG_REL):
        r.err(rels_name, f"root element is {root.tag}, expected Relationships in {PKG_REL}")
        return out
    names = set(z.namelist())
    for rel in root:
        rid, typ, tgt = rel.get("Id"), rel.get("Type"), rel.get("Target")
        if not rid or not typ or not tgt:
            r.err(rels_name, f"relationship missing Id/Type/Target: {rel.attrib}")
            continue
        if rid in out:
            r.err(rels_name, f"duplicate relationship Id {rid}")
        if rel.get("TargetMode") == "External":
            out[rid] = (typ, tgt)
            continue
        full = posixpath.normpath(tgt.lstrip("/")) if tgt.startswith("/") else posixpath.normpath(posixpath.join(source_dir, tgt))
        if full not in names:
            r.err(rels_name, f"{rid} targets missing part '{full}'")
        out[rid] = (typ, full)
    return out


GEOM_START = ("MoveTo", "RelMoveTo", "Ellipse", "InfiniteLine")


def check_shape(sh, where, r, ids, inherited=False):
    """inherited=True when this shape (or an ancestor) takes cells from a master,
    in which case omitted cells / partial geometry are legitimate."""
    inherited = inherited or sh.get("Master") is not None or sh.get("MasterShape") is not None
    sid = sh.get("ID")
    if sid is None or not sid.isdigit():
        r.err(where, f"Shape has missing/non-integer ID: {sid!r}")
    elif sid in ids:
        r.err(where, f"duplicate Shape ID {sid}")
    else:
        ids.add(sid)
    where = f"{where} shape {sid}"
    last = -1
    for ch in sh:
        t = local(ch)
        if ns(ch) != VNS:
            r.err(where, f"element {ch.tag} not in Visio namespace")
            continue
        if t not in SHAPE_ORDER:
            r.err(where, f"unexpected child <{t}> in Shape")
            continue
        idx = SHAPE_ORDER.index(t)
        if idx < last:
            r.err(where, f"<{t}> out of schema order")
        last = max(last, idx)
    cells = {}
    for c in sh.findall(q("Cell")):
        n = c.get("N")
        if n in cells:
            r.err(where, f"duplicate cell {n}")
        cells[n] = c.get("V")
    if not inherited:
        for req in ("PinX", "PinY", "Width", "Height"):
            if req not in cells:
                r.err(where, f"missing required cell {req}")
    # own cells only (sub-shapes are checked by the recursive call)
    own = list(sh.findall(q("Cell")))
    for sec in sh.findall(q("Section")):
        own += list(sec.iter(q("Cell")))
    check_cells(own, where, r)
    for sec in sh.findall(q("Section")):
        if not sec.get("N"):
            r.err(where, "Section without N")
        seen = set()
        for row in sec.findall(q("Row")):
            key = row.get("IX")
            if sec.get("N") == "Geometry":
                if not row.get("T"):
                    r.err(where, "Geometry row missing T")
                if key is None or not key.isdigit():
                    r.err(where, f"Geometry row bad IX {key!r}")
                elif key in seen:
                    r.err(where, f"duplicate Geometry row IX {key}")
                seen.add(key)
        if sec.get("N") == "Geometry":
            rows = sec.findall(q("Row"))
            if rows and not inherited and rows[0].get("Del") is None and rows[0].get("T") not in GEOM_START:
                r.err(where, f"Geometry starts with {rows[0].get('T')}; must start with one of {', '.join(GEOM_START)}")
    try:
        w, h = float(cells.get("Width", "nan")), float(cells.get("Height", "nan"))
        # 1-D shapes (connectors, with BeginX) legitimately have negative extents
        if (w < 0 or h < 0) and "BeginX" not in cells:
            r.warn(where, "negative Width/Height on a 2-D shape")
    except ValueError:
        pass
    for ch in sh.findall(q("Shapes")):
        for s in ch.findall(q("Shape")):
            check_shape(s, where, r, ids, inherited)
    return cells


def check_cells(cells, where, r):
    for c in cells:
        n, v = c.get("N"), c.get("V")
        if n is None:
            r.err(where, "Cell without N")
            continue
        if v is None:
            r.warn(where, f"Cell {n} has no V")
            continue
        if v == "Themed":  # value resolved from the document theme
            continue
        if n in NUMERIC:
            try:
                f = float(v)
                if f != f or f in (float("inf"), float("-inf")):
                    raise ValueError
            except ValueError:
                r.err(where, f"Cell {n} V={v!r} is not numeric")
        if n in COLOR and not (re.fullmatch(r"#[0-9A-Fa-f]{6}", v) or v.isdigit()):
            r.err(where, f"Cell {n} V={v!r} is not a valid colour")


STYLE_ATTRS = ("LineStyle", "FillStyle", "TextStyle")


def ids_all(root):
    return {s.get("ID") for s in root.iter(q("Shape"))}


def check_style_refs(el, where, r, styles):
    for a in STYLE_ATTRS:
        v = el.get(a)
        if v is not None and styles is not None and v not in styles:
            r.err(where, f"{a}={v} references a StyleSheet that does not exist")


def check_document(d, where, r):
    """Validates styles, fonts and colours. Returns (style_ids, face_names)."""
    ss = d.find(q("StyleSheets"))
    sheets = ss.findall(q("StyleSheet")) if ss is not None else []
    if not sheets:
        r.err(where, "no StyleSheet defined; shapes cannot resolve LineStyle/FillStyle/TextStyle and Visio reports the file as corrupt")
        return None, set()
    graph = {}
    for s in sheets:
        sid = s.get("ID")
        if sid is None or not sid.isdigit():
            r.err(where, f"StyleSheet with bad ID {sid!r}")
            continue
        if sid in graph:
            r.err(where, f"duplicate StyleSheet ID {sid}")
        graph[sid] = {a: s.get(a) for a in STYLE_ATTRS if s.get(a) is not None}
        check_cells(s.iter(q("Cell")), f"{where} StyleSheet {sid}", r)
    if "0" not in graph:
        r.err(where, "StyleSheet ID 0 ('No Style') is missing; it is the root of the style chain")
    elif graph["0"]:
        r.err(where, f"StyleSheet 0 must be the root and carry no {'/'.join(STYLE_ATTRS)} attributes "
                     f"(has {graph['0']}); a self-referencing root makes Visio hang while opening")
    styles = set(graph)
    for sid, parents in graph.items():
        for a, p in parents.items():
            if p not in styles:
                r.err(f"{where} StyleSheet {sid}", f"{a}={p} references a missing StyleSheet")
    # cycle detection per inheritance kind (Visio loops forever on cycles)
    for a in STYLE_ATTRS:
        for start in graph:
            seen, cur = [], start
            while cur is not None and cur in graph:
                if cur in seen:
                    cyc = " -> ".join(seen[seen.index(cur):] + [cur])
                    if not (cur == "0" and seen == ["0"]):  # root self-ref already reported
                        r.err(where, f"circular {a} inheritance: {cyc} (Visio hangs on open)")
                    break
                seen.append(cur)
                cur = graph[cur].get(a)
                if cur == seen[-1]:
                    if cur != "0":
                        r.err(where, f"StyleSheet {cur} inherits {a} from itself (Visio hangs on open)")
                    break
    ds = d.find(q("DocumentSettings"))
    if ds is not None:
        for a in ("DefaultTextStyle", "DefaultLineStyle", "DefaultFillStyle", "DefaultGuideStyle"):
            v = ds.get(a)
            if v is not None and v not in styles:
                r.err(where, f"DocumentSettings {a}={v} references a missing StyleSheet")
    dsh = d.find(q("DocumentSheet"))
    if dsh is not None:
        check_style_refs(dsh, f"{where} DocumentSheet", r, styles)
    # fonts
    faces = set()
    fn = d.find(q("FaceNames"))
    for f in (fn.findall(q("FaceName")) if fn is not None else []):
        name = f.get("NameU")
        w = f"{where} FaceName {name!r}"
        if not name:
            r.err(where, "FaceName without NameU")
            continue
        faces.add(name)
        for attr, count in (("UnicodeRanges", 4), ("CharSets", 2), ("Panose", 10)):
            v = f.get(attr)
            if v is None:
                continue
            parts = v.split()
            if len(parts) != count or not all(re.fullmatch(r"-?\d+", x) for x in parts):
                r.err(w, f"{attr}={v!r} must be {count} integers")
            elif attr == "Panose" and all(x == "0" for x in parts):
                r.warn(w, "Panose is all zeros; Visio cannot match the font (use real values or omit the attribute)")
        if f.get("ID") is not None:
            r.warn(w, "FaceName has an ID attribute; Visio 2013+ files identify fonts by NameU only")
    for c in d.iter(q("Cell")):
        if c.get("N") == "Font" and c.get("V") not in (None, "0", "Themed") and not c.get("V").isdigit():
            if c.get("V") not in faces:
                r.warn(where, f"Font {c.get('V')!r} used but not declared in FaceNames")
    # colours: IX 0-23 are Visio's built-in palette and must not be redefined
    cl = d.find(q("Colors"))
    for ce in (cl.findall(q("ColorEntry")) if cl is not None else []):
        ix = ce.get("IX")
        if ix is None or not ix.isdigit():
            r.err(where, f"ColorEntry with bad IX {ix!r}")
        elif int(ix) < 24:
            r.err(where, f"ColorEntry IX={ix} redefines a built-in palette colour (custom entries start at 24)")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", ce.get("RGB", "")):
            r.err(where, f"ColorEntry IX={ix} has bad RGB {ce.get('RGB')!r}")
    return styles, faces


def compare(target, reference):
    """Lists structural things a known-good reference has that the target lacks."""
    out = []
    with zipfile.ZipFile(target) as t, zipfile.ZipFile(reference) as ref:
        def ctypes(z):
            root = ET.fromstring(z.read("[Content_Types].xml"))
            return {e.get("ContentType") for e in root}

        def reltypes(z):
            s = set()
            for n in z.namelist():
                if n.endswith(".rels"):
                    for rel in ET.fromstring(z.read(n)):
                        s.add(rel.get("Type"))
            return s

        def doc_children(z):
            return [local(c) for c in ET.fromstring(z.read("visio/document.xml"))]

        def page_sheet_cells(z):
            p = ET.fromstring(z.read("visio/pages/pages.xml")).find(q("Page"))
            ps = p.find(q("PageSheet")) if p is not None else None
            return {c.get("N") for c in ps.findall(q("Cell"))} if ps is not None else set()

        # masters/media/theme content is drawing-specific, so only report generic gaps
        optional = {"application/vnd.ms-visio.master+xml", "application/vnd.ms-visio.masters+xml", "image/png",
                    "image/x-emf", "application/vnd.openxmlformats-officedocument.custom-properties+xml"}
        for ctp in sorted(ctypes(ref) - ctypes(t) - optional):
            out.append(f"content type present in reference only: {ctp}")
        for rt in sorted(reltypes(ref) - reltypes(t)):
            if not rt.endswith(("/masters", "/master", "/image", "/thumbnail", "/custom-properties")):
                out.append(f"relationship type present in reference only: {rt}")
        for ch in [c for c in dict.fromkeys(doc_children(ref)) if c not in doc_children(t)]:
            out.append(f"document.xml element present in reference only: <{ch}>")
        for c in sorted(page_sheet_cells(ref) - page_sheet_cells(t)):
            out.append(f"PageSheet cell present in reference only: {c}")
    return out


def validate(path):
    r = Report()
    if not os.path.isfile(path):
        r.err(path, "file not found")
        return r
    if os.path.getsize(path) == 0:
        r.err(path, "file is empty")
        return r
    if not zipfile.is_zipfile(path):
        r.err(path, "not a valid ZIP/OPC package (file corrupt or wrong format)")
        return r
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            r.err(bad, "CRC error in zip member")
        names = z.namelist()
        for n in names:
            if "\\" in n:
                r.err(n, "backslash in part name (must be '/')")
            if n.lower() != n.lower().strip():
                r.err(n, "whitespace in part name")
        if len({n.lower() for n in names}) != len(names):
            r.err("package", "duplicate part names (case-insensitive)")
        if names and names[0] != "[Content_Types].xml":
            r.warn("package", f"first entry is {names[0]!r}; [Content_Types].xml first is conventional")

        # content types
        ct = parse(z, "[Content_Types].xml", r)
        defaults, overrides = {}, {}
        if ct is not None:
            if ct.tag != q("Types", CT_NS):
                r.err("[Content_Types].xml", "root must be Types in the package content-types namespace")
            for e in ct:
                if e.tag == q("Default", CT_NS):
                    defaults[e.get("Extension", "").lower()] = e.get("ContentType")
                elif e.tag == q("Override", CT_NS):
                    overrides[e.get("PartName")] = e.get("ContentType")
            for pn in overrides:
                if pn.lstrip("/") not in names:
                    r.err("[Content_Types].xml", f"Override for missing part {pn}")
            for n in names:
                if n == "[Content_Types].xml":
                    continue
                if "/" + n not in overrides and n.rsplit(".", 1)[-1].lower() not in defaults:
                    r.err(n, "no content type (no Default or Override)")
            if defaults.get("rels") != CT_RELS:
                r.err("[Content_Types].xml", "Default for 'rels' missing or wrong")

        # package rels
        pr = check_rels(z, "_rels/.rels", r, "")
        doc = [t for (ty, t) in pr.values() if ty == f"{VREL}/document"]
        if not doc:
            r.err("_rels/.rels", f"no relationship of type {VREL}/document")
            return r
        docpart = doc[0]
        if overrides.get("/" + docpart) != CT_DOC:
            r.err("[Content_Types].xml", f"{docpart} must be {CT_DOC} (is {overrides.get('/' + docpart)})")

        if not any(t.startswith("docProps/") for (_, t) in pr.values()):
            r.warn("_rels/.rels", "no docProps (core/app properties); Visio-saved files always include them")

        # document
        styles = None
        d = parse(z, docpart, r)
        if d is not None:
            if d.tag != q("VisioDocument"):
                r.err(docpart, f"root is {d.tag}, expected VisioDocument in {VNS}")
            kids = [local(c) for c in d]
            for need in ("DocumentSettings", "Colors", "FaceNames", "StyleSheets"):
                if need not in kids:
                    r.warn(docpart, f"<{need}> absent (Visio desktop usually expects it; real files always include it)")
            styles, faces = check_document(d, docpart, r)
        drels = check_rels(z, posixpath.join(posixpath.dirname(docpart), "_rels", posixpath.basename(docpart) + ".rels"),
                           r, posixpath.dirname(docpart))
        pages_parts = [t for (ty, t) in drels.values() if ty == f"{VREL}/pages"]
        if not pages_parts:
            r.err(docpart, f"no relationship of type {VREL}/pages")
            return r
        pp = pages_parts[0]
        if overrides.get("/" + pp) != CT_PAGES:
            r.err("[Content_Types].xml", f"{pp} must be {CT_PAGES}")
        if not any(ty == f"{VREL}/windows" for (ty, _) in drels.values()):
            r.warn(docpart, "no windows.xml relationship; Visio-saved files always include one")
        # masters referenced by shapes must exist
        master_ids = set()
        mparts = [t for (ty, t) in drels.values() if ty == f"{VREL}/masters"]
        if mparts:
            m = parse(z, mparts[0], r)
            if m is not None:
                master_ids = {e.get("ID") for e in m.findall(q("Master"))}

        # pages
        pg = parse(z, pp, r)
        prels = check_rels(z, posixpath.join(posixpath.dirname(pp), "_rels", posixpath.basename(pp) + ".rels"),
                           r, posixpath.dirname(pp))
        if pg is None:
            return r
        if pg.tag != q("Pages"):
            r.err(pp, f"root is {pg.tag}, expected Pages")
        page_els = pg.findall(q("Page"))
        if not page_els:
            r.err(pp, "no pages defined")
        pids, pnames, used = set(), set(), set()
        for p in page_els:
            pid, pn = p.get("ID"), p.get("Name")
            w = f"{pp} page {pid}"
            if pid is None or not pid.isdigit():
                r.err(w, "Page ID missing/non-integer")
            elif pid in pids:
                r.err(w, "duplicate Page ID")
            pids.add(pid)
            if not pn:
                r.err(w, "Page missing Name")
            elif pn in pnames:
                r.err(w, f"duplicate page name {pn!r}")
            elif len(pn) > 31:
                r.warn(w, f"page name {pn!r} longer than 31 chars")
            pnames.add(pn)
            if p.get("NameU") is None:
                r.warn(w, "Page missing NameU")
            rel = p.find(q("Rel"))
            if rel is None or rel.get(q("id", RNS)) is None:
                r.err(w, "Page missing <Rel r:id>")
                continue
            rid = rel.get(q("id", RNS))
            if rid not in prels:
                r.err(w, f"Rel r:id={rid} not in pages.xml.rels")
                continue
            typ, target = prels[rid]
            if typ != f"{VREL}/page":
                r.err(w, f"relationship {rid} type {typ} should be {VREL}/page")
            if target in used:
                r.err(w, f"page part {target} used by more than one Page")
            used.add(target)
            if overrides.get("/" + target) != CT_PAGE:
                r.err("[Content_Types].xml", f"{target} must be {CT_PAGE}")
            ps = p.find(q("PageSheet"))
            if ps is None:
                r.warn(w, "no PageSheet")
            else:
                check_style_refs(ps, w, r, styles)
                check_cells(ps.iter(q("Cell")), w, r)
                pcells = {c.get("N"): c.get("V") for c in ps.findall(q("Cell"))}
                for need in ("PageWidth", "PageHeight"):
                    if need not in pcells:
                        r.err(w, f"PageSheet missing {need}")
                for need in ("PageScale", "DrawingScale"):
                    if need not in pcells:
                        r.warn(w, f"PageSheet missing {need}")
            # page content
            root = parse(z, target, r)
            if root is None:
                continue
            if root.tag != q("PageContents"):
                r.err(target, f"root is {root.tag}, expected PageContents")
                continue
            shapes = root.find(q("Shapes"))
            if shapes is None:
                r.warn(target, "page has no <Shapes>")
                continue
            ids = set()
            ntext = 0
            for sh in root.iter(q("Shape")):
                sw = f"{target} shape {sh.get('ID')}"
                check_style_refs(sh, sw, r, styles)
                if sh.get("Master") is not None and sh.get("Master") not in master_ids:
                    r.err(sw, f"Master={sh.get('Master')} not defined in masters.xml")
            page_ids = ids_all(root)
            for c in root.iter(q("Connect")):
                for a in ("FromSheet", "ToSheet"):
                    if c.get(a) not in page_ids:
                        r.err(target, f"Connect {a}={c.get(a)} references a missing shape")
            for sh in shapes.findall(q("Shape")):
                cells = check_shape(sh, target, r, ids)
                if sh.find(q("Text")) is not None:
                    ntext += 1
                try:
                    pw = float(next((c.get("V") for c in ps.findall(q("Cell")) if c.get("N") == "PageWidth"), "0")) if ps is not None else 0
                    ph = float(next((c.get("V") for c in ps.findall(q("Cell")) if c.get("N") == "PageHeight"), "0")) if ps is not None else 0
                    x, y = float(cells["PinX"]), float(cells["PinY"])
                    if pw and (x < -0.01 or y < -0.01 or x > pw + 0.01 or y > ph + 0.01):
                        r.warn(f"{target} shape {sh.get('ID')}", f"pin ({x:.2f},{y:.2f}) outside page {pw}x{ph}")
                except (KeyError, ValueError):
                    pass
            if not ids:
                r.warn(target, "page has no shapes")
        orphan = [n for n in names if re.fullmatch(r"visio/pages/page\d+\.xml", n) and n not in used]
        for o in orphan:
            r.warn(o, "page part not referenced by any Page")
    return r


def main():
    import argparse
    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagrams",
                           "SaaS_Replacement_Discovery_Pack.vsdx")
    ap = argparse.ArgumentParser(description="Validate a .vsdx package")
    ap.add_argument("file", nargs="?", default=default)
    ap.add_argument("--compare", metavar="REF.vsdx", help="known-good file to diff structure against")
    a = ap.parse_args()
    rep = validate(a.file)
    for sev, where, msg in rep.items:
        print(f"{sev:5} {where}: {msg}")
    print(f"\n{len(rep.errors)} error(s), {len(rep.items) - len(rep.errors)} warning(s) in {os.path.basename(a.file)}")
    if a.compare:
        diff = compare(a.file, a.compare)
        print(f"\nCompared with {os.path.basename(a.compare)}: {len(diff)} gap(s)")
        for line in diff:
            print("  GAP  " + line)
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()


