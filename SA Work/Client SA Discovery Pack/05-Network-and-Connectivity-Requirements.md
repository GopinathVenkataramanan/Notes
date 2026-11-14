# 05: Network and Connectivity Requirements

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with Network/Infrastructure) |
| Audience | SaaS vendor |
| Status | Draft v0.1 |
| Related | Diagrams 04 and 07, [04 Security](04-Security-Architecture-Requirements.md) |

## 1. Purpose

This document defines how users and client systems connect to the SaaS platform, and how the platform connects back to client and third-party systems.

## 2. Connectivity overview *(example)*

| Path | From | To | Route | Protocol |
|---|---|---|---|---|
| User access | Client workforce (office, remote) | SaaS UI | Internet (via client secure web gateway) | HTTPS |
| External user access | Customers / partners | SaaS portal | Internet | HTTPS |
| Inbound API | Enterprise API Gateway | SaaS REST APIs | Internet with IP allowlisting, or private connectivity | HTTPS + OAuth2 / mTLS |
| Outbound events | SaaS webhooks | Enterprise API Gateway / broker endpoint | Internet to the client public ingress | HTTPS, signed |
| File transfer | SaaS / Integration platform | Managed SFTP | Internet, key-based auth | SFTP |
| Migration | Client migration services | SaaS bulk import | Internet or private link | HTTPS |
| Data feed | SaaS | Enterprise data platform | Internet or private link | HTTPS / SFTP |

## 3. Requirements

Response codes: `C`, `CC`, `PC`, `NC`, `R`.

| ID | Requirement | Priority | Vendor response | Evidence / comment |
|---|---|---|---|---|
| NET-001 | Publish the full list of SaaS endpoints (FQDNs) and any IP ranges for each environment, and give notice before changes | Must | | |
| NET-002 | The SaaS tenant can be restricted to client egress IP ranges (IP allowlisting) for admin and API access | Must | | |
| NET-003 | Outbound calls from SaaS to the client originate from a published, stable set of IP addresses | Must | | |
| NET-004 | Private connectivity option (e.g. private link / dedicated interconnect) is available. State the cost and lead time | Should | | |
| NET-005 | Custom domain (e.g. `claims.example.govt.nz`) with client-managed DNS and certificates is supported | Should | | |
| NET-006 | TLS 1.2+ only. Weak ciphers disabled. HSTS enabled | Must | | |
| NET-007 | The platform works through the client secure web gateway / proxy (no unsupported protocols, WebSocket requirements documented) | Must | | |
| NET-008 | Bandwidth and latency expectations are stated for typical user transactions and bulk operations | Should | | |
| NET-009 | Email from the SaaS uses a client domain with SPF, DKIM and DMARC alignment | Should | | |
| NET-010 | No inbound connectivity into the client network except through the enterprise API gateway / SFTP | Must | | |
| NET-011 | Each SaaS environment (DEV, SIT, UAT, PROD) has separate endpoints and credentials | Must | | |

## 4. Client actions (for estimation of client-side effort)

| Action | Owner | Notes |
|---|---|---|
| Firewall and proxy rules for SaaS FQDNs | Client network team | Per environment |
| DNS records and certificates for custom domains | Client network team | If NET-005 is adopted |
| API gateway ingress for webhooks | Client integration team | Per environment |
| Private connectivity provisioning | Client network team | Only if NET-004 is adopted |

## 5. Vendor response required

Complete the response column, and provide a network architecture diagram, endpoint list and IP ranges per environment.
