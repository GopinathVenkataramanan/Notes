That changes the discovery approach significantly. For an on-premises legacy solution being replaced by a vendor-hosted SaaS COTS product, the discovery should focus less on replicating the existing architecture and more on understanding:
What business capabilities must be retained or changed.
What the SaaS product provides out of the box.
What configuration, customisation or extensions are needed.
How existing systems will integrate with the SaaS platform.
How data will be migrated from the on-premises solution.
What SaaS security, privacy, compliance and operational requirements must be satisfied.
What responsibilities remain with the client versus the SaaS vendor.
As Client Solution Architect, your role is to ensure the vendor understands the existing landscape and enterprise constraints, while proposing a SaaS solution that meets the business and technical requirements.
1. Revised cost estimation model for SaaS replacement
#chatgpt-mermaid-_r_1fd_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_1fd_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_1fd_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_1fd_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-_r_1fd_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_1fd_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_1fd_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_1fd_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_1fd_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_1fd_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fd_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fd_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_1fd_ p{margin:0;}#chatgpt-mermaid-_r_1fd_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ .cluster-label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ .cluster-label span{color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_1fd_ .label text,#chatgpt-mermaid-_r_1fd_ span{fill:rgb(13, 13, 13);color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ .node rect,#chatgpt-mermaid-_r_1fd_ .node circle,#chatgpt-mermaid-_r_1fd_ .node ellipse,#chatgpt-mermaid-_r_1fd_ .node polygon,#chatgpt-mermaid-_r_1fd_ .node path{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .rough-node .label text,#chatgpt-mermaid-_r_1fd_ .node .label text,#chatgpt-mermaid-_r_1fd_ .image-shape .label,#chatgpt-mermaid-_r_1fd_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_1fd_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .rough-node .label,#chatgpt-mermaid-_r_1fd_ .node .label,#chatgpt-mermaid-_r_1fd_ .image-shape .label,#chatgpt-mermaid-_r_1fd_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_1fd_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_1fd_ .root .anchor path{fill:rgb(143, 143, 143)!important;stroke-width:0;stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fd_ .arrowheadPath{fill:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fd_ .edgePath .path{stroke:rgb(143, 143, 143);stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .flowchart-link{stroke:rgb(143, 143, 143);fill:none;}#chatgpt-mermaid-_r_1fd_ .edgeLabel{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-_r_1fd_ .edgeLabel p{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-_r_1fd_ .edgeLabel rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-_r_1fd_ .labelBkg{background-color:rgba(252, 252, 252, 0.5);}#chatgpt-mermaid-_r_1fd_ .cluster rect{fill:rgb(243, 243, 243);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .cluster text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ .cluster span{color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(243, 243, 243);border:1px solid rgba(0, 0, 0, 0.1);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_1fd_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fd_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_1fd_ .icon-shape,#chatgpt-mermaid-_r_1fd_ .image-shape{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-_r_1fd_ .icon-shape p,#chatgpt-mermaid-_r_1fd_ .image-shape p{background-color:rgb(252, 252, 252);padding:2px;}#chatgpt-mermaid-_r_1fd_ .icon-shape .label rect,#chatgpt-mermaid-_r_1fd_ .image-shape .label rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-_r_1fd_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_1fd_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_1fd_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_1fd_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_1fd_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_1fd_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_1fd_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_1fd_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fd_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_1fd_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fd_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(0, 79, 153);}#chatgpt-mermaid-_r_1fd_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(0, 79, 153);}#chatgpt-mermaid-_r_1fd_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_1fd_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_1fd_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .node rect,#chatgpt-mermaid-_r_1fd_ .node circle,#chatgpt-mermaid-_r_1fd_ .node ellipse,#chatgpt-mermaid-_r_1fd_ .node polygon,#chatgpt-mermaid-_r_1fd_ .node path{fill:rgb(229, 243, 255);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_1fd_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_1fd_ .mermaid-decision .label-container{fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_1fd_ .edgePaths .flowchart-link{stroke:rgb(143, 143, 143);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_1fd_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fd_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}SaaS Replacement - VendorCost EstimateSaaS Subscription andLicensingProduct Configuration andExtensionsIntegration ImplementationData MigrationSecurity and ComplianceTesting and QualityDeployment and TransitionProject and ChangeManagementUsers, modules, environments,consumptionFit-gap, workflows, rules,forms, reportsAPIs, middleware, events,external systemsLegacy data, cleansing,mapping, historyIAM, privacy, residency,accreditation, auditSIT, UAT, regression,performance, securityCutover, training, legacydecommissioningGovernance, resources, changeand adoptionDiscovery Evidence andValidated AssumptionsVendor WBS, Resource Plan,Timeline and CommercialProposal
2. Revised deliverables by team
These are the deliverables I would request from each team specifically for a SaaS replacement.
A. BA team – business and product fit-gap
Deliverable
Required information
Business capability map
Existing capabilities and future requirements
As-Is business processes
Existing on-prem workflows
To-Be business processes
Desired processes using SaaS
Functional requirements catalogue
Prioritised functional requirements
Business rules catalogue
Existing rules and decision logic
Product fit-gap assessment
Standard SaaS functionality vs gaps
Customisation requirements
Features not supported through standard configuration
Forms and document catalogue
Existing forms, templates, letters and notifications
Reports catalogue
Current and future reporting requirements
User roles and personas
User types, permissions and access requirements
Business volumes
Users, claims, transactions and peak workloads
Business acceptance criteria
Acceptance conditions for the replacement

Critical deliverable: Product Fit-Gap Matrix
The vendor must classify every requirement into one of these categories:
Classification
Meaning
Cost implication
Standard
Available out of the box
Usually configuration only
Configuration
Achieved through SaaS configuration
Configuration effort
Extension
Requires supported extension or low-code development
Additional development
Customisation
Requires bespoke development or product modification
Higher cost and upgrade risk
Workaround
Business process change to accommodate product
Business change effort
Not supported
Product cannot meet requirement
Scope gap or alternative solution

B. Client SA and Technical BA – architecture and technology
Client Solution Architect
Deliverable
Required information
Existing application context diagram
Legacy solution and surrounding systems
Current-state architecture
On-prem infrastructure and application architecture
Target SaaS context diagram
SaaS platform and enterprise ecosystem
Target integration architecture
API gateway, iPaaS, messaging and integration patterns
Enterprise architecture standards
Approved platforms, technologies and patterns
SaaS architecture requirements
Multi-tenancy, availability, scalability and resilience expectations
Security architecture requirements
IAM, SSO, MFA, encryption, audit and privileged access
Network and connectivity requirements
Connectivity, IP allowlisting, private connectivity and DNS
SaaS operational requirements
Monitoring, incident management, support, logging and service ownership
NFR catalogue
Performance, availability, DR, RTO and RPO
Architecture risks and constraints
Vendor dependencies, technology constraints and architectural exceptions
Legacy decommissioning principles
Retirement of existing infrastructure and applications

Technical BA
Deliverable
Required information
Application inventory
Existing applications and ownership
Integration catalogue
All upstream and downstream integrations
Interface specifications
API, SOAP, REST, files, batch and event details
Data entity catalogue
Existing database entities and relationships
Data migration inventory
Records, attachments, historical data and volumes
Data mapping requirements
Legacy source to SaaS target mapping
Batch jobs inventory
Existing scheduled jobs and processing
Authentication inventory
Existing service accounts, certificates and authentication methods
Reporting and extraction inventory
Existing reports, data feeds and consumers
Technical dependency register
External systems, third parties and dependencies

Important SaaS-specific consideration: The vendor must identify which integration and connectivity capabilities are supported by their SaaS platform, including API limits, throttling, webhooks, event interfaces, file transfers and authentication mechanisms.
C. Test team
Deliverable
Required information
Test strategy
Overall testing approach
Functional test scope
Business capabilities and scenarios
SaaS integration test scope
Enterprise and external system integrations
Data migration validation strategy
Reconciliation, completeness and accuracy
Regression test scope
Existing business capabilities to preserve
Performance test requirements
Response time, concurrency and throughput
Security test requirements
Penetration testing and vulnerability assessment
SaaS environment requirements
Vendor-provided environments and client access
UAT approach
Business validation and acceptance
Test automation requirements
Automation framework and tooling

SaaS-specific testing should also cover vendor release changes, regression impacts, API compatibility and configuration migration across environments.
D. Project team
Deliverable
Required information
Project scope and objectives
Replacement scope and business outcomes
High-level delivery roadmap
Target milestones and phases
Governance model
Client/vendor responsibilities and approvals
Stakeholder register
Business SMEs and technical owners
Resource availability
Client and vendor resource assumptions
RAID register
Risks, assumptions, issues and dependencies
Change management strategy
Business process and user adoption
Training requirements
User and administrator training
Cutover constraints
Migration windows and business blackout periods
Legacy retirement plan
Data retention, infrastructure shutdown and contract termination

3. Additional SaaS-specific deliverables that should not be missed
I would make these mandatory because they can materially affect implementation cost and ongoing operating cost.
Area
Required deliverable
Key questions
SaaS licensing
Licensing and subscription model
Per-user, per-transaction, per-module or consumption-based?
SaaS environments
Environment strategy
How many environments are included and what do additional environments cost?
Product releases
Release management model
How often are releases deployed?
Extensibility
Customisation and extension model
What can be configured without affecting upgrades?
API management
API limits and throttling
What are the transaction limits?
Data residency
Hosting and residency declaration
Where is client data stored and processed?
Security
SaaS security assurance pack
ISO 27001, SOC 2, penetration tests and certifications?
Identity
SSO and identity integration
Entra ID, MFA, federation and provisioning?
DR and BCP
SaaS resilience documentation
RTO, RPO and disaster recovery commitments?
Privacy
Privacy and data processing assessment
Subprocessors, data access and breach notification?
Exit strategy
SaaS exit and data portability plan
How can data be exported and the service terminated?
Operations
SaaS shared responsibility matrix
What does the vendor operate versus the client?
Service management
SLA and support model
Incident response, service availability and escalation?

For a New Zealand government or similarly regulated environment, also include information security classification, data sovereignty, privacy, protective security requirements and Certification and Accreditation (C&A) evidence.
4. Updated end-to-end backtracking diagram
This is the diagram I would use as the primary architecture and estimation governance artefact.
Tying It All Together: Integration PaaS in the Next-Gen Enterprise | EDUCAUSE Review
er.educause.edu
#chatgpt-mermaid-_r_1fn_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-_r_1fn_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_1fn_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-_r_1fn_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-_r_1fn_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-_r_1fn_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-_r_1fn_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-_r_1fn_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-_r_1fn_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-_r_1fn_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fn_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fn_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-_r_1fn_ p{margin:0;}#chatgpt-mermaid-_r_1fn_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ .cluster-label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ .cluster-label span{color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-_r_1fn_ .label text,#chatgpt-mermaid-_r_1fn_ span{fill:rgb(13, 13, 13);color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ .node rect,#chatgpt-mermaid-_r_1fn_ .node circle,#chatgpt-mermaid-_r_1fn_ .node ellipse,#chatgpt-mermaid-_r_1fn_ .node polygon,#chatgpt-mermaid-_r_1fn_ .node path{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .rough-node .label text,#chatgpt-mermaid-_r_1fn_ .node .label text,#chatgpt-mermaid-_r_1fn_ .image-shape .label,#chatgpt-mermaid-_r_1fn_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-_r_1fn_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .rough-node .label,#chatgpt-mermaid-_r_1fn_ .node .label,#chatgpt-mermaid-_r_1fn_ .image-shape .label,#chatgpt-mermaid-_r_1fn_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-_r_1fn_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-_r_1fn_ .root .anchor path{fill:rgb(143, 143, 143)!important;stroke-width:0;stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fn_ .arrowheadPath{fill:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fn_ .edgePath .path{stroke:rgb(143, 143, 143);stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .flowchart-link{stroke:rgb(143, 143, 143);fill:none;}#chatgpt-mermaid-_r_1fn_ .edgeLabel{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-_r_1fn_ .edgeLabel p{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-_r_1fn_ .edgeLabel rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-_r_1fn_ .labelBkg{background-color:rgba(252, 252, 252, 0.5);}#chatgpt-mermaid-_r_1fn_ .cluster rect{fill:rgb(243, 243, 243);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .cluster text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ .cluster span{color:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(243, 243, 243);border:1px solid rgba(0, 0, 0, 0.1);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-_r_1fn_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(13, 13, 13);}#chatgpt-mermaid-_r_1fn_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-_r_1fn_ .icon-shape,#chatgpt-mermaid-_r_1fn_ .image-shape{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-_r_1fn_ .icon-shape p,#chatgpt-mermaid-_r_1fn_ .image-shape p{background-color:rgb(252, 252, 252);padding:2px;}#chatgpt-mermaid-_r_1fn_ .icon-shape .label rect,#chatgpt-mermaid-_r_1fn_ .image-shape .label rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-_r_1fn_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-_r_1fn_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-_r_1fn_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node rect,#chatgpt-mermaid-_r_1fn_ [data-look="neo"].cluster rect,#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-_r_1fn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-_r_1fn_-gradient);stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-_r_1fn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-_r_1fn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fn_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-_r_1fn_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-_r_1fn_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(0, 79, 153);}#chatgpt-mermaid-_r_1fn_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(0, 79, 153);}#chatgpt-mermaid-_r_1fn_ .node tspan[font-weight="normal"],#chatgpt-mermaid-_r_1fn_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-_r_1fn_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .node rect,#chatgpt-mermaid-_r_1fn_ .node circle,#chatgpt-mermaid-_r_1fn_ .node ellipse,#chatgpt-mermaid-_r_1fn_ .node polygon,#chatgpt-mermaid-_r_1fn_ .node path{fill:rgb(229, 243, 255);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-_r_1fn_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-_r_1fn_ .mermaid-decision .label-container{fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-dasharray:2,2;}#chatgpt-mermaid-_r_1fn_ .edgePaths .flowchart-link{stroke:rgb(143, 143, 143);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-_r_1fn_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-_r_1fn_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}FINAL SAAS VENDOR COSTLicensing + Implementation +Migration + Integration +Testing + OperationsVendor Work BreakdownStructureEffort by Role, Timeline andDependenciesProduct Fit-Gap andConfigurationIntegration and TechnicalScopeData Migration ScopeSecurity, NFR and ComplianceTesting, Cutover and TransitionBusiness Requirements andProcessesCurrent-State Application andIntegration InventoryData Inventory, Quality andMappingSaaS Architecture andEnterprise ConstraintsTest Strategy and AcceptanceCriteriaProject Scope, Resources andDelivery ConstraintsBA TEAMTECHNICAL BACLIENT SOLUTION ARCHITECTTEST TEAMPROJECT TEAMCONSOLIDATED DISCOVERYPACKVENDOR VALIDATION ANDESTIMATION
5. Additional responsibility: Client versus SaaS vendor
I strongly recommend having a shared responsibility matrix as part of discovery.
Activity
Client
SaaS vendor
Business requirements
Accountable
Consulted
Product fit-gap
Consulted
Responsible
SaaS platform infrastructure
Informed
Responsible
SaaS configuration
Approves
Responsible
Custom extensions
Approves architecture
Responsible
Enterprise integration
Shared
Shared
Legacy data extraction
Responsible
Consulted
Data transformation and loading
Shared
Shared
SaaS platform security
Assesses
Responsible
Client identity integration
Responsible
Supports
UAT
Responsible
Supports
SaaS platform testing
Consulted
Responsible
Cutover
Shared
Shared
SaaS operations
Shared
Responsible
Business operations
Responsible
Supports
Legacy decommissioning
Responsible
Consulted

The actual allocation must be confirmed against the vendor contract and product operating model.
6. What I would ask the vendor to submit as the final estimation pack
I would make the following eight outputs mandatory:
SaaS Product Fit-Gap Assessment – standard functionality, configuration, extensions, customisations and unsupported requirements.
Solution Architecture – target SaaS architecture, integration architecture, security and operational model.
Implementation Scope and WBS – every implementation activity broken down into work packages.
Integration and Data Migration Estimate – individual complexity and effort for each interface and migration object.
Resource and Effort Estimate – person-days by role, activity and phase.
Implementation Roadmap – dependencies, milestones, critical path and delivery duration.
Commercial Cost Breakdown – subscription, implementation, optional costs, third-party costs and recurring operational costs.
Assumptions, Risks and Exclusions – estimation confidence, unresolved dependencies and potential additional costs.
My strongest recommendation: Do not ask the vendor for a single fixed implementation price immediately after discovery. Ask for a cost breakdown with three levels of confidence:
Confirmed: supported by detailed discovery evidence.
Provisional: based on reasonable assumptions.
Unestimated: requires further investigation or a proof of concept.
This protects the client from a low initial estimate followed by substantial change requests during implementation.
I would position your role as the Client SA around three gates: Discovery completeness → Architecture alignment → Estimation validation. These gates give you control over both the quality of the proposed SaaS solution and the credibility of the vendor's commercial estimate.






Give me the example diagrams I have to produce as client SA
Client Solution Architect – diagrams to produce for SaaS replacement
For replacing an existing on-premises application with a vendor-hosted SaaS solution, I would recommend producing 10 core architecture diagrams for the vendor discovery and estimation workshop.
Your diagrams should help the vendor understand three things:
What exists today.
What the future SaaS solution needs to look like.
What needs to change, integrate, migrate or be retired.
You do not need to produce detailed low-level designs at this stage. These should be discovery-level architecture diagrams, sufficient for the vendor to understand complexity and estimate effort.
1. Diagram catalogue – what you should produce
01
Current-State System Context Diagram
Existing on-prem application, users, external systems and interfaces.
Must have
02
Current-State Application Landscape
Applications, databases, middleware, infrastructure and dependencies.
Must have
03
Target SaaS Solution Context Diagram
Future SaaS platform and its interaction with enterprise systems.
Must have
04
Target SaaS Integration Architecture
API gateway, middleware, APIs, events, files and connectivity.
Must have
05
Data Migration Architecture
Legacy extraction, transformation, loading and reconciliation.
Must have
06
Identity and Security Architecture
SSO, MFA, identity federation, provisioning and trust boundaries.
Must have
07
Environment and Deployment Architecture
SaaS environments, client environments and release connectivity.
Must have
08
Non-Functional Requirements Architecture
Availability, resilience, DR, performance, monitoring and audit.
Must have
09
SaaS Operational Responsibility Diagram
Client versus SaaS provider responsibilities and service boundaries.
Recommended
10
Legacy Decommissioning and Transition Diagram
Migration, coexistence, cutover and retirement of on-prem components.
Recommended
I'll use a hypothetical claims-management SaaS replacement to demonstrate the diagrams. Replace the example system names with your actual systems.
2. Example diagrams
Diagram 1 – Current-State System Context
Priority 1
Purpose: Show the existing on-prem solution, who uses it and which systems communicate with it.

External SystemsClient On-Premises Data CentreCRMFinance / ERPIdentity ProviderPayment GatewayReporting PlatformLegacy Claims ApplicationClaims DatabaseDocument RepositoryClaims OfficersClaims ManagersCustomers / Partners
What to capture:
Users and external actors.
Existing application boundaries.
Database and document repository.
Upstream and downstream systems.
Main integration directions.
System ownership.
Estimation value: Helps identify the systems and interfaces that may be impacted by replacement.
Diagram 2 – Current-State Application Landscape
Priority 2
Purpose: Give the vendor an understanding of the technology complexity behind the existing application.
Infrastructure LayerData LayerIntegration LayerApplication LayerPresentation LayerVirtual MachinesOperating SystemsMonitoringBackup / DRRelational DatabaseDocument StoreData WarehouseEnterprise Service BusAPI GatewayMessage QueueLegacy Claims EngineWorkflow EngineBusiness Rules EngineBatch ProcessingWeb ApplicationCustomer Portal
What to capture:
Application components and modules.
Middleware and integration technology.
Database and document storage.
On-prem infrastructure dependencies.
Batch and scheduled processing.
Existing operational dependencies.
Estimation value: Helps identify functionality, middleware and infrastructure that need replacement, integration or retirement.
Diagram 3 – Target SaaS Solution Context
Priority 3
Purpose: Show how the future SaaS product fits into the client's enterprise ecosystem.
Vendor-Hosted SaaS PlatformClient EnterpriseSaaS User InterfaceClaims ManagementWorkflow and RulesDocument ManagementSaaS ReportingVendor Managed Data StoreEntra ID / IdentityEnterprise API GatewayIntegration PlatformCRMFinance SystemEnterprise ReportingInternal UsersCustomers / Partners
What to capture:
SaaS platform boundary and vendor ownership.
Client-owned integration components.
Enterprise identity provider.
Upstream and downstream systems.
Reporting and data consumers.
External user access, if applicable.
Estimation value: Establishes the target scope and identifies which existing components remain client-owned.
Diagram 4 – Target SaaS Integration Architecture
Priority 4
Purpose: This is one of the most important diagrams for cost estimation. Show how the SaaS solution communicates with enterprise and external systems.
Enterprise SystemsClient Integration BoundarySaaS PlatformCRMFinanceDocument ServicesData PlatformExternal Government ServicesAPI ManagementIntegration Services / iPaaSMessage BrokerSecure File TransferClaims SaaSSaaS REST APIsWebhooks / Events
What to capture:
API-based integration.
Event and webhook integration.
Batch and file-based integration.
Middleware and API gateway.
Authentication and certificates.
Error handling and retry.
Data direction and frequency.
Estimation value: Gives the vendor a basis for estimating each integration separately.
Diagram 5 – Data Migration Architecture
Priority 5
Purpose: Show how data moves from the on-prem application into SaaS.
Vendor SaaSMigration ServicesOn-Prem LegacyBulk Import / APIsSaaS Data StoreHistorical ArchiveData ExtractionStaging AreaData CleansingTransformation and MappingValidation and ReconciliationClaims DatabaseDocument RepositoryHistorical Records
What to capture:
Source databases and document repositories.
Data extraction method.
Data cleansing and transformation.
Field mapping.
Migration tooling.
SaaS bulk load or API capability.
Reconciliation and validation.
Historical data and archival approach.
Estimation value: Helps estimate migration objects, volumes, transformation complexity and migration cycles.
Diagram 6 – Identity and Security Architecture
Priority 6
Purpose: Show how users, administrators and system integrations authenticate and access the SaaS platform.
SaaS Provider Security BoundaryClient Security BoundarySAML / OIDC FederationRole-Based Access ControlAudit LoggingEncryption and KeyManagementMicrosoft Entra IDMFA / Conditional AccessPrivileged Access ManagementBusiness UsersSaaS AdministratorsIntegration Service Accounts
What to capture:
Single sign-on (SAML/OIDC).
MFA and conditional access.
Role-based access control.
Service accounts and API authentication.
Privileged access.
Audit logging.
Encryption and key management.
Estimation value: Helps identify identity integration, security configuration and compliance activities.
Diagram 7 – Environment and Deployment Architecture
Priority 7
Purpose: Show how the SaaS vendor provides environments and how client integration components are deployed and promoted.
Client ManagedSaaS Vendor ManagedDEV IntegrationSIT IntegrationUAT IntegrationPROD IntegrationRelease / Deployment PipelineDevelopment / ConfigurationSIT EnvironmentUAT EnvironmentProduction Environment
What to capture:
SaaS environment availability.
Number of environments included in subscription.
Configuration promotion approach.
Integration environment mapping.
Test data refresh approach.
Release management.
Production deployment approvals.
Estimation value: Identifies additional environment licensing, setup, deployment and release management effort.
Diagram 8 – Non-Functional Requirements Architecture
Priority 8
Purpose: Translate NFR requirements into architecture capabilities and vendor obligations.
SaaS ApplicationAvailabilityPerformanceSecurityDisaster RecoveryMonitoringAudit and LoggingAvailability SLAResponse Time / ThroughputEncryption / VulnerabilityManagementRTO / RPO / BackupHealth Monitoring / AlertsAudit Trails / Log Retention
What to capture:
NFR
Example requirement
Availability
99.9% or agreed SLA
Performance
Agreed response time under defined load
Scalability
Peak concurrent users and transaction volumes
DR
Defined RTO and RPO
Security
Encryption at rest and in transit
Audit
Defined retention and accessibility
Monitoring
Incident alerts and service health
Data residency
Approved data storage and processing locations

These are examples only, not recommended contractual targets. Agree actual values with business and security stakeholders.
Estimation value: Helps identify SaaS subscription tiers, additional services and compliance costs.
Diagram 9 – SaaS Shared Responsibility Architecture
Recommended
Purpose: Clarify what the SaaS vendor manages and what the client must manage.
Client ResponsibilitiesShared ResponsibilitiesSaaS Provider ResponsibilitiesBusiness ConfigurationApprovalUser Access GovernanceBusiness Data OwnershipUAT and AcceptanceBusiness Process ManagementEnterprise IntegrationOwnershipIdentity and AccessIntegration ManagementIncident ManagementSecurity MonitoringRelease CoordinationCloud InfrastructurePlatform AvailabilitySaaS Application MaintenanceProduct Patching andUpgradesPlatform Backup and DRPlatform Security
Estimation value: Prevents duplication of operational activities and makes ongoing support costs transparent.
Diagram 10 – Legacy Decommissioning and Transition Architecture
Recommended
Purpose: Explain the transition from the legacy application to SaaS, including coexistence and eventual retirement.
Legacy On-Prem ApplicationHistorical Data ExtractionData MigrationSaaS PlatformValidation and ReconciliationBusiness CutoverLegacy Read-Only / ArchiveLegacy DecommissioningTemporary coexistence
What to capture:
Data migration sequence.
Parallel running requirements.
Business cutover.
Historical access requirements.
Legacy read-only period.
Data retention and disposal.
Infrastructure shutdown and contract termination.
Estimation value: Identifies migration, coexistence, archival and decommissioning costs.
3. How I would package these diagrams for the vendor
I would create one architecture document called:
Client Solution Architecture – SaaS Replacement Discovery Pack
Section
Diagram
Priority
1
Current-State System Context
Mandatory
2
Current-State Application Landscape
Mandatory
3
Target SaaS Solution Context
Mandatory
4
Target SaaS Integration Architecture
Mandatory
5
Data Migration Architecture
Mandatory
6
Identity and Security Architecture
Mandatory
7
Environment and Deployment Architecture
Mandatory
8
NFR Architecture
Mandatory
9
Shared Responsibility Architecture
Recommended
10
Legacy Decommissioning and Transition
Recommended

4. What level of detail should you produce?
Do not spend time producing detailed technical designs before the vendor discovery. Use these levels:
Diagram
Recommended detail
Current-state context
L1 – System context
Application landscape
L2 – Application components
Target SaaS context
L1 – System context
Integration architecture
L2 – Logical integration
Data migration
L2 – Migration flow
Security architecture
L2 – Logical security
Environment architecture
L2 – Environment topology
NFR architecture
L2 – Quality attributes
Shared responsibility
Conceptual
Decommissioning
Conceptual transition

5. My recommended order of production
As Client SA, I would create the diagrams in this order because each informs the next.
Current-State System Context
Establish what exists and what is being replaced.
Current-State Application Landscape
Understand the technical dependencies and legacy complexity.
Target SaaS Solution Context
Establish the future solution boundary and enterprise ecosystem.
Target Integration Architecture
Identify the interfaces that must be built or changed.
Data Migration Architecture
Establish migration complexity and legacy data dependencies.
Security and NFR Architecture
Establish the SaaS security and operational constraints.
Environment and Deployment Architecture
Identify environment, release and connectivity requirements.
Responsibility and Transition Diagrams
Establish operational ownership and retirement approach.
One important distinction: Your target SaaS architecture diagram is a client-level conceptual architecture, not the vendor's final solution design. Ask the vendor to validate it, identify gaps and produce the detailed target architecture as part of their proposal.
My suggestion is to maintain these diagrams in Visio using consistent shapes, colour coding and identifiers. Give every system, interface and component an ID (e.g. SYS-001, INT-001, DATA-001). Reuse those IDs in the integration catalogue, migration inventory and estimation workbook. This gives you end-to-end traceability from architecture to vendor cost.

