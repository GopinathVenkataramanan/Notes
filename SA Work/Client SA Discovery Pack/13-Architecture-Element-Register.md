# 13: Architecture Element Register

| Field | Value |
|---|---|
| Owner | Client Solution Architect (maintained with the Technical BA) |
| Audience | SaaS vendor, all discovery teams |
| Status | Draft v0.1 |

## 1. Purpose

This is the single source of element IDs used across the diagrams, the Technical BA catalogues and the vendor estimation workbook. It gives end-to-end traceability from architecture to vendor cost.

**Rules**
- An ID is never reused or renumbered. Retired elements keep their ID with status *Retired*.
- Every box on a diagram has an ID in this register. Every integration line has an INT-ID.
- The detailed interface specifications and the data mapping are held by the Technical BA and keyed by these IDs.

## 2. Systems (SYS) *(example; these match the Visio diagrams)*

| ID | Name | Type | Current / Target | Disposition | Business owner | Technical owner | Diagrams |
|---|---|---|---|---|---|---|---|
| SYS-001 | Legacy Claims Application | On-prem application | Current | Replace, then retire | Claims Operations | Application Services | 01, 02, 10 |
| SYS-002 | CRM | Enterprise application | Both | Retain, re-integrate | Customer Services | CRM team | 01, 03, 04 |
| SYS-003 | Finance / ERP | Enterprise application | Both | Retain, re-integrate | Finance | ERP team | 01, 03, 04 |
| SYS-004 | Identity Provider (Microsoft Entra ID) | Enterprise platform | Both | Retain, federate | CISO | Identity team | 01, 03, 06 |
| SYS-005 | Payment Gateway | External service | Both | Retain, re-integrate *(confirm)* | Finance | Third party | 01 |
| SYS-006 | Reporting Platform / Enterprise Reporting | Enterprise platform | Both | Retain, new data feed | Business Intelligence | Data team | 01, 03 |
| SYS-007 | Enterprise API Gateway | Enterprise platform | Target | Reuse | n/a | Integration team | 03, 04 |
| SYS-008 | Integration Platform / iPaaS | Enterprise platform | Target | Reuse | n/a | Integration team | 03, 04 |
| SYS-009 | Message Broker | Enterprise platform | Target | Reuse | n/a | Integration team | 04 |
| SYS-010 | Claims SaaS | Vendor SaaS | Target | New | Claims Operations | Vendor / Application Services | 03, 04, 05, 07 |
| SYS-011 | Secure File Transfer | Enterprise platform | Target | Reuse | n/a | Integration team | 04 |
| SYS-012 | Document Services | Enterprise platform | Target | Integrate *(confirm)* | Records | Records team | 04 |
| SYS-013 | Enterprise Data Platform | Enterprise platform | Target | Integrate | Business Intelligence | Data team | 04 |
| SYS-014 | External Government Services | External | Target | Integrate *(confirm)* | n/a | Third party | 04 |

## 3. Data stores (DATA)

| ID | Name | Owner system | Technology *(example)* | Volume *(example)* | Migration disposition |
|---|---|---|---|---|---|
| DATA-001 | Claims Database | SYS-001 | SQL Server | 400 GB, 1.2 M claims | Migrate active and recent. Archive the remainder |
| DATA-002 | Document Repository | SYS-001 | File share / ECM | 8 TB | Migrate linked documents. Archive the remainder |
| DATA-003 | Historical Records | SYS-001 | SQL Server / files | 150 GB | Archive (read-only) |
| DATA-010 | SaaS Data Store | SYS-010 | Vendor-managed | n/a | Target |
| DATA-011 | Historical Archive | SYS-010 or enterprise | To be decided (DEC-020) | n/a | Target |

## 4. Interfaces (INT) *(example; detailed specs in the Technical BA integration catalogue)*

| ID | Source | Target | Purpose | Pattern | Direction | Frequency | Current / Target | Diagram |
|---|---|---|---|---|---|---|---|---|
| INT-001 | SYS-001 | SYS-002 | Customer lookup / update | Sync API via ESB | Bi | Real-time | Current | 01 |
| INT-002 | SYS-001 | SYS-003 | Claim payments and GL postings | Batch file | Out | Daily | Current | 01 |
| INT-003 | SYS-001 | SYS-004 | User authentication | LDAP / Kerberos | In | Real-time | Current | 01 |
| INT-004 | SYS-001 | SYS-005 | Payment processing | API | Bi | Real-time | Current | 01 |
| INT-005 | SYS-001 | SYS-006 | Reporting extract | DB extract | Out | Nightly | Current | 01 |
| INT-101 | SYS-010 | SYS-004 | SSO (SAML/OIDC) and SCIM provisioning | Federation | Bi | Real-time | Target | 03, 06 |
| INT-102 | SYS-010 | SYS-002 | Customer lookup / update | REST via SYS-007/008 | Bi | Real-time | Target | 03, 04 |
| INT-103 | SYS-010 | SYS-003 | Claim payments and GL postings | Event via SYS-009 to SYS-008 | Out | Near real-time | Target | 03, 04 |
| INT-104 | SYS-010 | SYS-013 | Analytics data feed | Bulk / delta extract | Out | Daily | Target | 03, 04 |
| INT-105 | SYS-010 | SYS-012 | Records filing | REST via SYS-008 | Out | Event-driven | Target | 04 |
| INT-106 | SYS-010 | SYS-014 | Government service verification | REST via SYS-007 | Bi | Real-time | Target | 04 |
| INT-107 | SYS-010 | SYS-011 | Bulk file exchange | SFTP | Bi | Scheduled | Target | 04 |
| INT-901 | DATA-001/002/003 | SYS-010 | Data migration load | Bulk import / API | In | Migration cycles | Transition | 05 |

## 5. Environments (ENV) *(example; see diagram 07)*

| ID | SaaS environment | Client integration environment | Purpose | Data |
|---|---|---|---|---|
| ENV-001 | Development / Configuration | DEV Integration | Build and configuration | Synthetic |
| ENV-002 | SIT | SIT Integration | System integration test | Masked |
| ENV-003 | UAT | UAT Integration | User acceptance, migration rehearsal | Masked / production-like |
| ENV-004 | Production | PROD Integration | Live service | Production |

## 6. Change log

| Date | Change | By |
|---|---|---|
| | Initial register created from the discovery diagrams | Client SA |
