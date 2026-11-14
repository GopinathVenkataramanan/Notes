"""Build the Discovery Readiness Meeting deck.

Usage: python tools/build_readiness_deck.py
Output: Discovery Readiness Meeting/Discovery-Readiness-Meeting.pptx
Edit the data below and rebuild rather than editing the .pptx by hand.
"""
from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parent.parent / "Discovery Readiness Meeting" / "Discovery-Readiness-Meeting.pptx"

NAVY = RGBColor(0x14, 0x2B, 0x4D)
TEAL = RGBColor(0x00, 0x7A, 0x87)
LIGHT = RGBColor(0xEE, 0xF3, 0xF8)
GREY = RGBColor(0x55, 0x5F, 0x6B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xC0, 0x39, 0x2B)
AMBER = RGBColor(0xE6, 0x9B, 0x00)
GREEN = RGBColor(0x2E, 0x8B, 0x57)
FONT = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
page = {"n": 0}


def text(slide, x, y, w, h, content, size=16, bold=False, color=NAVY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = content if isinstance(content, list) else [content]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.name = FONT
        r.font.color.rgb = color
    return tb


def bullets(slide, x, y, w, h, items, size=18, color=NAVY):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = "\u2022  " + item
        r.font.size = Pt(size)
        r.font.name = FONT
        r.font.color.rgb = color
    return tb


def rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    s.shadow.inherit = False
    return s


def new_slide(title, notes="", subtitle=None):
    s = prs.slides.add_slide(BLANK)
    page["n"] += 1
    rect(s, 0, 0, 13.333, 1.1, NAVY)
    rect(s, 0, 1.1, 13.333, 0.06, TEAL)
    text(s, 0.5, 0.15, 11.5, 0.8, title, size=30, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    if subtitle:
        text(s, 0.5, 1.3, 12.3, 0.5, subtitle, size=16, color=GREY)
    text(s, 12.2, 7.05, 0.8, 0.3, str(page["n"]), size=11, color=GREY, align=PP_ALIGN.RIGHT)
    text(s, 0.5, 7.05, 8, 0.3, "Discovery Workshop Readiness | Client SA", size=11, color=GREY)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def table(slide, x, y, w, rows, col_w, size=13, row_h=0.42, rag_col=None):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows)))
    t = shape.table
    for i, cw in enumerate(col_w):
        t.columns[i].width = Inches(cw)
    for r, row in enumerate(rows):
        t.rows[r].height = Inches(row_h)
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (LIGHT if r % 2 else WHITE)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = val
            run.font.size = Pt(size)
            run.font.name = FONT
            run.font.bold = r == 0
            run.font.color.rgb = WHITE if r == 0 else NAVY
            if rag_col is not None and c == rag_col and r > 0:
                p.alignment = PP_ALIGN.CENTER
    return t


def team_slide(title, overall_note, rows, questions, notes):
    s = new_slide(title, notes)
    text(s, 0.5, 1.3, 12.3, 0.4, overall_note, size=15, color=GREY)
    table(s, 0.5, 1.8, 8.3, [["Deliverable", "Evidence of ready", "RAG", "ETA"]] + rows,
          [3.3, 3.0, 0.9, 1.1], size=12, row_h=0.5, rag_col=2)
    rect(s, 9.1, 1.8, 3.75, 4.9, LIGHT)
    text(s, 9.25, 1.85, 3.5, 0.4, "Questions for the lead", size=16, bold=True, color=TEAL)
    bullets(s, 9.25, 2.3, 3.5, 4.3, questions, size=13)
    text(s, 0.5, 6.55, 8.3, 0.4, "Overall: [R / A / G]     Top gap: ______     Top risk: ______", size=13, color=GREY)
    return s


# 1 Title
s = prs.slides.add_slide(BLANK)
page["n"] += 1
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0.6, 3.55, 3.0, 0.08, TEAL)
text(s, 0.6, 1.8, 12, 1.6, "Discovery Workshop Readiness Check", size=44, bold=True, color=WHITE, anchor=MSO_ANCHOR.BOTTOM)
text(s, 0.6, 3.8, 12, 0.6, "BA, Technical BA, Technical, Test and Project teams with the Client SA", size=20, color=WHITE)
text(s, 0.6, 4.5, 12, 0.5, "Facilitator: Client Solution Architect     |     Date: [dd/mm/yyyy]     |     90 minutes", size=16, color=RGBColor(0xBF, 0xCC, 0xDC))
s.notes_slide.notes_text_frame.text = "Welcome. Purpose: know what is ready, who owns each gap, and whether we go on the planned date."

# 2 Purpose
s = new_slide("Purpose and outcomes", "Three outcomes. This is not a status report: ask for evidence and blockers.")
cards = [("1", "Readiness position", "An honest RAG for each team against the Gate 1 criteria."),
         ("2", "Owners and dates", "Every gap has a named owner and a date before the workshop."),
         ("3", "Go / no-go call", "Go, conditional go or no-go for the planned workshop date.")]
for i, (n, h, d) in enumerate(cards):
    x = 0.5 + i * 4.2
    rect(s, x, 1.6, 3.9, 3.4, LIGHT)
    rect(s, x, 1.6, 3.9, 0.1, TEAL)
    text(s, x + 0.25, 1.85, 1, 0.8, n, size=40, bold=True, color=TEAL)
    text(s, x + 0.25, 2.75, 3.4, 0.5, h, size=22, bold=True)
    text(s, x + 0.25, 3.35, 3.4, 1.5, d, size=16, color=GREY)
text(s, 0.5, 5.4, 12.3, 1, "Why it matters: the vendor estimate is only as good as the consolidated discovery pack we give it.", size=18, color=NAVY)

# 3 Agenda
s = new_slide("Agenda (90 minutes)", "Team round is the main block: about 7 to 8 minutes each.")
table(s, 0.5, 1.5, 12.3, [
    ["Time", "Min", "Topic", "Lead"],
    ["0:00", "5", "Welcome, purpose, agenda, ground rules", "Client SA"],
    ["0:05", "5", "Where we are and how we rate readiness", "Client SA"],
    ["0:10", "45", "Team readiness round: Client SA, BA, Technical BA, Technical, Test, Project", "Each lead"],
    ["0:55", "10", "Heat map and cross-team dependencies", "Client SA"],
    ["1:05", "8", "Risks, blockers and asks", "All"],
    ["1:13", "7", "Workshop plan: agenda, roles, logistics, rehearsal", "Client SA, Project"],
    ["1:20", "7", "Actions, owners and dates", "Note-taker"],
    ["1:27", "3", "Go / conditional go / no-go and close", "Client SA"],
], [1.2, 0.9, 7.4, 2.8], size=15, row_h=0.55)

# 4 Ground rules
s = new_slide("Ground rules", "Reds raised here are cheap. Reds found on workshop day are expensive.")
bullets(s, 0.7, 1.7, 11.8, 5, [
    "Each lead speaks to their own slide for no more than 7 minutes, then questions.",
    "Rate with R / A / G against the definitions on the next slides. No in-between ratings.",
    "Raise blockers early. A red here is a request for help, not a failure.",
    "Evidence over activity: show the document, the link or the sign-off.",
    "Detail goes offline. We log an action with an owner and a date, then move on.",
    "Decisions go on the decision log. Disagreements on IDs, scope or dates get an owner, not a live debate.",
], size=22)

# 5 Where we are
s = new_slide("Where we are: how the pack comes together", "Shared IDs (SYS, INT, DATA, ENV) tie all teams' work together.")
boxes = [("BA team", "Requirements, processes, Product Fit-Gap Matrix"),
         ("Technical BA", "Application, integration and data inventories, interface specs"),
         ("Client SA", "Architecture, standards, NFRs, security, responsibilities"),
         ("Test team", "Test strategy, migration validation, performance and security testing"),
         ("Project team", "Scope, roadmap, governance, RAID, cutover constraints")]
for i, (h, d) in enumerate(boxes):
    y = 1.5 + i * 0.95
    rect(s, 0.5, y, 2.4, 0.8, TEAL if h == "Client SA" else NAVY)
    text(s, 0.5, y, 2.4, 0.8, h, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 3.0, y, 4.6, 0.8, d, size=13, color=GREY, anchor=MSO_ANCHOR.MIDDLE)
flow = [("Consolidated\ndiscovery pack", NAVY), ("Client discovery\nworkshop", TEAL), ("Vendor validation\nand estimation", NAVY), ("Vendor WBS and\nfinal cost", NAVY)]
for i, (h, c) in enumerate(flow):
    y = 1.5 + i * 1.2
    rect(s, 8.3, y, 4.5, 0.9, c)
    text(s, 8.3, y, 4.5, 0.9, h.split("\n"), size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 7.7, 3.2, 0.6, 0.6, "\u2192", size=36, bold=True, color=TEAL, align=PP_ALIGN.CENTER)
text(s, 0.5, 6.4, 12.3, 0.5, "Today's focus is the first two boxes on the right: is the pack ready for the workshop?", size=16, color=NAVY)

# 6 RAG definitions
s = new_slide("How we rate readiness", "Read the definitions out loud. Not green until reviewed by someone other than the author.")
defs = [(GREEN, "GREEN", "Complete and reviewed by someone other than the author. Evidence is in the shared pack folder."),
        (AMBER, "AMBER", "Content exists but is incomplete or unreviewed. A dated plan closes it before the workshop."),
        (RED, "RED", "Missing, or no credible plan to close it before the workshop. Needs help or a decision.")]
for i, (c, h, d) in enumerate(defs):
    y = 1.6 + i * 1.5
    rect(s, 0.5, y, 2.2, 1.2, c)
    text(s, 0.5, y, 2.2, 1.2, h, size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 2.7, y, 10.1, 1.2, LIGHT)
    text(s, 2.95, y, 9.7, 1.2, d, size=18, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.5, 6.2, 12.3, 0.6, "Gate rule: a gate passes when every Must item is met or has an approved exception.", size=16, color=GREY)

# 7 Client SA
team_slide("Client SA: architecture pack",
           "Docs 01 to 13 from the Client SA Discovery Pack. Presented first as the model for reporting.",
           [["Diagrams 01-08 (current and target)", "Actual names and IDs, no placeholders", "[ ]", "[date]"],
            ["Element Register (13)", "Every diagram element has an ID", "[ ]", "[date]"],
            ["EA standards (02)", "Confirmed with Enterprise Architecture", "[ ]", "[date]"],
            ["Security and network (04, 05)", "Reviewed by Security and Network", "[ ]", "[date]"],
            ["NFR catalogue (07)", "Agreed with business, security, ops", "[ ]", "[date]"],
            ["Shared responsibility, risks (08, 09)", "Reviewed by service mgmt, in RAID", "[ ]", "[date]"],
            ["(example) values replaced", "Replaced or marked TBC", "[ ]", "[date]"]],
           ["What would the client challenge first?",
            "Which NFR targets are still unagreed?",
            "Which elements lack a Technical BA entry?",
            "Where are we still using example data?"],
           "Go first so leads see the level of detail expected. Gate 1 items 1.1 to 1.13, 1.15.")

# 8 BA team
team_slide("BA team",
           "Business requirements, processes and the Product Fit-Gap Matrix.",
           [["Requirements baseline with IDs", "Agreed with business, MoSCoW set", "[ ]", "[date]"],
            ["Process models / scenarios", "Reviewed with process owners", "[ ]", "[date]"],
            ["Product Fit-Gap Matrix", "All in-scope requirements classified", "[ ]", "[date]"],
            ["Demo scenarios for workshop", "Prioritised, scripts agreed", "[ ]", "[date]"],
            ["Business stakeholder list", "Attendance confirmed", "[ ]", "[date]"],
            ["Open questions log", "Owners and dates assigned", "[ ]", "[date]"]],
           ["How many requirements are unclassified?",
            "Which processes must be demonstrated?",
            "Are priorities agreed with the business?",
            "Who must attend and are they confirmed?"],
           "Gate 1 item 1.14. Probe for evidence and unclassified counts.")

# 9 Technical BA
team_slide("Technical BA",
           "Application, integration and data inventories and interface specifications.",
           [["Application inventory", "Linked to SYS-IDs", "[ ]", "[date]"],
            ["Integration catalogue", "Every interface has an INT-ID", "[ ]", "[date]"],
            ["Interface specs", "Verified with system owners", "[ ]", "[date]"],
            ["Migration inventory", "Entities, volumes, quality findings", "[ ]", "[date]"],
            ["Data retention rules", "Agreed with records management", "[ ]", "[date]"],
            ["Match to Element Register", "IDs reconciled, gaps listed", "[ ]", "[date]"]],
           ["Does every interface have an INT-ID?",
            "Do we have migration volumes and entities?",
            "Where do the catalogue and the register differ?",
            "Which specs are unverified?"],
           "Gate 1 items 1.4 and 1.5. IDs must match the Element Register.")

# 10 Technical team
team_slide("Technical team",
           "Architecture, security, network, integration, infrastructure and environments.",
           [["EA standards confirmation", "Signed off by Enterprise Architecture", "[ ]", "[date]"],
            ["Security requirements, data class", "Reviewed by Security Architecture", "[ ]", "[date]"],
            ["Network and connectivity", "Reviewed by network team", "[ ]", "[date]"],
            ["Identity integration", "SSO, MFA, provisioning owner named", "[ ]", "[date]"],
            ["Integration platform / patterns", "Target patterns agreed", "[ ]", "[date]"],
            ["Environments (ENV-IDs)", "Integration and test envs available", "[ ]", "[date]"]],
           ["Are EA standards confirmed?",
            "Has Security confirmed data classification?",
            "Allowlisting, private link, DNS agreed?",
            "Who owns the identity integration?"],
           "Gate 1 items 1.6, 1.7, 1.9. Adjust if your technical team structure differs.")

# 11 Test team
team_slide("Test team",
           "Test strategy, migration validation, performance and security testing.",
           [["Test strategy draft", "Reviewed by project and SA", "[ ]", "[date]"],
            ["Migration validation approach", "Reconciliation and rehearsal plan", "[ ]", "[date]"],
            ["Performance test approach", "Linked to NFR targets", "[ ]", "[date]"],
            ["Security test approach", "Aligned with security requirements", "[ ]", "[date]"],
            ["Environments and test data", "Assumptions stated", "[ ]", "[date]"],
            ["Workshop questions for vendor", "Test tooling, sandboxes, support", "[ ]", "[date]"]],
           ["What do you need from the workshop to size testing?",
            "Do NFRs have measurable acceptance criteria?",
            "Are test environment assumptions stated?",
            "Which test data constraints exist?"],
           "Gate 1 item 1.14: test strategy in the consolidated pack.")

# 12 Project team
team_slide("Project team",
           "Scope, roadmap, governance, RAID and cutover constraints.",
           [["Scope and objectives", "Agreed, signed off by sponsor", "[ ]", "[date]"],
            ["Roadmap and key dates", "Shared with vendor", "[ ]", "[date]"],
            ["Governance and design authority", "Roles and decision path set", "[ ]", "[date]"],
            ["RAID log", "Includes architecture risks (09)", "[ ]", "[date]"],
            ["Cutover and blackout constraints", "Documented", "[ ]", "[date]"],
            ["Workshop logistics", "Invites, venue, pre-reads sent", "[ ]", "[date]"]],
           ["Is the RAID log current?",
            "Are budget and timeline boundaries shareable?",
            "Are logistics and invites confirmed?",
            "Who is the sponsor for escalations?"],
           "Gate 1 items 1.11 and 1.14.")

# 13 Heat map
s = new_slide("Readiness heat map", "Fill from the pre-submitted responses. Change a RAG only on evidence. Count Must items that are not green.")
hdr = ["Area", "Complete", "Reviewed", "Evidence in pack", "Blocker", "Overall"]
areas = ["Client SA", "BA team", "Technical BA", "Technical team", "Test team", "Project team"]
table(s, 0.5, 1.5, 12.3, [hdr] + [[a, "", "", "", "", ""] for a in areas],
      [2.6, 1.8, 1.8, 2.2, 2.3, 1.6], size=15, row_h=0.62)
text(s, 0.5, 6.3, 12.3, 0.5, "Must items not green: ___ of ___          Reds with no plan: ___", size=16, color=GREY)

# 14 Dependencies
s = new_slide("Cross-team dependencies", "Most risk sits between teams. Confirm giver, receiver and date for each.")
table(s, 0.5, 1.5, 12.3, [
    ["Giver", "Receiver", "What", "Due"],
    ["Technical BA", "BA team", "Integration and data scope for the fit-gap", "[date]"],
    ["Technical BA", "Client SA", "INT / DATA catalogue matched to Element Register IDs", "[date]"],
    ["Technical team, Client SA", "Test team", "NFR targets with measurable criteria", "[date]"],
    ["BA team", "Client SA", "Fit-gap results for target architecture", "[date]"],
    ["All teams", "Project team", "Risks, assumptions, constraints for the RAID log", "[date]"],
    ["Project team", "All teams", "Workshop date, attendees, agenda slots", "[date]"],
], [2.8, 2.2, 6.0, 1.3], size=15, row_h=0.65)

# 15 Risks
s = new_slide("Risks, blockers and asks", "Capture owner and mitigation for each. Escalate anything needing a sponsor decision.")
table(s, 0.5, 1.5, 12.3, [
    ["#", "Risk / blocker / ask", "Team", "Owner", "Mitigation or ask", "Date"],
    ["1", "", "", "", "", ""],
    ["2", "", "", "", "", ""],
    ["3", "", "", "", "", ""],
    ["4", "", "", "", "", ""],
    ["5", "", "", "", "", ""],
], [0.5, 4.0, 1.5, 1.6, 3.7, 1.0], size=14, row_h=0.7)
text(s, 0.5, 6.0, 12.3, 0.8, "Typical flags: SME availability, unverified interface specs, unagreed NFR values, unconfirmed data residency, client attendance.", size=15, color=GREY)

# 16 Workshop plan
s = new_slide("Workshop plan", "Agree agenda, roles, logistics, pre-read date and a dry run.")
cols = [("Agenda", ["Context and scope", "Current state walkthrough", "Target architecture and integration", "Data migration and decommissioning", "Security, NFRs, operations", "Next steps"]),
        ("Roles", ["Lead: Client SA", "Scribe: [name]", "Responders per topic", "Demo owner: BA", "Timekeeper: Project"]),
        ("Logistics", ["Date / venue / call link", "Client attendees confirmed", "Pre-read issued: [date]", "Dry run: T-2 days", "Checkpoint: T-3 days"])]
for i, (h, items) in enumerate(cols):
    x = 0.5 + i * 4.2
    rect(s, x, 1.5, 3.9, 5.0, LIGHT)
    rect(s, x, 1.5, 3.9, 0.1, TEAL)
    text(s, x + 0.2, 1.7, 3.5, 0.5, h, size=20, bold=True, color=TEAL)
    bullets(s, x + 0.2, 2.3, 3.6, 4.0, items, size=15)

# 17 Actions
s = new_slide("Actions, owners and dates", "Note-taker reads back every action. Fix missing owners or dates now.")
table(s, 0.5, 1.5, 12.3, [["#", "Action", "Owner", "Due", "Status"]] + [[str(i), "", "", "", ""] for i in range(1, 8)],
      [0.5, 6.5, 2.2, 1.6, 1.5], size=14, row_h=0.55)

# 18 Go / no-go
s = new_slide("Go / no-go and close", "State your proposal, ask for objections, set the next checkpoint.")
opts = [(GREEN, "GO", "All Must items green, or amber with a dated plan that lands before the workshop."),
        (AMBER, "CONDITIONAL GO", "Named reds with owner and date. Re-check at the checkpoint."),
        (RED, "NO-GO", "Reds with no credible plan. Re-plan the workshop date.")]
for i, (c, h, d) in enumerate(opts):
    y = 1.5 + i * 1.35
    rect(s, 0.5, y, 3.2, 1.15, c)
    text(s, 0.5, y, 3.2, 1.15, h, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 3.7, y, 9.1, 1.15, LIGHT)
    text(s, 3.95, y, 8.7, 1.15, d, size=17, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.5, 5.7, 12.3, 0.5, "Decision: [Go / Conditional go / No-go]          Next checkpoint: [date]", size=18, bold=True)
text(s, 0.5, 6.3, 12.3, 0.5, "Minutes, heat map and action log go out within 24 hours.", size=15, color=GREY)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print("Saved", OUT, "slides:", len(prs.slides))
