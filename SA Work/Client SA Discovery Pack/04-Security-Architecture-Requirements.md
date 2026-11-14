# 04: Security Architecture Requirements

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with Security Architecture) |
| Audience | SaaS vendor |
| Status | Draft v0.1 |
| Related | Diagram 06 Identity and Security, [05 Network](05-Network-and-Connectivity-Requirements.md), [11 Due-Diligence Questionnaire](11-Vendor-SaaS-Due-Diligence-Questionnaire.md) |

## 1. Purpose and context

This document defines the security requirements for identity, access, data protection, audit and assurance. Data in the solution is classified as **IN-CONFIDENCE** *(example)* and includes personal information. Controls must be proportionate to that classification and meet the applicable frameworks in section 9.

Response codes: `C`, `CC`, `PC`, `NC`, `R` (see the README).

## 2. Identity and authentication

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-001 | Workforce users authenticate through SSO with the enterprise IdP (SYS-004) using SAML 2.0 or OIDC | Must | | |
| SEC-002 | MFA and conditional access are enforced by the enterprise IdP. The SaaS honours the IdP session and step-up | Must | | |
| SEC-003 | No local SaaS accounts except documented break-glass accounts, which are vaulted, monitored and alerted on use | Must | | |
| SEC-004 | External users (customers/partners), if in scope, use an approved external identity service with MFA *(confirm scope)* | Should | | |
| SEC-005 | User provisioning and deprovisioning is automated from the IdP (SCIM 2.0 preferred). Leavers lose access within 1 hour *(example)* | Must | | |
| SEC-006 | Session timeout, concurrent session limits and re-authentication for sensitive actions are configurable | Should | | |

## 3. Authorisation and privileged access

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-010 | Role-based access control with least privilege. Roles can be mapped from IdP groups | Must | | |
| SEC-011 | Record-level or attribute-level access control is available where required (e.g. sensitive claims) | Should | | |
| SEC-012 | Segregation of duties between business admin, technical admin and security/audit roles | Must | | |
| SEC-013 | Privileged/admin access goes through the client PAM process (just-in-time, approved, time-bound) | Must | | |
| SEC-014 | Vendor staff access to client data or the tenant needs client approval, is logged, and is visible to the client | Must | | |
| SEC-015 | Periodic access recertification is supported (role and entitlement reports) | Must | | |

## 4. Integration and API security

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-020 | Integrations use OAuth 2.0 client credentials (or mTLS) with dedicated, scoped service identities per interface | Must | | |
| SEC-021 | Secrets and certificates are rotatable without downtime. State the rotation process and expiry notification | Must | | |
| SEC-022 | Webhooks are signed (HMAC or JWS) and delivered only to registered endpoints | Must | | |
| SEC-023 | API input validation, rate limiting and abuse protection are applied by the platform | Must | | |

## 5. Data protection

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-030 | Encryption in transit with TLS 1.2 or higher (TLS 1.3 preferred) on all interfaces | Must | | |
| SEC-031 | Encryption at rest (AES-256 or equivalent) for databases, files, backups and logs | Must | | |
| SEC-032 | Key management: describe the KMS/HSM. Customer-managed keys (BYOK/HYOK) are available *(state the cost)* | Should | | |
| SEC-033 | Sensitive data is masked or obfuscated in non-production environments | Must | | |
| SEC-034 | Uploaded files are malware-scanned, with file-type restrictions | Must | | |
| SEC-035 | Data residency per SAR-003, including backups, logs and support tooling | Must | | |
| SEC-036 | Secure data deletion on request and at exit, with a certificate of destruction | Must | | |

## 6. Audit, logging and monitoring

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-040 | Audit trail of user and admin actions (who, what, when, from where, before/after values) for business records | Must | | |
| SEC-041 | Security logs (authentication, admin, API, data export) are forwarded to the client SIEM in near real time | Must | | |
| SEC-042 | Audit logs are tamper-evident and retained for 7 years *(example; confirm against records obligations)* | Must | | |
| SEC-043 | Alerts on anomalous activity (mass export, privilege change, failed logins) | Should | | |

## 7. Application and platform security

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-050 | Secure SDLC aligned to OWASP ASVS / SAMM. Independent penetration test at least annually, with the summary shared | Must | | |
| SEC-051 | The client may perform its own security testing under agreed rules of engagement | Should | | |
| SEC-052 | Vulnerability management with patch SLAs *(example: critical 7 days, high 30 days)* | Must | | |
| SEC-053 | DDoS protection and WAF on internet-facing endpoints | Must | | |

## 8. Incident and breach management

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-060 | Security incidents affecting client data are notified within 24 hours *(example)* of detection | Must | | |
| SEC-061 | Vendor support enables the client to meet Privacy Act 2020 notifiable privacy breach obligations | Must | | |
| SEC-062 | Post-incident reports with root cause and remediation are provided | Must | | |

## 9. Assurance and compliance

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| SEC-070 | Current ISO/IEC 27001 certification and/or SOC 2 Type II report covering the in-scope service | Must | | |
| SEC-071 | Completed security questionnaire (see [11](11-Vendor-SaaS-Due-Diligence-Questionnaire.md)) | Must | | |
| SEC-072 | Supports the client Certification & Accreditation (C&A) process: evidence, control mapping, remediation plan | Must | | |
| SEC-073 | For NZ public sector: alignment with the NZISM, Protective Security Requirements (PSR) and the GCDO cloud risk assessment guidance *(where applicable)* | Must | | |
| SEC-074 | Privacy Impact Assessment input: data flows, sub-processors, access and retention | Must | | |

## 10. Vendor response required

Complete the response columns. Attach the ISO/SOC reports (under NDA if needed), the latest penetration-test summary, the security architecture overview and the incident response process.
