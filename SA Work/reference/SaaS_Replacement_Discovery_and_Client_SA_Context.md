# SaaS Replacement Discovery Workshop -- Chat Context

**Prepared:** 14 November 2026\
**Purpose:** Consolidated context from this conversation for reuse in
future discussions, planning, and preparation of a vendor discovery
workshop.

------------------------------------------------------------------------

## 1. Project scenario

The project is replacing an existing **on-premises solution with a SaaS
product**. A vendor is expected to participate in a discovery workshop
to understand the current solution, assess the requirements and
implementation complexity, and prepare a credible cost and effort
estimate.

The client-side Solution Architect (SA) is responsible for helping the
vendor understand the existing and target enterprise context,
identifying architecture constraints and dependencies, and ensuring the
vendor's proposed solution aligns with enterprise architecture.

The workshop should give the vendor enough information to estimate the
work across the full replacement lifecycle---not just SaaS
configuration. This includes licensing, configuration, extensions,
integrations, data migration, security, testing, deployment, transition,
and legacy decommissioning.

The exact business domain and SaaS product have not been specified in
this chat. Examples below are generic and should be tailored to the
actual solution.

------------------------------------------------------------------------

## 2. Desired outcome of discovery

The vendor should be able to produce:

1.  A clear understanding of the existing solution, its users, business
    capabilities, applications, integrations, data, and operational
    dependencies.
2.  A fit-gap assessment between business and technical requirements and
    the SaaS product's standard capabilities.
3.  A proposed target solution architecture and implementation approach.
4.  An inventory of integrations, data migration needs, security
    requirements, environments, and non-functional requirements.
5.  A work breakdown structure (WBS) covering the full implementation.
6.  Effort estimates by activity, role, and phase.
7.  A delivery roadmap, indicative timeline, resource plan, and key
    dependencies.
8.  A commercial estimate that separates one-off implementation costs
    from recurring SaaS and support costs.
9.  Documented assumptions, exclusions, risks, constraints, and estimate
    confidence.

The estimate should distinguish between: - Confirmed scope and
estimates. - Provisional scope and estimates based on assumptions. -
Items that cannot yet be estimated and require further investigation.

Avoid requesting a fixed-price commitment based only on a high-level
discovery discussion. The vendor should make assumptions and estimate
confidence explicit.

------------------------------------------------------------------------

## 3. Information and deliverables expected from each client team

### 3.1 Business Analysis (BA)

The BA team should provide the business and functional view:

-   Business capability map and scope boundaries.
-   Current-state (As-Is) business processes.
-   Desired future-state (To-Be) processes, where known.
-   Functional requirements and use cases.
-   Business rules, calculations, workflows, and decision points.
-   User personas, roles, responsibilities, and user volumes.
-   Forms, templates, correspondence, and document requirements.
-   Reports, dashboards, extracts, and analytics requirements.
-   Business data volumes and growth expectations.
-   Fit-gap questions and known product limitations.
-   Business priorities and criticality.
-   Acceptance criteria and business success measures.
-   Known process exceptions, manual workarounds, and pain points.

### 3.2 Client Solution Architect (SA)

The client SA should provide the enterprise and solution architecture
view:

-   Current-state system context diagram.
-   Current application and technology landscape.
-   Existing solution architecture and major components.
-   Target SaaS solution context diagram.
-   Target logical/application architecture, at an appropriate
    conceptual level.
-   Integration architecture and enterprise integration standards.
-   Identity and access management architecture.
-   Security, privacy, data residency, and compliance constraints.
-   Network and connectivity constraints.
-   Non-functional requirements (NFRs).
-   Environment and deployment considerations.
-   Operational support, monitoring, logging, and audit expectations.
-   Availability, business continuity, disaster recovery, RTO, and RPO
    expectations.
-   Architecture principles, standards, technology constraints, and
    approved platforms.
-   Key architecture risks, assumptions, dependencies, and decisions.
-   Transition, coexistence, and legacy decommissioning considerations.

The client SA should provide enough architecture context for the vendor
to understand the enterprise landscape and constraints. The vendor
should validate this information and develop the detailed
product-specific target design.

### 3.3 Technical Business Analyst (Technical BA)

The Technical BA should provide the detailed system and data view:

-   Application, interface, and system inventory.
-   Integration catalogue, including source, target, direction, purpose,
    frequency, and criticality.
-   Interface specifications and available API, event, file, or message
    definitions.
-   Data entity inventory and data ownership.
-   Data mapping and transformation rules, where known.
-   Data volumes, history, retention, and archival requirements.
-   Batch jobs, scheduled tasks, and event-driven processes.
-   Authentication and service-account inventory.
-   Reporting, data extraction, and downstream consumption requirements.
-   Document and attachment inventory.
-   Error handling, retries, reconciliation, and operational procedures.
-   Dependencies on databases, middleware, file shares, and external
    services.

### 3.4 Test team

The test team should provide the quality and verification view:

-   Test strategy and test scope.
-   Functional, integration, end-to-end, regression, performance,
    security, and accessibility testing needs, as applicable.
-   Data migration testing and reconciliation approach.
-   Test environments and test data requirements.
-   System integration testing (SIT) approach.
-   User acceptance testing (UAT) approach and business ownership.
-   Test automation opportunities and existing assets.
-   Non-functional test scenarios and acceptance thresholds.
-   Defect management and release entry/exit criteria.
-   Regression approach for SaaS vendor releases and product updates.

### 3.5 Project and delivery team

The project team should provide delivery context:

-   Project scope, objectives, and boundaries.
-   Delivery approach, phases, milestones, and target dates.
-   Governance, decision-making, and approval processes.
-   Client and vendor roles and responsibilities.
-   Resource availability and constraints.
-   RAID log (risks, assumptions, issues, and dependencies).
-   Procurement and commercial constraints.
-   Change management, communications, and training approach.
-   Cutover, business readiness, and go-live planning.
-   Legacy retirement and contract termination dependencies.
-   Reporting and status management expectations.

------------------------------------------------------------------------

## 4. SaaS-specific discovery considerations

The workshop should explicitly cover SaaS topics that may not apply in
the same way to an on-premises implementation.

### Product and subscription

-   SaaS subscription model, licensing metrics, tiers, and optional
    modules.
-   Number and type of environments included in the subscription.
-   User, transaction, storage, API, and other consumption limits.
-   API rate limits, throttling, and bulk processing constraints.
-   Additional costs for non-production environments, storage, support,
    or premium capabilities.

### Product configuration and extensibility

Classify each requirement as one of the following: - Standard product
capability. - Configuration. - Extension using supported platform
mechanisms. - Customisation or custom code. - Workaround. - Unsupported
requirement.

For each gap, capture the proposed approach, implications, ongoing
maintenance impact, and estimated effort.

### Security, privacy, and compliance

-   Data hosting locations and data residency.
-   Security assurance evidence, such as relevant ISO certifications and
    SOC reports.
-   Identity federation, SSO, MFA, RBAC, and privileged access.
-   Encryption in transit and at rest, key management, and secrets
    management.
-   Audit logging, monitoring, incident response, and security
    notifications.
-   Data classification, privacy obligations, retention, and deletion.
-   Subprocessors and third-party service providers.
-   Shared responsibility boundaries.
-   Exit arrangements and secure data return/deletion.

For a New Zealand organisation, assess applicable New Zealand privacy,
data residency, security classification, government protective security,
and certification/accreditation requirements where relevant. Do not
assume that every government-specific requirement applies to every
project.

### Service management and operations

-   Availability and service-level commitments.
-   Support hours, severity definitions, escalation, and incident
    communications.
-   Planned maintenance and SaaS release cadence.
-   Release notifications, testing windows, and customer control over
    updates.
-   Backup, restore, disaster recovery, RTO, and RPO.
-   Monitoring, audit access, service reporting, and operational
    integration.
-   Data portability, exit strategy, and vendor lock-in considerations.

------------------------------------------------------------------------

## 5. Architecture diagrams the client SA should prepare

The following diagrams form the recommended architecture pack for the
discovery workshop. They should be clear, high-level, and consistent.
They are not intended to replace the vendor's detailed solution design.

### Diagram 1 -- Current-State System Context

**Purpose:** Show the solution being replaced, its users, and the
systems it interacts with.

Include: - Business users, customers, administrators, and external
parties. - Existing on-premises application. - Application database and
document repository. - Identity provider. - CRM, finance, payment,
reporting, and other connected systems, as applicable. - Main
information or transaction flows.

Example Mermaid:

``` mermaid
flowchart LR
    Users[Business Users]
    External[External Parties]
    Legacy[On-Premises Legacy Application]
    DB[(Legacy Database)]
    Docs[(Document Repository)]
    IAM[Identity Provider]
    CRM[CRM]
    Finance[Finance System]
    Reporting[Reporting Platform]

    Users --> Legacy
    External --> Legacy
    Legacy --> DB
    Legacy --> Docs
    IAM --> Legacy
    Legacy <--> CRM
    Legacy <--> Finance
    Legacy --> Reporting
```

### Diagram 2 -- Current-State Application and Technology Landscape

**Purpose:** Show the major layers and components of the existing
solution.

Possible layers: - User/presentation layer. - Application and business
logic layer. - Integration and middleware layer. - Data and document
layer. - Infrastructure and hosting layer. - Security and operations
capabilities.

Show major technologies and ownership where known. Avoid cluttering this
view with every interface; use a separate integration diagram or
catalogue.

### Diagram 3 -- Target SaaS Solution Context

**Purpose:** Show how the proposed SaaS product fits into the client
enterprise landscape.

Include: - Client users and channels. - SaaS product and major
functional modules. - Client identity provider and SSO. - API management
or integration platform. - Connected enterprise systems. - Reporting and
analytics consumers. - Data and trust boundaries.

Example Mermaid:

``` mermaid
flowchart LR
    Users[Client Users]
    IAM[Client Identity Provider]
    Integration[Client Integration Platform / API Management]
    CRM[CRM]
    Finance[Finance System]
    Reporting[Reporting and Analytics]

    subgraph SaaS["Vendor SaaS Platform"]
        UI[Web User Interface]
        Core[Core Business Capabilities]
        Workflow[Workflow and Rules]
        Docs[Document Management]
        SaaSData[(SaaS Data Store)]
        UI --> Core
        Core --> Workflow
        Core --> Docs
        Core --> SaaSData
    end

    Users --> UI
    IAM -. SSO / Federation .-> UI
    Core <--> Integration
    Integration <--> CRM
    Integration <--> Finance
    Core --> Reporting
```

### Diagram 4 -- Target SaaS Integration Architecture

**Purpose:** Show how the SaaS product exchanges data with client and
third-party systems.

Include: - SaaS APIs, webhooks, events, bulk interfaces, or file
transfer. - Client API gateway/API management. - Integration
platform/iPaaS. - Message broker or event platform, if applicable. -
SFTP or managed file transfer, if applicable. - Source and target
systems. - Authentication and trust boundaries. - Direction and broad
purpose of each flow.

Example Mermaid:

``` mermaid
flowchart LR
    SaaS[SaaS Product]
    APIM[API Management]
    iPaaS[Integration Platform]
    Broker[Message Broker]
    SFTP[Managed File Transfer]
    CRM[CRM]
    ERP[Finance / ERP]
    DWH[Data Warehouse]

    SaaS <--> APIM
    APIM <--> iPaaS
    iPaaS <--> Broker
    iPaaS <--> CRM
    iPaaS <--> ERP
    SaaS --> SFTP
    SFTP --> iPaaS
    iPaaS --> DWH
```

### Diagram 5 -- Data Migration Architecture

**Purpose:** Explain how data and documents move from the legacy
environment into the SaaS product, and how completeness and accuracy
will be verified.

Include: - Legacy database and document stores. - Extraction method and
staging area. - Data profiling and cleansing. - Transformation and
mapping. - Validation and reconciliation. - SaaS bulk import/API
mechanisms. - Historical data archive or read-only access. - Migration
rehearsal and final migration. - Error handling and exception
remediation.

Example Mermaid:

``` mermaid
flowchart LR
    Source[(Legacy Database)]
    Docs[(Legacy Documents)]
    Extract[Extract]
    Stage[(Secure Staging)]
    Clean[Profile and Cleanse]
    Transform[Transform and Map]
    Validate[Validate and Reconcile]
    Import[SaaS Import / APIs]
    Target[(SaaS Data)]
    Archive[(Archive / Read-only Access)]

    Source --> Extract
    Docs --> Extract
    Extract --> Stage
    Stage --> Clean
    Clean --> Transform
    Transform --> Validate
    Validate --> Import
    Import --> Target
    Source --> Archive
    Docs --> Archive
```

### Diagram 6 -- Identity and Security Architecture

**Purpose:** Show how users, administrators, and services authenticate
and how access is controlled.

Include: - Workforce identity provider. - SSO federation protocol, such
as SAML or OIDC, where applicable. - MFA and conditional access. - SaaS
user and administrator roles. - RBAC and segregation of duties. -
Service identities and API authentication. - Privileged access
management. - Audit logs and security monitoring. - Encryption and
key-management boundaries, where relevant.

### Diagram 7 -- Environment and Deployment Architecture

**Purpose:** Show the environments and release/deployment touchpoints
across the vendor SaaS platform and client-managed components.

Include: - Vendor-provided development, test, UAT, and production
environments, as applicable. - Client-managed integration
environments. - Connectivity between each environment. - Configuration
promotion and release management. - Test data and production data
boundaries. - SaaS vendor release process and client regression
testing. - Environment-specific endpoints and credentials at a
conceptual level.

Do not assume the vendor provides a particular number or type of
environments; confirm this during discovery.

### Diagram 8 -- Non-Functional Requirements (NFR) Architecture View

**Purpose:** Make the key quality attributes and service expectations
visible.

Cover: - Availability and resilience. - Performance and response
times. - Capacity, concurrency, and throughput. - Scalability and
storage growth. - Security and privacy. - Auditability and
traceability. - Backup and recovery. - Disaster recovery, RTO, and
RPO. - Monitoring, alerting, and support. - Accessibility and usability,
where applicable. - Data retention and archival.

This may be a structured diagram or a concise architecture view
supported by an NFR catalogue. The catalogue should contain measurable
targets wherever possible.

### Diagram 9 -- SaaS Shared Responsibility Architecture

**Purpose:** Make clear which party is responsible for each technology
and operational control.

Show three responsibility groupings: - Vendor responsibility. - Shared
responsibility. - Client responsibility.

Typical topics include: - SaaS platform infrastructure and patching. -
Application availability and platform operations. - Identity and access
management. - User and role administration. - Data quality,
classification, and retention. - Integration services and credentials. -
Security monitoring and incident response. - Backup, recovery, and
business continuity. - Configuration, release testing, and change
management.

Confirm actual responsibilities against the vendor's contract, service
description, and security documentation.

### Diagram 10 -- Transition, Coexistence, and Legacy Decommissioning

**Purpose:** Explain how the organisation moves from the on-premises
solution to SaaS while controlling business and data risk.

Include: - Legacy operation during implementation. - Data extraction and
migration rehearsals. - Integration build and testing. - SaaS validation
and business acceptance. - Cutover and go-live. - Any required
coexistence or dual-running period. - Read-only legacy access or
archive. - Final legacy shutdown and decommissioning. - Contract,
infrastructure, and support retirement dependencies.

------------------------------------------------------------------------

## 6. Recommended diagram preparation order

Prepare the diagrams in this order so that each view builds on the
previous one:

1.  Current-State System Context.
2.  Current-State Application and Technology Landscape.
3.  Target SaaS Solution Context.
4.  Target SaaS Integration Architecture.
5.  Data Migration Architecture.
6.  Identity and Security Architecture.
7.  NFR Architecture View.
8.  Environment and Deployment Architecture.
9.  SaaS Shared Responsibility Architecture.
10. Transition and Legacy Decommissioning.

The first four diagrams are especially important for helping the vendor
understand scope and integration complexity. Data migration, security,
NFRs, environments, and transition are important for producing a
complete estimate rather than an application-only estimate.

------------------------------------------------------------------------

## 7. Traceability across diagrams, inventories, and estimates

Use consistent identifiers across the architecture diagrams, interface
catalogue, data migration inventory, requirements, risks, and vendor
estimate workbook.

Suggested identifier conventions:

  Item          Example      Description
  ------------- ------------ ------------------------------------------
  System        `SYS-001`    Unique system identifier
  Interface     `INT-001`    Unique integration/interface identifier
  Data entity   `DATA-001`   Unique data entity or migration object
  Requirement   `REQ-001`    Functional or non-functional requirement
  Risk          `RISK-001`   Project or architecture risk
  Assumption    `ASM-001`    Estimation or design assumption
  Decision      `ADR-001`    Architecture decision record

For every interface, capture at least: - Interface ID. - Source and
target system IDs. - Business purpose. - Direction. - Pattern (API,
event, file, batch, etc.). - Frequency and expected volume. - Data
sensitivity/classification. - Authentication method. - Error handling
and reconciliation. - Criticality and availability expectations. -
Current-state and target-state approach. - Known
specification/documentation. - Open questions and assumptions.

This traceability allows the vendor to connect each proposed integration
or migration activity to a known system, requirement, and estimate line.

------------------------------------------------------------------------

## 8. Suggested vendor estimation structure

Ask the vendor to provide estimates against a WBS that includes, at
minimum:

1.  Discovery and detailed requirements.
2.  SaaS subscription, licensing, and environment setup.
3.  Product configuration.
4.  Extensions and custom development, if permitted.
5.  Integrations and interface development.
6.  Data extraction, cleansing, transformation, migration, and
    reconciliation.
7.  Security, identity, privacy, and compliance activities.
8.  Reporting and analytics.
9.  Testing: functional, integration, regression, performance, security,
    and migration.
10. Training and change management.
11. Deployment, cutover, and go-live support.
12. Coexistence, archival, and legacy decommissioning.
13. Project management, architecture, and governance.
14. Warranty, hypercare, and ongoing support transition.

For each WBS line, request: - Description and deliverable. - Estimate by
role or skill. - Effort (person-days or hours). - Duration and
dependencies. - Client effort versus vendor effort. - One-off cost
versus recurring cost. - Assumptions and exclusions. - Confidence level
and outstanding questions.

Keep recurring costs separate from one-time costs. Recurring costs may
include subscriptions, additional environments, storage, API
consumption, premium support, and third-party services.

------------------------------------------------------------------------

## 9. Practical discovery workshop agenda

A possible workshop sequence:

1.  **Objectives and scope** -- business drivers, boundaries, outcomes,
    and success measures.
2.  **Current solution overview** -- users, processes, application
    landscape, technology, and operational model.
3.  **Business capabilities and requirements** -- workflows, business
    rules, exceptions, reports, and pain points.
4.  **SaaS product overview and fit-gap** -- standard capabilities,
    configuration, extensions, workarounds, and gaps.
5.  **Integrations** -- systems, interfaces, patterns, volumes,
    security, and dependencies.
6.  **Data migration** -- data entities, quality, history, documents,
    volume, retention, and archive.
7.  **Security and non-functional requirements** -- identity, privacy,
    resilience, performance, service levels, and compliance.
8.  **Environments and delivery approach** -- SaaS environments, client
    environments, release management, testing, and deployment.
9.  **Transition and operations** -- cutover, coexistence, support,
    vendor releases, and decommissioning.
10. **Estimation assumptions and next steps** -- open questions,
    evidence required, owners, due dates, and estimate confidence.

Record decisions, actions, assumptions, and unanswered questions as the
workshop progresses.

------------------------------------------------------------------------

## 10. Client SA preparation checklist

### Before the workshop

-   [ ] Confirm scope, objectives, stakeholders, and decision-makers.
-   [ ] Obtain the latest current-state architecture and system
    inventory.
-   [ ] Prepare the current-state context and landscape diagrams.
-   [ ] Prepare the target SaaS context diagram.
-   [ ] Obtain the integration catalogue and identify missing interface
    specifications.
-   [ ] Understand major data stores, data volumes, and document
    repositories.
-   [ ] Gather identity, security, privacy, and compliance constraints.
-   [ ] Gather NFRs, service levels, availability, RTO, and RPO
    expectations.
-   [ ] Confirm enterprise architecture standards and approved
    integration patterns.
-   [ ] Identify known constraints, risks, assumptions, and
    dependencies.
-   [ ] Agree with BA, Technical BA, Test, and Project teams on their
    inputs.
-   [ ] Prepare a list of open questions for the vendor.

### During the workshop

-   [ ] Explain the current architecture and business/system boundaries.
-   [ ] Validate the vendor's understanding of each system and
    interface.
-   [ ] Challenge assumptions about SaaS capabilities and integration
    patterns.
-   [ ] Identify configuration versus extension versus customisation.
-   [ ] Confirm data migration scope and reconciliation expectations.
-   [ ] Clarify security and shared responsibility boundaries.
-   [ ] Capture SaaS environment, API, storage, and licensing
    constraints.
-   [ ] Identify dependencies and client-side work.
-   [ ] Record risks, decisions, assumptions, exclusions, and open
    questions.
-   [ ] Ensure all estimate items can be traced to requirements,
    systems, or interfaces.

### After the workshop

-   [ ] Publish updated diagrams and inventories.
-   [ ] Close or assign open questions.
-   [ ] Review the vendor fit-gap assessment.
-   [ ] Review the proposed target architecture for enterprise
    alignment.
-   [ ] Validate integration and migration estimates.
-   [ ] Check that testing, security, transition, and decommissioning
    are included.
-   [ ] Review client-side effort and dependencies, not only vendor
    effort.
-   [ ] Challenge unsubstantiated assumptions and low-confidence
    estimates.
-   [ ] Confirm one-off and recurring cost breakdowns.
-   [ ] Record architecture decisions and required approvals.

------------------------------------------------------------------------

## 11. Key principles for the client SA

-   Present the **current state accurately**, including undocumented
    integrations and manual workarounds.
-   Keep the client architecture diagrams **conceptual and readable**;
    do not attempt to design every vendor SaaS internal component.
-   Clearly distinguish what the client owns from what the SaaS vendor
    owns.
-   Do not assume that SaaS eliminates integration, data, security,
    operational, or testing complexity.
-   Ask the vendor to demonstrate how each requirement is met: standard
    capability, configuration, extension, customisation, workaround, or
    unsupported.
-   Make API limits, data volumes, migration history, environment
    availability, and SaaS release cadence explicit.
-   Include the complete transition and legacy retirement scope.
-   Ensure estimates include client-side activities and dependencies.
-   Use consistent IDs across diagrams and inventories to support
    traceability.
-   Treat the vendor's proposed design as subject to client enterprise
    architecture review and applicable security
    certification/accreditation processes.

------------------------------------------------------------------------

## 12. Recommended discovery pack contents

A practical pack to share with the vendor can be organised as follows:

``` text
Client SaaS Replacement Discovery Pack/
├── 01_Project_Context/
│   ├── Project_Overview_and_Scope
│   ├── Business_Objectives
│   └── Stakeholders_and_Governance
├── 02_Business/
│   ├── Capability_Map
│   ├── As_Is_and_To_Be_Processes
│   ├── Functional_Requirements
│   └── Business_Rules_and_Reports
├── 03_Architecture/
│   ├── Current_State_System_Context
│   ├── Current_State_Application_Landscape
│   ├── Target_SaaS_Context
│   ├── Target_Integration_Architecture
│   ├── Data_Migration_Architecture
│   ├── Identity_and_Security_View
│   ├── NFR_Architecture_View
│   ├── Environment_and_Deployment_View
│   ├── Shared_Responsibility_View
│   └── Transition_and_Decommissioning_View
├── 04_Technical_Inventories/
│   ├── System_Inventory
│   ├── Interface_Catalogue
│   ├── Data_and_Document_Inventory
│   └── Batch_and_Scheduled_Jobs
├── 05_Test_and_Quality/
│   ├── Test_Strategy
│   ├── NFR_Test_Requirements
│   └── Migration_Reconciliation_Approach
├── 06_Security_and_Operations/
│   ├── Security_and_Privacy_Requirements
│   ├── Operational_Requirements
│   └── Service_Levels_and_DR
└── 07_Estimation/
    ├── Assumptions_and_Constraints
    ├── Risks_and_Dependencies
    ├── Open_Questions
    └── Vendor_Estimation_Template
```

Only include documents that exist and are approved for vendor sharing.
Mark draft, provisional, confidential, or restricted material
appropriately.

------------------------------------------------------------------------

## 13. Outstanding information to tailor this pack

The following details were not specified in this conversation and should
be confirmed before turning the generic guidance into a project-specific
pack:

-   Business domain and purpose of the existing solution.
-   Name and type of the SaaS product under consideration.
-   Number of users, user groups, and locations.
-   Number of connected systems and known integration patterns.
-   Data volumes, historical data period, and document volumes.
-   Regulatory, privacy, security classification, and data residency
    requirements.
-   Required implementation date and any contractual deadlines.
-   Whether historical data must be migrated, archived, or both.
-   Whether parallel running or phased migration is expected.
-   Whether the vendor is responsible for implementation only or also
    ongoing managed services.

------------------------------------------------------------------------

**Suggested document name:**
`SaaS_Replacement_Discovery_and_Client_SA_Context.md`

**Suggested pack title:** *Client Solution Architecture -- SaaS
Replacement Discovery Pack*
