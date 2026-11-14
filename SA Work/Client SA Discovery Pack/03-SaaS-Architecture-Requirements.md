# 03: SaaS Architecture Requirements

| Field | Value |
|---|---|
| Owner | Client Solution Architect |
| Audience | SaaS vendor |
| Status | Draft v0.1 |
| Related | [02 Standards](02-Enterprise-Architecture-Standards.md), [07 NFR Catalogue](07-NFR-Catalogue.md), diagrams 03, 04 and 07 |

## 1. Purpose

These are the architectural expectations for the SaaS platform itself: tenancy, hosting, scalability, resilience, extensibility, integration capability, environments and data portability. Quantitative targets are in the [NFR Catalogue](07-NFR-Catalogue.md).

Response codes: `C` Complies as standard, `CC` Complies with configuration, `PC` Partial, `NC` No, `R` Roadmap (give the date).

## 2. Tenancy and hosting

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-001 | Describe the tenancy model (multi-tenant shared, multi-tenant logically isolated, single-tenant) and how client data is isolated | Must | | |
| SAR-002 | State the hosting provider(s), regions and data centre locations for primary, DR and backup | Must | | |
| SAR-003 | Client data (including backups, logs and support copies) is stored and processed only in approved locations *(example: New Zealand or Australia)* | Must | | |
| SAR-004 | List all sub-processors and their locations, and give notice before any change | Must | | |
| SAR-005 | Describe the platform architecture: application tiers, data stores and the shared versus dedicated components | Must | | |

## 3. Scalability and resilience

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-010 | The platform scales to the peak volumes in NFR-010 to NFR-013 without degradation | Must | | |
| SAR-011 | Describe horizontal/vertical scaling and the noisy-neighbour protections | Should | | |
| SAR-012 | No single point of failure in the production service. Describe the redundancy across availability zones | Must | | |
| SAR-013 | Describe DR topology, failover method (automatic/manual), and tested RTO/RPO (see NFR-030 to NFR-033) | Must | | |
| SAR-014 | Backups are encrypted, immutable or protected from deletion, and restore-tested at least annually *(example)* | Must | | |
| SAR-015 | The client can request point-in-time restore of its tenant data. State the granularity and the cost | Should | | |

## 4. Extensibility and configuration

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-020 | Describe the configuration capabilities (workflow, rules, forms, templates, roles) that business administrators can perform without code | Must | | |
| SAR-021 | Describe the supported extension model (low-code, scripting, SDK, serverless functions) and how upgrade safety is guaranteed | Must | | |
| SAR-022 | Configuration and extensions are retained and remain compatible across vendor releases. State the vendor's obligations when a release breaks them | Must | | |
| SAR-023 | Configuration can be exported, version-controlled and promoted between environments (not re-keyed manually) | Should | | |
| SAR-024 | Any customisation that is not upgrade-safe is identified explicitly in the fit-gap and costed separately | Must | | |

## 5. Integration capability

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-030 | Supply the full API catalogue (OpenAPI), covering all business objects needed by the INT-IDs in [13](13-Architecture-Element-Register.md) | Must | | |
| SAR-031 | State API limits: rate limits, throttling, payload size, concurrency and daily quotas, and the cost of increases | Must | | |
| SAR-032 | Outbound events/webhooks for key business state changes, with signing, retry and replay | Must | | |
| SAR-033 | Bulk import/export capability (API or file) for migration and reporting, with stated throughput | Must | | |
| SAR-034 | API authentication supports OAuth 2.0 client credentials, plus mutual TLS or certificate-bound tokens *(should)* | Must | | |
| SAR-035 | Incremental data extract (delta/CDC) for the enterprise data platform | Must | | |
| SAR-036 | Backwards-compatible API versioning with a published deprecation policy | Must | | |

## 6. Environments

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-040 | State the environments included in the subscription and the cost of additional ones. Minimum expected *(example)*: DEV/Config, SIT, UAT, PROD | Must | | |
| SAR-041 | Non-production environments are refreshed from production on request, with data masking for sensitive data | Must | | |
| SAR-042 | Non-production environments receive vendor releases ahead of production (preview window, state the duration) | Must | | |
| SAR-043 | Each environment can be integrated with the corresponding client integration environment (diagram 07) | Must | | |

## 7. Release management

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-050 | State the release frequency (major/minor/patch), the notice period and the release notes process | Must | | |
| SAR-051 | The client can defer non-security releases for a defined period. State the limit | Should | | |
| SAR-052 | Maintenance windows are agreed and fall outside the business hours in NFR-001 | Must | | |
| SAR-053 | Describe the feature-toggle approach for new functionality | Could | | |

## 8. Data ownership, portability and exit

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SAR-060 | The client retains ownership of all data, including metadata, attachments, audit logs and configuration | Must | | |
| SAR-061 | Full data export in documented open formats (e.g. CSV/JSON plus native attachment files) at any time, without professional-services cost | Must | | |
| SAR-062 | An exit plan covering assisted export, transition period, data deletion and a certificate of destruction | Must | | |
| SAR-063 | State the data retention after contract end and the deletion timescales | Must | | |

## 9. Vendor response required

Complete the response columns. Attach the platform architecture overview, API catalogue, environment strategy and release calendar.
