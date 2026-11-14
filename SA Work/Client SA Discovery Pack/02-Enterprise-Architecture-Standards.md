# 02: Enterprise Architecture Standards

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with Enterprise Architecture) |
| Audience | SaaS vendor |
| Status | Draft v0.1 |

## 1. Purpose

This document sets out the client's approved platforms, technologies, patterns and architecture principles that the SaaS solution and its implementation must align with. Any deviation must be raised as an architecture exception (section 6) and logged in [09](09-Architecture-Risks-and-Constraints.md).

## 2. Architecture principles

| ID | Principle | Rationale | Implication for the vendor |
|---|---|---|---|
| EAS-P01 | **Adopt before adapt.** Use standard SaaS functionality and configuration before extension or customisation | Lowers cost and upgrade risk | Every requirement is classified in the Product Fit-Gap Matrix. Customisation needs client design-authority approval |
| EAS-P02 | **Upgrade-safe extensions only.** | Keeps the vendor release cadence | Only supported extension frameworks and low-code. No product source changes |
| EAS-P03 | **Integrate through the enterprise integration layer.** | Gives one point of control, security and monitoring | No point-to-point integrations from SaaS to back-end systems |
| EAS-P04 | **API-first, event-enabled.** | Gives loose coupling | Prefer REST APIs and events. Use files only where no API is available |
| EAS-P05 | **The client owns its data.** | Supports sovereignty, portability and exit | Full data export in open formats at any time and on exit |
| EAS-P06 | **One enterprise identity.** | Gives security and lifecycle control | All human access through the enterprise IdP (SSO + MFA). No local accounts except break-glass |
| EAS-P07 | **Secure by design.** | Manages risk | Security controls per [04](04-Security-Architecture-Requirements.md), with evidence provided |
| EAS-P08 | **Observable by default.** | Supports operations | Logs, metrics and health status are exposed to client monitoring |
| EAS-P09 | **Reuse enterprise capabilities.** | Avoids duplication | Use client document, reporting and notification platforms where mandated (section 3) |

## 3. Approved enterprise platforms *(example; replace with the actual standards)*

| ID | Capability | Approved standard | Mandatory for this solution? | Notes |
|---|---|---|---|---|
| EAS-001 | Identity provider | Microsoft Entra ID (SYS-004) | Yes | SAML 2.0 or OIDC. SCIM provisioning preferred |
| EAS-002 | API management | Enterprise API Gateway | Yes | All inbound and outbound APIs published and secured here |
| EAS-003 | Integration / iPaaS | Enterprise Integration Platform | Yes | Orchestration, transformation, retry, error handling |
| EAS-004 | Messaging / events | Enterprise Message Broker | Yes, for async | Webhooks/events are consumed through the broker |
| EAS-005 | File transfer | Managed Secure File Transfer (SFTP) | Where files are needed | PGP encryption for sensitive files |
| EAS-006 | Enterprise reporting / analytics | Enterprise Data Platform | Yes | SaaS provides a data feed. Operational reports may stay in SaaS |
| EAS-007 | Security monitoring | Enterprise SIEM | Yes | SaaS audit and security logs are forwarded |
| EAS-008 | Service management | Enterprise ITSM tool | Yes | Incident, problem and change are integrated with vendor support |
| EAS-009 | Document / records management | Enterprise records platform | To be confirmed | Retention-governed records may need to be filed here |
| EAS-010 | Email / notifications | Enterprise mail relay | Should | Sending domain authenticated (SPF/DKIM/DMARC) |

## 4. Approved integration patterns

| ID | Pattern | Use when | Standard |
|---|---|---|---|
| EAS-I01 | Synchronous request/response API | Real-time lookup or transaction | REST/JSON, OAuth 2.0 client credentials, TLS 1.2+ |
| EAS-I02 | Event / webhook | State change notification | Signed webhook to the broker, at-least-once delivery, idempotent consumers |
| EAS-I03 | Scheduled batch / file | Bulk or legacy-system exchange | SFTP, agreed schema, control totals, PGP where sensitive |
| EAS-I04 | Bulk data extract | Analytics / reporting feed | Incremental extract (CDC or delta API) to the data platform |
| EAS-I05 | Prohibited | Direct database access, shared credentials, point-to-point bypassing EAS-002/003 | Not permitted |

## 5. Technology and data standards

| ID | Area | Standard |
|---|---|---|
| EAS-T01 | Data formats | JSON (APIs), CSV/XML with published schema (files), ISO 8601 date-times in UTC |
| EAS-T02 | Character encoding | UTF-8 |
| EAS-T03 | API specification | OpenAPI 3.x supplied for every API the solution exposes or consumes |
| EAS-T04 | Versioning | Semantic API versioning, with at least 12 months' deprecation notice *(example)* |
| EAS-T05 | Reference data | Client master data (e.g. customer, cost centre) is mastered in the source system, not in SaaS |
| EAS-T06 | Browser support | Current versions of Edge and Chrome *(example)* |
| EAS-T07 | Accessibility | WCAG 2.1 AA conformance (or the applicable government standard) |
| EAS-T08 | Language / locale | en-NZ, NZD currency, NZ date format *(example)* |

## 6. Architecture exceptions

Deviations from these standards need a documented exception approved by the client design authority.

| Exception ID | Standard | Proposed deviation | Justification | Risk / mitigation | Decision | Date |
|---|---|---|---|---|---|---|
| EXC-001 | *(example)* EAS-I05 | Nightly direct DB extract during the migration period only | No bulk API for historical data | Time-boxed, read-only, removed at cutover | Pending | |

## 7. Vendor response required

For each EAS item, state compliance (C / CC / PC / NC / R). Explain every PC or NC and propose an alternative.
