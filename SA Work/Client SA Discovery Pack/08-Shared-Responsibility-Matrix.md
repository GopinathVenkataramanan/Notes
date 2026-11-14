# 08: Shared Responsibility Matrix

| Field | Value |
|---|---|
| Owner | Client Solution Architect (with Project and Service Management) |
| Audience | SaaS vendor |
| Status | Draft v0.1 |
| Related | Diagram 09 SaaS Shared Responsibility, [06 Operations](06-SaaS-Operational-Requirements.md) |

## 1. Purpose

This matrix makes explicit who does what, both during implementation and in ongoing operation. It prevents gaps and duplicated effort, and makes support costs transparent.

> The final allocation must be confirmed against the vendor contract and the product operating model. The vendor must state any disagreement in their response.

## 2. Responsibility summary (from diagram 09)

| Client | Shared | SaaS provider |
|---|---|---|
| Business configuration approval | Enterprise integration ownership | Cloud infrastructure |
| User access governance | Identity and access | Platform availability |
| Business data ownership | Integration management | SaaS application maintenance |
| UAT and acceptance | Incident management | Product patching and upgrades |
| Business process management | Security monitoring | Platform backup and DR |
| | Release coordination | Platform security |

## 3. Implementation responsibilities

Key: Responsible = does the work · Accountable = owns the outcome · Consulted · Informed · Approves · Supports · Shared

| Activity | Client | SaaS vendor | Notes / to confirm |
|---|---|---|---|
| Business requirements | Accountable | Consulted | |
| Product fit-gap | Consulted | Responsible | Uses the BA Product Fit-Gap Matrix |
| SaaS platform infrastructure | Informed | Responsible | |
| SaaS configuration | Approves | Responsible | |
| Custom extensions | Approves architecture | Responsible | Client design authority |
| Enterprise integration | Shared | Shared | Client builds the iPaaS/API gateway side. Vendor provides APIs/events and support |
| Legacy data extraction | Responsible | Consulted | |
| Data transformation and loading | Shared | Shared | Split to be confirmed per migration object |
| SaaS platform security | Assesses | Responsible | |
| Client identity integration | Responsible | Supports | |
| SaaS platform testing | Consulted | Responsible | |
| System integration testing | Shared | Shared | |
| UAT | Responsible | Supports | |
| Cutover | Shared | Shared | Joint cutover plan |
| Training (end users) | Responsible | Supports | Train-the-trainer by the vendor *(example)* |
| Legacy decommissioning | Responsible | Consulted | |

## 4. Run / BAU responsibilities

| Activity | Client | SaaS vendor | Notes / to confirm |
|---|---|---|---|
| SaaS operations (hosting, availability, capacity) | Informed | Responsible | |
| Product patching and upgrades | Informed / regression tests | Responsible | |
| Platform backup and DR | Informed | Responsible | Client may request a restore |
| Platform security (infrastructure, application) | Assesses | Responsible | |
| Security monitoring | Shared | Shared | Vendor monitors the platform. Client SOC monitors forwarded logs |
| Incident management | Shared | Shared | Client service desk is first contact for users |
| Integration management and monitoring | Responsible (client side) | Responsible (SaaS side) | |
| User access governance and recertification | Responsible | Supports | |
| Business configuration changes | Approves / Responsible *(example)* | Supports | Depends on admin capability |
| Release coordination and regression | Shared | Shared | |
| Business operations | Responsible | Supports | |
| Business data ownership and quality | Responsible | Informed | |
| Licence management | Responsible | Supports | |

## 5. Vendor response required

Confirm or propose changes for each row, identify any activities that carry additional charges, and state the vendor roles that perform each responsibility.
