# 14: Client SA Review Gates Checklist

| Field | Value |
|---|---|
| Owner | Client Solution Architect |
| Audience | **Internal (client only).** Do not issue to the vendor |
| Status | Draft v0.1 |

## 1. Purpose

The Client SA controls both the quality of the proposed SaaS solution and the credibility of the vendor estimate through three gates:

**Gate 1: Discovery completeness → Gate 2: Architecture alignment → Gate 3: Estimation validation**

A gate passes when every *Must* item is met or has an approved exception.

## 2. Gate 1: Discovery completeness (before issuing to the vendor)

| # | Check | Must / Should | Status | Evidence |
|---|---|---|---|---|
| 1.1 | Diagrams 01-08 complete, with actual system names and IDs | Must | | |
| 1.2 | Diagrams 09-10 complete | Should | | |
| 1.3 | Every diagram element is in the Element Register (13) | Must | | |
| 1.4 | Every current-state interface has an INT-ID and a Technical BA catalogue entry | Must | | |
| 1.5 | Migration inventory (volumes, entities) available from the Technical BA | Must | | |
| 1.6 | EA standards (02) confirmed with Enterprise Architecture | Must | | |
| 1.7 | Security requirements (04) reviewed by Security Architecture. Data classification confirmed | Must | | |
| 1.8 | NFR values (07) agreed with business, security and operations | Must | | |
| 1.9 | Network requirements (05) reviewed by the network team | Must | | |
| 1.10 | Shared responsibility (08) reviewed by service management | Must | | |
| 1.11 | Risks, assumptions and constraints (09) logged and reflected in the project RAID | Must | | |
| 1.12 | Decommissioning principles (10) reviewed with records management | Must | | |
| 1.13 | Due-diligence questionnaire (11) includes the regulatory supplement where applicable | Must | | |
| 1.14 | BA Product Fit-Gap Matrix, test strategy and project constraints are available in the consolidated pack | Must | | |
| 1.15 | All *(example)* values replaced or explicitly marked as "to be confirmed" | Must | | |

## 3. Gate 2: Architecture alignment (vendor solution architecture review)

| # | Check | Must / Should | Status | Evidence |
|---|---|---|---|---|
| 2.1 | Vendor has validated or corrected every client diagram. Differences are explained | Must | | |
| 2.2 | Target integration architecture follows EAS-P03 / EAS-I05 (no point-to-point, no DB access) | Must | | |
| 2.3 | Every INT-ID has an agreed pattern, authentication and error-handling approach | Must | | |
| 2.4 | API limits (SAR-031) are sufficient for integration and migration volumes | Must | | |
| 2.5 | Customisations are minimised, justified and approved by the design authority | Must | | |
| 2.6 | Identity design meets SEC-001 to SEC-006 (SSO, MFA, provisioning, no local accounts) | Must | | |
| 2.7 | Data residency (SAR-003, DDQ-030/031) confirmed in writing, including sub-processors | Must | | |
| 2.8 | NFRs are met by the proposed subscription tier, or the gaps are accepted | Must | | |
| 2.9 | Environment strategy maps to the client integration environments (ENV-IDs) | Must | | |
| 2.10 | Shared responsibility matrix agreed, with no unowned activities | Must | | |
| 2.11 | Exit / data portability approach is acceptable | Must | | |
| 2.12 | Security assurance evidence received. C&A path agreed | Must | | |
| 2.13 | Architecture decisions recorded (ADR log in 09) | Should | | |

## 4. Gate 3: Estimation validation

| # | Check | Must / Should | Status | Evidence |
|---|---|---|---|---|
| 3.1 | All eight mandatory outputs (12) received | Must | | |
| 3.2 | Every requirement has a fit-gap classification. Non-standard items are costed | Must | | |
| 3.3 | Every INT-ID and migration object has its own estimate line | Must | | |
| 3.4 | Every WBS line traces to requirement / element / NFR IDs | Must | | |
| 3.5 | Confidence levels are applied. The Unestimated items have a plan and a cost range | Must | | |
| 3.6 | Assumptions are consistent with the client assumptions (09), and conflicts are resolved | Must | | |
| 3.7 | Subscription costs reflect volumes (07 section 2), environments and consumption drivers | Must | | |
| 3.8 | Recurring run costs and 5-year TCO included | Must | | |
| 3.9 | Exclusions reviewed. Client-side costs (integration, identity, network, decommissioning) estimated separately | Must | | |
| 3.10 | Effort benchmarked against comparable implementations or vendor references | Should | | |
| 3.11 | Migration cycles and cutover rehearsals included (DEC-011) | Must | | |
| 3.12 | Risk contingency aligned with the risk register | Should | | |

## 5. Red flags to escalate

- A single fixed price with no breakdown or confidence levels.
- Integration or migration estimated as one lump sum.
- "Standard" claimed for requirements the BA team flagged as complex, without a demonstration.
- Data residency or exit terms that are vague or deferred to the contract.
- API limits that are undisclosed or "to be confirmed".
- Heavy reliance on customisation, or roadmap features with no committed dates.

## 6. Gate sign-off

| Gate | Date | Outcome (Pass / Conditional / Fail) | Conditions | Signed off by |
|---|---|---|---|---|
| 1 Discovery completeness | | | | |
| 2 Architecture alignment | | | | |
| 3 Estimation validation | | | | |
