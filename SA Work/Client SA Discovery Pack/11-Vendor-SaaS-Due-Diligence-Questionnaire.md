# 11: Vendor SaaS Due-Diligence Questionnaire

| Field | Value |
|---|---|
| Owner | Client Solution Architect |
| Audience | SaaS vendor |
| Status | Draft v0.1 |

## 1. Purpose

These SaaS-specific questions materially affect implementation cost and ongoing operating cost. They are often missed in requirements-led discovery. Answers are mandatory.

## 2. Questionnaire

| ID | Area | Required deliverable | Key questions | Vendor answer | Evidence |
|---|---|---|---|---|---|
| DDQ-001 | Licensing | Licensing and subscription model | Per user, per transaction, per module or consumption-based? What are the price drivers, tiers and annual escalation? | | |
| DDQ-002 | Licensing | Licence metrics | How are named, concurrent, external and integration users counted? Are API calls or storage charged? | | |
| DDQ-010 | Environments | Environment strategy | How many environments are included? What do additional or refreshed environments cost? | | |
| DDQ-020 | Releases | Release management model | How often are releases deployed? Can they be deferred? What notice and preview periods apply? | | |
| DDQ-021 | Extensibility | Customisation and extension model | What can be configured without affecting upgrades? Who maintains extensions through releases? | | |
| DDQ-022 | API management | API limits and throttling | What are the transaction, rate, payload and concurrency limits? What does it cost to raise them? | | |
| DDQ-030 | Data residency | Hosting and residency declaration | Where is client data stored, processed, backed up and accessed for support? | | |
| DDQ-031 | Data residency | Sub-processors | Who are the sub-processors and where are they? How is the client notified of changes? | | |
| DDQ-040 | Security | SaaS security assurance pack | ISO 27001, SOC 2 Type II, penetration tests, other certifications? When were they last audited? | | |
| DDQ-041 | Identity | SSO and identity integration | Entra ID, MFA, federation (SAML/OIDC), SCIM provisioning, and external identity? | | |
| DDQ-050 | DR and BCP | SaaS resilience documentation | What RTO, RPO and DR commitments are contractual? When was the last DR test? | | |
| DDQ-060 | Privacy | Privacy and data processing assessment | Data processing terms, vendor staff access to data, breach notification timeframes? | | |
| DDQ-070 | Exit | SaaS exit and data portability plan | How can all data be exported? In what formats? What does exit assistance cost? How is deletion confirmed? | | |
| DDQ-080 | Operations | SaaS shared responsibility matrix | What does the vendor operate versus the client? (respond to [08](08-Shared-Responsibility-Matrix.md)) | | |
| DDQ-090 | Service management | SLA and support model | What are the incident response targets, service availability, service credits and escalation? | | |
| DDQ-100 | Roadmap | Product roadmap | Which features relevant to our gaps are on the roadmap, with dates? How binding are they? | | |
| DDQ-110 | Viability | Vendor and product viability | Customer base in the region, comparable references, financial stability, local support presence? | | |

## 3. Regulated / NZ public-sector supplement *(include where applicable)*

| ID | Area | Key questions | Vendor answer | Evidence |
|---|---|---|---|---|
| DDQ-200 | Information classification | Is the service suitable for the data classification (e.g. IN-CONFIDENCE / SENSITIVE)? | | |
| DDQ-201 | Data sovereignty | Can all data, including backups and logs, be held in New Zealand (or an approved jurisdiction)? What foreign-jurisdiction legal access risks exist? | | |
| DDQ-202 | Privacy | How does the service support Privacy Act 2020 obligations (access/correction requests, notifiable breaches)? | | |
| DDQ-203 | Protective security | How does the vendor align with the Protective Security Requirements (PSR) and the NZISM controls? | | |
| DDQ-204 | Certification & Accreditation | What C&A evidence is available (control mappings, prior government C&A, IRAP or equivalent)? | | |
| DDQ-205 | Cloud risk assessment | Will the vendor complete the GCDO cloud risk assessment questionnaire or equivalent? | | |
| DDQ-206 | Records | How are Public Records Act retention and disposal requirements supported? | | |
| DDQ-207 | Official information | How fast can records be retrieved to respond to OIA requests? | | |

## 4. Response instructions

- Answer every question. "Not applicable" must be justified.
- Reference the supporting evidence (document name, section).
- State where an answer carries an extra cost, and include it in the commercial breakdown ([12](12-Vendor-Estimation-Pack-Requirements.md)).
