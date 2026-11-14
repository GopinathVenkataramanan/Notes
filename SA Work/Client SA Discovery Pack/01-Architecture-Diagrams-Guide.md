# 01: Architecture Diagrams Guide

| Field | Value |
|---|---|
| Owner | Client Solution Architect |
| Audience | SaaS vendor (discovery and estimation), client architecture and project teams |
| Status | Draft v0.1 |
| Source file | [diagrams/SaaS_Replacement_Discovery_Pack.vsdx](diagrams/SaaS_Replacement_Discovery_Pack.vsdx) (10 pages) |

## 1. Purpose

This document explains each diagram in the discovery pack: what it shows, what must be captured, and how the vendor should use it for estimation. These are **discovery-level** diagrams (L1/L2/conceptual). They are deliberately not low-level designs.

## 2. Notation and colour key

| Colour | Meaning |
|---|---|
| Orange | Users and actors |
| Grey | Legacy / on-premises components (in scope for replacement or retirement) |
| Blue | Vendor SaaS platform and vendor-managed components |
| Green | Client-owned enterprise and integration components |
| Purple | External / third-party systems |
| Yellow | Data stores and data artefacts |
| Red | Security-critical components |
| Dashed container | Boundary (trust, ownership or hosting) |
| Solid arrow | Synchronous / primary flow, arrowhead shows direction |
| Dashed arrow | Asynchronous, batch, or reconciliation flow |
| Double-headed arrow | Bi-directional exchange |

Every system, interface and data store carries an ID from the [Architecture Element Register](13-Architecture-Element-Register.md).

## 3. Diagram catalogue

| Page | Diagram | Level | Priority | Primary estimation value |
|---|---|---|---|---|
| 01 | Current-State System Context | L1 | Mandatory | Systems and interfaces impacted by replacement |
| 02 | Current-State Application Landscape | L2 | Mandatory | Functions, middleware and infrastructure to replace, integrate or retire |
| 03 | Target SaaS Solution Context | L1 | Mandatory | Target scope and the components that stay client-owned |
| 04 | Target SaaS Integration Architecture | L2 | Mandatory | Per-interface integration estimate |
| 05 | Data Migration Architecture | L2 | Mandatory | Migration objects, volumes, transformation complexity, cycles |
| 06 | Identity and Security Architecture | L2 | Mandatory | Identity integration, security configuration, compliance activities |
| 07 | Environment and Deployment Architecture | L2 | Mandatory | Environment licensing, setup, deployment and release effort |
| 08 | Non-Functional Requirements Architecture | L2 | Mandatory | Subscription tier, additional services, compliance costs |
| 09 | SaaS Shared Responsibility | Conceptual | Recommended | Removes duplicated operational activities and makes support costs visible |
| 10 | Legacy Decommissioning and Transition | Conceptual | Recommended | Coexistence, archival and decommissioning costs |

## 4. Diagram details

### Diagram 01: Current-State System Context (L1)

**Purpose:** Show the existing on-prem solution, who uses it and which systems communicate with it.

**What to capture**
- [ ] Users and external actors (internal staff, managers, customers, partners)
- [ ] Existing application boundary (SYS-001)
- [ ] Database and document repository (DATA-001, DATA-002)
- [ ] Upstream and downstream systems (SYS-002 to SYS-006)
- [ ] Main integration directions
- [ ] System ownership (business and technical owners in the Element Register)

**Vendor should use it to:** confirm the full set of systems affected by the replacement.

### Diagram 02: Current-State Application Landscape (L2)

**Purpose:** Show the vendor the technology complexity behind the existing application.

**What to capture**
- [ ] Application components and modules (claims engine, workflow, rules, batch)
- [ ] Middleware and integration technology (ESB, API gateway, message queue)
- [ ] Database, document storage, data warehouse
- [ ] On-prem infrastructure dependencies (VMs, OS, monitoring, backup/DR)
- [ ] Batch and scheduled processing
- [ ] Operational dependencies

**Vendor should use it to:** identify functionality that SaaS must replace, and middleware or infrastructure that will be integrated or retired.

### Diagram 03: Target SaaS Solution Context (L1)

**Purpose:** Show how the future SaaS product fits into the client's enterprise ecosystem.

**What to capture**
- [ ] SaaS platform boundary and vendor ownership (SYS-010)
- [ ] Client-owned integration components (API gateway, integration platform)
- [ ] Enterprise identity provider (SYS-004)
- [ ] Upstream and downstream systems
- [ ] Reporting and data consumers
- [ ] External user access, if applicable

**Vendor should use it to:** establish the target scope and which existing components remain client-owned.

### Diagram 04: Target SaaS Integration Architecture (L2)

**Purpose:** Show how the SaaS solution communicates with enterprise and external systems. This is one of the most important diagrams for cost estimation.

**What to capture**
- [ ] API-based integration (REST/OAuth2 via API Management)
- [ ] Event and webhook integration (via message broker)
- [ ] Batch and file-based integration (secure file transfer)
- [ ] Middleware and API gateway
- [ ] Authentication and certificates for each interface
- [ ] Error handling and retry approach
- [ ] Data direction and frequency (detailed in the Technical BA integration catalogue, keyed by INT-ID)

**Vendor should use it to:** estimate each integration separately, using the INT-IDs in [13](13-Architecture-Element-Register.md).

### Diagram 05: Data Migration Architecture (L2)

**Purpose:** Show how data moves from the on-prem application into SaaS.

**What to capture**
- [ ] Source databases and document repositories (DATA-001 to DATA-003)
- [ ] Data extraction method
- [ ] Data cleansing and transformation
- [ ] Field mapping (Technical BA data mapping requirements)
- [ ] Migration tooling
- [ ] SaaS bulk-load or API capability, and its limits
- [ ] Reconciliation and validation
- [ ] Historical data and archival approach

**Vendor should use it to:** estimate migration objects, volumes, transformation complexity and the number of migration cycles (trial loads, dress rehearsals, production).

### Diagram 06: Identity and Security Architecture (L2)

**Purpose:** Show how users, administrators and integrations authenticate to and access the SaaS platform.

**What to capture**
- [ ] Single sign-on (SAML 2.0 / OIDC) with the enterprise IdP
- [ ] MFA and conditional access
- [ ] Role-based access control
- [ ] Service accounts and API authentication
- [ ] Privileged access
- [ ] Audit logging
- [ ] Encryption and key management
- [ ] Trust boundaries (client versus SaaS provider)

**Vendor should use it to:** identify identity integration, security configuration and compliance activities. Requirements are in [04](04-Security-Architecture-Requirements.md).

### Diagram 07: Environment and Deployment Architecture (L2)

**Purpose:** Show how the vendor provides SaaS environments and how client integration components map to them and are promoted.

**What to capture**
- [ ] SaaS environments available, and how many are included in the subscription
- [ ] Mapping of client integration environments to SaaS environments
- [ ] Configuration promotion approach
- [ ] Test data refresh approach (including masking)
- [ ] Release management and production deployment approvals

**Vendor should use it to:** identify additional environment licensing, setup, deployment and release management effort.

### Diagram 08: Non-Functional Requirements Architecture (L2)

**Purpose:** Translate NFRs into architecture capabilities and vendor obligations.

**What to capture:** availability, performance, scalability, DR, security, audit, monitoring and data residency. Targets are in the [NFR Catalogue](07-NFR-Catalogue.md).

**Vendor should use it to:** identify the required subscription tier, any additional services, and compliance costs.

### Diagram 09: SaaS Shared Responsibility (Conceptual)

**Purpose:** Clarify what the vendor manages, what the client manages, and what is shared. The detail is in the [Shared Responsibility Matrix](08-Shared-Responsibility-Matrix.md).

**Vendor should use it to:** avoid duplicated operational activities and make ongoing support costs visible.

### Diagram 10: Legacy Decommissioning and Transition (Conceptual)

**Purpose:** Explain the transition from legacy to SaaS, including coexistence and eventual retirement.

**What to capture**
- [ ] Data migration sequence
- [ ] Parallel running requirements
- [ ] Business cutover
- [ ] Historical access requirements and the legacy read-only period
- [ ] Data retention and disposal
- [ ] Infrastructure shutdown and contract termination

**Vendor should use it to:** estimate migration, coexistence, archival and decommissioning costs. Principles are in [10](10-Legacy-Decommissioning-Principles.md).

## 5. Diagram quality checklist (apply to every page)

- [ ] Title, level (L1/L2/Conceptual) and a "valid as at" date
- [ ] Every box has an element ID that exists in the register
- [ ] Every arrow shows direction. Integration arrows carry an INT-ID or a protocol label
- [ ] Boundaries are labelled with the owner (client / vendor / third party)
- [ ] Colours follow the key in section 2
- [ ] Example names have been replaced with actual system names
- [ ] Assumptions shown on the diagram are also logged in [09](09-Architecture-Risks-and-Constraints.md)

## 6. Vendor response required

For each diagram, the vendor confirms or corrects the representation, identifies gaps, and states how their product and implementation approach address it. The vendor's own detailed target architecture is a required proposal output (see [12](12-Vendor-Estimation-Pack-Requirements.md)).
