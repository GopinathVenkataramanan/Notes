# 06: SaaS Operational Requirements

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with Service Management / Operations) |
| Audience | SaaS vendor |
| Status | Draft v0.1 |
| Related | [07 NFR Catalogue](07-NFR-Catalogue.md), [08 Shared Responsibility](08-Shared-Responsibility-Matrix.md) |

## 1. Purpose

This document defines how the SaaS service will be supported, monitored and operated after go-live, and how vendor operations integrate with client service management.

## 2. Service ownership *(example)*

| Role | Client | Vendor |
|---|---|---|
| Business service owner | Claims Operations Manager | n/a |
| Technical service owner | Application Services Manager | Customer Success / Service Delivery Manager |
| Platform operations | n/a | Vendor SRE / Operations |
| Integration operations | Integration Platform team | Supports API/webhook issues |
| Security operations | Security Operations Centre | Vendor security team |
| Release coordination | Change Manager | Vendor release management |

## 3. Requirements

Response codes: `C`, `CC`, `PC`, `NC`, `R`.

### 3.1 Support and incident management

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| OPS-001 | Support hours cover NZ business hours as a minimum. 24x7 for Priority 1 *(example)* | Must | | |
| OPS-002 | Incident priority definitions and response/resolution targets (see the table in 3.2) | Must | | |
| OPS-003 | Support is raised via portal, email and phone. Ticket integration with the client ITSM tool (EAS-008) | Should | | |
| OPS-004 | Named service delivery manager and monthly service review | Must | | |
| OPS-005 | Problem management with root-cause analysis for P1/P2 incidents within 5 business days *(example)* | Must | | |
| OPS-006 | Escalation path to vendor management, documented with contacts | Must | | |

### 3.2 Incident priority targets *(example; agree in the SLA)*

| Priority | Definition | Response | Restore / workaround | Updates |
|---|---|---|---|---|
| P1 Critical | Service unavailable or a major security incident | 15 min | 4 h | Hourly |
| P2 High | Major function degraded, no workaround | 1 h | 8 h | Every 4 h |
| P3 Medium | Function impaired, workaround exists | 4 h | 5 business days | Daily |
| P4 Low | Minor issue / request | 1 business day | Next release / agreed | Weekly |

### 3.3 Monitoring and observability

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| OPS-010 | Public or tenant-specific service status page with subscription alerts | Must | | |
| OPS-011 | Health, availability and performance metrics are available to the client (API or dashboard) | Must | | |
| OPS-012 | Integration monitoring: failed API calls, webhook delivery failures, queue backlogs are visible and alertable | Must | | |
| OPS-013 | Logs (application, audit, integration) are exportable to client tooling (SIEM / log analytics) | Must | | |
| OPS-014 | Monthly service report: availability against SLA, incidents, capacity, upcoming changes | Must | | |

### 3.4 Change and release

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| OPS-020 | Release notes issued at least 4 weeks *(example)* before production release | Must | | |
| OPS-021 | Planned maintenance notified at least 5 business days *(example)* in advance, outside business hours | Must | | |
| OPS-022 | Emergency changes are notified as soon as practicable, with post-change reporting | Must | | |
| OPS-023 | Client configuration changes follow client change management, with an audit trail in SaaS | Must | | |

### 3.5 Capacity, licensing and administration

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| OPS-030 | License and consumption usage reporting (users, transactions, storage, API calls) | Must | | |
| OPS-031 | Alerts before consumption thresholds that would incur additional charges | Should | | |
| OPS-032 | Admin documentation and training for client business and technical administrators | Must | | |

### 3.6 Continuity

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| OPS-040 | Vendor BCP/DR plan is tested at least annually, with results shared | Must | | |
| OPS-041 | Client participation in DR tests, or evidence of the tenant-level restore test | Should | | |
| OPS-042 | Vendor financial viability and escrow / continuity arrangements described | Should | | |

## 4. Hypercare *(example)*

- Hypercare period of 6 weeks after go-live, with daily vendor stand-ups and elevated priority on defects.
- Exit criteria: no open P1/P2 incidents, stable integration error rates, and handover to BAU support signed off.

## 5. Vendor response required

Complete the response columns. Attach the support model, SLA schedule, sample monthly service report and status page URL.
