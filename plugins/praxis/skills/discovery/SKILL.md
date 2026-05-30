---
name: discovery
description: Design before code. Runs the Discovery state machine (clarify → model → architecture → slice) to produce issues in plan.md. Use when designing a new project, feature, or system.
---

# Discovery

Design before code. This skill runs a deterministic state machine that produces well-defined issues in `plan.md`.

## Communication

Explain concepts to the user using business language — workflows, rules, responsibilities, integrations. Avoid jargon. Use analogies when helpful.

**The plan document is a technical artifact and always uses precise technical language.** Only the conversational explanations and summaries presented to the user use business language.

## Language

- **All artifacts** (plan.md, issues, code, comments, commit messages) must be written in **English**.
- **Chat with the user** must be in the **same language the user uses**. Mirror the user's language.

## State Machine

```
idle → clarify → clarify_review → model → model_review → architecture → architecture_review → slice → idle
```

## Steps

| Step                  | Skill                  | What to do                                           |
| --------------------- | ---------------------- | ---------------------------------------------------- |
| clarify               | praxis:collaborative-design  | Understand the problem space through visual scenarios|
| clarify_review        | praxis:complexity-review     | Challenge and simplify what was clarified            |
| model                 | praxis:event-modeling        | Map behavior as events, commands, views, and slices  |
| model_review          | praxis:complexity-review     | Challenge and simplify the model                     |
| architecture          | praxis:backend-architecture / praxis:frontend-architecture | Define domain boundaries, ports, and adapters        |
| architecture_review   | praxis:complexity-review     | Challenge and simplify the architecture              |
| slice                 | praxis:collaborative-design  | Break work into vertical slices with dependencies    |

## How to Run

1. **Setup**: Ensure you are on `main` with a clean working tree (`git status` → no uncommitted changes, `git pull` to update). Extract a name and description from the user's request. If `plan.md` already exists, overwrite it. Create `plan.md` using the template below (frontmatter starts with `state: clarify`).
2. **Execute each step**:
   - Use the Skill tool to invoke the skill listed for the current step (e.g., `skill: "praxis:collaborative-design"`). This is MANDATORY — do NOT attempt to perform the step yourself without loading the sub-skill first. The sub-skill contains specific methodology, formats, and checklists that must be followed.
   - Present a summary to the user and **wait for confirmation** before moving on.
   - Write the step output to the corresponding section in the plan document.
   - Update `state` in the frontmatter to the next step.
3. **Open questions**: When something is unclear or a tradeoff needs a decision:
   - Assign an ID (OQ-1, OQ-2, ...).
   - Record it in the Open Questions section of the plan document with: text, context, options, tradeoffs, and recommendation.
   - **A step CANNOT be completed while it has unresolved open questions.**
   - Present open questions one at a time.
   - **When resolving**: Keep the original question intact (text, context, options, tradeoffs, recommendation). Add a `**Resolution**` field with the decision and a `**Status**: resolved` field. **Never delete or overwrite the original content** — the history of what was considered matters.
   - **Propagate implications**: After resolving a question, review the entire plan document and update all sections affected by the decision (e.g., if a question resolves a modeling choice, update Step 2; if it changes a boundary, update Step 3). This ensures the plan stays consistent.
4. **Create issues**: When you reach the `slice` step and slices are confirmed, add each issue to the `## Issues` section of the plan document using the issue template below.
5. **Done**: After issues are added to the plan, update `state: idle` in the frontmatter.

## State Tracking

State is tracked in the first lines of `plan.md` as YAML frontmatter:

```yaml
---
state: clarify          # current step in the state machine
type: discovery         # "discovery" or "implementation"
---
```

**How to update state**: Edit the frontmatter directly in `plan.md` whenever you transition to a new step or start implementation.

## State Transition Protocol

Before doing any work in a step, follow this protocol:

1. **Read current state**: Read `state` from plan.md frontmatter.
2. **Advance one step only**: Update `state` to the **immediately next** step in the state machine. Never jump ahead.
3. **Print progress**: Show the user the current position:
   ```
   ▶ step_name (N/total) — Remaining: step1 → step2 → ... → idle
   ```
4. **Skip protocol**: If a step does not apply, do NOT skip silently. Instead:
   - Print: `⏭ step_name — Skip reason: {reason}`
   - Auto-advance to the next step immediately. Do not wait for confirmation on skips.
5. **Architecture is mandatory**: Always invoke the architecture skills (`praxis:backend-architecture` for backend, `praxis:frontend-architecture` for frontend) even when the code is simple. The goal is to set a precedent of organized code from the start. Never skip architecture steps citing simplicity.

## Plan Document Template

Create at `plan.md`:

```markdown
---
state: clarify
type: discovery
---

# {name}

{description}

## Step 1: Clarify

## Step 2: Model
### Aggregates
### Slices

## Step 3: Architecture
### Ports
### Adapters

## Step 4: Slice
### MVP
### Slice map

## Open Questions
<!-- Use this format for each question:
### OQ-{N}: {title}
**Status**: open | resolved
**Step**: {step where it arose}
**Text**: {the question}
**Context**: {why this matters}
**Options**:
1. {option A} — {tradeoff}
2. {option B} — {tradeoff}
**Recommendation**: {recommended option and why}
**Resolution**: {decision taken — added when resolved}
-->

## Complexity Challenges
<!-- Use this format for each challenge:
### CD-{N}: {Dimension name} — {one-line challenge}
**Status**: Open | Resolved
**Dimension**: #{number} — {dimension name}
**Challenge**: {What assumption is being questioned? What seems over-engineered?}
**Context**: {Why this matters for this specific proposal}
**Options**:
1. {simpler alternative} — {tradeoff}
2. {proposed approach} — {tradeoff}
**Resolution**: {How it was resolved — which option was chosen and why}
-->

## Issues
```

## Issue Template (within the plan document)

Add each issue as a subsection under `## Issues`, numbered sequentially:

```markdown
### Issue {NN}: {title}

**Status**: pending

**What**: {description}

**Acceptance Criteria**: {acceptanceCriteria}

**Specs**: {specs}

**Context**: {context}

**Blocked by**: {blockedBy or "none"}
```

## Rules

- **Wait for user confirmation** before advancing only when there are open questions or decisions needed. Auto-advance when a step completes cleanly or is skipped.
- **Never skip steps.** Follow the state machine order exactly. Use the skip protocol when a step does not apply.
- **Open questions block progress.** Resolve all before completing a step.
- **Issues can only be created during the `slice` step.**
- **Everything lives in `plan.md` at the project root** — plan, open questions, and issues in one document.
