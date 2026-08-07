# AI-Assisted Development Workflow Steering

## Purpose

This steering document defines the mandatory workflow for AI-assisted software development. The objective is to accelerate implementation while ensuring product quality, user experience, accessibility, and architectural consistency through human oversight.

This workflow applies to all feature development, enhancements, and specification updates.

---

# Development Principles

The AI assistant shall:

* Treat the specification as the primary source of truth.
* Never assume UI or UX intent beyond what is described in the specification.
* Prefer incremental, reviewable changes over large autonomous modifications.
* Clearly communicate assumptions and impacted areas before implementation.
* Produce changes that are traceable back to specification requirements.

---

# Phase 1 — Specification Analysis

## Objective

Determine exactly what has changed and identify the impact across the system.

### AI Responsibilities

When a specification changes, the AI must:

1. Compare the updated specification with the previous version.
2. Summarize the functional differences.
3. Identify:

   * affected features
   * affected APIs
   * affected database objects
   * affected UI screens
   * affected services
   * affected integrations
4. Produce an implementation impact report.

Example:

```text
Specification Changes

✓ User authentication now supports Google OAuth

Affected Areas

Frontend
- Login Page
- Authentication Context

Backend
- Auth Controller
- OAuth Service
- User Model

Infrastructure
- Environment Variables
- OAuth Secrets

Tests
- Authentication Integration Tests
```

### Human Responsibilities

Product Owner or Technical Lead reviews:

* correctness of interpretation
* completeness of impacted areas
* implementation scope

No implementation begins until the impact report is accepted.

---

# Phase 2 — Design Review (Mandatory for UI Changes)

## Objective

Ensure all user experience decisions receive explicit human approval before implementation.

This phase is required whenever changes affect:

* screens
* layouts
* navigation
* workflows
* user interactions
* accessibility
* responsive behavior
* component appearance
* design system usage

## AI Responsibilities

Before modifying frontend code, the AI must generate:

* affected screens
* updated user flow
* wireframes or mockups (where supported)
* component hierarchy
* visual diff summary
* accessibility considerations
* responsive design considerations

Example:

```text
UI Proposal

Order Details Screen

+ Add "Cancel Order" button

Confirmation Dialog

Title:
Cancel Order?

Buttons:
Cancel
Confirm

Status Badge

Pending → Cancelled

Accessibility

✓ Keyboard navigation
✓ Screen reader labels
✓ Focus management
```

The AI must stop after presenting the proposal.

No frontend implementation shall begin without approval.

---

## Human Responsibilities

Designer, Product Owner, or UX Lead must review:

* usability
* interaction flow
* wording
* accessibility
* consistency with design system

Approval is required before implementation.

---

# Phase 3 — Implementation

## Objective

Implement approved functionality while maintaining engineering quality.

### AI Responsibilities

The AI shall:

* implement only approved changes
* minimize unrelated modifications
* preserve existing architecture
* follow project coding standards
* reuse existing components
* avoid introducing duplicate UI components
* follow naming conventions
* update documentation where necessary

If implementation differs from the approved design, the AI must explain why.

---

# Design System Rules

The AI shall:

* reuse existing design tokens
* reuse existing components
* avoid introducing new colors
* avoid introducing new typography
* avoid changing spacing rules
* avoid creating new patterns without approval

New reusable components require human review.

---

# Backend Rules

The AI shall:

* preserve API compatibility where possible
* document breaking changes
* update migrations safely
* update API documentation
* update tests

---

# Phase 4 — Validation

## Objective

Verify that the implementation satisfies functional, visual, and accessibility requirements.

### AI Responsibilities

Before considering work complete, the AI shall verify:

### Functional

* unit tests
* integration tests
* API tests

### Quality

* linting
* formatting
* static analysis

### Accessibility

* keyboard navigation
* focus order
* semantic HTML
* color contrast
* ARIA attributes

### Visual

* visual regression tests
* responsive layouts
* design consistency

The AI shall summarize validation results.

Example:

```text
Validation Summary

Unit Tests
✓ Passed

Integration Tests
✓ Passed

Accessibility
✓ Passed

Visual Regression
✓ No unexpected changes

Responsive Layout
✓ Mobile
✓ Tablet
✓ Desktop
```

---

# Human Review Requirements

The following changes require mandatory human approval:

| Change Type        | Required Reviewer |
| ------------------ | ----------------- |
| UX Flow            | Product Owner     |
| Visual Design      | Designer          |
| Accessibility      | UX or QA          |
| Architecture       | Tech Lead         |
| Database Schema    | Tech Lead         |
| Security           | Security Reviewer |
| Public API Changes | Engineering Lead  |

---

# Pull Request Requirements

Every AI-generated pull request must include:

## Specification Summary

* What changed

## Files Modified

* Complete list

## UI Impact

* Screens changed
* Components changed

## Backend Impact

* APIs
* Database
* Services

## Testing

* Unit Tests
* Integration Tests
* Accessibility
* Visual Regression

## Risks

* Known limitations
* Assumptions
* Follow-up work

---

# Human-in-the-Loop Policy

The AI must pause and request review when:

* UI changes are proposed.
* User workflows change.
* Navigation changes.
* New reusable components are introduced.
* Accessibility behavior changes.
* Security-sensitive functionality changes.
* Database schemas change.
* Public APIs change.

Implementation may continue only after explicit approval.

---

# Definition of Done

A feature is complete only when:

* Specification changes are implemented.
* Design approval has been obtained (if applicable).
* Code follows project standards.
* Tests pass.
* Accessibility checks pass.
* Visual regression checks pass.
* Documentation is updated.
* Human reviewers approve the changes.

No feature shall be considered complete solely because the AI has generated code.
