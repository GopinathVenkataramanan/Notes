# 12: Vendor Estimation Pack Requirements

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with the Project / Commercial lead) |
| Audience | SaaS vendor |
| Status | Draft v0.1 |

## 1. Purpose

This document defines what the vendor must submit after discovery so that the estimate can be validated, compared and traced back to discovery evidence.

## 2. Cost model the estimate must cover

| Cost area | Drivers |
|---|---|
| SaaS subscription and licensing | Users, modules, environments, consumption |
| Product configuration and extensions | Fit-gap, workflows, rules, forms, reports |
| Integration implementation | APIs, middleware, events, external systems (per INT-ID) |
| Data migration | Legacy data, cleansing, mapping, history (per migration object) |
| Security and compliance | IAM, privacy, residency, accreditation, audit |
| Testing and quality | SIT, UAT support, regression, performance, security |
| Deployment and transition | Cutover, training, legacy decommissioning support |
| Project and change management | Governance, resources, change and adoption |

## 3. Mandatory outputs

| # | Output | Minimum content |
|---|---|---|
| 1 | **SaaS Product Fit-Gap Assessment** | Every requirement classified (section 4), with effort for each non-standard item |
| 2 | **Solution Architecture** | Target SaaS architecture, integration architecture, security architecture, operational model. Validates or corrects diagrams 01-10 |
| 3 | **Implementation Scope and WBS** | Every implementation activity broken down into work packages, with a WBS ID |
| 4 | **Integration and Data Migration Estimate** | Complexity and effort per interface (INT-ID) and per migration object (DATA-ID / entity) |
| 5 | **Resource and Effort Estimate** | Person-days by role, activity and phase. Rate card |
| 6 | **Implementation Roadmap** | Phases, milestones, dependencies, critical path, duration |
| 7 | **Commercial Cost Breakdown** | Subscription (by year), implementation, optional costs, third-party costs, recurring operational costs. 5-year TCO *(example)* |
| 8 | **Assumptions, Risks and Exclusions** | Estimation confidence, unresolved dependencies, potential additional costs, responses to [09](09-Architecture-Risks-and-Constraints.md) |

## 4. Fit-gap classification (mandatory for every requirement)

| Classification | Meaning | Cost implication |
|---|---|---|
| Standard | Available out of the box | Usually configuration only |
| Configuration | Achieved through SaaS configuration | Configuration effort |
| Extension | Requires a supported extension or low-code development | Additional development |
| Customisation | Requires bespoke development or product modification | Higher cost and upgrade risk |
| Workaround | Business process changes to fit the product | Business change effort |
| Not supported | The product cannot meet the requirement | Scope gap or alternative solution |

## 5. Estimate confidence levels

Do **not** submit a single fixed price. Tag every line item with one of these:

| Level | Meaning |
|---|---|
| **Confirmed** | Supported by detailed discovery evidence |
| **Provisional** | Based on reasonable, stated assumptions |
| **Unestimated** | Needs further investigation or a proof of concept. State the investigation needed |

This protects both parties from a low initial estimate followed by substantial change requests.

## 6. Traceability requirements

- Every WBS item references the requirement IDs, element IDs (SYS/INT/DATA/ENV) or NFR IDs it delivers.
- Every integration estimate line maps to exactly one INT-ID in [13](13-Architecture-Element-Register.md).
- Every migration estimate line maps to a DATA-ID and an entity in the Technical BA data migration inventory.
- Every assumption is listed once and referenced by ID wherever it affects cost.

## 7. Estimation workbook structure *(suggested)*

| Sheet | Columns |
|---|---|
| Summary | Cost area, Year 0 (implementation), Years 1-5 (run), confidence split |
| WBS | WBS ID, work package, phase, role, person-days, rate, cost, confidence, trace IDs, assumption IDs |
| Integrations | INT-ID, source, target, pattern, complexity (L/M/H), build days, test days, confidence |
| Migration | DATA-ID, entity, volume, transformation complexity, cycles, days, confidence |
| Subscription | Module, metric, quantity, unit price, annual cost, escalation |
| Assumptions | ID, assumption, impact, cost if wrong |

## 8. Submission

Submit all eight outputs, the completed response columns in documents 02-11, and the estimation workbook, by *(date)*.
