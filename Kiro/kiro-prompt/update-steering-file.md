Update the existing Kiro steering file to incorporate an AI-assisted development workflow with mandatory human approval gates. Preserve all existing project-specific standards, coding conventions, architectural guidance, and technology-specific rules. Extend the steering file instead of replacing it.

Add the following guidance:

## AI-Assisted Development Workflow

Introduce a four-phase workflow that all feature development and specification-driven changes must follow.

### Phase 1 – Specification Analysis

When a specification changes, the AI must:

* Compare the updated specification with the previous version.
* Summarize the functional differences.
* Identify all impacted areas including:

  * frontend screens
  * backend services
  * APIs
  * database schema
  * integrations
  * tests
* Produce an implementation impact report before making code changes.
* Clearly state any assumptions or ambiguities.

The AI should not begin implementation until the specification has been analyzed.

---

### Phase 2 – Design Review (Required for UI Changes)

If any change affects the user interface, user experience, workflows, navigation, layouts, forms, components, responsive behavior, or accessibility, the AI must stop implementation and produce a design proposal.

The proposal should include:

* impacted screens
* user flow changes
* affected components
* wireframes or mockups when supported
* visual diff summary
* accessibility considerations
* responsive design considerations

The AI must explicitly request human approval from a Product Owner, Designer, or UX reviewer before modifying frontend code.

UI implementation must not proceed without approval.

---

### Phase 3 – Implementation

After approval, implement only the approved changes.

The AI should:

* minimize unrelated code changes
* preserve existing architecture
* reuse existing components
* follow project coding standards
* follow the established design system
* avoid creating duplicate components
* avoid introducing new design patterns without approval
* document any implementation decisions that differ from the approved design

---

### Phase 4 – Validation

Before considering work complete, the AI must verify:

Functional Quality

* unit tests
* integration tests
* API tests

Code Quality

* linting
* formatting
* static analysis

Accessibility

* keyboard navigation
* focus order
* semantic HTML
* ARIA compliance
* color contrast

Visual Quality

* visual regression tests
* responsive layouts
* consistency with the design system

The AI should provide a validation summary before requesting merge approval.

---

## Human Approval Gates

Add explicit rules stating that the AI must pause and request human approval whenever changes involve:

* UI or UX
* navigation
* workflows
* design system modifications
* reusable UI components
* accessibility behavior
* security-sensitive functionality
* authentication or authorization
* public APIs
* database schema
* architectural changes

The steering should make it clear that these changes require review before implementation or merge.

---

## Pull Request Expectations

Require AI-generated pull requests to include:

* specification summary
* impacted components
* impacted backend services
* files changed
* testing performed
* accessibility results
* visual regression results
* assumptions
* known risks

---

## Definition of Done

Update the Definition of Done to require:

* specification implemented
* design approval completed (when UI changes exist)
* coding standards followed
* tests passing
* accessibility validated
* visual regression completed
* documentation updated
* required human approvals obtained before merge

---

Do not remove or overwrite any existing steering content. Merge these workflow rules into the appropriate sections of the current steering file, maintaining the existing structure and avoiding duplication. If similar guidance already exists, enhance it rather than creating redundant sections.
