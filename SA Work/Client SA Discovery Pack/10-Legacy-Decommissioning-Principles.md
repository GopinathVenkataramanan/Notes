# 10: Legacy Decommissioning Principles

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with the Project team and Records Management) |
| Audience | SaaS vendor, project team |
| Status | Draft v0.1 |
| Related | Diagram 10 Legacy Decommissioning and Transition, diagram 05 Data Migration |

## 1. Purpose

This document sets out the principles and requirements for transitioning from the legacy on-premises solution (SYS-001) to the SaaS solution (SYS-010) and retiring the legacy components.

## 2. Transition sequence (from diagram 10)

1. Legacy on-prem application (in service)
2. Historical data extraction
3. Data migration (trial loads, then dress rehearsal, then production load)
4. SaaS platform live
5. Validation and reconciliation
6. Business cutover
7. Legacy read-only / archive
8. Legacy decommissioning

Steps 1-4 run inside a **temporary coexistence (parallel run)** period.

## 3. Principles

| ID | Principle |
|---|---|
| DEC-P01 | **No data loss.** Every record in migration scope is reconciled (counts, control totals, sampled content) before cutover sign-off |
| DEC-P02 | **Minimise coexistence.** Keep the parallel run short. Avoid dual data entry. Where coexistence is unavoidable, define the system of record per entity |
| DEC-P03 | **Migrate what is needed, archive the rest.** Active and recent records go to SaaS. Older historical records go to a read-only archive, according to the retention schedule |
| DEC-P04 | **Retention obligations survive the system.** Records retention and disposal obligations apply to the legacy, archive and SaaS copies |
| DEC-P05 | **Reversible cutover.** A documented rollback plan with go/no-go criteria exists until the point of no return |
| DEC-P06 | **Clean shutdown.** Infrastructure, licences, interfaces, accounts, certificates, firewall rules and contracts are retired and evidenced |
| DEC-P07 | **Secure disposal.** Legacy storage and backups are sanitised according to the security standard (NZISM media sanitisation, where applicable) |

## 4. Requirements

| ID | Requirement | Owner | Priority |
|---|---|---|---|
| DEC-001 | Define the migration scope by entity and age (see ASM-003) and the archive scope | Business / Data lead | Must |
| DEC-002 | Define the system of record for every entity during coexistence | Client SA | Must |
| DEC-003 | Define the interface switch-over sequence (INT-IDs) from SYS-001 to SYS-010 | Client SA / Integration | Must |
| DEC-010 | Cutover window and blackout periods agreed *(example: 48-hour weekend window)* | Project | Must |
| DEC-011 | At least 2 full migration dress rehearsals before production cutover *(example)* | Vendor / Data lead | Must |
| DEC-012 | Go/no-go criteria and a rollback plan approved | Project / Client SA | Must |
| DEC-020 | Historical access approach decided: migrate to SaaS, SaaS archive tier, enterprise archive, or a read-only legacy instance | Client SA / Business | Must |
| DEC-021 | Legacy read-only period defined *(example: 6 months)*, with an access-control approach | Business | Must |
| DEC-022 | Archived data remains searchable and retrievable for audit, legal and OIA/privacy requests within agreed timescales | Records / Client SA | Must |
| DEC-030 | Decommissioning inventory: servers, databases, storage, backups, licences, interfaces, DNS, certificates, service accounts, firewall rules, monitoring, support contracts | Infrastructure | Must |
| DEC-031 | Disposal of legacy data according to the approved disposal authority, with evidence recorded | Records | Must |
| DEC-032 | Legacy vendor contract termination dates are aligned with the read-only period end | Commercial | Must |
| DEC-033 | Decommissioning sign-off by the business owner, security and records management | Project | Must |

## 5. Decommissioning inventory *(example; complete with the Technical BA application inventory)*

| Item | ID | Action | Target date | Evidence |
|---|---|---|---|---|
| Legacy Claims Application | SYS-001 | Read-only, then shut down | | |
| Claims Database | DATA-001 | Archive, then sanitise | | |
| Document Repository | DATA-002 | Migrate/archive, then sanitise | | |
| ESB flows for SYS-001 | INT-0xx | Remove after switch-over | | |
| VMs, OS and backup jobs | n/a | Decommission | | |
| Legacy licences and support | n/a | Terminate | | |

## 6. Vendor response required

Describe the vendor's migration and cutover approach, archive options and costs, the tooling, the number of migration cycles, and the vendor's responsibilities in coexistence and cutover.
