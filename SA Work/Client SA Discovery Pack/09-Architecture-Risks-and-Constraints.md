# 09: Architecture Risks, Assumptions, Constraints and Dependencies

| Field | Value |
|---|---|
| Owner | Client Solution Architect |
| Audience | SaaS vendor, project team (feeds the project RAID register) |
| Status | Draft v0.1 |

## 1. Purpose

This document records the architectural risks, assumptions, constraints and dependencies that can affect the solution design or the vendor estimate. The vendor must address each item in their proposal and identify any new ones.

Scoring: Likelihood (L) and Impact (I) on a 1-5 scale. Rating = L x I (High ≥ 15, Medium 8-14, Low ≤ 7).

## 2. Architecture risks *(examples)*

| ID | Risk | L | I | Rating | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| RSK-001 | SaaS API limits/throttling are insufficient for integration or migration volumes | 3 | 4 | 12 | Confirm limits (SAR-031). Load test early. Negotiate higher limits | Client SA / Vendor | Open |
| RSK-002 | Requirements met only through non-upgrade-safe customisation, raising lifecycle cost | 3 | 4 | 12 | Fit-gap classification. Design authority approval. Prefer process change | Client SA / BA | Open |
| RSK-003 | Legacy data quality problems extend migration cycles | 4 | 4 | 16 | Early data profiling. Cleansing workstream. Trial migrations | Data lead | Open |
| RSK-004 | Data residency cannot be met for all data (logs, support tooling, sub-processors) | 2 | 5 | 10 | Vendor declaration (DDQ-030). Contractual commitment | Security | Open |
| RSK-005 | Vendor releases cause regressions in configuration or integrations | 3 | 3 | 9 | Preview environments (SAR-042). Automated regression suite | Test lead | Open |
| RSK-006 | Historical documents (8 TB *(example)*) cannot be bulk-loaded within the cutover window | 3 | 4 | 12 | Phased migration. Archive strategy (DEC-020). Throughput test | Client SA | Open |
| RSK-007 | Security C&A is not completed before go-live | 3 | 5 | 15 | Start C&A in discovery. Early evidence from the vendor | Security | Open |
| RSK-008 | Vendor lock-in / exit difficulty | 2 | 4 | 8 | Exit plan (SAR-062). Open export formats | Client SA | Open |
| RSK-009 | Enterprise integration platform capacity or skills are insufficient for new interfaces | 3 | 3 | 9 | Capacity review. Integration team engagement | Integration lead | Open |

## 3. Assumptions *(examples; to be validated)*

| ID | Assumption | Impact if wrong | Validation by |
|---|---|---|---|
| ASM-001 | All workforce users are in Entra ID and licensed for conditional access | Additional identity work | Identity team |
| ASM-002 | The existing enterprise API gateway and integration platform are reused, so no new middleware is needed | New platform cost | Integration lead |
| ASM-003 | Only claims from the last 7 years are migrated. Older claims are archived read-only | Migration volume/cost | Business owner |
| ASM-004 | The vendor's standard SaaS tier meets NFR-002 and NFR-030/031 | Higher subscription tier | Vendor |
| ASM-005 | Customer/partner portal functionality is provided by the SaaS product | Separate portal build | Vendor / BA |

## 4. Constraints *(examples)*

| ID | Constraint | Source |
|---|---|---|
| CON-001 | Client data must remain in approved jurisdictions | Policy / contract |
| CON-002 | All integrations go through the enterprise API gateway and integration platform | EA standards (EAS-P03) |
| CON-003 | Workforce authentication only via the enterprise IdP with MFA | Security policy (SEC-001/002) |
| CON-004 | Legacy platform support ends *(date)*, so go-live must precede it | Vendor contract |
| CON-005 | No cutover during financial year-end or peak claims periods *(blackout dates)* | Business |
| CON-006 | Records must be retained according to the approved retention and disposal schedule | Public Records Act 2005 *(if applicable)* |

## 5. Dependencies

| ID | Dependency | Type | Needed by | Owner |
|---|---|---|---|---|
| DEP-001 | Integration platform environments (DEV/SIT/UAT/PROD) available | Internal | SIT start | Integration lead |
| DEP-002 | Entra ID enterprise application registration and group design | Internal | Build start | Identity team |
| DEP-003 | Changes to CRM (SYS-002) and Finance (SYS-003) interfaces | Internal / third party | SIT start | System owners |
| DEP-004 | Vendor provision of non-production environments | Vendor | Build start | Vendor |
| DEP-005 | Security C&A outcome | Internal | Go-live | Security |

## 6. Architecture decisions log

| ID | Decision | Options considered | Rationale | Date | Approved by |
|---|---|---|---|---|---|
| ADR-001 | *(example)* Use the enterprise iPaaS for all SaaS integrations | Point-to-point. Vendor-hosted connectors | EAS-P03, single monitoring point | | Design authority |

## 7. Vendor response required

Comment on each item, propose mitigations within the vendor's control, add any risks the vendor sees, and state the estimate contingency associated with each.
