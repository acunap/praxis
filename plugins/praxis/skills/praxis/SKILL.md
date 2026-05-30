---
name: praxis
description: Design before code, then build with TDD — one end-to-end workflow. Runs a single deterministic state machine (discovery → implementation) whose current step is always derived from docs/specs/<timestamp_slug>/metadata.json. Use when designing or building any new project, feature, or system.
---

# Praxis

One end-to-end workflow: **design before code, then build with TDD**. This skill runs a single deterministic state machine that first *discovers* the design (producing a spec folder under `docs/specs/<timestamp_slug>/`) and then *implements* each issue. There is no separate discovery/implementation invocation — the **current step is always derived from `metadata.json`**, so re-running this skill resumes exactly where the workflow left off.

## Communication

Explain concepts to the user using business language — workflows, rules, responsibilities, integrations. Describe what is being designed or built and why, not how. Avoid jargon and code snippets in summaries unless asked. Use analogies when helpful.

**The artifacts are technical and always use precise technical language.** `SPEC.md`, `metadata.json`, issue files, code, tests, and commit messages use precise technical language. Only the conversational explanations and summaries presented to the user use business language.

## Language

- **All artifacts** (`SPEC.md`, `metadata.json`, issue files, code, tests, comments, commit messages) must be written in **English**.
- **Chat with the user** must be in the **same language the user uses**. Mirror the user's language.

## The Workflow

The workflow has two phases — **discovery** and **implementation** — that form a single continuous state machine. `metadata.json` is the single source of truth: every phase is `null` until complete, then holds an ISO 8601 timestamp. The current step is whatever the JSON says is next; you never track a state machine "by hand".

```
DISCOVERY (once per spec)
  clarify → clarify_review → model → model_review → architecture → architecture_review → slice
                                                                                          │
                                                                          (issues created)│
                                                                                          ▼
IMPLEMENTATION (per issue, repeated)
  understand → scout → architecture → tdd → simplify → test_quality → complexity → spec → commit
                                                                                          │
                                                                       (all issues done)  ▼
                                                                                        → PR
```

### Discovery steps

| Step                  | Skill                                                      | What to do                                            |
| --------------------- | ---------------------------------------------------------- | ----------------------------------------------------- |
| clarify               | praxis:collaborative-design                                | Understand the problem space through visual scenarios |
| clarify_review        | praxis:complexity-review                                   | Challenge and simplify what was clarified             |
| model                 | praxis:event-modeling                                      | Map behavior as events, commands, views, and slices   |
| model_review          | praxis:complexity-review                                   | Challenge and simplify the model                      |
| architecture          | praxis:backend-architecture / praxis:frontend-architecture | Define domain boundaries, ports, and adapters         |
| architecture_review   | praxis:complexity-review                                   | Challenge and simplify the architecture               |
| slice                 | praxis:collaborative-design                                | Break work into vertical slices with dependencies     |

### Implementation steps (per issue)

| Step         | Skill                  | What to do                                                                         |
| ------------ | ---------------------- | ---------------------------------------------------------------------------------- |
| understand   | (none)                 | Read the issue file and the spec context                                           |
| scout        | (context-dependent)    | Assess if touched code follows architecture; refactor only what this issue touches |
| architecture | (context-dependent)    | Define structure using the appropriate skill (see below)                           |
| tdd          | praxis:tdd             | Implement following the architecture's build order                                 |
| simplify     | praxis:code-simplifier | Simplify the result                                                                |
| test_quality | praxis:test-desiderata | Check test quality                                                                 |
| complexity   | praxis:complexity-review | Challenge unnecessary complexity                                                 |
| spec         | praxis:bdd-with-approvals | Write acceptance specs and verify they pass                                     |
| commit       | (none)                 | Commit the issue's changes                                                          |

**Architecture skill selection** (used in both `architecture` steps):
- Backend → `praxis:backend-architecture`
- Frontend → `praxis:frontend-architecture`

## Spec Folder Layout

Everything lives under one folder per spec:

```
docs/specs/<timestamp_slug>/
├── metadata.json          # single source of truth: discovery phases + issue registry (status + per-issue phases)
├── SPEC.md                # design document: clarify, model, architecture, slice, open questions, complexity challenges
├── ISSUE-01-<slug>.md     # one file per issue — content only
├── ISSUE-02-<slug>.md
└── ...
```

- **`metadata.json`** is the single source of truth for state, issue status, and phases. Do not duplicate status inside the markdown files.
- **`SPEC.md`** and the **issue files** hold content/context only.

## Multiple specs and concurrent work

Several people may run praxis at the same time, each on a **different** spec. The rule that makes this safe is: **one person per spec at a time, never two people on the same spec concurrently.** Because each spec is a separate folder with its own `metadata.json`, two people working two different specs never touch the same file — interleaved commits to `main` land in different folders and don't conflict. There is therefore no shared-state contention to resolve; the only thing the skill must get right is **picking the correct spec** when more than one is active.

**Never auto-pick the most recent spec.** When several specs are active, you must select deterministically or ask.

## Selecting the active spec

Do this **first**, before computing any step. A spec is **active** if it is not fully complete — i.e. some `discovery` phase is `null`, it has no issues yet, or any issue is not `done`.

**Use the bundled helper instead of reading every `metadata.json` yourself** (token-efficient): run

```
python3 <skill_dir>/list_active_specs.py
```

where `<skill_dir>` is this skill's directory (`${CLAUDE_PLUGIN_ROOT}/skills/praxis` when installed as a plugin, or `plugins/praxis/skills/praxis` in local dev). It scans `docs/specs/*/metadata.json` in the current project and prints a compact JSON array of the **active** specs only — each with `slug`, `name`, `description`, `phase`, a human-readable `state` (e.g. `discovery · model`, `ISSUE-02 · tdd`), `next_issue`, and issue counts. Match the user's reference and drive the menu off this output; only open an individual `metadata.json` once a single spec is selected. (Requires `python3`.)

1. **Match the user's reference** — if the user named a spec, match it against the active specs. Slugs are hard to remember, so accept an **approximate description** (e.g. "the login one", "billing", "el de export") and match it against each spec's `name`, `description`, and `slug` in `metadata.json` — not just an exact slug.
   - **Exactly one good match** → use it. State which spec you picked so the user can correct you (e.g. `Working on 1717000000_login-form (Login form).`).
   - **No match, or several plausible matches** → fall through to listing and asking (step 3) rather than guessing.
2. **Infer from branch** — else, if the current git branch is `praxis/<slug>` (or `praxis/<slug>/...`), use that spec. During implementation this makes selection automatic and silent.
3. **By active count** — else, from the helper's list of active specs:
   - **0 active** → the user is starting new functionality: bootstrap a **new** spec (see Setup) and start discovery at `clarify`. Each run of new functionality is always a new spec folder; never overwrite or extend an existing spec.
   - **exactly 1 active** → use it.
   - **more than 1 active** → **list each active spec with a one-line state and ask the user which to work on.** Do not guess. Example:
     ```
     Several specs are active — which do you want to work on?
       • 1717000000_login-form    — discovery · model
       • 1717009999_billing-export — ISSUE-02 pending (3 issues, 1 done)
     ```

## How to Determine the Current Step

Once the active spec is selected, read its `metadata.json` and compute the position — never assume:

1. **Any phase under `discovery` is `null`** → the current step is the **first** `null` discovery phase. Stay in the discovery phase.
2. **All discovery phases have timestamps, and some issue is `pending`/`in_progress` (and not `blocked`)** → enter the implementation phase. Pick the **active issue** (see below) and the current step is its **first `null` phase**.
3. **All issues are `done`** → the workflow is complete: create the pull request.

**Picking the active issue** (within the selected spec): an `in_progress` issue takes priority. Otherwise pick the first issue in `metadata.json` whose `status` is `pending` and whose `blocked_by` dependencies are all `done`.

## How to Run

### Setup (only when bootstrapping a new spec)

- Ensure you are on `main` with a clean working tree (`git status` → no uncommitted changes, `git pull` to update).
- Extract a `name` and `description` from the user's request.
- **Generate the slug** (see below) and create the directory `docs/specs/<timestamp_slug>/` (create parent dirs if needed).
- Write `SPEC.md` from the template below and `metadata.json` with all discovery phases set to `null` and `issues` empty.

### Execute one step at a time

Follow the **State Transition Protocol** below for every step, regardless of phase.

**Discovery phase specifics:**
- Use the Skill tool to invoke the skill listed for the current step. This is MANDATORY — do NOT attempt to perform the step yourself without loading the sub-skill first. The sub-skill contains specific methodology, formats, and checklists that must be followed.
- Write the step output to the corresponding section in `SPEC.md`.
- **Open questions**: when something is unclear or a tradeoff needs a decision:
  - Assign an ID (OQ-1, OQ-2, ...).
  - Record it in the Open Questions section of `SPEC.md` with: text, context, options, tradeoffs, and recommendation.
  - **A step CANNOT be completed while it has unresolved open questions.**
  - Present open questions one at a time.
  - **When resolving**: keep the original question intact (text, context, options, tradeoffs, recommendation). Add a `**Resolution**` field with the decision and a `**Status**: resolved` field. **Never delete or overwrite the original content** — the history of what was considered matters.
  - **Propagate implications**: after resolving a question, review the whole of `SPEC.md` and update all sections affected by the decision. This keeps the spec consistent.
- **Creating issues happens only during the `slice` step.** When slices are confirmed, for each issue:
  - Create a file `ISSUE-NN-<slug>.md` in the spec folder using the issue template below (numbered sequentially, slug derived from the issue title).
  - Add an entry to the `issues` object in `metadata.json` keyed by `ISSUE-NN` with `title`, `file`, `status: "pending"`, `blocked_by`, and a `phases` object with every implementation phase set to `null`.

**Implementation phase specifics:**
- Work the spec on a dedicated branch named `praxis/<slug>` (create it before the first issue if it doesn't exist, then check it out). This branch name is what lets the skill infer the active spec automatically on later runs, and keeps concurrent work on other specs isolated on their own branches.
- `understand`: read the issue file and `SPEC.md` for context. Confirm understanding with the user.
- `scout`: assess the existing code this issue will touch. Use `praxis:backend-architecture` (backend) or `praxis:frontend-architecture` (frontend) to evaluate alignment. If the code already follows the architecture, use the skip protocol. If not, refactor **only the code this issue touches** with a dedicated `refactor(scope): ...` commit before continuing.
- `architecture`: invoke `praxis:backend-architecture` or `praxis:frontend-architecture` (MANDATORY — load the sub-skill first).
- `tdd`: invoke `praxis:tdd` to implement inside-out — domain first, then ports, then adapters.
- `simplify`: invoke `praxis:code-simplifier`.
- `test_quality`: invoke `praxis:test-desiderata`.
- `complexity`: invoke `praxis:complexity-review`.
- `spec`: invoke `praxis:bdd-with-approvals` to write acceptance specs and verify they pass.
- `commit`: commit the issue's changes. Set the issue's `status` to `done` in `metadata.json`.
- **When all issues are done**: create the pull request.

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

State lives in `metadata.json`, not in frontmatter. Each phase is `null` until complete, then holds an ISO 8601 timestamp. The discovery phases live in the top-level `discovery` object; each issue carries its own `phases` object.

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

After the `slice` step, `issues` is populated. As implementation progresses, each issue's `status` and `phases` advance:

```json
"issues": {
  "ISSUE-01": {
    "title": "Login form",
    "file": "ISSUE-01-login-form.md",
    "status": "in_progress",
    "blocked_by": [],
    "phases": {
      "understand": "2026-05-30T10:00:00Z",
      "scout": "2026-05-30T10:20:00Z",
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

- **`status`**: `pending` → `in_progress` → `done`.
- **Current step for an issue**: the first phase whose value is `null`. When all phases have timestamps and the commit is done, set `status: "done"`.
- **How to update state**: edit `metadata.json` directly, setting the relevant phase to the current timestamp whenever you complete a step.

### Blocked state

When a phase cannot complete (TDD stuck, acceptance criteria not met, etc.), set a blocked status on the issue:

```json
"ISSUE-01": {
  "status": "blocked",
  "block_reason": "Acceptance criteria requires async email delivery, but current design uses sync calls",
  "block_step": "architecture",
  "phases": { ... }
}
```

To unblock: resolve the issue at `block_step`, clear the block fields, then resume from the first `null` phase.

## State Transition Protocol

Before doing any work in a step, follow this protocol — it is identical in both phases:

1. **Read current state**: read `metadata.json` and compute the current step (see "How to Determine the Current Step").
2. **Advance one step only**: complete the current step and set its phase to the current ISO 8601 timestamp. Never jump ahead.
3. **Print progress**: show the user the current position.
   - Discovery: `▶ discovery · step_name (N/total) — Remaining: step1 → step2 → ... → slice`
   - Implementation: `▶ ISSUE-NN · step_name (N/total) — Remaining: step1 → step2 → ... → commit`
4. **Skip protocol**: if a step does not apply, do NOT skip silently. Instead:
   - Print: `⏭ step_name — Skip reason: {reason}`
   - Set the phase timestamp and auto-advance immediately. Do not wait for confirmation on skips.
5. **Architecture is mandatory**: always invoke the architecture skills (`praxis:backend-architecture` for backend, `praxis:frontend-architecture` for frontend) even when the code is simple — in both the discovery `architecture` step and the per-issue `architecture` step. The goal is to set a precedent of organized code from the start. Never skip architecture steps citing simplicity.

## Contextual Skills

Use the Skill tool to invoke these when relevant (mostly during implementation):
- `praxis:dockerfile-review` — when working with Dockerfiles
- `praxis:expand-contract` — when making breaking changes (DB migrations, API changes)
- `praxis:thinkies` — when stuck or exploring alternatives

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

- **The current step is always derived from `metadata.json`.** Read it first, every time. Never track the state machine by hand.
- **Select the spec before anything else.** With multiple active specs, never auto-pick the most recent — match the user's approximate description against each spec's name/description/slug, infer from the `praxis/<slug>` branch, or list the active specs and ask. One person per spec at a time; concurrent work on different specs is safe because each spec is an isolated folder.
- **Wait for user confirmation** before advancing only when there are open questions or decisions needed. Auto-advance when a step completes cleanly or is skipped.
- **Never skip steps.** Follow the state machine order exactly. Use the skip protocol when a step does not apply.
- **Open questions block progress.** Resolve all before completing a step.
- **Issues can only be created during the `slice` step.**
- **Everything lives in `docs/specs/<timestamp_slug>/`** — `SPEC.md`, `metadata.json`, and one file per issue, in one folder.
- **`metadata.json` is the single source of truth** for state and issue status — never track status in the markdown files.
- **During implementation, only modify issue tracking in `metadata.json`** — update `status` and per-issue `phases`. Do not edit `SPEC.md` or the issue content files.
- **Each issue ends with a commit**, not a PR. The PR is created once all issues in the spec are done.
- **Test data must always be anonymous.** Never use real names, emails, or any personally identifiable information in tests. Use generic placeholders like `user@example.com`, `John Doe`, etc.
