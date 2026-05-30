---
name: discovery
description: Design before code. Runs the Discovery state machine (clarify → model → architecture → slice) to produce a spec folder under docs/specs/<timestamp_slug>/. Use when designing a new project, feature, or system.
---

# Discovery

Design before code. This skill runs a deterministic state machine that produces a **spec folder** under `docs/specs/<timestamp_slug>/` containing `SPEC.md`, `metadata.json`, and one file per issue.

## Communication

Explain concepts to the user using business language — workflows, rules, responsibilities, integrations. Avoid jargon. Use analogies when helpful.

**The spec artifacts are technical and always use precise technical language.** Only the conversational explanations and summaries presented to the user use business language.

## Language

- **All artifacts** (`SPEC.md`, `metadata.json`, issue files, code, comments, commit messages) must be written in **English**.
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

## Spec Folder Layout

Everything lives under one folder per spec:

```
docs/specs/<timestamp_slug>/
├── metadata.json          # single source of truth: state (phases as ISO timestamps) + issue registry
├── SPEC.md                # design document: clarify, model, architecture, slice, open questions, complexity challenges
├── ISSUE-01-<slug>.md     # one file per issue — content only
├── ISSUE-02-<slug>.md
└── ...
```

- **`metadata.json`** is the single source of truth for state and issue status/phases. Do not duplicate status inside the markdown files.
- **`SPEC.md`** and the **issue files** hold content only.

## How to Run

1. **Setup**:
   - Ensure you are on `main` with a clean working tree (`git status` → no uncommitted changes, `git pull` to update).
   - Extract a `name` and `description` from the user's request.
   - **Generate the slug** (see below) and create the directory `docs/specs/<timestamp_slug>/` (create parent dirs if needed).
   - Each discovery run creates a **new** spec folder. Never overwrite or extend an existing spec — new functionality is always a new spec.
   - Write `SPEC.md` from the template below and `metadata.json` with all discovery phases set to `null` and `issues` empty, then set the `clarify` phase to the current ISO 8601 timestamp once the clarify step begins.
2. **Execute each step**:
   - Use the Skill tool to invoke the skill listed for the current step (e.g., `skill: "praxis:collaborative-design"`). This is MANDATORY — do NOT attempt to perform the step yourself without loading the sub-skill first. The sub-skill contains specific methodology, formats, and checklists that must be followed.
   - Present a summary to the user and **wait for confirmation** before moving on.
   - Write the step output to the corresponding section in `SPEC.md`.
   - Set the step's phase to the current ISO 8601 timestamp in `metadata.json`.
3. **Open questions**: When something is unclear or a tradeoff needs a decision:
   - Assign an ID (OQ-1, OQ-2, ...).
   - Record it in the Open Questions section of `SPEC.md` with: text, context, options, tradeoffs, and recommendation.
   - **A step CANNOT be completed while it has unresolved open questions.**
   - Present open questions one at a time.
   - **When resolving**: Keep the original question intact (text, context, options, tradeoffs, recommendation). Add a `**Resolution**` field with the decision and a `**Status**: resolved` field. **Never delete or overwrite the original content** — the history of what was considered matters.
   - **Propagate implications**: After resolving a question, review the whole of `SPEC.md` and update all sections affected by the decision (e.g., if a question resolves a modeling choice, update the Model section; if it changes a boundary, update Architecture). This keeps the spec consistent.
4. **Create issues**: When you reach the `slice` step and slices are confirmed, for each issue:
   - Create a file `ISSUE-NN-<slug>.md` in the spec folder using the issue template below (numbered sequentially, slug derived from the issue title).
   - Add an entry to the `issues` object in `metadata.json` keyed by `ISSUE-NN` with `title`, `file`, `status: "pending"`, `blocked_by`, and a `phases` object with every implementation phase set to `null`.
5. **Done**: After all issues are created and registered, every discovery phase in `metadata.json` has a timestamp. The spec is ready for implementation.

## Slug Generation

- Get the current Unix timestamp in seconds (`date +%s`).
- Build the slug from `name`:
  - Convert to lowercase.
  - Replace spaces and consecutive whitespace with a single hyphen `-`.
  - Remove all characters except lowercase letters, digits, and hyphens.
  - Remove leading/trailing hyphens and collapse consecutive hyphens into one.
- Combine as `<timestamp>_<slug>`.
- If a folder with the same slug already exists, append a counter: `<timestamp>_<slug>-2`, then `-3`, etc.

## State Tracking

State lives in `metadata.json`, not in frontmatter. Each phase is `null` until complete, then holds an ISO 8601 timestamp.

```json
{
  "name": "<project name>",
  "description": "<short description>",
  "slug": "<timestamp_slug>",
  "created": "<ISO 8601 timestamp>",
  "discovery": {
    "clarify": null,
    "clarify_review": null,
    "model": null,
    "model_review": null,
    "architecture": null,
    "architecture_review": null,
    "slice": null
  },
  "issues": {}
}
```

After the `slice` step, `issues` is populated:

```json
"issues": {
  "ISSUE-01": {
    "title": "Login form",
    "file": "ISSUE-01-login-form.md",
    "status": "pending",
    "blocked_by": [],
    "phases": {
      "understand": null,
      "scout": null,
      "architecture": null,
      "tdd": null,
      "simplify": null,
      "test_quality": null,
      "complexity": null,
      "spec": null,
      "commit": null
    }
  }
}
```

**How to determine the current step**: the current discovery step is the first phase in `discovery` whose value is `null`. When all discovery phases have timestamps, discovery is complete (`idle`).

**How to update state**: edit `metadata.json` directly, setting the relevant phase to the current timestamp whenever you complete a step.

## State Transition Protocol

Before doing any work in a step, follow this protocol:

1. **Read current state**: read `metadata.json` and find the first `null` phase under `discovery`.
2. **Advance one step only**: complete the current step and set its phase to the current timestamp. Never jump ahead.
3. **Print progress**: show the user the current position:
   ```
   ▶ step_name (N/total) — Remaining: step1 → step2 → ... → idle
   ```
4. **Skip protocol**: if a step does not apply, do NOT skip silently. Instead:
   - Print: `⏭ step_name — Skip reason: {reason}`
   - Set the phase timestamp and auto-advance immediately. Do not wait for confirmation on skips.
5. **Architecture is mandatory**: Always invoke the architecture skills (`praxis:backend-architecture` for backend, `praxis:frontend-architecture` for frontend) even when the code is simple. The goal is to set a precedent of organized code from the start. Never skip architecture steps citing simplicity.

## SPEC.md Template

Create at `docs/specs/<timestamp_slug>/SPEC.md`:

```markdown
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
```

## metadata.json Template

Create at `docs/specs/<timestamp_slug>/metadata.json`:

```json
{
  "name": "{name}",
  "description": "{description}",
  "slug": "{timestamp_slug}",
  "created": "{ISO 8601 timestamp}",
  "discovery": {
    "clarify": null,
    "clarify_review": null,
    "model": null,
    "model_review": null,
    "architecture": null,
    "architecture_review": null,
    "slice": null
  },
  "issues": {}
}
```

## Issue File Template

Create each issue as its own file `docs/specs/<timestamp_slug>/ISSUE-NN-<slug>.md`. The file holds **content only** — status and phases live in `metadata.json`.

```markdown
# ISSUE-NN: {title}

## What
{description}

## Acceptance Criteria
{acceptanceCriteria}

## Specs
{specs}

## Context
{context}

## Blocked by
{blockedBy or "none"}
```

## Rules

- **Wait for user confirmation** before advancing only when there are open questions or decisions needed. Auto-advance when a step completes cleanly or is skipped.
- **Never skip steps.** Follow the state machine order exactly. Use the skip protocol when a step does not apply.
- **Open questions block progress.** Resolve all before completing a step.
- **Issues can only be created during the `slice` step.**
- **Everything lives in `docs/specs/<timestamp_slug>/`** — `SPEC.md`, `metadata.json`, and one file per issue, in one folder.
- **`metadata.json` is the single source of truth** for state and issue status — never track status in the markdown files.
