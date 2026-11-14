"""Generates a multi-page Visio (.vsdx) discovery pack plus SVG previews.
Run: python build_vsdx.py   (stdlib only)"""
import os, zipfile
from xml.sax.saxutils import escape

PW, PH = 13.333, 7.5
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "diagrams")

# kind -> (fill, line, font colour)
K = {
    "user":   ("#FCE4D6", "#C55A11", "#000000"),
    "legacy": ("#D9D9D9", "#595959", "#000000"),
    "saas":   ("#DDEBF7", "#2E75B6", "#000000"),
    "client": ("#E2F0D9", "#548235", "#000000"),
    "ext":    ("#E4DFEC", "#7030A0", "#000000"),
    "data":   ("#FFF2CC", "#BF9000", "#000000"),
    "sec":    ("#F8CBAD", "#C00000", "#000000"),
    "cont":   ("#F7F7F7", "#7F7F7F", "#404040"),
    "contS":  ("#EEF5FB", "#2E75B6", "#1F4E79"),
    "contC":  ("#F2F8EE", "#548235", "#375623"),
    "contL":  ("#F0F0F0", "#595959", "#404040"),
    "contE":  ("#F4F1F8", "#7030A0", "#4B1F6F"),
    "contX":  ("#FFF8E5", "#BF9000", "#7F6000"),
    "white":  ("#FFFFFF", "#FFFFFF", "#000000"),
}


class Page:
    def __init__(self, name, title, subtitle=""):
        self.name, self.items, self.boxes = name, [], {}
        self.text(0.4, 0.2, 12.5, 0.45, title, size=0.24, bold=True, align="l")
        if subtitle:
            self.text(0.4, 0.62, 12.5, 0.3, subtitle, size=0.12, align="l", color="#595959")
        self.text(0.4, 7.15, 12.5, 0.25,
                  "Client Solution Architecture - SaaS Replacement Discovery Pack | Example data: replace with actual systems",
                  size=0.09, align="l", color="#7F7F7F")

    # --- primitives (x, y measured from top-left, inches) ---
    def text(self, x, y, w, h, t, size=0.125, bold=False, align="c", color="#000000"):
        self.items.append(dict(t="shape", x=x, y=y, w=w, h=h, text=t, fill=None, line=None,
                               dash=False, size=size, bold=bold, align=align, color=color, valign="m"))

    def cont(self, key, x, y, w, h, t, kind="cont"):
        f, l, c = K[kind]
        self.boxes[key] = (x, y, w, h)
        self.items.append(dict(t="shape", x=x, y=y, w=w, h=h, text=t, fill=f, line=l, dash=True,
                               size=0.14, bold=True, align="l", color=c, valign="t", round=0.05))

    def box(self, key, x, y, w, h, t, kind="saas", sid=None):
        f, l, c = K[kind]
        self.boxes[key] = (x, y, w, h)
        self.items.append(dict(t="shape", x=x, y=y, w=w, h=h, text=t + (("\n" + sid) if sid else ""),
                               fill=f, line=l, dash=False, size=0.125, bold=False, align="c",
                               color=c, valign="m", round=0.08, sid=sid))

    def edge(self, a, b, label="", dashed=False, both=False):
        ax, ay, aw, ah = self.boxes[a]
        bx, by, bw, bh = self.boxes[b]
        lo, hi = max(ax, bx), min(ax + aw, bx + bw)
        if hi - lo > 0.05:  # vertical overlap -> straight vertical
            x = (lo + hi) / 2
            if ay < by:
                pts = [(x, ay + ah), (x, by)]
            else:
                pts = [(x, ay), (x, by + bh)]
        else:  # side to side, H-V-H
            if ax + aw <= bx:
                x1, x2 = ax + aw, bx
            else:
                x1, x2 = ax, bx + bw
            y1, y2 = ay + ah / 2, by + bh / 2
            mx = (x1 + x2) / 2
            pts = [(x1, y1), (mx, y1), (mx, y2), (x2, y2)] if abs(y1 - y2) > 0.01 else [(x1, y1), (x2, y2)]
        self.items.append(dict(t="line", pts=pts, dashed=dashed, both=both))
        if label:
            # label on the longest segment
            segs = list(zip(pts, pts[1:]))
            s = max(segs, key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
            mx, my = (s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2
            w = max(0.5, len(label) * 0.075)
            self.items.append(dict(t="shape", x=mx - w / 2, y=my - 0.11, w=w, h=0.22, text=label,
                                   fill="#FFFFFF", line=None, dash=False, size=0.095, bold=False,
                                   align="c", color="#404040", valign="m"))

    # --- renderers ---
    def vsdx_xml(self):
        out, sid = [], 0
        for it in self.items:
            sid += 1
            if it["t"] == "line":
                xs = [p[0] for p in it["pts"]]; ys = [PH - p[1] for p in it["pts"]]
                minx, miny = min(xs), min(ys)
                w, h = max(max(xs) - minx, 0.01), max(max(ys) - miny, 0.01)
                rows = ""
                for i, (px, py) in enumerate(zip(xs, ys)):
                    rows += (f'<Row T="{"MoveTo" if i == 0 else "LineTo"}" IX="{i + 1}">'
                             f'<Cell N="X" V="{px - minx:.4f}"/><Cell N="Y" V="{py - miny:.4f}"/></Row>')
                out.append(
                    f'<Shape ID="{sid}" Type="Shape" LineStyle="{STYLE}" FillStyle="{STYLE}" TextStyle="{STYLE}"><Cell N="PinX" V="{minx + w / 2:.4f}"/><Cell N="PinY" V="{miny + h / 2:.4f}"/>'
                    f'<Cell N="Width" V="{w:.4f}"/><Cell N="Height" V="{h:.4f}"/><Cell N="LocPinX" V="{w / 2:.4f}"/>'
                    f'<Cell N="LocPinY" V="{h / 2:.4f}"/><Cell N="LineColor" V="#404040"/><Cell N="LineWeight" V="0.012"/>'
                    f'<Cell N="LinePattern" V="{2 if it["dashed"] else 1}"/><Cell N="FillPattern" V="0"/>'
                    f'<Cell N="EndArrow" V="4"/><Cell N="EndArrowSize" V="2"/>'
                    + ('<Cell N="BeginArrow" V="4"/><Cell N="BeginArrowSize" V="2"/>' if it["both"] else "")
                    + f'<Section N="Geometry" IX="0"><Cell N="NoFill" V="1"/>{rows}</Section></Shape>')
                continue
            x, y, w, h = it["x"], PH - it["y"] - it["h"], it["w"], it["h"]
            fill = it["fill"]
            geo = (f'<Section N="Geometry" IX="0"><Cell N="NoFill" V="{0 if fill else 1}"/><Cell N="NoLine" V="{0 if it["line"] else 1}"/>'
                   f'<Row T="MoveTo" IX="1"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row>'
                   f'<Row T="LineTo" IX="2"><Cell N="X" V="{w:.4f}"/><Cell N="Y" V="0"/></Row>'
                   f'<Row T="LineTo" IX="3"><Cell N="X" V="{w:.4f}"/><Cell N="Y" V="{h:.4f}"/></Row>'
                   f'<Row T="LineTo" IX="4"><Cell N="X" V="0"/><Cell N="Y" V="{h:.4f}"/></Row>'
                   f'<Row T="LineTo" IX="5"><Cell N="X" V="0"/><Cell N="Y" V="0"/></Row></Section>')
            va = {"t": 0, "m": 1}[it["valign"]]
            ha = {"l": 0, "c": 1}[it["align"]]
            style = 1 if it["bold"] else 0
            out.append(
                f'<Shape ID="{sid}" Type="Shape" LineStyle="{STYLE}" FillStyle="{STYLE}" TextStyle="{STYLE}"><Cell N="PinX" V="{x + w / 2:.4f}"/><Cell N="PinY" V="{y + h / 2:.4f}"/>'
                f'<Cell N="Width" V="{w:.4f}"/><Cell N="Height" V="{h:.4f}"/><Cell N="LocPinX" V="{w / 2:.4f}"/>'
                f'<Cell N="LocPinY" V="{h / 2:.4f}"/>'
                f'<Cell N="FillForegnd" V="{fill or "#FFFFFF"}"/><Cell N="FillPattern" V="{1 if fill else 0}"/>'
                f'<Cell N="LineColor" V="{it["line"] or "#000000"}"/><Cell N="LineWeight" V="0.012"/>'
                f'<Cell N="LinePattern" V="{0 if not it["line"] else (2 if it["dash"] else 1)}"/>'
                f'<Cell N="Rounding" V="{it.get("round", 0)}"/><Cell N="VerticalAlign" V="{va}"/>'
                f'<Cell N="LeftMargin" V="0.06"/><Cell N="RightMargin" V="0.06"/><Cell N="TopMargin" V="0.05"/><Cell N="BottomMargin" V="0.05"/>'
                f'{geo}'
                f'<Section N="Character"><Row IX="0"><Cell N="Size" V="{it["size"]}"/><Cell N="Color" V="{it["color"]}"/><Cell N="Style" V="{style}"/></Row></Section>'
                f'<Section N="Paragraph"><Row IX="0"><Cell N="HorzAlign" V="{ha}"/></Row></Section>'
                f'<Text>{escape(it["text"])}</Text></Shape>')
        return ('<?xml version="1.0" encoding="utf-8"?>'
                '<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xml:space="preserve">'
                f'<Shapes>{"".join(out)}</Shapes></PageContents>')

    def svg(self):
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="1333" height="750" font-family="Segoe UI,Arial">'
             '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse">'
             '<path d="M0,0 L8,4 L0,8 z" fill="#404040"/></marker></defs>'
             f'<rect width="{PW}" height="{PH}" fill="#fff"/>']
        for it in self.items:
            if it["t"] == "line":
                p = " ".join(f"{x},{y}" for x, y in it["pts"])
                s.append(f'<polyline points="{p}" fill="none" stroke="#404040" stroke-width="0.012" '
                         f'{"stroke-dasharray=\"0.06\"" if it["dashed"] else ""} marker-end="url(#a)" '
                         f'{"marker-start=\"url(#a)\"" if it["both"] else ""}/>')
                continue
            x, y, w, h = it["x"], it["y"], it["w"], it["h"]
            if it["fill"]:
                s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{it.get("round", 0)}" fill="{it["fill"]}" '
                         f'stroke="{it["line"] or "none"}" stroke-width="0.012" {"stroke-dasharray=\"0.06\"" if it["dash"] else ""}/>')
            lines = it["text"].split("\n")
            lh = it["size"] * 1.2
            if it["valign"] == "t":
                ty = y + 0.05 + it["size"]
            else:
                ty = y + h / 2 - (len(lines) - 1) * lh / 2 + it["size"] * 0.35
            tx, anc = (x + 0.08, "start") if it["align"] == "l" else (x + w / 2, "middle")
            for i, ln in enumerate(lines):
                s.append(f'<text x="{tx}" y="{ty + i * lh:.3f}" font-size="{it["size"]}" text-anchor="{anc}" '
                         f'fill="{it["color"]}" font-weight="{"bold" if it["bold"] else "normal"}">{escape(ln)}</text>')
        s.append("</svg>")
        return "".join(s)


# ----------------------------------------------------------------- diagrams
def d01():
    p = Page("01 Current-State Context", "Diagram 1 - Current-State System Context (L1)",
             "Existing on-prem claims solution, its users and the systems it exchanges data with")
    p.box("u1", 0.4, 1.6, 2.3, 0.85, "Claims Officers", "user")
    p.box("u2", 0.4, 3.0, 2.3, 0.85, "Claims Managers", "user")
    p.box("u3", 0.4, 4.4, 2.3, 0.85, "Customers / Partners", "user")
    p.cont("dc", 3.5, 1.0, 5.2, 5.8, "Client On-Premises Data Centre", "contL")
    p.box("app", 4.3, 1.8, 3.6, 1.2, "Legacy Claims Application", "legacy", "SYS-001")
    p.box("db", 3.8, 4.4, 2.2, 1.0, "Claims Database", "data", "DATA-001")
    p.box("doc", 6.3, 4.4, 2.2, 1.0, "Document Repository", "data", "DATA-002")
    p.cont("ex", 9.5, 1.0, 3.4, 5.8, "External Systems", "contE")
    names = [("crm", "CRM", "SYS-002"), ("fin", "Finance / ERP", "SYS-003"), ("idp", "Identity Provider", "SYS-004"),
             ("pay", "Payment Gateway", "SYS-005"), ("rep", "Reporting Platform", "SYS-006")]
    for i, (k, n, s) in enumerate(names):
        p.box(k, 9.85, 1.5 + i * 1.05, 2.7, 0.85, n, "ext", s)
    for u in ("u1", "u2", "u3"):
        p.edge(u, "app")
    p.edge("app", "db", "SQL"); p.edge("app", "doc", "files")
    for k, _, _ in names:
        p.edge("app", k, both=True)
    return p


def d02():
    p = Page("02 Current-State Landscape", "Diagram 2 - Current-State Application Landscape (L2)",
             "Application components, middleware, data stores and infrastructure dependencies")
    layers = [("Presentation Layer", ["Web Application", "Customer Portal"], "client"),
              ("Application Layer", ["Legacy Claims Engine", "Workflow Engine", "Business Rules Engine", "Batch Processing"], "legacy"),
              ("Integration Layer", ["Enterprise Service Bus", "API Gateway", "Message Queue"], "ext"),
              ("Data Layer", ["Relational Database", "Document Store", "Data Warehouse"], "data"),
              ("Infrastructure Layer", ["Virtual Machines", "Operating Systems", "Monitoring", "Backup / DR"], "saas")]
    for i, (n, items, kind) in enumerate(layers):
        y = 1.0 + i * 1.22
        p.cont(f"L{i}", 0.4, y, 12.5, 1.02, n, "cont")
        for j, it in enumerate(items):
            p.box(f"{i}_{j}", 2.6 + j * 2.5, y + 0.3, 2.2, 0.6, it, kind)
    for a, b in [("0_0", "1_0"), ("0_1", "1_1"), ("1_0", "2_0"), ("1_1", "2_1"), ("1_2", "2_2"),
                 ("2_0", "3_0"), ("2_1", "3_1"), ("2_2", "3_2")]:
        p.edge(a, b)
    return p


def d03():
    p = Page("03 Target SaaS Context", "Diagram 3 - Target SaaS Solution Context (L1)",
             "Future vendor-hosted SaaS platform within the client enterprise ecosystem")
    p.box("u1", 0.4, 1.6, 2.2, 0.8, "Internal Users", "user")
    p.box("u2", 0.4, 2.8, 2.2, 0.8, "Customers / Partners", "user")
    p.cont("saas", 3.4, 1.0, 4.6, 5.8, "Vendor-Hosted SaaS Platform", "contS")
    sa = ["SaaS User Interface", "Claims Management", "Workflow and Rules", "Document Management",
          "SaaS Reporting", "Vendor Managed Data Store"]
    for i, n in enumerate(sa):
        p.box(f"s{i}", 3.8, 1.6 + i * 0.85, 3.8, 0.7, n, "saas", "SYS-010" if i == 1 else None)
    p.cont("ent", 8.9, 1.0, 4.0, 5.8, "Client Enterprise", "contC")
    p.box("idp", 9.2, 1.6, 3.4, 0.7, "Entra ID / Identity", "client", "SYS-004")
    p.box("gw", 9.2, 2.45, 3.4, 0.7, "Enterprise API Gateway", "client")
    p.box("ip", 9.2, 3.3, 3.4, 0.7, "Integration Platform", "client")
    p.box("crm", 9.2, 4.15, 1.6, 0.7, "CRM", "ext", "SYS-002")
    p.box("fin", 11.0, 4.15, 1.6, 0.7, "Finance System", "ext", "SYS-003")
    p.box("rep", 9.2, 5.0, 3.4, 0.7, "Enterprise Reporting", "ext", "SYS-006")
    p.edge("u1", "s0"); p.edge("u2", "s0")
    p.edge("s0", "idp", "SSO", both=True)
    p.edge("s1", "gw", "REST APIs", both=True)
    p.edge("s2", "ip", "events", both=True)
    p.edge("s4", "rep", "data feed")
    p.edge("ip", "crm"); p.edge("ip", "fin")
    return p


def d04():
    p = Page("04 Target Integration", "Diagram 4 - Target SaaS Integration Architecture (L2)",
             "API, event and file integration between the SaaS platform and enterprise / external systems")
    p.cont("saas", 0.4, 1.0, 2.9, 5.8, "SaaS Platform", "contS")
    p.box("api", 0.7, 1.6, 2.3, 0.8, "SaaS REST APIs", "saas")
    p.box("cs", 0.7, 3.4, 2.3, 1.0, "Claims SaaS", "saas", "SYS-010")
    p.box("wh", 0.7, 5.2, 2.3, 0.8, "Webhooks / Events", "saas")
    p.cont("cib", 4.2, 1.0, 4.2, 5.8, "Client Integration Boundary", "contC")
    p.box("apim", 4.6, 1.6, 3.4, 0.8, "API Management", "client")
    p.box("ipaas", 4.6, 2.9, 3.4, 0.8, "Integration Services / iPaaS", "client")
    p.box("mb", 4.6, 4.2, 3.4, 0.8, "Message Broker", "client")
    p.box("sft", 4.6, 5.5, 3.4, 0.8, "Secure File Transfer", "client")
    p.cont("ent", 9.4, 1.0, 3.5, 5.8, "Enterprise Systems", "contE")
    for i, (k, n, s) in enumerate([("crm", "CRM", "SYS-002"), ("fin", "Finance", "SYS-003"),
                                   ("docs", "Document Services", None), ("dp", "Data Platform", None),
                                   ("gov", "External Government Services", None)]):
        p.box(k, 9.7, 1.5 + i * 1.05, 2.9, 0.8, n, "ext", s)
    p.edge("api", "apim", "REST/OAuth2", both=True)
    p.edge("cs", "api"); p.edge("cs", "wh")
    p.edge("wh", "mb", "events")
    p.edge("cs", "sft", "files", dashed=True, both=True)
    p.edge("apim", "ipaas"); p.edge("mb", "ipaas")
    for k in ("crm", "fin", "docs", "dp", "gov"):
        p.edge("ipaas", k, both=True)
    return p


def d05():
    p = Page("05 Data Migration", "Diagram 5 - Data Migration Architecture (L2)",
             "Extraction, transformation, load and reconciliation from legacy to SaaS")
    p.cont("src", 0.4, 1.0, 2.8, 5.8, "On-Prem Legacy", "contL")
    p.box("db", 0.7, 1.6, 2.2, 0.9, "Claims Database", "data", "DATA-001")
    p.box("doc", 0.7, 3.2, 2.2, 0.9, "Document Repository", "data", "DATA-002")
    p.box("his", 0.7, 4.8, 2.2, 0.9, "Historical Records", "data", "DATA-003")
    p.cont("mig", 3.8, 1.0, 5.4, 5.8, "Migration Services", "contC")
    for i, n in enumerate(["Data Extraction", "Staging Area", "Data Cleansing",
                           "Transformation and Mapping", "Validation and Reconciliation"]):
        p.box(f"m{i}", 5.0, 1.6 + i * 1.0, 3.0, 0.75, n, "client")
    p.cont("sa", 9.8, 1.0, 3.1, 5.8, "Vendor SaaS", "contS")
    p.box("bulk", 10.1, 1.6, 2.5, 0.9, "Bulk Import / APIs", "saas")
    p.box("store", 10.1, 3.2, 2.5, 0.9, "SaaS Data Store", "saas")
    p.box("arch", 10.1, 4.8, 2.5, 0.9, "Historical Archive", "saas")
    for k in ("db", "doc", "his"):
        p.edge(k, "m0")
    for i in range(4):
        p.edge(f"m{i}", f"m{i + 1}")
    p.edge("m3", "bulk", "load")
    p.edge("bulk", "store")
    p.edge("store", "m4", "reconcile", dashed=True)
    p.edge("m4", "arch", "archive", dashed=True)
    return p


def d06():
    p = Page("06 Identity and Security", "Diagram 6 - Identity and Security Architecture (L2)",
             "SSO, MFA, federation, provisioning, privileged access and trust boundaries")
    p.cont("cl", 0.4, 1.0, 5.0, 5.8, "Client Security Boundary", "contC")
    p.box("bu", 0.7, 1.6, 1.9, 0.9, "Business Users", "user")
    p.box("ad", 0.7, 3.0, 1.9, 0.9, "SaaS Administrators", "user")
    p.box("sa", 0.7, 4.4, 1.9, 0.9, "Integration Service Accounts", "user")
    p.box("idp", 3.1, 1.6, 2.0, 1.0, "Microsoft Entra ID", "client", "SYS-004")
    p.box("mfa", 3.1, 3.1, 2.0, 0.9, "MFA / Conditional Access", "client")
    p.box("pam", 3.1, 4.6, 2.0, 1.0, "Privileged Access Management", "client")
    p.cont("sp", 7.0, 1.0, 5.9, 5.8, "SaaS Provider Security Boundary", "contS")
    p.box("fed", 7.4, 1.6, 5.1, 0.8, "SAML / OIDC Federation", "saas")
    p.box("rbac", 7.4, 2.9, 5.1, 0.8, "Role-Based Access Control", "saas")
    p.box("aud", 7.4, 4.2, 5.1, 0.8, "Audit Logging", "saas")
    p.box("enc", 7.4, 5.5, 5.1, 0.8, "Encryption and Key Management", "sec")
    p.edge("bu", "idp"); p.edge("sa", "idp", "OAuth2")
    p.edge("ad", "pam")
    p.edge("mfa", "idp", "policy")
    p.edge("idp", "fed", "SAML / OIDC", both=True)
    p.edge("pam", "rbac", "admin roles")
    p.edge("fed", "rbac"); p.edge("rbac", "aud"); p.edge("aud", "enc")
    return p


def d07():
    p = Page("07 Environments", "Diagram 7 - Environment and Deployment Architecture (L2)",
             "SaaS vendor environments, client integration environments and release connectivity")
    p.cont("cl", 0.4, 1.0, 4.4, 5.0, "Client Managed", "contC")
    p.cont("sv", 8.5, 1.0, 4.4, 5.0, "SaaS Vendor Managed", "contS")
    cl = ["DEV Integration", "SIT Integration", "UAT Integration", "PROD Integration"]
    sv = ["Development / Configuration", "SIT Environment", "UAT Environment", "Production Environment"]
    for i in range(4):
        p.box(f"c{i}", 0.7, 1.6 + i * 1.1, 3.8, 0.75, cl[i], "client")
        p.box(f"v{i}", 8.8, 1.6 + i * 1.1, 3.8, 0.75, sv[i], "saas")
        p.edge(f"c{i}", f"v{i}", "API / events", both=True)
    for i in range(3):
        p.edge(f"v{i}", f"v{i + 1}", "promote")
    p.box("pipe", 0.4, 6.2, 12.5, 0.75, "Release / Deployment Pipeline (configuration promotion, approvals, test data refresh)", "ext")
    p.edge("pipe", "c3", "deploy"); p.edge("pipe", "v3", "release")
    return p


def d08():
    p = Page("08 NFR", "Diagram 8 - Non-Functional Requirements Architecture (L2)",
             "Quality attributes translated into SaaS capabilities and vendor obligations (values are examples only)")
    top = [("Availability", "Availability SLA (e.g. 99.9%)"), ("Performance", "Response Time / Throughput"),
           ("Security", "Encryption / Vulnerability Management")]
    bot = [("Disaster Recovery", "RTO / RPO / Backup"), ("Monitoring", "Health Monitoring / Alerts"),
           ("Audit and Logging", "Audit Trails / Log Retention")]
    xs = [0.6, 4.75, 8.9]
    p.box("app", 0.6, 3.55, 12.1, 0.9, "SaaS Application", "saas")
    for i in range(3):
        p.box(f"tr{i}", xs[i], 1.1, 3.8, 0.7, top[i][1], "data")
        p.box(f"tc{i}", xs[i], 2.3, 3.8, 0.7, top[i][0], "client")
        p.box(f"bc{i}", xs[i], 5.0, 3.8, 0.7, bot[i][0], "client")
        p.box(f"br{i}", xs[i], 6.15, 3.8, 0.7, bot[i][1], "data")
        p.edge(f"tr{i}", f"tc{i}", "defines", dashed=True)
        p.edge(f"tc{i}", "app")
        p.edge("app", f"bc{i}")
        p.edge(f"br{i}", f"bc{i}", "defines", dashed=True)
    return p


def d09():
    p = Page("09 Shared Responsibility", "Diagram 9 - SaaS Shared Responsibility (Conceptual)",
             "What the client manages, what is shared, and what the SaaS provider manages")
    cols = [("Client Responsibilities", "contC", "client", 0.4,
             ["Business Configuration Approval", "User Access Governance", "Business Data Ownership",
              "UAT and Acceptance", "Business Process Management"]),
            ("Shared Responsibilities", "contX", "data", 4.65,
             ["Enterprise Integration Ownership", "Identity and Access", "Integration Management",
              "Incident Management", "Security Monitoring", "Release Coordination"]),
            ("SaaS Provider Responsibilities", "contS", "saas", 8.9,
             ["Cloud Infrastructure", "Platform Availability", "SaaS Application Maintenance",
              "Product Patching and Upgrades", "Platform Backup and DR", "Platform Security"])]
    for n, ck, bk, x, items in cols:
        p.cont(n, x, 1.0, 4.0, 5.8, n, ck)
        for i, it in enumerate(items):
            p.box(f"{n}{i}", x + 0.3, 1.6 + i * 0.85, 3.4, 0.65, it, bk)
    return p


def d10():
    p = Page("10 Decommissioning", "Diagram 10 - Legacy Decommissioning and Transition (Conceptual)",
             "Migration, coexistence, cutover and retirement of on-prem components")
    p.cont("co", 0.2, 1.0, 12.9, 2.6, "Temporary coexistence (parallel run)", "contX")
    xs = [0.4, 3.6, 6.8, 10.0]
    for i, (k, n, kind) in enumerate([("leg", "1. Legacy On-Prem Application", "legacy"),
                                      ("ext", "2. Historical Data Extraction", "client"),
                                      ("mig", "3. Data Migration", "client"),
                                      ("saas", "4. SaaS Platform", "saas")]):
        p.box(k, xs[i], 1.6, 2.7, 1.2, n, kind)
    p.box("val", 10.0, 4.2, 2.7, 1.0, "5. Validation and Reconciliation", "client")
    p.box("cut", 6.8, 4.2, 2.7, 1.0, "6. Business Cutover", "user")
    p.box("ro", 3.6, 4.2, 2.7, 1.0, "7. Legacy Read-Only / Archive", "legacy")
    p.box("dec", 0.4, 4.2, 2.7, 1.0, "8. Legacy Decommissioning", "sec")
    p.edge("leg", "ext"); p.edge("ext", "mig"); p.edge("mig", "saas")
    p.edge("saas", "val"); p.edge("val", "cut"); p.edge("cut", "ro"); p.edge("ro", "dec")
    p.text(0.4, 5.5, 12.5, 0.9,
           "Decommissioning scope: data retention and disposal, historical access requirements, infrastructure shutdown, contract termination",
           size=0.12, align="l", color="#404040")
    return p


# ----------------------------------------------------------------- packaging
CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>'
      '<Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>'
      '{pages}'
      '<Override PartName="/visio/windows.xml" ContentType="application/vnd.ms-visio.windows+xml"/>'
      '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
      '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
      '</Types>')
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
VR = "http://schemas.microsoft.com/visio/2010/relationships"
NS = 'xmlns="http://schemas.microsoft.com/office/visio/2012/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'


# Style chain mirrors what Visio writes: "No Style" (ID 0) is the ROOT and must NOT carry
# LineStyle/FillStyle/TextStyle attributes (a self-reference makes Visio hang on open).
# "Normal" (ID 3) inherits from 0 and is what every shape points at.
STYLE = 3
_ROOT_CELLS = "".join(f'<Cell N="{n}" V="{v}"/>' for n, v in [
    ("EnableLineProps", 1), ("EnableFillProps", 1), ("EnableTextProps", 1), ("HideForApply", 0),
    ("LineWeight", "0.01041666666666667"), ("LineColor", 0), ("LinePattern", 1), ("Rounding", 0),
    ("EndArrowSize", 2), ("BeginArrow", 0), ("EndArrow", 0), ("LineCap", 0), ("BeginArrowSize", 2),
    ("LineColorTrans", 0), ("CompoundType", 0),
    ("FillForegnd", 1), ("FillBkgnd", 0), ("FillPattern", 1), ("ShdwForegnd", 0), ("ShdwPattern", 0),
    ("FillForegndTrans", 0), ("FillBkgndTrans", 0), ("ShdwForegndTrans", 0), ("ShapeShdwType", 0),
    ("ShapeShdwOffsetX", 0), ("ShapeShdwOffsetY", 0), ("ShapeShdwObliqueAngle", 0),
    ("ShapeShdwScaleFactor", 1), ("ShapeShdwBlur", 0), ("ShapeShdwShow", 0),
    ("LeftMargin", 0), ("RightMargin", 0), ("TopMargin", 0), ("BottomMargin", 0), ("VerticalAlign", 1),
    ("TextBkgnd", 0), ("DefaultTabStop", "0.5"), ("TextDirection", 0), ("TextBkgndTrans", 0)])
_ROOT_SECTIONS = (
    '<Section N="Character"><Row IX="0"><Cell N="Font" V="Calibri"/><Cell N="Color" V="0"/><Cell N="Style" V="0"/>'
    '<Cell N="Case" V="0"/><Cell N="Pos" V="0"/><Cell N="FontScale" V="1"/><Cell N="Size" V="0.1666666666666667"/>'
    '<Cell N="DblUnderline" V="0"/><Cell N="Overline" V="0"/><Cell N="Strikethru" V="0"/><Cell N="DoubleStrikethrough" V="0"/>'
    '<Cell N="Letterspace" V="0"/><Cell N="ColorTrans" V="0"/><Cell N="AsianFont" V="0"/><Cell N="ComplexScriptFont" V="0"/>'
    '<Cell N="ComplexScriptSize" V="-1"/><Cell N="LangID" V="en-US"/></Row></Section>'
    '<Section N="Paragraph"><Row IX="0"><Cell N="IndFirst" V="0"/><Cell N="IndLeft" V="0"/><Cell N="IndRight" V="0"/>'
    '<Cell N="SpLine" V="-1.2"/><Cell N="SpBefore" V="0"/><Cell N="SpAfter" V="0"/><Cell N="HorzAlign" V="1"/>'
    '<Cell N="Bullet" V="0"/><Cell N="BulletStr" V=""/><Cell N="BulletFont" V="0"/><Cell N="BulletFontSize" V="-1"/>'
    '<Cell N="TextPosAfterBullet" V="0"/><Cell N="Flags" V="0"/></Row></Section>'
    '<Section N="Tabs"><Row IX="0"/></Section>')
DOC_XML = ('<?xml version="1.0" encoding="utf-8"?>'
           f'<VisioDocument {NS} xml:space="preserve">'
           f'<DocumentSettings TopPage="0" DefaultTextStyle="{STYLE}" DefaultLineStyle="{STYLE}" DefaultFillStyle="{STYLE}" DefaultGuideStyle="{STYLE}">'
           '<GlueSettings>9</GlueSettings><SnapSettings>65847</SnapSettings><SnapExtensions>34</SnapExtensions><SnapAngles/>'
           '<DynamicGridEnabled>1</DynamicGridEnabled><ProtectStyles>0</ProtectStyles><ProtectShapes>0</ProtectShapes>'
           '<ProtectMasters>0</ProtectMasters><ProtectBkgnds>0</ProtectBkgnds></DocumentSettings>'
           '<Colors><ColorEntry IX="24" RGB="#000000"/><ColorEntry IX="25" RGB="#FFFFFF"/></Colors>'
           '<FaceNames><FaceName NameU="Calibri" UnicodeRanges="-469750017 -1040178053 9 0" CharSets="536871423 0" '
           'Panose="2 15 5 2 2 2 4 3 2 4" Flags="357"/></FaceNames>'
           '<StyleSheets>'
           f'<StyleSheet ID="0" NameU="No Style" IsCustomNameU="1" Name="No Style" IsCustomName="1">{_ROOT_CELLS}{_ROOT_SECTIONS}</StyleSheet>'
           f'<StyleSheet ID="{STYLE}" NameU="Normal" IsCustomNameU="1" Name="Normal" IsCustomName="1" LineStyle="0" FillStyle="0" TextStyle="0">'
           '<Cell N="LeftMargin" V="0.05555555555555555"/><Cell N="RightMargin" V="0.05555555555555555"/>'
           '<Cell N="TopMargin" V="0.05555555555555555"/><Cell N="BottomMargin" V="0.05555555555555555"/></StyleSheet>'
           '</StyleSheets>'
           '<DocumentSheet NameU="TheDoc" IsCustomNameU="1" Name="TheDoc" IsCustomName="1" LineStyle="0" FillStyle="0" TextStyle="0">'
           '<Cell N="OutputFormat" V="0"/><Cell N="LockPreview" V="0"/><Cell N="AddMarkup" V="0"/><Cell N="ViewMarkup" V="0"/>'
           '<Cell N="PreviewQuality" V="0"/><Cell N="PreviewScope" V="0"/><Cell N="DocLangID" V="en-US"/></DocumentSheet>'
           '</VisioDocument>')

WINDOWS_XML = ('<?xml version="1.0" encoding="utf-8"?>'
               f'<Windows ClientWidth="1600" ClientHeight="900" {NS} xml:space="preserve">'
               '<Window ID="0" WindowType="Drawing" WindowState="1073741824" WindowLeft="0" WindowTop="0" '
               'WindowWidth="1600" WindowHeight="900" ContainerType="Page" Page="0" ViewScale="-1" '
               f'ViewCenterX="{PW / 2}" ViewCenterY="{PH / 2}">'
               '<ShowRulers>1</ShowRulers><ShowGrid>1</ShowGrid><ShowPageBreaks>0</ShowPageBreaks><ShowGuides>1</ShowGuides>'
               '<ShowConnectionPoints>1</ShowConnectionPoints><GlueSettings>9</GlueSettings><SnapSettings>65847</SnapSettings>'
               '<SnapExtensions>34</SnapExtensions><SnapAngles/><DynamicGridEnabled>1</DynamicGridEnabled>'
               '<TabSplitterPos>0.5</TabSplitterPos></Window></Windows>')


def app_xml(pages):
    names = "".join(f"<vt:lpstr>{escape(p.name)}</vt:lpstr>" for p in pages)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Template></Template><Application>Microsoft Visio</Application><ScaleCrop>false</ScaleCrop>'
            '<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Pages</vt:lpstr></vt:variant>'
            f'<vt:variant><vt:i4>{len(pages)}</vt:i4></vt:variant></vt:vector></HeadingPairs>'
            f'<TitlesOfParts><vt:vector size="{len(pages)}" baseType="lpstr">{names}</vt:vector></TitlesOfParts>'
            '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
            '<AppVersion>16.0000</AppVersion></Properties>')


def core_xml():
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>SaaS Replacement Discovery Pack</dc:title><dc:creator>build_vsdx.py</dc:creator>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
            '<dc:language>en-US</dc:language></cp:coreProperties>')


def write_vsdx(pages, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT.format(pages="".join(
            f'<Override PartName="/visio/pages/page{i + 1}.xml" ContentType="application/vnd.ms-visio.page+xml"/>'
            for i in range(len(pages)))))
        z.writestr("_rels/.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL}">'
                                  f'<Relationship Id="rId1" Type="{VR}/document" Target="visio/document.xml"/>'
                                  f'<Relationship Id="rId2" Type="{REL}/metadata/core-properties" Target="docProps/core.xml"/>'
                                  '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                                  '</Relationships>')
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("docProps/app.xml", app_xml(pages))
        z.writestr("visio/document.xml", DOC_XML)
        z.writestr("visio/_rels/document.xml.rels", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{REL}">'
                                                    f'<Relationship Id="rId1" Type="{VR}/pages" Target="pages/pages.xml"/>'
                                                    f'<Relationship Id="rId2" Type="{VR}/windows" Target="windows.xml"/></Relationships>')
        z.writestr("visio/windows.xml", WINDOWS_XML)
        pg = "".join(
            f'<Page ID="{i}" NameU="{escape(p.name)}" Name="{escape(p.name)}" ViewScale="-1" ViewCenterX="{PW / 2}" ViewCenterY="{PH / 2}">'
            f'<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">'
            f'<Cell N="PageWidth" V="{PW}"/><Cell N="PageHeight" V="{PH}"/>'
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


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
    pages = [f() for f in (d01, d02, d03, d04, d05, d06, d07, d08, d09, d10)]
    write_vsdx(pages, os.path.join(OUT, "SaaS_Replacement_Discovery_Pack.vsdx"))
    for i, p in enumerate(pages, 1):
        with open(os.path.join(OUT, "preview", f"diagram{i:02d}.svg"), "w", encoding="utf-8") as f:
            f.write(p.svg())
    print("done", len(pages))
