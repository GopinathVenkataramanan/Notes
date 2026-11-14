# 07: Non-Functional Requirements (NFR) Catalogue

| Field | Value |
|---|---|
| Owner | Client Solution Architect |
| Audience | SaaS vendor, client test team |
| Status | Draft v0.1 |
| Related | Diagram 08 NFR Architecture, [03](03-SaaS-Architecture-Requirements.md), [04](04-Security-Architecture-Requirements.md), [06](06-SaaS-Operational-Requirements.md) |

> **Important:** All values below are *examples only*, not recommended contractual targets. Agree the actual values with business, security and operations stakeholders before issuing.

## 1. Purpose

These are quantified quality attributes that the SaaS solution must meet. They feed the vendor's choice of subscription tier, the SLA schedule and the test team's performance and resilience testing.

Each NFR must be **measurable**, with a defined **measurement method** and **verification approach**.

## 2. Business context for sizing *(example; replace with BA business volumes)*

| Metric | Current | Year 3 | Year 5 |
|---|---|---|---|
| Named internal users | 350 | 400 | 450 |
| Peak concurrent internal users | 200 | 230 | 260 |
| External users (portal) | 20,000 | 30,000 | 40,000 |
| New claims per year | 60,000 | 70,000 | 80,000 |
| Peak claims per hour | 400 | 470 | 540 |
| Documents per year | 500,000 | 600,000 | 700,000 |
| Migrated claims (historical) | 1.2 million | n/a | n/a |
| Migrated documents | 8 TB | n/a | n/a |

## 3. NFR catalogue

| ID | Category | Requirement *(example values)* | Measurement / verification | Priority | Vendor response |
|---|---|---|---|---|---|
| NFR-001 | Availability | Business hours: Mon-Fri 07:00-19:00 NZT, Sat 08:00-13:00 | Defines the SLA window | Must | |
| NFR-002 | Availability | 99.9% monthly availability for production, excluding agreed maintenance | Vendor monitoring and monthly report | Must | |
| NFR-003 | Availability | Planned maintenance outside business hours, max 4 h/month | Release calendar | Must | |
| NFR-010 | Performance | 95% of UI page loads < 2 s, 99% < 4 s, at peak concurrency | Performance test plus production monitoring | Must | |
| NFR-011 | Performance | Search results < 3 s for 95% of queries | Performance test | Must | |
| NFR-012 | Performance | Synchronous API responses < 1 s at p95 at peak load | API monitoring | Must | |
| NFR-013 | Performance | Event/webhook delivery < 60 s from business event | Integration monitoring | Should | |
| NFR-014 | Performance | Bulk import throughput supports a full migration within the cutover window (see DEC-010) | Migration dress rehearsal | Must | |
| NFR-020 | Scalability | Supports Year 5 volumes (section 2) without re-architecture | Vendor capacity statement, load test | Must | |
| NFR-021 | Scalability | Handles 2x peak load for 1 hour (seasonal surge) | Load test | Should | |
| NFR-030 | Disaster recovery | RTO ≤ 4 hours for production | DR test evidence | Must | |
| NFR-031 | Disaster recovery | RPO ≤ 15 minutes | DR test evidence | Must | |
| NFR-032 | Backup | Daily backups retained 35 days. Monthly retained 12 months | Vendor backup policy | Must | |
| NFR-033 | Backup | Tenant-level restore available on request within 2 business days | Restore test | Should | |
| NFR-040 | Security | Encryption in transit TLS 1.2+ and at rest AES-256 | Assurance evidence | Must | |
| NFR-041 | Security | Critical vulnerabilities patched within 7 days | Vendor reports | Must | |
| NFR-050 | Audit | Audit trail retained 7 years and retrievable within 2 business days | Audit test | Must | |
| NFR-051 | Logging | Security logs delivered to SIEM within 15 minutes | Integration test | Must | |
| NFR-060 | Monitoring | P1 incidents detected and notified within 15 minutes | Incident records | Must | |
| NFR-070 | Data residency | Data stored and processed in approved jurisdictions only (SAR-003) | Vendor declaration, contract | Must | |
| NFR-080 | Usability / accessibility | WCAG 2.1 AA for the internal UI and external portal | Accessibility audit | Must | |
| NFR-081 | Supportability | Supported on current Edge/Chrome. Mobile-responsive portal | Test | Should | |
| NFR-090 | Data retention | Claims records retained per the retention schedule *(e.g. 10 years after closure)*, then disposed | Configuration and audit | Must | |
| NFR-100 | Interoperability | All integrations use documented, versioned APIs (EAS-T03/T04) | API catalogue | Must | |

## 4. Traceability

| NFR | Diagram | Test type | SLA clause |
|---|---|---|---|
| NFR-002, 003 | 08 | Operational acceptance | Availability |
| NFR-010 to 014 | 04, 05, 08 | Performance test | Performance |
| NFR-030 to 033 | 08 | DR test | Resilience |
| NFR-040, 041, 050, 051 | 06, 08 | Security test | Security |
| NFR-070 | 03, 08 | Contract review | Data location |

## 5. Vendor response required

For each NFR: compliance code, the subscription tier needed to meet it, any extra cost, and the evidence. Highlight NFRs that cannot be met and propose alternatives.
