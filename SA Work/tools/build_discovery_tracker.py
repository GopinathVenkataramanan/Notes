"""Build the Discovery Workshop Tracker workbook (readiness -> workshop -> gates 1-3 -> close-out).

Usage:  python tools\\build_discovery_tracker.py        (needs xlsxwriter)
Output: Discovery Tracker/Discovery-Workshop-Tracker.xlsx

Content comes from the workspace references: the Client SA Discovery Pack (docs 01-14), the readiness
meeting script and deck, reference1-3.md (team deliverables, cost model, fit-gap classes, vendor outputs)
and the Mermaid/Visio diagram set. Edit the data below and rebuild rather than editing the .xlsx by hand.
Rows are pre-filled with EXAMPLE status data so the dashboards render; replace it with real values.
"""
import datetime as dt
import os

import xlsxwriter
from xlsxwriter.utility import xl_col_to_name, xl_rowcol_to_cell

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "Discovery Tracker", "Discovery-Workshop-Tracker.xlsx")

# Example timeline: the build date is the readiness meeting day; the workshop is 14 days later.
TODAY = dt.date.today()
W = TODAY + dt.timedelta(days=14)


def d(n):
    return W + dt.timedelta(days=n)


NAVY, TEAL, LIGHT, GREY, WHITE = "#142B4D", "#007A87", "#EEF3F8", "#555F6B", "#FFFFFF"
RED, AMBER, GREEN, SLATE = "#C0392B", "#E69B00", "#2E8B57", "#8A96A3"
RED_BG, AMBER_BG, GREEN_BG, GREY_BG = "#F6D5D1", "#FCEBC7", "#D5EEDF", "#E4E8EC"
FONT = "Segoe UI"

PHASES = ["1 Readiness", "2 Workshop", "3 Discovery completeness", "4 Architecture alignment",
          "5 Estimation validation", "6 Close-out"]
CLIENT_TEAMS = ["Client SA", "BA Team", "Technical BA", "Technical Team", "Test Team", "Project Team"]
LISTS = {
    "lstTeams": CLIENT_TEAMS + ["Vendor", "All teams"],
    "lstStatus": ["Not started", "In progress", "Draft complete", "In review", "Complete", "N/A"],
    "lstYesNo": ["Yes", "No"],
    "lstPriority": ["Must", "Should", "Could"],
    "lstPhase": PHASES,
    "lstGate": ["Met", "Partially met", "Not met", "Exception approved", "N/A"],
    "lstOutcome": ["Pass", "Conditional", "Fail"],
    "lstCall": ["GO", "CONDITIONAL GO", "NO-GO"],
    "lstRAIDType": ["Risk", "Assumption", "Issue", "Dependency"],
    "lstRAIDStatus": ["Open", "Mitigating", "Closed"],
    "lstAction": ["Open", "In progress", "Done", "Cancelled"],
    "lstDep": ["Not started", "In progress", "Delivered"],
    "lstSession": ["Planned", "Confirmed", "Done", "Deferred"],
    "lstVendorOut": ["Not received", "Received", "Under review", "Accepted", "Rework required"],
    "lstConf": ["Confirmed", "Provisional", "Unestimated"],
    "lstRACI": ["Accountable", "Responsible", "Consulted", "Informed", "Shared", "Approves",
                "Approves architecture", "Supports", "Assesses"],
    "lstScore": [1, 2, 3, 4, 5],
}
FITGAP = ["Standard", "Configuration", "Extension", "Customisation", "Workaround", "Not supported", "Unclassified"]

# ----------------------------------------------------------------- deliverables register
# (ID, team, category, deliverable, evidence of ready, pack ref, gate item, priority, owner, example status, due offset)
S_C, S_R, S_D, S_P, S_N = "Complete", "In review", "Draft complete", "In progress", "Not started"
DELIV = [
    ("CSA-01", "Client SA", "Architecture", "Diagrams 01-08 (current and target)", "Actual names and IDs, no placeholders", "01, diagrams/", "1.1", "Must", "Client SA", S_R, -6),
    ("CSA-02", "Client SA", "Architecture", "Diagrams 09-10 (responsibility, decommissioning)", "Reviewed with service management", "01, diagrams/", "1.2", "Should", "Client SA", S_D, -5),
    ("CSA-03", "Client SA", "Standards", "Enterprise Architecture Standards", "Confirmed with Enterprise Architecture", "02", "1.6", "Must", "Client SA", S_C, -18),
    ("CSA-04", "Client SA", "Architecture", "SaaS Architecture Requirements", "Multi-tenancy, availability, resilience stated", "03", "", "Must", "Client SA", S_C, -18),
    ("CSA-05", "Client SA", "Security", "Security Architecture Requirements", "Reviewed by Security Architecture", "04", "1.7", "Must", "Security Architect", S_R, -7),
    ("CSA-06", "Client SA", "Network", "Network and Connectivity Requirements", "Reviewed by the network team", "05", "1.9", "Must", "Network Lead", S_P, -6),
    ("CSA-07", "Client SA", "Operations", "SaaS Operational Requirements", "Monitoring, incident, support, logging defined", "06", "", "Must", "Client SA", S_D, -6),
    ("CSA-08", "Client SA", "NFR", "NFR Catalogue (performance, availability, DR, RTO/RPO)", "Agreed with business, security, operations", "07", "1.8", "Must", "Client SA", S_P, -16),
    ("CSA-09", "Client SA", "Operations", "Shared Responsibility Matrix", "Reviewed by service management", "08", "1.10", "Must", "Client SA", S_D, -5),
    ("CSA-10", "Client SA", "Governance", "Architecture Risks and Constraints", "Logged and reflected in project RAID", "09", "1.11", "Must", "Client SA", S_C, -17),
    ("CSA-11", "Client SA", "Transition", "Legacy Decommissioning Principles", "Reviewed with records management", "10", "1.12", "Must", "Client SA", S_P, -4),
    ("CSA-12", "Client SA", "Vendor", "Vendor SaaS Due-Diligence Questionnaire", "Includes regulatory supplement", "11", "1.13", "Must", "Client SA", S_C, -17),
    ("CSA-13", "Client SA", "Vendor", "Vendor Estimation Pack Requirements", "Eight mandatory outputs defined", "12", "", "Must", "Client SA", S_C, -17),
    ("CSA-14", "Client SA", "Traceability", "Architecture Element Register (SYS/INT/DATA/ENV)", "Every diagram element has an ID", "13", "1.3", "Must", "Client SA", S_R, -6),
    ("CSA-15", "Client SA", "Quality", "All (example) values replaced or marked TBC", "No example data left in the pack", "All", "1.15", "Must", "Client SA", S_P, -3),
    ("BA-01", "BA Team", "Business", "Business capability map", "Existing capabilities and future requirements", "BA pack", "1.14", "Must", "BA Lead", S_C, -18),
    ("BA-02", "BA Team", "Process", "As-Is business processes", "Reviewed with process owners", "BA pack", "1.14", "Must", "BA Lead", S_C, -18),
    ("BA-03", "BA Team", "Process", "To-Be business processes (SaaS)", "Desired processes using SaaS", "BA pack", "1.14", "Must", "BA Lead", S_R, -7),
    ("BA-04", "BA Team", "Requirements", "Functional requirements catalogue", "IDs and MoSCoW agreed with the business", "BA pack", "1.14", "Must", "BA Lead", S_R, -7),
    ("BA-05", "BA Team", "Requirements", "Business rules catalogue", "Existing rules and decision logic", "BA pack", "", "Must", "BA Analyst", S_D, -6),
    ("BA-06", "BA Team", "Fit-gap", "Product Fit-Gap Matrix", "All in-scope requirements classified", "BA pack", "1.14", "Must", "BA Lead", S_P, -5),
    ("BA-07", "BA Team", "Requirements", "Customisation requirements", "Features not met by configuration", "BA pack", "", "Should", "BA Analyst", S_P, -5),
    ("BA-08", "BA Team", "Content", "Forms and document catalogue", "Forms, templates, letters, notifications", "BA pack", "", "Should", "BA Analyst", S_D, -6),
    ("BA-09", "BA Team", "Reporting", "Reports catalogue", "Current and future reporting", "BA pack", "", "Should", "BA Analyst", S_P, -5),
    ("BA-10", "BA Team", "Access", "User roles and personas", "User types, permissions, access", "BA pack", "", "Must", "BA Analyst", S_C, -16),
    ("BA-11", "BA Team", "Volumes", "Business volumes", "Users, claims, transactions, peaks", "BA pack", "", "Must", "BA Lead", S_P, -15),
    ("BA-12", "BA Team", "Acceptance", "Business acceptance criteria", "Acceptance conditions for replacement", "BA pack", "", "Should", "BA Lead", S_N, -4),
    ("BA-13", "BA Team", "Workshop", "Demo scenarios for the workshop", "Prioritised, scripts agreed", "Workshop", "", "Must", "BA Lead", S_P, -4),
    ("BA-14", "BA Team", "Workshop", "Business stakeholder list", "Attendance confirmed", "Workshop", "", "Must", "BA Lead", S_C, -15),
    ("TBA-01", "Technical BA", "Inventory", "Application inventory", "Linked to SYS-IDs, owners named", "TBA pack", "", "Must", "Tech BA Lead", S_C, -18),
    ("TBA-02", "Technical BA", "Integration", "Integration catalogue", "Every interface has an INT-ID", "TBA pack", "1.4", "Must", "Tech BA Lead", S_R, -7),
    ("TBA-03", "Technical BA", "Integration", "Interface specifications", "Verified with system owners", "TBA pack", "1.4", "Must", "Tech BA Lead", S_P, -5),
    ("TBA-04", "Technical BA", "Data", "Data entity catalogue", "Entities and relationships", "TBA pack", "", "Should", "Data Analyst", S_D, -6),
    ("TBA-05", "Technical BA", "Data", "Data migration inventory", "Entities, volumes, quality findings", "TBA pack", "1.5", "Must", "Data Analyst", S_P, -16),
    ("TBA-06", "Technical BA", "Data", "Data mapping requirements", "Legacy source to SaaS target mapping", "TBA pack", "", "Should", "Data Analyst", S_N, -3),
    ("TBA-07", "Technical BA", "Inventory", "Batch jobs inventory", "Scheduled jobs and processing", "TBA pack", "", "Should", "Tech BA Lead", S_C, -16),
    ("TBA-08", "Technical BA", "Security", "Authentication inventory", "Service accounts, certificates, methods", "TBA pack", "", "Must", "Tech BA Lead", S_D, -6),
    ("TBA-09", "Technical BA", "Reporting", "Reporting and extraction inventory", "Reports, feeds and consumers", "TBA pack", "", "Should", "Tech BA Lead", S_P, -5),
    ("TBA-10", "Technical BA", "Dependencies", "Technical dependency register", "External systems and third parties", "TBA pack", "", "Must", "Tech BA Lead", S_R, -7),
    ("TBA-11", "Technical BA", "Traceability", "Catalogue reconciled to Element Register", "IDs reconciled, gaps listed", "13", "1.3", "Must", "Tech BA Lead", S_P, -6),
    ("TBA-12", "Technical BA", "Data", "Data retention rules", "Agreed with records management", "TBA pack", "", "Must", "Data Analyst", S_N, -4),
    ("TEC-01", "Technical Team", "Standards", "EA standards confirmation", "Signed off by Enterprise Architecture", "02", "1.6", "Must", "EA Lead", S_C, -17),
    ("TEC-02", "Technical Team", "Security", "Security requirements and data classification", "Reviewed by Security Architecture", "04", "1.7", "Must", "Security Architect", S_R, -7),
    ("TEC-03", "Technical Team", "Network", "Network and connectivity review", "Allowlisting, private link, DNS agreed", "05", "1.9", "Must", "Network Lead", S_P, -6),
    ("TEC-04", "Technical Team", "Identity", "Identity integration owner (SSO, MFA, provisioning)", "Owner named, approach agreed", "04", "", "Must", "Identity Lead", S_C, -16),
    ("TEC-05", "Technical Team", "Integration", "Integration platform and target patterns", "Target patterns agreed", "02, diagram 04", "", "Must", "Integration Lead", S_D, -6),
    ("TEC-06", "Technical Team", "Environments", "Environments mapped to ENV-IDs", "Integration and test envs available", "diagram 07", "", "Must", "Platform Lead", S_P, -15),
    ("TST-01", "Test Team", "Strategy", "Test strategy", "Reviewed by project and SA", "Test pack", "1.14", "Must", "Test Lead", S_R, -7),
    ("TST-02", "Test Team", "Scope", "Functional test scope", "Capabilities and scenarios", "Test pack", "", "Must", "Test Lead", S_D, -6),
    ("TST-03", "Test Team", "Scope", "SaaS integration test scope", "Enterprise and external integrations", "Test pack", "", "Must", "Test Lead", S_P, -5),
    ("TST-04", "Test Team", "Migration", "Data migration validation strategy", "Reconciliation and rehearsal plan", "Test pack", "", "Must", "Test Lead", S_P, -5),
    ("TST-05", "Test Team", "Scope", "Regression test scope", "Capabilities to preserve, vendor releases", "Test pack", "", "Should", "Test Analyst", S_N, -4),
    ("TST-06", "Test Team", "NFR", "Performance test requirements", "Linked to NFR targets", "Test pack", "", "Must", "Test Analyst", S_P, -5),
    ("TST-07", "Test Team", "Security", "Security test requirements", "Pen test and vulnerability assessment", "Test pack", "", "Must", "Test Analyst", S_D, -6),
    ("TST-08", "Test Team", "Environments", "SaaS environment requirements", "Vendor environments and client access", "Test pack", "", "Should", "Test Lead", S_P, -5),
    ("TST-09", "Test Team", "Acceptance", "UAT approach", "Business validation and acceptance", "Test pack", "", "Must", "Test Lead", S_D, -6),
    ("TST-10", "Test Team", "Tooling", "Test automation requirements", "Framework and tooling", "Test pack", "", "Could", "Test Analyst", S_N, -2),
    ("TST-11", "Test Team", "Workshop", "Workshop questions for the vendor", "Tooling, sandboxes, support", "Workshop", "", "Should", "Test Lead", S_C, -15),
    ("PRJ-01", "Project Team", "Scope", "Project scope and objectives", "Agreed, signed off by sponsor", "Project pack", "1.14", "Must", "Project Manager", S_C, -18),
    ("PRJ-02", "Project Team", "Planning", "High-level delivery roadmap", "Milestones and phases shared", "Project pack", "", "Must", "Project Manager", S_R, -7),
    ("PRJ-03", "Project Team", "Governance", "Governance model and design authority", "Roles and decision path set", "Project pack", "", "Must", "Project Manager", S_C, -17),
    ("PRJ-04", "Project Team", "Stakeholders", "Stakeholder register", "Business SMEs and technical owners", "Project pack", "", "Must", "Project Manager", S_C, -17),
    ("PRJ-05", "Project Team", "Resources", "Resource availability", "Client and vendor resource assumptions", "Project pack", "", "Must", "Project Manager", S_P, -15),
    ("PRJ-06", "Project Team", "RAID", "RAID register", "Includes architecture risks (09)", "Project pack", "1.11", "Must", "Project Manager", S_R, -7),
    ("PRJ-07", "Project Team", "Change", "Change management strategy", "Process and user adoption", "Project pack", "", "Should", "Change Lead", S_N, -3),
    ("PRJ-08", "Project Team", "Change", "Training requirements", "User and administrator training", "Project pack", "", "Should", "Change Lead", S_N, -3),
    ("PRJ-09", "Project Team", "Transition", "Cutover constraints", "Migration windows, blackout periods", "Project pack", "", "Must", "Project Manager", S_D, -6),
    ("PRJ-10", "Project Team", "Transition", "Legacy retirement plan", "Retention, shutdown, contract exit", "Project pack, 10", "", "Should", "Project Manager", S_P, -5),
    ("PRJ-11", "Project Team", "Workshop", "Workshop logistics", "Invites, venue, pre-reads sent", "Workshop", "", "Must", "Project Manager", S_P, -5),
]
# SaaS-specific evidence requested from the vendor (feeds Gate 2); due after the pack is issued.
VENDOR_ITEMS = [
    ("Licensing and subscription model", "Per user, transaction, module or consumption"),
    ("Environment strategy", "Included environments and cost of extras"),
    ("Release management model", "Release cadence and regression impact"),
    ("Customisation and extension model", "What can change without affecting upgrades"),
    ("API limits and throttling", "Transaction limits, webhooks, events, files"),
    ("Hosting and data residency declaration", "Storage and processing locations, sub-processors"),
    ("SaaS security assurance pack", "ISO 27001, SOC 2, pen tests, C&A evidence"),
    ("SSO and identity integration", "Entra ID, MFA, federation, provisioning"),
    ("SaaS resilience documentation", "RTO, RPO and DR commitments"),
    ("Privacy and data processing assessment", "Sub-processors, access, breach notification"),
    ("SaaS exit and data portability plan", "Export and termination approach"),
    ("Vendor shared responsibility matrix", "Vendor-operated versus client-operated"),
    ("SLA and support model", "Incident response, availability, escalation"),
]
for i, (n, e) in enumerate(VENDOR_ITEMS, 1):
    DELIV.append((f"VEN-{i:02d}", "Vendor", "SaaS evidence", n, e, "11 DDQ", "2.x", "Must", "Vendor", S_N, 28))
BLOCKERS = {"CSA-08": "Operations has not agreed RTO / RPO values", "TBA-05": "Legacy DB extract access pending",
            "TEC-06": "SIT integration environment not provisioned"}

# ----------------------------------------------------------------- lifecycle plan (phase, task, owner, start, end, milestone)
PLAN = [
    (PHASES[0], "Confirm workshop date, attendees and format with the client", "Project Manager", -24, -21, "No"),
    (PHASES[0], "Send invite, agenda and pre-read for readiness meeting", "Client SA", -20, -18, "No"),
    (PHASES[0], "Leads pre-fill readiness status, evidence, blockers, ETA", "All leads", -18, -15, "No"),
    (PHASES[0], "Check Element Register IDs against Technical BA catalogue", "Client SA", -17, -15, "No"),
    (PHASES[0], "Prepare readiness heat map from pre-filled responses", "Client SA", -15, -14, "No"),
    (PHASES[0], "Readiness meeting (90 min) and go / no-go call", "Client SA", -14, -14, "Yes"),
    (PHASES[0], "Issue minutes, heat map, actions and go / no-go outcome", "Note-taker", -13, -13, "No"),
    (PHASES[0], "Close readiness actions and reds", "All leads", -13, -4, "No"),
    (PHASES[0], "Issue pre-read pack to the client", "Project Manager", -5, -5, "Yes"),
    (PHASES[0], "Checkpoint meeting (T-3)", "Client SA", -3, -3, "Yes"),
    (PHASES[0], "Workshop dry run (T-2)", "Client SA", -2, -2, "No"),
    (PHASES[1], "Discovery workshop day 1 (sessions 1-4)", "Client SA", 0, 0, "Yes"),
    (PHASES[1], "Discovery workshop day 2 (sessions 5-8)", "Client SA", 1, 1, "Yes"),
    (PHASES[1], "Capture outcomes, decisions and open questions", "Note-taker", 1, 3, "No"),
    (PHASES[1], "Distribute workshop summary and question log", "Project Manager", 3, 4, "No"),
    (PHASES[2], "Update deliverables with workshop feedback", "All leads", 4, 12, "No"),
    (PHASES[2], "Replace all (example) values or mark TBC", "Client SA", 5, 12, "No"),
    (PHASES[2], "Gate 1 review: discovery completeness", "Client SA", 13, 13, "Yes"),
    (PHASES[2], "Issue consolidated discovery pack to the vendor", "Project Manager", 14, 14, "Yes"),
    (PHASES[3], "Vendor validates client diagrams and identifies gaps", "Vendor", 15, 28, "No"),
    (PHASES[3], "Receive SaaS-specific evidence (DDQ, residency, API limits)", "Vendor", 15, 28, "No"),
    (PHASES[3], "Vendor solution architecture review", "Client SA", 30, 31, "No"),
    (PHASES[3], "Gate 2 review: architecture alignment", "Client SA", 32, 32, "Yes"),
    (PHASES[4], "Vendor submits the eight mandatory estimation outputs", "Vendor", 33, 47, "No"),
    (PHASES[4], "Traceability and confidence review of WBS and estimate", "Client SA", 48, 52, "No"),
    (PHASES[4], "Red-flag check and vendor clarifications", "Client SA", 50, 54, "No"),
    (PHASES[4], "Gate 3 review: estimation validation", "Client SA", 56, 56, "Yes"),
    (PHASES[5], "Discovery completeness report to sponsor", "Client SA", 57, 59, "No"),
    (PHASES[5], "Lessons learned and archive evidence", "Project Manager", 60, 62, "Yes"),
]

# ----------------------------------------------------------------- workshop sessions
SESSIONS = [
    ("Context, scope and objectives", 0, "09:00", 45, "Project Manager", "Sponsor, business owner", "Project pack", "Confirmed"),
    ("Current-state walkthrough", 0, "09:45", 75, "Client SA", "System owners", "Diagrams 01-02, 13", "Confirmed"),
    ("Business processes and fit-gap demo", 0, "11:15", 90, "BA Lead", "Process owners, SMEs", "BA pack", "Planned"),
    ("Target architecture and integration", 0, "13:30", 90, "Client SA", "Integration, EA", "Diagrams 03-04, 02", "Confirmed"),
    ("Data migration and decommissioning", 1, "09:00", 75, "Tech BA Lead", "Data owners, records mgmt", "Diagrams 05, 10; 10", "Planned"),
    ("Security, identity and NFRs", 1, "10:30", 75, "Security Architect", "Security, privacy", "Diagrams 06, 08; 04, 07", "Planned"),
    ("Environments, testing and operations", 1, "13:00", 75, "Test Lead", "Ops, service mgmt", "Diagram 07, 09; 06, 08", "Planned"),
    ("Estimation approach and next steps", 1, "14:30", 45, "Client SA", "Sponsor, procurement", "12, Gates", "Planned"),
]

# ----------------------------------------------------------------- gates (doc 14)
GATE1 = [("1.1", "Diagrams 01-08 complete, with actual system names and IDs", "Must", "Partially met"),
         ("1.2", "Diagrams 09-10 complete", "Should", "Partially met"),
         ("1.3", "Every diagram element is in the Element Register (13)", "Must", "Partially met"),
         ("1.4", "Every current-state interface has an INT-ID and a Technical BA catalogue entry", "Must", ""),
         ("1.5", "Migration inventory (volumes, entities) available from the Technical BA", "Must", ""),
         ("1.6", "EA standards (02) confirmed with Enterprise Architecture", "Must", "Met"),
         ("1.7", "Security requirements (04) reviewed; data classification confirmed", "Must", ""),
         ("1.8", "NFR values (07) agreed with business, security and operations", "Must", "Not met"),
         ("1.9", "Network requirements (05) reviewed by the network team", "Must", ""),
         ("1.10", "Shared responsibility (08) reviewed by service management", "Must", ""),
         ("1.11", "Risks, assumptions, constraints (09) logged and in the project RAID", "Must", "Met"),
         ("1.12", "Decommissioning principles (10) reviewed with records management", "Must", ""),
         ("1.13", "Due-diligence questionnaire (11) includes regulatory supplement", "Must", "Met"),
         ("1.14", "BA fit-gap, test strategy and project constraints in the consolidated pack", "Must", ""),
         ("1.15", "All (example) values replaced or marked 'to be confirmed'", "Must", "")]
GATE2 = [("2.1", "Vendor has validated or corrected every client diagram", "Must"),
         ("2.2", "Integration follows EAS-P03 / EAS-I05 (no point-to-point, no DB access)", "Must"),
         ("2.3", "Every INT-ID has an agreed pattern, authentication and error handling", "Must"),
         ("2.4", "API limits (SAR-031) sufficient for integration and migration volumes", "Must"),
         ("2.5", "Customisations minimised, justified and approved by design authority", "Must"),
         ("2.6", "Identity design meets SEC-001 to SEC-006", "Must"),
         ("2.7", "Data residency confirmed in writing, including sub-processors", "Must"),
         ("2.8", "NFRs met by subscription tier, or gaps accepted", "Must"),
         ("2.9", "Environment strategy maps to client ENV-IDs", "Must"),
         ("2.10", "Shared responsibility matrix agreed, no unowned activities", "Must"),
         ("2.11", "Exit / data portability approach is acceptable", "Must"),
         ("2.12", "Security assurance evidence received; C&A path agreed", "Must"),
         ("2.13", "Architecture decisions recorded (ADR log in 09)", "Should")]
GATE3 = [("3.1", "All eight mandatory outputs (12) received", "Must"),
         ("3.2", "Every requirement has a fit-gap classification; non-standard items costed", "Must"),
         ("3.3", "Every INT-ID and migration object has its own estimate line", "Must"),
         ("3.4", "Every WBS line traces to requirement / element / NFR IDs", "Must"),
         ("3.5", "Confidence levels applied; Unestimated items have a plan and range", "Must"),
         ("3.6", "Assumptions consistent with client assumptions (09)", "Must"),
         ("3.7", "Subscription costs reflect volumes, environments, consumption", "Must"),
         ("3.8", "Recurring run costs and 5-year TCO included", "Must"),
         ("3.9", "Exclusions reviewed; client-side costs estimated separately", "Must"),
         ("3.10", "Effort benchmarked against comparable implementations", "Should"),
         ("3.11", "Migration cycles and cutover rehearsals included (DEC-011)", "Must"),
         ("3.12", "Risk contingency aligned with the risk register", "Should")]
RED_FLAGS = ["A single fixed price with no breakdown or confidence levels",
             "Integration or migration estimated as one lump sum",
             "'Standard' claimed for complex requirements without a demonstration",
             "Data residency or exit terms vague or deferred to the contract",
             "API limits undisclosed or 'to be confirmed'",
             "Heavy reliance on customisation, or roadmap features without committed dates"]

# ----------------------------------------------------------------- vendor estimation outputs (doc 12 / reference2)
VENDOR_OUT = [
    ("SaaS Product Fit-Gap Assessment", "Standard, configuration, extensions, customisations, unsupported"),
    ("Solution Architecture", "Target SaaS, integration, security and operational model"),
    ("Implementation Scope and WBS", "Every activity broken into work packages"),
    ("Integration and Data Migration Estimate", "Complexity and effort per interface and migration object"),
    ("Resource and Effort Estimate", "Person-days by role, activity and phase"),
    ("Implementation Roadmap", "Dependencies, milestones, critical path, duration"),
    ("Commercial Cost Breakdown", "Subscription, implementation, optional, third-party, recurring"),
    ("Assumptions, Risks and Exclusions", "Confidence, unresolved dependencies, potential extra costs"),
]
# cost component, drivers, up to three source deliverable IDs (reference1 cost model)
COST = [
    ("Product / licensing", "User volumes, modules, environments, licences", "BA-11", "BA-10", "VEN-01"),
    ("Functional implementation", "Processes, features, configuration, customisation", "BA-04", "BA-06", "BA-03"),
    ("Integration", "Number, complexity and type of interfaces", "TBA-02", "TBA-03", "TEC-05"),
    ("Data migration", "Volumes, quality, transformation, history", "TBA-05", "TBA-06", "TBA-04"),
    ("Security and compliance", "Controls, identity, privacy, accreditation", "CSA-05", "TEC-02", "TEC-04"),
    ("Infrastructure / environments", "Environments, connectivity, deployment", "TEC-06", "CSA-06", "VEN-02"),
    ("Testing", "SIT, UAT, regression, performance, security", "TST-01", "TST-03", "TST-06"),
    ("Deployment", "Cutover, release, migration, go-live", "PRJ-09", "TST-04", "CSA-11"),
    ("Project management", "Governance, coordination, reporting", "PRJ-03", "PRJ-02", "PRJ-05"),
    ("Support and transition", "Training, knowledge transfer, hypercare", "PRJ-08", "CSA-07", "CSA-09"),
]
FIT_AREAS = [  # example preliminary BA fit-gap counts per capability area
    ("Claims intake and lodgement", [14, 9, 2, 1, 1, 0, 3]),
    ("Assessment and decisioning", [8, 11, 4, 2, 0, 1, 4]),
    ("Case management and workflow", [12, 10, 3, 1, 2, 0, 2]),
    ("Payments and finance", [6, 5, 3, 2, 0, 1, 3]),
    ("Customer and partner management", [10, 6, 1, 0, 1, 0, 2]),
    ("Documents and correspondence", [7, 8, 2, 1, 0, 0, 1]),
    ("Reporting and analytics", [9, 4, 2, 0, 1, 1, 5]),
]
RESP = [("Business requirements", "Accountable", "Consulted", "Yes"), ("Product fit-gap", "Consulted", "Responsible", "Yes"),
        ("SaaS platform infrastructure", "Informed", "Responsible", "Yes"), ("SaaS configuration", "Approves", "Responsible", "Yes"),
        ("Custom extensions", "Approves architecture", "Responsible", "No"), ("Enterprise integration", "Shared", "Shared", "No"),
        ("Legacy data extraction", "Responsible", "Consulted", "Yes"), ("Data transformation and loading", "Shared", "Shared", "No"),
        ("SaaS platform security", "Assesses", "Responsible", "Yes"), ("Client identity integration", "Responsible", "Supports", "Yes"),
        ("UAT", "Responsible", "Supports", "Yes"), ("SaaS platform testing", "Consulted", "Responsible", "No"),
        ("Cutover", "Shared", "Shared", "No"), ("SaaS operations", "Shared", "Responsible", "No"),
        ("Business operations", "Responsible", "Supports", "Yes"), ("Legacy decommissioning", "Responsible", "Consulted", "No")]
# type, title, team, owner, raised offset, likelihood, impact, mitigation, due offset, status
RAID = [
    ("Risk", "Business SME availability for workshop sessions", "BA Team", "BA Lead", -20, 3, 4, "Confirm attendance; nominate delegates", -4, "Mitigating"),
    ("Risk", "Interface specifications unverified with system owners", "Technical BA", "Tech BA Lead", -18, 4, 4, "Owner walkthroughs before T-5", -5, "Open"),
    ("Issue", "NFR values (RTO / RPO) not agreed by operations", "Client SA", "Client SA", -16, 5, 4, "Escalate to service owner; propose interim values", -7, "Open"),
    ("Risk", "Data residency not confirmed by vendor in writing", "Client SA", "Client SA", -15, 3, 5, "Add DDQ-030/031 as gate 2 must", 28, "Open"),
    ("Risk", "Vendor API limits undisclosed", "Technical Team", "Integration Lead", -15, 3, 4, "Request limits in DDQ; test in sandbox", 28, "Open"),
    ("Issue", "Legacy database extract access pending", "Technical BA", "Data Analyst", -14, 4, 3, "Raise access request with DBA team", -8, "Open"),
    ("Assumption", "Subscription includes three non-production environments", "Technical Team", "Platform Lead", -18, 2, 3, "Validate with vendor environment strategy", 28, "Open"),
    ("Dependency", "Identity team capacity for SSO / MFA design", "Technical Team", "Identity Lead", -17, 2, 3, "Book capacity for weeks 3-6", -2, "Mitigating"),
    ("Risk", "Example values left in the pack at issue", "Client SA", "Client SA", -14, 2, 4, "Gate 1 item 1.15 check", 12, "Open"),
    ("Risk", "Client attendee list incomplete", "Project Team", "Project Manager", -19, 2, 3, "Confirm invitees at checkpoint", -3, "Closed"),
]
DEPS = [("Technical BA", "BA Team", "Integration and data scope for the fit-gap", -8, "In progress"),
        ("Technical BA", "Client SA", "INT / DATA catalogue matched to Element Register IDs", -6, "In progress"),
        ("Technical Team", "Test Team", "NFR targets with measurable criteria", -16, "Not started"),
        ("BA Team", "Client SA", "Fit-gap results for target architecture", -5, "Not started"),
        ("All teams", "Project Team", "Risks, assumptions, constraints for the RAID log", -15, "Delivered"),
        ("Project Team", "All teams", "Workshop date, attendees, agenda slots", -16, "Delivered")]
# action, source, team, owner, raised, due, status
ACTIONS = [("Agree interim RTO / RPO values with operations", "Readiness meeting", "Client SA", "Client SA", 0, -9, "Open"),
           ("Walk through unverified interface specs with system owners", "Readiness meeting", "Technical BA", "Tech BA Lead", 0, -6, "Open"),
           ("Provision SIT integration environment", "Readiness meeting", "Technical Team", "Platform Lead", 0, -7, "In progress"),
           ("Complete Product Fit-Gap classification for in-scope requirements", "Readiness meeting", "BA Team", "BA Lead", 0, -5, "In progress"),
           ("Confirm client attendees per session", "Readiness meeting", "Project Team", "Project Manager", 0, -6, "Open"),
           ("Book workshop dry run (T-2)", "Readiness meeting", "Client SA", "Client SA", 0, -10, "Done"),
           ("Replace (example) values in diagrams 01-08", "Readiness meeting", "Client SA", "Client SA", 0, -4, "Open"),
           ("Send readiness minutes and heat map", "Readiness meeting", "Project Team", "Note-taker", 0, -13, "Done")]
DECISIONS = [("Workshop runs over two days with eight sessions", "Readiness meeting", "Client SA, Project Manager", "Allows demo time for fit-gap", "Agenda updated"),
             ("Shared IDs (SYS / INT / DATA / ENV) are the single key across all packs", "Readiness meeting", "Client SA", "Prevents traceability gaps", "Technical BA catalogue re-keyed")]
PRE_CHECK = [("Send invite with agenda and pre-read", "Client SA", -20, "Yes"),
             ("Leads pre-fill their readiness slide (24h before)", "All leads", -15, "Yes"),
             ("Pull Element Register and check missing catalogue entries", "Client SA", -15, "Yes"),
             ("Prepare heat map from pre-filled responses", "Client SA", -14, "Yes"),
             ("Book note-taker; open actions and decisions logs", "Project Manager", -15, "Yes"),
             ("Confirm workshop date, attendees and format with client", "Project Manager", -21, "Yes")]
RUN_SHEET = [("0:00", 5, "1-4", "Welcome, purpose, agenda, ground rules", "Client SA"),
             ("0:05", 5, "5-6", "Where we are and how we rate readiness", "Client SA"),
             ("0:10", 45, "7-12", "Team readiness round (7-8 min each)", "Each lead"),
             ("0:55", 10, "13-14", "Heat map and cross-team dependencies", "Client SA"),
             ("1:05", 8, "15", "Risks, blockers and asks", "All"),
             ("1:13", 7, "16", "Workshop plan: agenda, roles, logistics, rehearsal", "Client SA, Project"),
             ("1:20", 7, "17", "Actions, owners and dates", "Note-taker"),
             ("1:27", 3, "18", "Go / conditional go / no-go and close", "Client SA")]
POST_CHECK = [("Send minutes, final heat map, actions and go / no-go outcome", "Client SA", -13, "No"),
              ("Update Gate 1 checklist with status and evidence links", "Client SA", -13, "No"),
              ("Update the RAID log with new risks", "Project Manager", -13, "No"),
              ("Set the checkpoint meeting (T-3)", "Project Manager", -13, "No"),
              ("Schedule the dry run (T-2)", "Client SA", -13, "No")]
DIAGRAMS = [  # (no, name, level, priority, mermaid stem) - Visio files live in diagrams/mermaid-visio/
    ("01", "Current-State System Context", "L1", "Must", "current-state-system-context"),
    ("02", "Current-State Application Landscape", "L2", "Must", "Current-State Application Landscape"),
    ("03", "Target SaaS Solution Context", "L1", "Must", "Target SaaS Solution Context"),
    ("04", "Target SaaS Integration Architecture", "L2", "Must", "Target SaaS Integration Architecture"),
    ("05", "Data Migration Architecture", "L2", "Must", "Data Migration Architecture"),
    ("06", "Identity and Security Architecture", "L2", "Must", "Identity and Security Architecture"),
    ("07", "Environment and Deployment Architecture", "L2", "Must", "Environment and Deployment Architecture"),
    ("08", "Non-Functional Requirements Architecture", "L2", "Must", "Non-Functional Requirements Architecture"),
    ("09", "SaaS Shared Responsibility", "Conceptual", "Should", "SaaS Shared Responsibility Architecture"),
    ("10", "Legacy Decommissioning and Transition", "Conceptual", "Should", "Legacy Decommissioning and Transition Architecture"),
    ("E1", "Revised Cost Estimation Model", "Governance", "Should", "Revised cost estimation model"),
    ("E2", "Cost Estimation Traceability", "Governance", "Should", "costEstimationTraceablityDiagram"),
    ("E3", "Backtracking Diagram", "Governance", "Could", "Backtracking diagram"),
    ("E4", "Updated End-to-End Backtracking", "Governance", "Should", "updatedE2EBacktracking"),
]

# ================================================================= workbook helpers
class Book:
    def __init__(self, path):
        self.wb = xlsxwriter.Workbook(path)
        self.wb.set_properties({"title": "Discovery Workshop Tracker", "author": "Client Solution Architect",
                                "comments": "Generated by tools/build_discovery_tracker.py"})
        self._fmt = {}

    def F(self, **kw):
        kw.setdefault("font_name", FONT)
        kw.setdefault("font_size", 10)
        key = tuple(sorted(kw.items()))
        if key not in self._fmt:
            self._fmt[key] = self.wb.add_format(kw)
        return self._fmt[key]


B = None  # set in main()
STATUS_COLOURS = {"Green": (GREEN_BG, GREEN), "Amber": (AMBER_BG, "#9A6700"), "Red": (RED_BG, RED),
                  "N/A": (GREY_BG, GREY)}
OUTCOME_COLOURS = {"Pass": (GREEN, WHITE), "Conditional": (AMBER, WHITE), "Fail": (RED, WHITE),
                   "In progress": ("#3C6E9F", WHITE), "Not assessed": (SLATE, WHITE),
                   "GO": (GREEN, WHITE), "CONDITIONAL GO": (AMBER, WHITE), "NO-GO": (RED, WHITE),
                   "Complete": (GREEN, WHITE), "Not started": (SLATE, WHITE)}


def cf_text(ws, r1, c1, r2, c2, mapping, bold=True):
    for text, (bg, fg) in mapping.items():
        ws.conditional_format(r1, c1, r2, c2, {"type": "cell", "criteria": "equal to", "value": f'"{text}"',
                                               "format": B.F(bg_color=bg, font_color=fg, bold=bold)})


def sheet_header(ws, title, subtitle, width_cols=12):
    ws.hide_gridlines(2)
    ws.set_row(0, 30)
    ws.set_row(1, 18)
    ws.merge_range(0, 0, 0, width_cols - 1, title, B.F(bold=True, font_size=16, font_color=WHITE, bg_color=NAVY,
                                                       valign="vcenter", indent=1))
    ws.merge_range(1, 0, 1, width_cols - 1, subtitle, B.F(italic=True, font_color=GREY, bg_color=LIGHT,
                                                          valign="vcenter", indent=1))
    ws.write_url(0, width_cols, "internal:'Home'!A1", B.F(font_color=TEAL, underline=1, bold=True), "<< Home")


HDR = None


def table(ws, name, r0, c0, columns, data, spare=0, style="Table Style Light 9"):
    """columns: dicts with header, width, fmt (format kwargs), formula, valid (list name), cf (mapping)."""
    rows = [list(r) + [None] * (len(columns) - len(r)) for r in data] + [[None] * len(columns) for _ in range(spare)]
    n = max(len(rows), 1)
    spec = []
    for col in columns:
        s = {"header": col["header"], "header_format": B.F(bold=True, font_color=WHITE, bg_color=NAVY,
                                                           text_wrap=True, valign="vcenter")}
        s["format"] = B.F(**col.get("fmt", {}), valign="top", text_wrap=col.get("wrap", True))
        if col.get("formula"):
            s["formula"] = col["formula"]
        spec.append(s)
    ws.add_table(r0, c0, r0 + n, c0 + len(columns) - 1,
                 {"name": name, "columns": spec, "data": rows, "style": style, "autofilter": True})
    ws.set_row(r0, 32)
    idx = {}
    for k, col in enumerate(columns):
        c = c0 + k
        idx[col["header"]] = c
        ws.set_column(c, c, col.get("width", 14))
        if col.get("valid"):
            ws.data_validation(r0 + 1, c, r0 + n + 40, c, {"validate": "list", "source": "=" + col["valid"]})
        if col.get("cf"):
            cf_text(ws, r0 + 1, c, r0 + n + 40, c, col["cf"])
        if col.get("bar"):
            ws.conditional_format(r0 + 1, c, r0 + n, c, {"type": "data_bar", "bar_color": "#8FCFD6", "bar_solid": True,
                                                         "min_type": "num", "min_value": 0,
                                                         "max_type": "num", "max_value": 1})
    return {"first": r0 + 1, "last": r0 + n, "col": idx}


DATE = {"num_format": "dd-mmm-yy", "align": "center"}
PCT = {"num_format": "0%", "align": "center"}
CENTER = {"align": "center"}

# ================================================================= Settings and Home
def build_settings(ws):
    sheet_header(ws, "Settings and lists", "Project details drive every date calculation. Lists feed the drop-downs.", 4)
    ws.set_column(0, 0, 2)
    ws.set_column(1, 1, 30)
    ws.set_column(2, 2, 34)
    lab = B.F(bold=True, font_color=NAVY, bg_color=LIGHT, border=1, border_color="#C9D3DE")
    inp = B.F(bg_color="#FFF8E1", border=1, border_color="#C9D3DE")
    inp_d = B.F(bg_color="#FFF8E1", border=1, border_color="#C9D3DE", num_format="dd-mmm-yyyy", align="left")
    calc_d = B.F(bg_color=GREY_BG, border=1, border_color="#C9D3DE", num_format="dd-mmm-yyyy", align="left", bold=True)
    calc_n = B.F(bg_color=GREY_BG, border=1, border_color="#C9D3DE", bold=True, align="left")
    ws.write(3, 1, "Project", B.F(bold=True, font_size=12, font_color=TEAL))
    fields = [("Project name", "Claims SaaS Replacement (example)", inp), ("Client organisation", "[Client]", inp),
              ("SaaS vendor", "[Vendor]", inp), ("Client Solution Architect", "[Name]", inp),
              ("Readiness meeting date", d(-14), inp_d), ("Discovery workshop date (day 1)", W, inp_d),
              ("Today override (optional)", None, inp_d), ("Today (used by all formulas)", "=IF(C11<>\"\",C11,TODAY())", calc_d),
              ("Days to workshop", "=C10-C12", calc_n)]
    for i, (k, v, f) in enumerate(fields):
        ws.write(4 + i, 1, k, lab)
        if v is None:
            ws.write_blank(4 + i, 2, None, f)
        else:
            ws.write(4 + i, 2, v, f)
    ws.write(14, 1, "Yellow cells are inputs. Grey cells are calculated.", B.F(italic=True, font_color=GREY))
    for name, ref in [("ProjectName", "$C$5"), ("ReadinessDate", "$C$9"), ("WorkshopDate", "$C$10"), ("TodayDate", "$C$12")]:
        B.wb.define_name(name, f"=Settings!{ref}")
    col = 4
    for name, items in LISTS.items():
        ws.set_column(col, col, 20)
        ws.write(3, col, name, B.F(bold=True, font_color=WHITE, bg_color=TEAL))
        for k, it in enumerate(items):
            ws.write(4 + k, col, it, B.F(border=1, border_color="#C9D3DE"))
        letter = xl_col_to_name(col)
        B.wb.define_name(name, f"=Settings!${letter}$5:${letter}${4 + len(items)}")
        col += 1


SHEETS = [  # name, tab colour, purpose
    ("Executive Dashboard", TEAL, "One-page lifecycle view: progress, readiness call, gates, risk"),
    ("Readiness Dashboard", TEAL, "Team heat map, go / no-go metrics, dependencies, sessions"),
    ("Estimation Dashboard", TEAL, "Fit-gap, cost-evidence confidence, vendor outputs, red flags"),
    ("Phase Plan", NAVY, "Readiness to close-out task plan with weekly Gantt"),
    ("Deliverables", NAVY, "Master register of every team deliverable with auto RAG"),
    ("Diagrams", NAVY, "The 14 architecture diagrams (Mermaid source and Visio files)"),
    ("Readiness Meeting", NAVY, "Pre / post checklists, run sheet and go / no-go record"),
    ("Workshop Sessions", NAVY, "Discovery workshop agenda, attendees and outcomes"),
    ("Gates", NAVY, "Gate 1-3 checklists (doc 14), red flags and sign-off"),
    ("Vendor Outputs", NAVY, "The eight mandatory vendor estimation outputs"),
    ("Cost Traceability", NAVY, "Cost components traced to discovery evidence and confidence"),
    ("Fit-Gap", NAVY, "Product fit-gap classification by capability area"),
    ("Responsibility", NAVY, "Client versus SaaS vendor shared responsibility matrix"),
    ("RAID", GREY, "Risks, assumptions, issues, dependencies with scoring"),
    ("Dependencies", GREY, "Cross-team dependencies (giver, receiver, due)"),
    ("Actions", GREY, "Action log with overdue flag"),
    ("Decisions", GREY, "Decision log"),
    ("Settings", SLATE, "Project dates, today override and drop-down lists"),
]


def build_home(ws):
    ws.hide_gridlines(2)
    ws.set_column(0, 0, 3)
    ws.set_column(1, 1, 26)
    ws.set_column(2, 2, 70)
    ws.set_column(3, 3, 3)
    ws.set_column(4, 4, 22)
    ws.set_column(5, 5, 60)
    ws.set_row(1, 44)
    ws.merge_range(1, 1, 1, 5, "Discovery Workshop Tracker", B.F(bold=True, font_size=24, font_color=WHITE,
                                                                  bg_color=NAVY, valign="vcenter", indent=1))
    ws.merge_range(2, 1, 2, 5, '=ProjectName&"   |   Readiness → Workshop → Gate 1 Discovery → Gate 2 Architecture → Gate 3 Estimation → Close-out"',
                   B.F(font_color=WHITE, bg_color=TEAL, valign="vcenter", indent=1, bold=True))
    ws.set_row(2, 22)
    ws.merge_range(4, 1, 4, 5, "EXAMPLE DATA: rows are pre-filled with example statuses so the dashboards render. "
                   "Replace owners, statuses, dates and evidence with real values before use.",
                   B.F(bold=True, font_color="#7A4B00", bg_color=AMBER_BG, border=1, border_color=AMBER, text_wrap=True, valign="vcenter", indent=1))
    ws.set_row(4, 30)
    ws.write(6, 1, "Workbook map", B.F(bold=True, font_size=13, font_color=TEAL))
    for i, (name, colour, purpose) in enumerate(SHEETS):
        ws.write_url(7 + i, 1, f"internal:'{name}'!A1", B.F(bold=True, font_color=colour, underline=1), name)
        ws.write(7 + i, 2, purpose, B.F(font_color=GREY))
    ws.write(6, 4, "How to use", B.F(bold=True, font_size=13, font_color=TEAL))
    steps = ["1. Set the project name and workshop date on Settings.",
             "2. Leads update their rows on Deliverables (status, reviewed, evidence, due, blocker).",
             "3. Before the readiness meeting, check the Readiness Dashboard heat map and proposed call.",
             "4. Record the call on Readiness Meeting; log actions, decisions and RAID items.",
             "5. Run the workshop from Workshop Sessions; update Phase Plan progress.",
             "6. Assess Gates 1-3, record vendor outputs, fit-gap and cost confidence.",
             "7. Sign off each gate; the Executive Dashboard shows overall completeness."]
    for i, s in enumerate(steps):
        ws.merge_range(7 + i, 4, 7 + i, 5, s, B.F(text_wrap=True))
    ws.write(15, 4, "RAG rules (applied automatically)", B.F(bold=True, font_size=13, font_color=TEAL))
    rag = [("Green", "Complete, reviewed by someone other than the author, and evidence linked.", GREEN),
           ("Amber", "Content exists or is planned with a due date that has not passed.", AMBER),
           ("Red", "Blocked, overdue, or not complete with no due date (no credible plan).", RED)]
    for i, (k, v, c) in enumerate(rag):
        ws.write(16 + i, 4, k, B.F(bold=True, font_color=WHITE, bg_color=c, align="center"))
        ws.write(16 + i, 5, v, B.F(text_wrap=True))
    ws.write(20, 4, "Readiness call", B.F(bold=True, font_size=13, font_color=TEAL))
    call = [("GO", "All Must items green, or amber with a dated plan landing before the workshop.", GREEN),
            ("CONDITIONAL GO", "Named reds with an owner and a date. Re-check at the checkpoint.", AMBER),
            ("NO-GO", "Reds with no credible plan (no owner or no date). Re-plan the workshop.", RED)]
    for i, (k, v, c) in enumerate(call):
        ws.write(21 + i, 4, k, B.F(bold=True, font_color=WHITE, bg_color=c, align="center"))
        ws.write(21 + i, 5, v, B.F(text_wrap=True))
    ws.write(25, 4, "Gate rule", B.F(bold=True, font_size=13, font_color=TEAL))
    ws.merge_range(26, 4, 26, 5, "A gate passes when every Must item is Met (or N/A) or has an approved exception.",
                   B.F(text_wrap=True))
    ws.write(27, 1, "Sources in this workspace", B.F(bold=True, font_size=13, font_color=TEAL))
    src = ["Client SA Discovery Pack/ (docs 01-14, gate checklist 14)",
           "Discovery Readiness Meeting/ (facilitator script and deck)",
           "reference/reference1.md, referernce2.md, reference3.md (deliverables, cost model, fit-gap, vendor outputs)",
           "diagrams/mermaids/ and diagrams/mermaid-visio/ (architecture diagrams)"]
    for i, s in enumerate(src):
        ws.write(28 + i, 2, s, B.F(font_color=GREY))
        ws.write(28 + i, 1, "•", B.F(font_color=TEAL, align="right"))

# ================================================================= core trackers
RAG_CF = {k: STATUS_COLOURS[k] for k in ("Green", "Amber", "Red", "N/A")}


def build_deliverables(ws):
    sheet_header(ws, "Deliverables register",
                 "Every team deliverable for the consolidated discovery pack. RAG, progress and days-to-due are calculated.", 19)
    rows = []
    for (i, team, cat, name, ev, ref, gate, prio, owner, status, off) in DELIV:
        phase = PHASES[3] if team == "Vendor" else PHASES[0]
        reviewed = "Yes" if status == S_C else ("No" if status != S_N else None)
        link = f"Pack/{team}/{i}" if status in (S_C, S_R) else None
        rows.append([i, phase, team, cat, name, ev, ref, gate, prio, owner, d(off), status, reviewed, link,
                     BLOCKERS.get(i), None, None, None, None])
    cols = [
        {"header": "ID", "width": 9, "fmt": {"bold": True}},
        {"header": "Phase", "width": 16, "valid": "lstPhase"},
        {"header": "Team", "width": 14, "valid": "lstTeams"},
        {"header": "Category", "width": 13},
        {"header": "Deliverable", "width": 36},
        {"header": "Evidence of ready", "width": 32, "fmt": {"font_color": GREY}},
        {"header": "Pack ref", "width": 11},
        {"header": "Gate item", "width": 7, "fmt": CENTER},
        {"header": "Priority", "width": 9, "valid": "lstPriority", "fmt": CENTER},
        {"header": "Owner", "width": 15},
        {"header": "Due date", "width": 11, "fmt": DATE},
        {"header": "Status", "width": 13, "valid": "lstStatus"},
        {"header": "Reviewed", "width": 9, "valid": "lstYesNo", "fmt": CENTER},
        {"header": "Evidence link", "width": 22, "fmt": {"font_color": TEAL}},
        {"header": "Blocker", "width": 26, "fmt": {"font_color": RED}},
        {"header": "Progress", "width": 10, "fmt": PCT, "bar": True,
         "formula": '=IF([@ID]="","",IF([@Status]="Complete",IF([@Reviewed]="Yes",1,0.9),IF([@Status]="In review",0.8,'
                    'IF([@Status]="Draft complete",0.6,IF([@Status]="In progress",0.3,0)))))'},
        {"header": "RAG", "width": 9, "fmt": CENTER, "cf": RAG_CF,
         "formula": '=IF([@ID]="","",IF([@Status]="N/A","N/A",IF(AND([@Status]="Complete",[@Reviewed]="Yes",'
                    '[@[Evidence link]]<>""),"Green",IF(OR([@Blocker]<>"",[@[Due date]]="",[@[Due date]]<TodayDate),"Red","Amber"))))'},
        {"header": "Days to due", "width": 9, "fmt": {"align": "center", "num_format": "0;[Red]-0"},
         "formula": '=IF(OR([@ID]="",[@[Due date]]="",[@RAG]="Green"),"",[@[Due date]]-TodayDate)'},
        {"header": "Notes", "width": 24},
    ]
    t = table(ws, "tblDeliv", 3, 0, cols, rows)
    ws.freeze_panes(4, 5)
    return t


def build_diagrams(ws):
    sheet_header(ws, "Architecture diagrams",
                 "Discovery-level diagrams (reference3.md). Links open the Mermaid source and the generated Visio file.", 11)
    rows = []
    for k, (no, name, lvl, prio, stem) in enumerate(DIAGRAMS):
        status = "In review" if k < 2 else "Draft complete"
        rows.append([no, name, lvl, prio, stem + ".txt", stem + ".vsdx", status, "No", None, None])
    cols = [{"header": "No", "width": 6, "fmt": {"bold": True, "align": "center"}},
            {"header": "Diagram", "width": 38},
            {"header": "Level", "width": 11, "fmt": CENTER},
            {"header": "Priority", "width": 9, "valid": "lstPriority", "fmt": CENTER},
            {"header": "Mermaid source", "width": 40},
            {"header": "Visio file", "width": 40},
            {"header": "Status", "width": 14, "valid": "lstStatus"},
            {"header": "Reviewed", "width": 9, "valid": "lstYesNo", "fmt": CENTER},
            {"header": "RAG", "width": 9, "fmt": CENTER, "cf": RAG_CF,
             "formula": '=IF([@No]="","",IF(AND([@Status]="Complete",[@Reviewed]="Yes"),"Green",IF([@Status]="Not started","Red","Amber")))'},
            {"header": "Notes", "width": 30}]
    t = table(ws, "tblDiag", 3, 0, cols, rows)
    link = B.F(font_color=TEAL, underline=1, valign="top")
    for k, (no, name, lvl, prio, stem) in enumerate(DIAGRAMS):
        r = t["first"] + k
        ws.write_url(r, 4, f"external:..\\diagrams\\mermaids\\{stem}.txt", link, f"mermaids/{stem}.txt")
        ws.write_url(r, 5, f"external:..\\diagrams\\mermaid-visio\\{stem}.vsdx", link, f"mermaid-visio/{stem}.vsdx")
    ws.freeze_panes(4, 2)
    return t


def build_plan(ws):
    rows = []
    for k, (ph, task, owner, s, e, ms) in enumerate(PLAN, 1):
        prog = 1.0 if e < -14 else (0.5 if s <= -14 <= e else 0.0)
        rows.append([f"P{k:02d}", ph, task, owner, d(s), d(e), ms, prog, None, None])
    cols = [{"header": "ID", "width": 6, "fmt": {"bold": True}},
            {"header": "Phase", "width": 25, "valid": "lstPhase", "wrap": False},
            {"header": "Task", "width": 46},
            {"header": "Owner", "width": 15},
            {"header": "Start", "width": 10, "fmt": DATE},
            {"header": "End", "width": 10, "fmt": DATE},
            {"header": "Milestone", "width": 9, "valid": "lstYesNo", "fmt": CENTER},
            {"header": "Progress", "width": 9, "fmt": PCT, "bar": True},
            {"header": "Status", "width": 12, "fmt": CENTER,
             "cf": {"Done": (GREEN_BG, GREEN), "Overdue": (RED_BG, RED), "In progress": (AMBER_BG, "#9A6700"),
                    "Due to start": ("#DCE9F5", NAVY), "Not started": (GREY_BG, GREY)},
             "formula": '=IF([@Task]="","",IF([@Progress]>=1,"Done",IF([@End]<TodayDate,"Overdue",'
                        'IF([@Progress]>0,"In progress",IF([@Start]<=TodayDate,"Due to start","Not started")))))'},
            {"header": "Notes", "width": 18}]
    sheet_header(ws, "Phase plan: readiness to close-out",
                 "Enter Progress (0-100%) per task. Status and the Gantt update from dates, progress and Today.", 10)
    t = table(ws, "tblPlan", 4, 0, cols, rows)
    g0 = 10
    start = d(-24) - dt.timedelta(days=d(-24).weekday())
    weeks = ((d(63) - start).days // 7) + 1
    ws.write(3, g0, "Weekly Gantt (week commencing)", B.F(bold=True, font_color=TEAL))
    hdr = B.F(bold=True, font_color=WHITE, bg_color=TEAL, num_format="dd-mmm", align="center", valign="vcenter",
              rotation=90, font_size=9)
    for k in range(weeks):
        ws.set_column(g0 + k, g0 + k, 3.6)
        ws.write_datetime(4, g0 + k, dt.datetime.combine(start + dt.timedelta(days=7 * k), dt.time()), hdr)
    ws.set_row(4, 46)
    r1, r2, c2 = t["first"], t["last"], g0 + weeks - 1
    top = xl_rowcol_to_cell(r1, g0, row_abs=False, col_abs=False)
    colL = xl_col_to_name(g0)
    rr = r1 + 1
    inweek = f"AND($E{rr}<={colL}$5+6,$F{rr}>={colL}$5)"
    ws.conditional_format(r1, g0, r2, c2, {"type": "formula", "criteria": f"=AND({inweek},$G{rr}=\"Yes\")",
                                           "format": B.F(bg_color=NAVY), "stop_if_true": True})
    ws.conditional_format(r1, g0, r2, c2, {"type": "formula", "criteria": f"=AND({inweek},$H{rr}>=1)",
                                           "format": B.F(bg_color=GREEN), "stop_if_true": True})
    ws.conditional_format(r1, g0, r2, c2, {"type": "formula", "criteria": f"=AND({inweek},$F{rr}<TodayDate)",
                                           "format": B.F(bg_color=RED), "stop_if_true": True})
    ws.conditional_format(r1, g0, r2, c2, {"type": "formula", "criteria": f"={inweek}",
                                           "format": B.F(bg_color="#5FB3BD"), "stop_if_true": True})
    ws.conditional_format(r1, g0, r2, c2, {"type": "formula",
                                           "criteria": f"=AND(TodayDate>={colL}$5,TodayDate<{colL}$5+7)",
                                           "format": B.F(bg_color="#FFF1CC")})
    ws.conditional_format(4, g0, 4, c2, {"type": "formula", "criteria": f"=AND(TodayDate>={colL}$5,TodayDate<{colL}$5+7)",
                                         "format": B.F(bg_color=AMBER, font_color=WHITE, bold=True)})
    ws.write(r2 + 2, g0, "Legend:", B.F(bold=True, font_color=GREY))
    for k, (txt, c) in enumerate([("Milestone", NAVY), ("Done", GREEN), ("Overdue", RED), ("Planned", "#5FB3BD"),
                                  ("This week", "#FFF1CC")]):
        ws.merge_range(r2 + 2, g0 + 2 + k * 4, r2 + 2, g0 + 4 + k * 4, txt,
                       B.F(bg_color=c, font_color=WHITE if c not in ("#FFF1CC",) else NAVY, align="center", font_size=9))
    ws.freeze_panes(5, 3)
    _ = top
    return t

YN_CF = {"Yes": (GREEN_BG, GREEN), "No": (GREY_BG, GREY)}
DV = 'tblDeliv[Team],"<>Vendor",tblDeliv[Priority],"Must"'  # readiness scope: client-team Must items


def build_readiness(ws):
    sheet_header(ws, "Readiness meeting (90 minutes)",
                 "Facilitator script basis: Gate 1 of doc 14. Checklists, run sheet and the go / no-go record.", 10)
    four = [{"header": "Item", "width": 50}, {"header": "Owner", "width": 18},
            {"header": "Due", "width": 10, "fmt": DATE}, {"header": "Done", "width": 9, "valid": "lstYesNo", "fmt": CENTER, "cf": YN_CF}]
    ws.write(3, 0, "Before the meeting (T-3 days to T-0)", B.F(bold=True, font_size=12, font_color=TEAL))
    t1 = table(ws, "tblPre", 4, 0, four, [[a, b, d(c), e] for a, b, c, e in PRE_CHECK])
    r = t1["last"] + 2
    ws.write(r, 0, "Run sheet", B.F(bold=True, font_size=12, font_color=TEAL))
    run_cols = [{"header": "Topic", "width": 50}, {"header": "Lead", "width": 18}, {"header": "Time", "width": 10, "fmt": CENTER},
                {"header": "Minutes", "width": 9, "fmt": CENTER}, {"header": "Slides", "width": 8, "fmt": CENTER},
                {"header": "Covered", "width": 9, "valid": "lstYesNo", "fmt": CENTER, "cf": YN_CF}]
    t2 = table(ws, "tblRun", r + 1, 0, run_cols, [[tp, ld, tm, mn, sl, None] for tm, mn, sl, tp, ld in RUN_SHEET])
    r = t2["last"] + 2
    ws.write(r, 0, "After the meeting (within 24 hours)", B.F(bold=True, font_size=12, font_color=TEAL))
    table(ws, "tblPost", r + 1, 0, four, [[a, b, d(c), e] for a, b, c, e in POST_CHECK])
    # go / no-go panel
    L, V = 7, 8
    ws.set_column(6, 6, 3)
    ws.set_column(L, L, 36)
    ws.set_column(V, V, 20)
    ws.merge_range(3, L, 3, V, "Go / no-go assessment (calculated)", B.F(bold=True, font_color=WHITE, bg_color=TEAL, indent=1))
    lab = B.F(bg_color=LIGHT, border=1, border_color="#C9D3DE", indent=1)
    val = B.F(bold=True, border=1, border_color="#C9D3DE", align="center", font_size=11)
    metrics = [("Client-team Must deliverables", f'=COUNTIFS({DV},tblDeliv[Status],"<>N/A")'),
               ("Must items green", f'=COUNTIFS({DV},tblDeliv[RAG],"Green")'),
               ("Must items not green", "=I5-I6"),
               ("Must items red", f'=COUNTIFS({DV},tblDeliv[RAG],"Red")'),
               ("Reds without owner or due date", f'=COUNTIFS({DV},tblDeliv[RAG],"Red",tblDeliv[Due date],"")'
                                                  f'+COUNTIFS({DV},tblDeliv[RAG],"Red",tblDeliv[Due date],"<>",tblDeliv[Owner],"")'),
               ("Open readiness actions", '=COUNTIFS(tblActions[Source],"Readiness meeting",tblActions[Status],"Open")'
                                          '+COUNTIFS(tblActions[Source],"Readiness meeting",tblActions[Status],"In progress")')]
    for k, (a, f) in enumerate(metrics):
        ws.write(4 + k, L, a, lab)
        ws.write_formula(4 + k, V, f, val)
    ws.write(10, L, "PROPOSED CALL", B.F(bold=True, font_color=WHITE, bg_color=NAVY, indent=1, font_size=12))
    ws.write_formula(10, V, '=IF(I8=0,"GO",IF(I9=0,"CONDITIONAL GO","NO-GO"))',
                     B.F(bold=True, align="center", font_size=12, border=1))
    cf_text(ws, 10, V, 10, V, {k: OUTCOME_COLOURS[k] for k in ("GO", "CONDITIONAL GO", "NO-GO")})
    B.wb.define_name("ReadinessCall", "='Readiness Meeting'!$I$11")
    B.wb.define_name("MustNotGreen", "='Readiness Meeting'!$I$7")
    B.wb.define_name("MustRed", "='Readiness Meeting'!$I$8")
    B.wb.define_name("RedsNoPlan", "='Readiness Meeting'!$I$9")
    ws.merge_range(12, L, 12, V, "Decision record", B.F(bold=True, font_color=WHITE, bg_color=TEAL, indent=1))
    inp = B.F(bg_color="#FFF8E1", border=1, border_color="#C9D3DE", align="center")
    rec = [("Recorded call", "CONDITIONAL GO", inp), ("Decision date", d(-14), B.F(bg_color="#FFF8E1", border=1, border_color="#C9D3DE", align="center", num_format="dd-mmm-yy")),
           ("Decided by", "Client SA", inp), ("Next checkpoint (T-3)", "=WorkshopDate-3", B.F(border=1, border_color="#C9D3DE", align="center", num_format="dd-mmm-yy", bg_color=GREY_BG)),
           ("Dry run (T-2)", "=WorkshopDate-2", B.F(border=1, border_color="#C9D3DE", align="center", num_format="dd-mmm-yy", bg_color=GREY_BG)),
           ("Conditions", "Close overdue reds by the T-3 checkpoint", inp)]
    for k, (a, v, f) in enumerate(rec):
        ws.write(13 + k, L, a, lab)
        ws.write(13 + k, V, v, f)
    ws.data_validation(13, V, 13, V, {"validate": "list", "source": "=lstCall"})
    cf_text(ws, 13, V, 13, V, {k: OUTCOME_COLOURS[k] for k in ("GO", "CONDITIONAL GO", "NO-GO")})
    B.wb.define_name("ReadinessDecision", "='Readiness Meeting'!$I$14")
    ws.merge_range(20, L, 22, V, "Call rules: GO when no Must item is red. CONDITIONAL GO when every red has an owner "
                   "and a due date. NO-GO when any red has no credible plan.",
                   B.F(text_wrap=True, font_color=GREY, italic=True, valign="top"))


def build_sessions(ws):
    sheet_header(ws, "Discovery workshop sessions", "Two-day agenda from the workshop plan (slide 16). Track outcomes per session.", 13)
    rows = [[f"S{k}", s, d(day), tm, mins, lead, att, refs, st, "No", 0, 0, None]
            for k, (s, day, tm, mins, lead, att, refs, st) in enumerate(SESSIONS, 1)]
    cols = [{"header": "No", "width": 5, "fmt": {"bold": True}}, {"header": "Session", "width": 36},
            {"header": "Date", "width": 10, "fmt": DATE}, {"header": "Start", "width": 7, "fmt": CENTER},
            {"header": "Minutes", "width": 8, "fmt": CENTER}, {"header": "Lead", "width": 16},
            {"header": "Client attendees", "width": 24}, {"header": "Pack refs", "width": 20},
            {"header": "Status", "width": 11, "valid": "lstSession",
             "cf": {"Done": (GREEN_BG, GREEN), "Confirmed": ("#DCE9F5", NAVY), "Planned": (GREY_BG, GREY), "Deferred": (RED_BG, RED)}},
            {"header": "Outcomes captured", "width": 10, "valid": "lstYesNo", "fmt": CENTER, "cf": YN_CF},
            {"header": "Open questions", "width": 9, "fmt": CENTER}, {"header": "Decisions", "width": 9, "fmt": CENTER},
            {"header": "Notes", "width": 26}]
    t = table(ws, "tblSessions", 3, 0, cols, rows, spare=2)
    ws.freeze_panes(4, 2)
    return t


GATE_CF = {"Met": (GREEN_BG, GREEN), "Exception approved": ("#DCE9F5", NAVY), "Partially met": (AMBER_BG, "#9A6700"),
           "Not met": (RED_BG, RED), "N/A": (GREY_BG, GREY)}


def build_gates(ws):
    sheet_header(ws, "Client SA review gates", "Doc 14 (internal, client only). A gate passes when every Must item is Met, N/A or has an approved exception.", 8)
    widths = [6, 62, 9, 17, 26, 14, 10, 22]
    for c, w in enumerate(widths):
        ws.set_column(c, c, w)
    hdr = B.F(bold=True, font_color=WHITE, bg_color=NAVY, align="center", text_wrap=True, valign="vcenter")
    ws.write_row(3, 1, ["Gate", "Must items", "Must met", "Calculated outcome", "Recorded outcome", "Date", "Signed off by"], hdr)
    starts = []
    r = 9
    cols = [{"header": "Item", "width": 6, "fmt": {"bold": True}}, {"header": "Check", "width": 62},
            {"header": "Priority", "width": 9, "fmt": CENTER, "valid": "lstPriority"},
            {"header": "Status", "width": 17, "valid": "lstGate", "cf": GATE_CF},
            {"header": "Evidence", "width": 26}, {"header": "Owner", "width": 14},
            {"header": "Date", "width": 10, "fmt": DATE}, {"header": "Notes", "width": 22}]
    titles = ["Gate 1: Discovery completeness (before issuing to the vendor)",
              "Gate 2: Architecture alignment (vendor solution architecture review)", "Gate 3: Estimation validation"]
    for g, items in enumerate([GATE1, GATE2, GATE3], 1):
        ws.merge_range(r, 0, r, 7, titles[g - 1], B.F(bold=True, font_color=WHITE, bg_color=TEAL, indent=1, font_size=11))
        data = [[i, c, p, (s[0] if s and s[0] else None), None, "Client SA", None, None] for (i, c, p, *s) in items]
        t = table(ws, f"tblGate{g}", r + 1, 0, cols, data)
        starts.append(t)
        r = t["last"] + 2
    ws.merge_range(r, 0, r, 7, "Red flags to escalate (estimation)", B.F(bold=True, font_color=WHITE, bg_color=RED, indent=1, font_size=11))
    rf_cols = [{"header": "Item", "width": 6, "fmt": {"bold": True}}, {"header": "Red flag", "width": 62},
               {"header": "Present", "width": 9, "valid": "lstYesNo", "fmt": CENTER,
                "cf": {"Yes": (RED_BG, RED), "No": (GREEN_BG, GREEN)}}]
    table(ws, "tblRedFlags", r + 1, 0, rf_cols, [[f"RF{k}", f, None] for k, f in enumerate(RED_FLAGS, 1)])
    out_f = B.F(bold=True, align="center", border=1, border_color="#C9D3DE")
    num_f = B.F(align="center", border=1, border_color="#C9D3DE")
    inp = B.F(bg_color="#FFF8E1", border=1, border_color="#C9D3DE", align="center")
    names = ["Gate 1  Discovery completeness", "Gate 2  Architecture alignment", "Gate 3  Estimation validation"]
    for g in range(1, 4):
        rr = 3 + g
        P, S = f"tblGate{g}[Priority]", f"tblGate{g}[Status]"
        ws.write(rr, 1, names[g - 1], B.F(bold=True, bg_color=LIGHT, border=1, border_color="#C9D3DE", indent=1))
        ws.write_formula(rr, 2, f'=COUNTIFS({P},"Must")', num_f)
        ws.write_formula(rr, 3, f'=COUNTIFS({P},"Must",{S},"Met")+COUNTIFS({P},"Must",{S},"Exception approved")'
                                f'+COUNTIFS({P},"Must",{S},"N/A")', num_f)
        e = rr + 1
        ws.write_formula(rr, 4, f'=IF(COUNTIFS({S},"<>")=0,"Not assessed",IF(D{e}=C{e},"Pass",'
                                f'IF(COUNTIFS({P},"Must",{S},"<>")<C{e},"In progress",'
                                f'IF(COUNTIFS({P},"Must",{S},"Not met")>0,"Fail","Conditional"))))', out_f)
        ws.write_blank(rr, 5, None, inp)
        ws.write_blank(rr, 6, None, B.F(bg_color="#FFF8E1", border=1, border_color="#C9D3DE", num_format="dd-mmm-yy"))
        ws.write_blank(rr, 7, None, inp)
        ws.data_validation(rr, 5, rr, 5, {"validate": "list", "source": "=lstOutcome"})
        B.wb.define_name(f"Gate{g}Outcome", f"=Gates!$E${e}")
        B.wb.define_name(f"Gate{g}Met", f"=Gates!$D${e}")
        B.wb.define_name(f"Gate{g}Must", f"=Gates!$C${e}")
    cf_text(ws, 4, 4, 6, 5, {k: OUTCOME_COLOURS[k] for k in ("Pass", "Conditional", "Fail", "In progress", "Not assessed")})
    ws.freeze_panes(3, 0)
    return starts

MONEY = {"num_format": "#,##0", "align": "right"}
CONF_CF = {"Confirmed": (GREEN_BG, GREEN), "Provisional": (AMBER_BG, "#9A6700"), "Unestimated": (RED_BG, RED)}


def build_vendor_outputs(ws):
    sheet_header(ws, "Vendor estimation outputs", "The eight mandatory outputs (doc 12). Gate 3 item 3.1 needs all eight accepted.", 10)
    rows = [[f"VO{k}", o, c, d(47), None, "Not received", None, None, "Client SA", None] for k, (o, c) in enumerate(VENDOR_OUT, 1)]
    cols = [{"header": "#", "width": 5, "fmt": {"bold": True}}, {"header": "Output", "width": 34},
            {"header": "Expected contents", "width": 46, "fmt": {"font_color": GREY}},
            {"header": "Due", "width": 10, "fmt": DATE}, {"header": "Received", "width": 10, "fmt": DATE},
            {"header": "Status", "width": 15, "valid": "lstVendorOut",
             "cf": {"Accepted": (GREEN_BG, GREEN), "Received": ("#DCE9F5", NAVY), "Under review": (AMBER_BG, "#9A6700"),
                    "Rework required": (RED_BG, RED), "Not received": (GREY_BG, GREY)}},
            {"header": "Traceable to IDs", "width": 10, "valid": "lstYesNo", "fmt": CENTER, "cf": YN_CF},
            {"header": "Confidence levels applied", "width": 11, "valid": "lstYesNo", "fmt": CENTER, "cf": YN_CF},
            {"header": "Reviewer", "width": 14}, {"header": "Notes", "width": 26}]
    table(ws, "tblVendor", 3, 0, cols, rows)
    ws.freeze_panes(4, 2)


def build_cost(ws):
    sheet_header(ws, "Cost traceability", "Each cost component traces to discovery evidence (reference1 cost model). "
                 "Evidence progress comes from the Deliverables register.", 12)
    rows = [[f"C{k:02d}", c, drv, s1, s2, s3, None, None, None, None, None, None] for k, (c, drv, s1, s2, s3) in enumerate(COST, 1)]

    def p(k):
        return f"IFERROR(INDEX(tblDeliv[Progress],MATCH([@[Source {k}]],tblDeliv[ID],0)),0)"

    def n(k):
        return f"ISNUMBER(MATCH([@[Source {k}]],tblDeliv[ID],0))"
    prog = (f'=IF([@[Cost component]]="","",IF(({n(1)})+({n(2)})+({n(3)})=0,"",'
            f'({p(1)}+{p(2)}+{p(3)})/(({n(1)})+({n(2)})+({n(3)}))))')
    cols = [{"header": "#", "width": 5, "fmt": {"bold": True}}, {"header": "Cost component", "width": 26},
            {"header": "What drives the cost", "width": 40, "fmt": {"font_color": GREY}},
            {"header": "Source 1", "width": 9, "fmt": CENTER}, {"header": "Source 2", "width": 9, "fmt": CENTER},
            {"header": "Source 3", "width": 9, "fmt": CENTER},
            {"header": "Evidence progress", "width": 10, "fmt": PCT, "bar": True, "formula": prog},
            {"header": "Expected confidence", "width": 13, "fmt": CENTER, "cf": CONF_CF,
             "formula": '=IF([@[Evidence progress]]="","",IF([@[Evidence progress]]>=0.85,"Confirmed",'
                        'IF([@[Evidence progress]]>=0.5,"Provisional","Unestimated")))'},
            {"header": "Vendor confidence", "width": 13, "valid": "lstConf", "fmt": CENTER, "cf": CONF_CF},
            {"header": "Estimate low", "width": 12, "fmt": MONEY}, {"header": "Estimate high", "width": 12, "fmt": MONEY},
            {"header": "Notes", "width": 24}]
    table(ws, "tblCost", 3, 0, cols, rows)
    ws.write(16, 1, "Confidence bands: Confirmed >= 85% evidence progress, Provisional >= 50%, otherwise Unestimated.",
             B.F(italic=True, font_color=GREY))
    ws.freeze_panes(4, 2)


def build_fitgap(ws):
    sheet_header(ws, "Product fit-gap by capability area", "Count of requirements per classification (reference2). "
                 "Example preliminary BA counts; the vendor confirms in output VO1.", 11)
    rows = [[a] + v + [None, None] for a, v in FIT_AREAS]
    cols = [{"header": "Capability area", "width": 32}] + \
           [{"header": h, "width": 12, "fmt": CENTER} for h in FITGAP] + \
           [{"header": "Total", "width": 9, "fmt": {"bold": True, "align": "center"},
             "formula": "=SUM(tblFitGap[@[Standard]:[Unclassified]])"},
            {"header": "Standard or config", "width": 11, "fmt": PCT, "bar": True,
             "formula": '=IF([@Total]=0,"",([@Standard]+[@Configuration])/[@Total])'}]
    table(ws, "tblFitGap", 3, 0, cols, rows, spare=1)
    legend = [("Standard", "Available out of the box", "Usually configuration only"),
              ("Configuration", "Achieved through SaaS configuration", "Configuration effort"),
              ("Extension", "Supported extension or low-code", "Additional development"),
              ("Customisation", "Bespoke development or product change", "Higher cost and upgrade risk"),
              ("Workaround", "Business process change", "Business change effort"),
              ("Not supported", "Product cannot meet requirement", "Scope gap or alternative"),
              ("Unclassified", "Not yet assessed", "Estimation risk")]
    r = 15
    ws.write_row(r, 0, ["Classification", "Meaning", "", "", "Cost implication"], B.F(bold=True, font_color=WHITE, bg_color=TEAL))
    for k, (a, b, c) in enumerate(legend, 1):
        ws.write(r + k, 0, a, B.F(bold=True))
        ws.merge_range(r + k, 1, r + k, 3, b, B.F(font_color=GREY))
        ws.merge_range(r + k, 4, r + k, 6, c, B.F(font_color=GREY))
    ws.write(r, 1, "Meaning", B.F(bold=True, font_color=WHITE, bg_color=TEAL))
    ws.freeze_panes(4, 1)


def build_resp(ws):
    sheet_header(ws, "Shared responsibility: client versus SaaS vendor", "Confirm against the vendor contract and operating model (doc 08).", 6)
    cols = [{"header": "Activity", "width": 34}, {"header": "Client", "width": 20, "valid": "lstRACI"},
            {"header": "SaaS vendor", "width": 20, "valid": "lstRACI"},
            {"header": "Agreed", "width": 9, "valid": "lstYesNo", "fmt": CENTER, "cf": YN_CF},
            {"header": "Check", "width": 12, "fmt": CENTER,
             "cf": {"Agreed": (GREEN_BG, GREEN), "To confirm": (AMBER_BG, "#9A6700"), "Unowned": (RED_BG, RED)},
             "formula": '=IF([@Activity]="","",IF(OR([@Client]="",[@[SaaS vendor]]=""),"Unowned",IF([@Agreed]="Yes","Agreed","To confirm")))'},
            {"header": "Notes", "width": 30}]
    table(ws, "tblResp", 3, 0, cols, [list(x) + [None, None] for x in RESP], spare=2)
    ws.freeze_panes(4, 1)


def build_raid(ws):
    sheet_header(ws, "RAID log", "Score = likelihood x impact (1-5). High >= 15, Medium >= 8.", 14)
    rows = [[f"R{k:02d}", t, ti, tm, ow, d(ra), li, im, None, None, mi, d(du), st]
            for k, (t, ti, tm, ow, ra, li, im, mi, du, st) in enumerate(RAID, 1)]
    cols = [{"header": "ID", "width": 6, "fmt": {"bold": True}}, {"header": "Type", "width": 11, "valid": "lstRAIDType"},
            {"header": "Title", "width": 44}, {"header": "Team", "width": 14, "valid": "lstTeams"},
            {"header": "Owner", "width": 15}, {"header": "Raised", "width": 10, "fmt": DATE},
            {"header": "Likelihood", "width": 9, "valid": "lstScore", "fmt": CENTER},
            {"header": "Impact", "width": 8, "valid": "lstScore", "fmt": CENTER},
            {"header": "Score", "width": 7, "fmt": {"align": "center", "bold": True},
             "formula": '=IF(OR([@Likelihood]="",[@Impact]=""),"",[@Likelihood]*[@Impact])'},
            {"header": "Rating", "width": 9, "fmt": CENTER,
             "cf": {"High": (RED, WHITE), "Medium": (AMBER, WHITE), "Low": (GREEN, WHITE)},
             "formula": '=IF([@Score]="","",IF([@Score]>=15,"High",IF([@Score]>=8,"Medium","Low")))'},
            {"header": "Mitigation", "width": 38}, {"header": "Due", "width": 10, "fmt": DATE},
            {"header": "Status", "width": 11, "valid": "lstRAIDStatus",
             "cf": {"Closed": (GREEN_BG, GREEN), "Mitigating": (AMBER_BG, "#9A6700"), "Open": ("#DCE9F5", NAVY)}}]
    table(ws, "tblRAID", 3, 0, cols, rows, spare=10)
    ws.freeze_panes(4, 3)


def build_deps(ws):
    sheet_header(ws, "Cross-team dependencies", "Most risk sits between teams (slide 14). Confirm giver, receiver and date.", 8)
    rows = [[f"D{k}", g, r, w, d(du), st, None, None] for k, (g, r, w, du, st) in enumerate(DEPS, 1)]
    cols = [{"header": "No", "width": 5, "fmt": {"bold": True}}, {"header": "Giver", "width": 16, "valid": "lstTeams"},
            {"header": "Receiver", "width": 16, "valid": "lstTeams"}, {"header": "What", "width": 50},
            {"header": "Due", "width": 10, "fmt": DATE}, {"header": "Status", "width": 12, "valid": "lstDep"},
            {"header": "RAG", "width": 8, "fmt": CENTER, "cf": RAG_CF,
             "formula": '=IF([@What]="","",IF([@Status]="Delivered","Green",IF(OR([@Due]="",[@Due]<TodayDate),"Red","Amber")))'},
            {"header": "Notes", "width": 26}]
    table(ws, "tblDeps", 3, 0, cols, rows, spare=6)
    ws.freeze_panes(4, 1)


def build_actions(ws):
    sheet_header(ws, "Action log", "Every action needs an owner and a due date. Overdue is calculated.", 10)
    rows = [[f"A{k:02d}", a, s, t, o, d(-14 + ra), d(du), st, None, None] for k, (a, s, t, o, ra, du, st) in enumerate(ACTIONS, 1)]
    cols = [{"header": "#", "width": 5, "fmt": {"bold": True}}, {"header": "Action", "width": 50},
            {"header": "Source", "width": 18}, {"header": "Team", "width": 14, "valid": "lstTeams"},
            {"header": "Owner", "width": 15}, {"header": "Raised", "width": 10, "fmt": DATE},
            {"header": "Due", "width": 10, "fmt": DATE}, {"header": "Status", "width": 11, "valid": "lstAction",
                                                          "cf": {"Done": (GREEN_BG, GREEN), "Cancelled": (GREY_BG, GREY)}},
            {"header": "Overdue", "width": 9, "fmt": CENTER, "cf": {"Yes": (RED, WHITE)},
             "formula": '=IF([@Action]="","",IF(AND([@Status]<>"Done",[@Status]<>"Cancelled",[@Due]<>"",[@Due]<TodayDate),"Yes","No"))'},
            {"header": "Notes", "width": 26}]
    table(ws, "tblActions", 3, 0, cols, rows, spare=12)
    ws.freeze_panes(4, 2)


def build_decisions(ws):
    sheet_header(ws, "Decision log", "Disagreements on IDs, scope or dates get a logged decision and an owner.", 7)
    rows = [[f"DEC{k:02d}", a, f, d(-14), m, r, i] for k, (a, f, m, r, i) in enumerate(DECISIONS, 1)]
    cols = [{"header": "#", "width": 7, "fmt": {"bold": True}}, {"header": "Decision", "width": 50},
            {"header": "Forum", "width": 18}, {"header": "Date", "width": 10, "fmt": DATE},
            {"header": "Made by", "width": 22}, {"header": "Rationale", "width": 32}, {"header": "Impact", "width": 28}]
    table(ws, "tblDecisions", 3, 0, cols, rows, spare=10)
    ws.freeze_panes(4, 2)

# ================================================================= dashboards
DATA_COL = 20  # column U: calculated chart data, kept off the visible canvas


def dash_setup(ws, title, subtitle):
    ws.hide_gridlines(2)
    ws.set_zoom(90)
    ws.set_column(0, 0, 2)
    ws.set_column(1, 18, 9.3)
    ws.set_column(19, 19, 3)
    ws.set_column(DATA_COL, DATA_COL, 26)
    ws.set_column(DATA_COL + 1, DATA_COL + 4, 11)
    ws.set_row(0, 34)
    ws.set_row(1, 20)
    ws.merge_range(0, 1, 0, 18, title, B.F(bold=True, font_size=20, font_color=WHITE, bg_color=NAVY, valign="vcenter", indent=1))
    ws.merge_range(1, 1, 1, 18, subtitle, B.F(font_color=WHITE, bg_color=TEAL, valign="vcenter", indent=1, bold=True))
    ws.merge_range(2, 1, 2, 18, '="Project: "&ProjectName&"     |     Workshop: "&TEXT(WorkshopDate,"dd mmm yyyy")'
                   '&"     |     Today: "&TEXT(TodayDate,"dd mmm yyyy")&"     |     Proposed readiness call: "&ReadinessCall',
                   B.F(font_color=GREY, bg_color=LIGHT, valign="vcenter", indent=1, italic=True))
    ws.write_url(0, 19, "internal:'Home'!A1", B.F(font_color=TEAL, underline=1, bold=True), "Home")
    ws.write(2, DATA_COL, "Chart data (calculated, do not edit)", B.F(bold=True, font_color=SLATE, italic=True))


def tile(ws, r, c, w, label, value, sub, accent, numfmt="0", size=24):
    ws.merge_range(r, c, r, c + w - 1, label, B.F(bold=True, font_color=WHITE, bg_color=accent, align="center",
                                                  valign="vcenter", font_size=9, left=2, right=2, left_color=WHITE, right_color=WHITE))
    ws.merge_range(r + 1, c, r + 2, c + w - 1, value, B.F(bold=True, font_size=size, font_color=accent, bg_color=LIGHT,
                                                          align="center", valign="vcenter", num_format=numfmt,
                                                          left=2, right=2, left_color=WHITE, right_color=WHITE))
    ws.merge_range(r + 3, c, r + 3, c + w - 1, sub, B.F(font_color=GREY, bg_color=LIGHT, align="center", valign="vcenter",
                                                        font_size=9, left=2, right=2, left_color=WHITE, right_color=WHITE,
                                                        bottom=2, bottom_color=accent))
    ws.set_row(r, 18)
    ws.set_row(r + 3, 18)
    return r + 1, c  # value cell


def warn_if_positive(ws, cell_rc):
    r, c = cell_rc
    ws.conditional_format(r, c, r, c, {"type": "cell", "criteria": ">", "value": 0,
                                       "format": B.F(font_color=RED, bg_color=RED_BG)})


def section(ws, r, text):
    ws.merge_range(r, 1, r, 18, text, B.F(bold=True, font_color=NAVY, font_size=11, bottom=2, bottom_color=TEAL))
    ws.set_row(r, 22)


def status_block(ws, r, c, w, label, value, sub):
    ws.merge_range(r, c, r, c + w - 1, label, B.F(bold=True, font_color=NAVY, bg_color=LIGHT, align="center", font_size=9,
                                                  left=2, right=2, left_color=WHITE, right_color=WHITE))
    ws.merge_range(r + 1, c, r + 2, c + w - 1, value, B.F(bold=True, font_size=16, align="center", valign="vcenter",
                                                          font_color=WHITE, bg_color=SLATE, left=2, right=2,
                                                          left_color=WHITE, right_color=WHITE))
    ws.merge_range(r + 3, c, r + 3, c + w - 1, sub, B.F(font_color=GREY, bg_color=LIGHT, align="center", font_size=9,
                                                        left=2, right=2, left_color=WHITE, right_color=WHITE))
    cf_text(ws, r + 1, c, r + 1, c, OUTCOME_COLOURS)


def chart_style(ch, title, legend=True):
    ch.set_title({"name": title, "name_font": {"name": FONT, "size": 11, "bold": True, "color": NAVY}})
    ch.set_chartarea({"border": {"color": "#D5DCE4"}, "fill": {"color": WHITE}})
    ch.set_legend({"position": "bottom", "font": {"name": FONT, "size": 9}} if legend else {"none": True})
    return ch


def ref(sheet, r1, c1, r2, c2):
    return f"='{sheet}'!{xl_rowcol_to_cell(r1, c1, True, True)}:{xl_rowcol_to_cell(r2, c2, True, True)}"


def build_exec(ws):
    name = "Executive Dashboard"
    dash_setup(ws, "Executive Dashboard", "Discovery workshop lifecycle: readiness to completeness")
    tiles = [
        ("LIFECYCLE PROGRESS", "=AVERAGE(tblPlan[Progress])",
         '=COUNTIF(tblPlan[Status],"Done")&" of "&COUNTA(tblPlan[Task])&" plan tasks done"', TEAL, "0%"),
        ("DAYS TO WORKSHOP", "=WorkshopDate-TodayDate", '=TEXT(WorkshopDate,"ddd dd mmm yyyy")', NAVY, '0;"Held "0" days ago"'),
        ("DELIVERABLES GREEN", '=IFERROR(COUNTIF(tblDeliv[RAG],"Green")/COUNTIFS(tblDeliv[Status],"<>N/A"),0)',
         '=COUNTIF(tblDeliv[RAG],"Green")&" of "&COUNTIFS(tblDeliv[Status],"<>N/A")&" (incl. vendor)"', GREEN, "0%"),
        ("MUST ITEMS NOT GREEN", "=MustNotGreen", '="Red: "&MustRed&"   |   Red with no plan: "&RedsNoPlan', RED, "0"),
        ("OPEN ACTIONS", '=COUNTIF(tblActions[Status],"Open")+COUNTIF(tblActions[Status],"In progress")',
         '="Overdue: "&COUNTIF(tblActions[Overdue],"Yes")', AMBER, "0"),
        ("HIGH RISKS OPEN", '=COUNTIFS(tblRAID[Rating],"High",tblRAID[Status],"<>Closed")',
         '="Open RAID items: "&COUNTIFS(tblRAID[Status],"<>Closed",tblRAID[Title],"<>")', "#7A3E9D", "0"),
    ]
    for k, (lab, v, s, col, fmt) in enumerate(tiles):
        cell = tile(ws, 4, 1 + 3 * k, 3, lab, v, s, col, fmt)
        if k >= 3:
            warn_if_positive(ws, cell)
    # lifecycle data
    dc = DATA_COL
    ws.write_row(4, dc, ["Phase", "Progress", "Status"], B.F(bold=True, font_color=SLATE))
    for k, ph in enumerate(PHASES):
        r = 5 + k
        ws.write(r, dc, ph)
        ws.write_formula(r, dc + 1, f'=IFERROR(AVERAGEIFS(tblPlan[Progress],tblPlan[Phase],{xl_rowcol_to_cell(r, dc)}),0)', B.F(num_format="0%"))
        ws.write_formula(r, dc + 2, f'=IF({xl_rowcol_to_cell(r, dc + 1)}>=1,"Complete",IF({xl_rowcol_to_cell(r, dc + 1)}>0,"In progress","Not started"))')
    section(ws, 9, "DISCOVERY LIFECYCLE")
    for k, ph in enumerate(PHASES):
        c = 1 + 3 * k
        num, txt = ph.split(" ", 1)
        ws.merge_range(10, c, 10, c + 2, f"{num}  {txt.upper()}", B.F(bold=True, font_color=WHITE, bg_color=NAVY, align="center",
                                                                     valign="vcenter", font_size=9, text_wrap=True,
                                                                     left=2, right=2, left_color=WHITE, right_color=WHITE))
        ws.merge_range(11, c, 11, c + 2, f"={xl_rowcol_to_cell(5 + k, dc + 2)}", B.F(bold=True, align="center", font_color=WHITE,
                                                                                bg_color=SLATE, left=2, right=2,
                                                                                left_color=WHITE, right_color=WHITE))
        ws.merge_range(12, c, 12, c + 2, f"={xl_rowcol_to_cell(5 + k, dc + 1)}", B.F(bold=True, align="center", font_size=14,
                                                                                font_color=NAVY, bg_color=LIGHT, num_format="0%",
                                                                                left=2, right=2, left_color=WHITE, right_color=WHITE))
    ws.set_row(10, 30)
    ws.set_row(12, 24)
    cf_text(ws, 11, 1, 11, 18, {"Complete": (GREEN, WHITE), "In progress": (AMBER, WHITE), "Not started": (SLATE, WHITE)})
    section(ws, 14, "READINESS CALL AND GATES")
    status_block(ws, 15, 1, 6, "WORKSHOP READINESS (PROPOSED)", "=ReadinessCall", '="Recorded: "&IF(ReadinessDecision="","-",ReadinessDecision)')
    for g, (c, lab) in enumerate([(7, "GATE 1  DISCOVERY COMPLETENESS"), (11, "GATE 2  ARCHITECTURE ALIGNMENT"),
                                  (15, "GATE 3  ESTIMATION VALIDATION")], 1):
        status_block(ws, 15, c, 4, lab, f"=Gate{g}Outcome", f'=Gate{g}Met&" of "&Gate{g}Must&" Must items met"')
    section(ws, 20, "PROGRESS, READINESS AND RISK")
    # team RAG data
    ws.write_row(12, dc, ["Team", "Green", "Amber", "Red"], B.F(bold=True, font_color=SLATE))
    teams = CLIENT_TEAMS + ["Vendor"]
    for k, t in enumerate(teams):
        r = 13 + k
        ws.write(r, dc, t)
        for j, rag in enumerate(["Green", "Amber", "Red"]):
            ws.write_formula(r, dc + 1 + j, f'=COUNTIFS(tblDeliv[Team],{xl_rowcol_to_cell(r, dc)},tblDeliv[RAG],"{rag}")')
    # gate data
    ws.write_row(22, dc, ["Gate", "Must met", "Remaining"], B.F(bold=True, font_color=SLATE))
    for g in range(1, 4):
        ws.write(22 + g, dc, f"Gate {g}")
        ws.write_formula(22 + g, dc + 1, f"=Gate{g}Met")
        ws.write_formula(22 + g, dc + 2, f"=Gate{g}Must-Gate{g}Met")
    ws.write_row(28, dc, ["Rating", "Open items"], B.F(bold=True, font_color=SLATE))
    for k, rt in enumerate(["High", "Medium", "Low"]):
        ws.write(29 + k, dc, rt)
        ws.write_formula(29 + k, dc + 1, f'=COUNTIFS(tblRAID[Rating],"{rt}",tblRAID[Status],"<>Closed")')
    c1 = B.wb.add_chart({"type": "bar"})
    c1.add_series({"name": "Progress", "categories": ref(name, 5, dc, 10, dc), "values": ref(name, 5, dc + 1, 10, dc + 1),
                   "fill": {"color": TEAL}, "gap": 60, "data_labels": {"value": True, "num_format": "0%", "font": {"name": FONT, "size": 9}}})
    c1.set_x_axis({"min": 0, "max": 1, "num_format": "0%", "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}},
                   "num_font": {"name": FONT, "size": 9}})
    c1.set_y_axis({"reverse": True, "num_font": {"name": FONT, "size": 9}})
    chart_style(c1, "Progress by lifecycle phase", legend=False)
    c1.set_size({"width": 610, "height": 300})
    ws.insert_chart(21, 1, c1, {"x_offset": 4, "y_offset": 6})
    c2 = B.wb.add_chart({"type": "bar", "subtype": "stacked"})
    for j, (rag, col) in enumerate([("Green", GREEN), ("Amber", AMBER), ("Red", RED)]):
        c2.add_series({"name": rag, "categories": ref(name, 13, dc, 19, dc), "values": ref(name, 13, dc + 1 + j, 19, dc + 1 + j),
                       "fill": {"color": col}, "gap": 50, "data_labels": {"value": True, "num_format": "0;-0;;@", "font": {"name": FONT, "size": 8, "color": WHITE}}})
    c2.set_y_axis({"reverse": True, "num_font": {"name": FONT, "size": 9}})
    c2.set_x_axis({"num_font": {"name": FONT, "size": 9}, "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}}})
    chart_style(c2, "Deliverable RAG by team")
    c2.set_size({"width": 610, "height": 300})
    ws.insert_chart(21, 10, c2, {"x_offset": 4, "y_offset": 6})
    c3 = B.wb.add_chart({"type": "column", "subtype": "stacked"})
    c3.add_series({"name": "Must met", "categories": ref(name, 23, dc, 25, dc), "values": ref(name, 23, dc + 1, 25, dc + 1),
                   "fill": {"color": GREEN}, "gap": 80, "data_labels": {"value": True, "num_format": "0;-0;;@", "font": {"name": FONT, "size": 9, "color": WHITE}}})
    c3.add_series({"name": "Remaining", "categories": ref(name, 23, dc, 25, dc), "values": ref(name, 23, dc + 2, 25, dc + 2),
                   "fill": {"color": "#C9D3DE"}, "data_labels": {"value": True, "num_format": "0;-0;;@", "font": {"name": FONT, "size": 9}}})
    c3.set_y_axis({"num_font": {"name": FONT, "size": 9}, "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}}})
    c3.set_x_axis({"num_font": {"name": FONT, "size": 9}})
    chart_style(c3, "Gate Must items met")
    c3.set_size({"width": 610, "height": 290})
    ws.insert_chart(38, 1, c3, {"x_offset": 4, "y_offset": 4})
    c4 = B.wb.add_chart({"type": "doughnut"})
    c4.add_series({"name": "Open RAID", "categories": ref(name, 29, dc, 31, dc), "values": ref(name, 29, dc + 1, 31, dc + 1),
                   "points": [{"fill": {"color": RED}}, {"fill": {"color": AMBER}}, {"fill": {"color": GREEN}}],
                   "data_labels": {"value": True, "num_format": "0;-0;;@", "font": {"name": FONT, "size": 10, "bold": True, "color": WHITE}}})
    c4.set_hole_size(55)
    chart_style(c4, "Open RAID items by rating")
    c4.set_size({"width": 610, "height": 290})
    ws.insert_chart(38, 10, c4, {"x_offset": 4, "y_offset": 4})

def build_readiness_dash(ws):
    name = "Readiness Dashboard"
    dash_setup(ws, "Readiness Dashboard", "Is the consolidated discovery pack ready for the client workshop?")
    tiles = [
        ("PROPOSED CALL", "=ReadinessCall", '="Recorded: "&IF(ReadinessDecision="","-",ReadinessDecision)', NAVY, "@", 15),
        ("DAYS TO WORKSHOP", "=WorkshopDate-TodayDate", '="Checkpoint T-3: "&TEXT(WorkshopDate-3,"dd mmm")', TEAL, '0;"Held"', 24),
        ("MUST ITEMS NOT GREEN", "=MustNotGreen", "=\"of \"&'Readiness Meeting'!I5&\" client-team Must items\"", RED, "0", 24),
        ("REDS WITHOUT A PLAN", "=RedsNoPlan", '="Must items red: "&MustRed', RED, "0", 24),
        ("DEPENDENCIES AT RISK", '=COUNTIF(tblDeps[RAG],"Red")',
         '=COUNTIF(tblDeps[RAG],"Green")&" of "&COUNTA(tblDeps[What])&" delivered"', AMBER, "0", 24),
        ("SESSIONS CONFIRMED", '=COUNTIF(tblSessions[Status],"Confirmed")+COUNTIF(tblSessions[Status],"Done")',
         '="of "&COUNTA(tblSessions[Session])&" workshop sessions"', GREEN, "0", 24),
    ]
    for k, (lab, v, s, col, fmt, size) in enumerate(tiles):
        cell = tile(ws, 4, 1 + 3 * k, 3, lab, v, s, col, fmt, size)
        if k == 0:
            cf_text(ws, cell[0], cell[1], cell[0], cell[1], {x: OUTCOME_COLOURS[x] for x in ("GO", "CONDITIONAL GO", "NO-GO")})
        if k in (2, 3, 4):
            warn_if_positive(ws, cell)
    section(ws, 9, "TEAM READINESS HEAT MAP (client teams, from the Deliverables register)")
    hdr = B.F(bold=True, font_color=WHITE, bg_color=NAVY, align="center", valign="vcenter", text_wrap=True, font_size=9)
    ws.merge_range(10, 1, 10, 2, "Team", hdr)
    heads = ["Items", "Avg progress", "Complete", "Reviewed", "Evidence linked", "Blockers", "Green", "Amber", "Red"]
    for j, h in enumerate(heads):
        ws.write(10, 3 + j, h, hdr)
    ws.merge_range(10, 12, 10, 13, "Overall", hdr)
    ws.set_row(10, 30)
    cell = B.F(align="center", border=1, border_color=WHITE, bg_color=LIGHT)
    pct = B.F(align="center", border=1, border_color=WHITE, num_format="0%", bold=True)
    for k, t in enumerate(CLIENT_TEAMS):
        r = 11 + k
        e = r + 1
        T = f"$B{e}"
        ws.merge_range(r, 1, r, 2, t, B.F(bold=True, font_color=NAVY, bg_color=LIGHT, border=1, border_color=WHITE, indent=1))
        f = [f'=COUNTIFS(tblDeliv[Team],{T},tblDeliv[Status],"<>N/A")',
             f"=IFERROR(AVERAGEIFS(tblDeliv[Progress],tblDeliv[Team],{T}),0)",
             f'=IFERROR(COUNTIFS(tblDeliv[Team],{T},tblDeliv[Status],"Complete")/$D{e},0)',
             f'=IFERROR(COUNTIFS(tblDeliv[Team],{T},tblDeliv[Reviewed],"Yes")/$D{e},0)',
             f'=IFERROR(COUNTIFS(tblDeliv[Team],{T},tblDeliv[Evidence link],"<>")/$D{e},0)',
             f'=COUNTIFS(tblDeliv[Team],{T},tblDeliv[Blocker],"<>")',
             f'=COUNTIFS(tblDeliv[Team],{T},tblDeliv[RAG],"Green")',
             f'=COUNTIFS(tblDeliv[Team],{T},tblDeliv[RAG],"Amber")',
             f'=COUNTIFS(tblDeliv[Team],{T},tblDeliv[RAG],"Red")']
        for j, fx in enumerate(f):
            ws.write_formula(r, 3 + j, fx, pct if 1 <= j <= 4 else cell)
        ws.merge_range(r, 12, r, 13, f'=IF(COUNTIFS(tblDeliv[Team],{T},tblDeliv[Priority],"Must",tblDeliv[RAG],"Red")>0,"Red",'
                                     f'IF(K{e}+L{e}>0,"Amber","Green"))', B.F(bold=True, align="center", border=1, border_color=WHITE))
        ws.set_row(r, 20)
    ws.conditional_format(11, 4, 16, 7, {"type": "3_color_scale", "min_type": "num", "min_value": 0, "mid_type": "num",
                                         "mid_value": 0.5, "max_type": "num", "max_value": 1,
                                         "min_color": "#F4B6AE", "mid_color": "#FBE3A6", "max_color": "#A8DCBC"})
    ws.conditional_format(11, 8, 16, 8, {"type": "cell", "criteria": ">", "value": 0, "format": B.F(bg_color=RED_BG, font_color=RED, bold=True)})
    ws.conditional_format(11, 11, 16, 11, {"type": "cell", "criteria": ">", "value": 0, "format": B.F(bg_color=RED_BG, font_color=RED, bold=True)})
    cf_text(ws, 11, 12, 16, 12, {"Green": (GREEN, WHITE), "Amber": (AMBER, WHITE), "Red": (RED, WHITE)})
    # readiness meeting panel
    ws.merge_range(10, 15, 10, 18, "READINESS MEETING", hdr)
    lab = B.F(bg_color=LIGHT, border=1, border_color=WHITE, font_size=9, indent=1)
    val = B.F(bold=True, align="center", border=1, border_color=WHITE, bg_color=LIGHT)
    panel = [("Pre-meeting checklist", '=COUNTIF(tblPre[Done],"Yes")&" / "&COUNTA(tblPre[Item])'),
             ("Run sheet covered", '=COUNTIF(tblRun[Covered],"Yes")&" / "&COUNTA(tblRun[Topic])'),
             ("Post-meeting checklist", '=COUNTIF(tblPost[Done],"Yes")&" / "&COUNTA(tblPost[Item])'),
             ("Open readiness actions", "='Readiness Meeting'!I10"),
             ("Next checkpoint (T-3)", '=TEXT(WorkshopDate-3,"ddd dd mmm")'),
             ("Dry run (T-2)", '=TEXT(WorkshopDate-2,"ddd dd mmm")')]
    for k, (a, fx) in enumerate(panel):
        ws.merge_range(11 + k, 15, 11 + k, 16, a, lab)
        ws.merge_range(11 + k, 17, 11 + k, 18, fx, val)
    section(ws, 18, "READINESS BY TEAM")
    c1 = B.wb.add_chart({"type": "bar"})
    c1.add_series({"name": "Avg progress", "categories": ref(name, 11, 1, 16, 1), "values": ref(name, 11, 4, 16, 4),
                   "fill": {"color": TEAL}, "gap": 60, "data_labels": {"value": True, "num_format": "0%", "font": {"name": FONT, "size": 9}}})
    c1.add_series({"name": "Reviewed", "categories": ref(name, 11, 1, 16, 1), "values": ref(name, 11, 6, 16, 6),
                   "fill": {"color": NAVY}, "data_labels": {"value": True, "num_format": "0%", "font": {"name": FONT, "size": 9}}})
    c1.set_x_axis({"min": 0, "max": 1, "num_format": "0%", "num_font": {"name": FONT, "size": 9},
                   "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}}})
    c1.set_y_axis({"reverse": True, "num_font": {"name": FONT, "size": 9}})
    chart_style(c1, "Average progress and review coverage")
    c1.set_size({"width": 610, "height": 300})
    ws.insert_chart(19, 1, c1, {"x_offset": 4, "y_offset": 6})
    c2 = B.wb.add_chart({"type": "column", "subtype": "stacked"})
    for j, (rag, col) in enumerate([("Green", GREEN), ("Amber", AMBER), ("Red", RED)]):
        c2.add_series({"name": rag, "categories": ref(name, 11, 1, 16, 1), "values": ref(name, 11, 9 + j, 16, 9 + j),
                       "fill": {"color": col}, "gap": 60, "data_labels": {"value": True, "num_format": "0;-0;;@", "font": {"name": FONT, "size": 8, "color": WHITE}}})
    c2.set_x_axis({"num_font": {"name": FONT, "size": 9}})
    c2.set_y_axis({"num_font": {"name": FONT, "size": 9}, "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}}})
    chart_style(c2, "Deliverable RAG mix by team")
    c2.set_size({"width": 610, "height": 300})
    ws.insert_chart(19, 10, c2, {"x_offset": 4, "y_offset": 6})
    # dependencies mirror
    section(ws, 36, "CROSS-TEAM DEPENDENCIES")
    spans = [("#", 1, 1), ("Giver", 2, 3), ("Receiver", 4, 5), ("What", 6, 12), ("Due", 13, 14), ("Status", 15, 16), ("RAG", 17, 18)]
    for h, a, b in spans:
        (ws.merge_range(37, a, 37, b, h, hdr) if a != b else ws.write(37, a, h, hdr))
    row_f = B.F(border=1, border_color=WHITE, bg_color=LIGHT, font_size=9)
    for k in range(1, 9):
        r = 37 + k
        vals = [("#", f'=IFERROR(INDEX(tblDeps[No],{k})&"","")'), ("Giver", f'=IFERROR(INDEX(tblDeps[Giver],{k})&"","")'),
                ("Receiver", f'=IFERROR(INDEX(tblDeps[Receiver],{k})&"","")'), ("What", f'=IFERROR(INDEX(tblDeps[What],{k})&"","")'),
                ("Due", f'=IFERROR(IF(INDEX(tblDeps[Due],{k})="","",INDEX(tblDeps[Due],{k})),"")'),
                ("Status", f'=IFERROR(INDEX(tblDeps[Status],{k})&"","")'), ("RAG", f'=IFERROR(INDEX(tblDeps[RAG],{k})&"","")')]
        for (h, a, b), (_, fx) in zip(spans, vals):
            fmt = B.F(border=1, border_color=WHITE, bg_color=LIGHT, font_size=9, num_format="dd-mmm-yy", align="center") if h == "Due" else row_f
            (ws.merge_range(r, a, r, b, fx, fmt) if a != b else ws.write_formula(r, a, fx, fmt))
    cf_text(ws, 38, 17, 45, 17, {"Green": (GREEN, WHITE), "Amber": (AMBER, WHITE), "Red": (RED, WHITE)})
    # sessions mirror
    section(ws, 47, "WORKSHOP SESSIONS")
    spans = [("#", 1, 1), ("Session", 2, 7), ("Date", 8, 9), ("Start", 10, 10), ("Lead", 11, 13), ("Status", 14, 15),
             ("Outcomes", 16, 16), ("Questions", 17, 17), ("Decisions", 18, 18)]
    cols = ["No", "Session", "Date", "Start", "Lead", "Status", "Outcomes captured", "Open questions", "Decisions"]
    for h, a, b in spans:
        (ws.merge_range(48, a, 48, b, h, hdr) if a != b else ws.write(48, a, h, hdr))
    for k in range(1, 9):
        r = 48 + k
        for (h, a, b), col in zip(spans, cols):
            if h == "Date":
                fx = f'=IFERROR(IF(INDEX(tblSessions[Date],{k})="","",INDEX(tblSessions[Date],{k})),"")'
                fmt = B.F(border=1, border_color=WHITE, bg_color=LIGHT, font_size=9, num_format="ddd dd-mmm", align="center")
            else:
                fx = f'=IFERROR(INDEX(tblSessions[[{col}]],{k})&"","")'
                fmt = row_f
            (ws.merge_range(r, a, r, b, fx, fmt) if a != b else ws.write_formula(r, a, fx, fmt))
    cf_text(ws, 49, 14, 56, 14, {"Done": (GREEN, WHITE), "Confirmed": (TEAL, WHITE), "Planned": (SLATE, WHITE), "Deferred": (RED, WHITE)})

def build_estimation_dash(ws):
    name = "Estimation Dashboard"
    dash_setup(ws, "Estimation Dashboard", "Architecture alignment and estimation validation: is the vendor estimate defensible?")
    tiles = [
        ("VENDOR OUTPUTS RECEIVED", '=COUNTIFS(tblVendor[Status],"<>Not received",tblVendor[Output],"<>")',
         '="Accepted: "&COUNTIF(tblVendor[Status],"Accepted")&" of "&COUNTA(tblVendor[Output])', NAVY, "0"),
        ("STANDARD OR CONFIG FIT", "=IFERROR((SUM(tblFitGap[Standard])+SUM(tblFitGap[Configuration]))/SUM(tblFitGap[Total]),0)",
         '=SUM(tblFitGap[Total])&" requirements  |  unclassified "&SUM(tblFitGap[Unclassified])', GREEN, "0%"),
        ("CUSTOM / NOT SUPPORTED", "=SUM(tblFitGap[Customisation])+SUM(tblFitGap[Not supported])",
         '="Extensions: "&SUM(tblFitGap[Extension])&"  |  workarounds "&SUM(tblFitGap[Workaround])', RED, "0"),
        ("COST EVIDENCE CONFIRMED", '=COUNTIF(tblCost[Expected confidence],"Confirmed")',
         '="Provisional "&COUNTIF(tblCost[Expected confidence],"Provisional")&"  |  unestimated "&COUNTIF(tblCost[Expected confidence],"Unestimated")', TEAL, "0"),
        ("RED FLAGS PRESENT", '=COUNTIF(tblRedFlags[Present],"Yes")',
         '="Assessed: "&COUNTA(tblRedFlags[Present])&" of "&COUNTA(tblRedFlags[Red flag])', RED, "0"),
        ("RESPONSIBILITIES AGREED", '=IFERROR(COUNTIF(tblResp[Check],"Agreed")/COUNTA(tblResp[Activity]),0)',
         '="Unowned: "&COUNTIF(tblResp[Check],"Unowned")&"  |  to confirm "&COUNTIF(tblResp[Check],"To confirm")', AMBER, "0%"),
    ]
    for k, (lab, v, s, col, fmt) in enumerate(tiles):
        cell = tile(ws, 4, 1 + 3 * k, 3, lab, v, s, col, fmt)
        if k in (2, 4):
            warn_if_positive(ws, cell)
    section(ws, 9, "GATE STATUS")
    for g, (c, lab) in enumerate([(1, "GATE 1  DISCOVERY COMPLETENESS"), (7, "GATE 2  ARCHITECTURE ALIGNMENT"),
                                  (13, "GATE 3  ESTIMATION VALIDATION")], 1):
        status_block(ws, 10, c, 6, lab, f"=Gate{g}Outcome", f'=Gate{g}Met&" of "&Gate{g}Must&" Must items met"')
    section(ws, 15, "FIT-GAP AND ESTIMATE CONFIDENCE")
    dc = DATA_COL
    ws.write_row(4, dc, ["Confidence", "Components"], B.F(bold=True, font_color=SLATE))
    for k, cf in enumerate(LISTS["lstConf"]):
        ws.write(5 + k, dc, cf)
        ws.write_formula(5 + k, dc + 1, f'=COUNTIF(tblCost[Expected confidence],"{cf}")')
    ws.write_row(10, dc, ["Vendor output status", "Count"], B.F(bold=True, font_color=SLATE))
    for k, st in enumerate(LISTS["lstVendorOut"]):
        ws.write(11 + k, dc, st)
        ws.write_formula(11 + k, dc + 1, f'=COUNTIF(tblVendor[Status],"{st}")')
    c1 = B.wb.add_chart({"type": "bar", "subtype": "stacked"})
    palette = [GREEN, "#7CC4A0", "#3C6E9F", AMBER, "#B08BC4", RED, SLATE]
    n = len(FIT_AREAS)
    for j, cls in enumerate(FITGAP):
        c1.add_series({"name": cls, "categories": ref("Fit-Gap", 4, 0, 3 + n, 0), "values": ref("Fit-Gap", 4, 1 + j, 3 + n, 1 + j),
                       "fill": {"color": palette[j]}, "gap": 50})
    c1.set_y_axis({"reverse": True, "num_font": {"name": FONT, "size": 9}})
    c1.set_x_axis({"num_font": {"name": FONT, "size": 9}, "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}}})
    chart_style(c1, "Requirements by fit-gap classification")
    c1.set_size({"width": 760, "height": 320})
    ws.insert_chart(16, 1, c1, {"x_offset": 4, "y_offset": 6})
    c2 = B.wb.add_chart({"type": "doughnut"})
    c2.add_series({"name": "Confidence", "categories": ref(name, 5, dc, 7, dc), "values": ref(name, 5, dc + 1, 7, dc + 1),
                   "points": [{"fill": {"color": GREEN}}, {"fill": {"color": AMBER}}, {"fill": {"color": RED}}],
                   "data_labels": {"value": True, "num_format": "0;-0;;@", "font": {"name": FONT, "size": 10, "bold": True, "color": WHITE}}})
    c2.set_hole_size(55)
    chart_style(c2, "Cost components by expected confidence")
    c2.set_size({"width": 460, "height": 320})
    ws.insert_chart(16, 12, c2, {"x_offset": 4, "y_offset": 6})
    section(ws, 34, "COST EVIDENCE AND VENDOR OUTPUTS")
    nc = len(COST)
    c3 = B.wb.add_chart({"type": "bar"})
    c3.add_series({"name": "Evidence progress", "categories": ref("Cost Traceability", 4, 1, 3 + nc, 1),
                   "values": ref("Cost Traceability", 4, 6, 3 + nc, 6), "fill": {"color": TEAL}, "gap": 50,
                   "data_labels": {"value": True, "num_format": "0%", "font": {"name": FONT, "size": 9}}})
    c3.set_x_axis({"min": 0, "max": 1, "num_format": "0%", "num_font": {"name": FONT, "size": 9},
                   "major_gridlines": {"visible": True, "line": {"color": "#E4E8EC"}}})
    c3.set_y_axis({"reverse": True, "num_font": {"name": FONT, "size": 9}})
    chart_style(c3, "Discovery evidence behind each cost component", legend=False)
    c3.set_size({"width": 610, "height": 330})
    ws.insert_chart(35, 1, c3, {"x_offset": 4, "y_offset": 6})
    hdr = B.F(bold=True, font_color=WHITE, bg_color=NAVY, align="center", valign="vcenter", text_wrap=True, font_size=9)
    row_f = B.F(border=1, border_color=WHITE, bg_color=LIGHT, font_size=9, valign="vcenter")
    spans = [("Vendor output", 10, 14, "Output"), ("Status", 15, 16, "Status"), ("Traceable", 17, 17, "Traceable to IDs"),
             ("Confidence", 18, 18, "Confidence levels applied")]
    for h, a, b, _ in spans:
        (ws.merge_range(36, a, 36, b, h, hdr) if a != b else ws.write(36, a, h, hdr))
    for k in range(1, 9):
        r = 36 + k
        ws.set_row(r, 26)
        for h, a, b, col in spans:
            fx = f'=IFERROR(INDEX(tblVendor[[{col}]],{k})&"","")'
            (ws.merge_range(r, a, r, b, fx, row_f) if a != b else ws.write_formula(r, a, fx, row_f))
    cf_text(ws, 37, 15, 44, 15, {"Accepted": (GREEN, WHITE), "Received": (TEAL, WHITE), "Under review": (AMBER, WHITE),
                                 "Rework required": (RED, WHITE), "Not received": (SLATE, WHITE)})
    cf_text(ws, 37, 17, 44, 18, {"Yes": (GREEN_BG, GREEN), "No": (RED_BG, RED)})


# ================================================================= main
def main():
    global B
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    B = Book(OUT)
    ws = {}
    for name in ["Home"] + [s[0] for s in SHEETS]:
        ws[name] = B.wb.add_worksheet(name)
    ws["Home"].set_tab_color(NAVY)
    for name, colour, _ in SHEETS:
        ws[name].set_tab_color(colour)
    build_settings(ws["Settings"])
    build_home(ws["Home"])
    build_deliverables(ws["Deliverables"])
    build_diagrams(ws["Diagrams"])
    build_plan(ws["Phase Plan"])
    build_readiness(ws["Readiness Meeting"])
    build_sessions(ws["Workshop Sessions"])
    build_gates(ws["Gates"])
    build_vendor_outputs(ws["Vendor Outputs"])
    build_cost(ws["Cost Traceability"])
    build_fitgap(ws["Fit-Gap"])
    build_resp(ws["Responsibility"])
    build_raid(ws["RAID"])
    build_deps(ws["Dependencies"])
    build_actions(ws["Actions"])
    build_decisions(ws["Decisions"])
    build_exec(ws["Executive Dashboard"])
    build_readiness_dash(ws["Readiness Dashboard"])
    build_estimation_dash(ws["Estimation Dashboard"])
    for name in ("Executive Dashboard", "Readiness Dashboard", "Estimation Dashboard"):
        ws[name].set_landscape()
        ws[name].fit_to_pages(1, 0)
        ws[name].print_area(0, 0, 60, 19)
    ws["Home"].activate()
    B.wb.close()
    print("Saved", os.path.normpath(OUT), "sheets:", len(ws))


if __name__ == "__main__":
    main()
