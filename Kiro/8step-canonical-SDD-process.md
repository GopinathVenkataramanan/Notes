A canonical **Spec-Driven Development (SDD)** workflow organizes software delivery around an executable, evolving specification rather than around code alone. While organizations implement SDD differently, a robust workflow can be described in **eight phases**, separated by **phase gates** and connected by **feedback loops**.

```text
Vision
   │
   ▼
[1] Problem Definition
   │ Gate 1
   ▼
[2] Requirements Specification
   │ Gate 2
   ▼
[3] System Design
   │ Gate 3
   ▼
[4] Specification Validation
   │ Gate 4
   ▼
[5] Implementation
   │ Gate 5
   ▼
[6] Verification & Testing
   │ Gate 6
   ▼
[7] Deployment & Release
   │ Gate 7
   ▼
[8] Operations & Evolution
   │
   └───────────────┐
                   ▼
          Continuous Feedback
```

## Phase 1: Problem Definition

### Purpose

Clearly define the business or technical problem before designing a solution.

### Activities

* Stakeholder interviews
* Business goals
* User research
* Constraints
* Success metrics
* Risk identification

### Deliverables

* Vision statement
* Problem statement
* Success criteria
* Stakeholder map

### Phase Gate 1

Questions:

* Is the problem clearly understood?
* Is scope agreed?
* Are objectives measurable?

If **No**, iterate.

---

## Phase 2: Requirements Specification

### Purpose

Convert goals into precise, testable specifications.

### Activities

Functional requirements

Example:

> Users shall reset passwords.

Non-functional requirements

Examples:

* latency
* availability
* security
* scalability

Acceptance criteria

Edge cases

Business rules

Data contracts

API contracts

### Deliverables

* Software Requirements Specification (SRS)
* User stories
* Use cases
* Domain model
* Acceptance criteria

### Phase Gate 2

Requirements must be:

* complete
* consistent
* testable
* traceable
* unambiguous

---

## Phase 3: System Design

### Purpose

Transform specifications into architecture.

### Activities

Architecture

Component decomposition

Data model

API design

State machines

Sequence diagrams

Technology decisions

Security design

### Deliverables

* Architecture specification
* Interface specifications
* Database schema
* Design diagrams

### Phase Gate 3

Review for:

* feasibility
* maintainability
* scalability
* compliance
* risk

---

## Phase 4: Specification Validation

### Purpose

Verify the specification before implementation begins.

### Activities

Specification reviews

Model checking

Simulation

Prototyping

Stakeholder walkthroughs

Requirement traceability

Formal verification (where applicable)

### Deliverables

* Approved specification
* Review findings
* Risk register updates

### Phase Gate 4

Questions

Can every requirement be:

* implemented?
* tested?
* traced?
* validated?

If not:

Return to Requirements or Design.

---

## Phase 5: Implementation

### Purpose

Write code that conforms to the specification.

### Activities

Coding

Code generation

Code reviews

Static analysis

Documentation

Continuous integration

### Deliverables

* Source code
* Build artifacts
* Internal documentation

### Phase Gate 5

Verify

* Coding standards
* Build passes
* Static analysis passes
* Specification traceability maintained

---

## Phase 6: Verification & Testing

### Purpose

Ensure implementation satisfies the specification.

### Testing Pyramid

* Unit tests
* Integration tests
* System tests
* Acceptance tests
* Performance tests
* Security tests
* Regression tests

### Activities

Automated testing

Manual testing

Coverage analysis

Requirements traceability matrix

Defect analysis

### Deliverables

* Test reports
* Coverage reports
* Defect log
* Validation report

### Phase Gate 6

Questions

Does every requirement pass?

Are critical defects resolved?

If no:

Return to Implementation.

---

## Phase 7: Deployment & Release

### Purpose

Safely release the validated system.

### Activities

Release planning

Infrastructure provisioning

Migration

Canary deployment

Blue/green deployment

Rollback planning

Monitoring setup

Documentation

### Deliverables

* Release package
* Deployment guide
* Release notes
* Operational runbooks

### Phase Gate 7

Verify

* deployment succeeds
* monitoring active
* rollback tested
* stakeholders approve release

---

## Phase 8: Operations & Evolution

### Purpose

Operate the software while continuously improving both the product and its specifications.

### Activities

Production monitoring

Incident management

Performance optimization

Customer feedback

Requirement updates

Technical debt reduction

Specification evolution

### Deliverables

* Operational metrics
* Incident reports
* Updated specifications
* Product roadmap

---

# Phase Gates

Phase gates are formal decision points that ensure quality before proceeding.

| Gate   | Review Focus             | Outcome                  |
| ------ | ------------------------ | ------------------------ |
| Gate 1 | Problem understood       | Continue or redefine     |
| Gate 2 | Requirements quality     | Approve SRS              |
| Gate 3 | Design quality           | Approve architecture     |
| Gate 4 | Specification validation | Ready for implementation |
| Gate 5 | Code quality             | Ready for testing        |
| Gate 6 | Verification complete    | Ready for release        |
| Gate 7 | Operational readiness    | Production deployment    |

---

# Feedback Loops

Spec-driven development is iterative rather than strictly linear. Typical feedback loops include:

| From              | To                 | Reason                             |
| ----------------- | ------------------ | ---------------------------------- |
| Testing           | Implementation     | Fix defects                        |
| Implementation    | Design             | Design issue discovered            |
| Design            | Requirements       | Missing or conflicting requirement |
| Operations        | Requirements       | New business needs                 |
| Monitoring        | Design             | Performance improvements           |
| Customer feedback | Problem Definition | Reassess goals                     |
| Security review   | Design             | Threat mitigation                  |
| Compliance audit  | Requirements       | Regulatory updates                 |

---

# End-to-End Traceability

A hallmark of mature SDD is maintaining traceability from business goals to operational outcomes:

```text
Business Goal
      │
      ▼
Requirement
      │
      ▼
Design Element
      │
      ▼
Implementation
      │
      ▼
Test Case
      │
      ▼
Deployment
      │
      ▼
Production Metric
      │
      ▼
User Feedback
      │
      └──────────────► Updated Requirement
```

This enables every requirement to be linked to corresponding design decisions, implementation artifacts, test cases, deployment records, and operational metrics, making changes easier to assess and validate over the software's lifecycle.

### Key principles

* **Specifications are the primary source of truth**, with code implementing rather than defining system behavior.
* **Phase gates** provide structured quality checkpoints before advancing.
* **Feedback loops** enable continuous refinement based on validation, implementation discoveries, and operational experience.
* **End-to-end traceability** connects requirements through design, code, testing, deployment, and production, supporting governance, impact analysis, and continuous improvement.
