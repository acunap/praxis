---
name: implementation
description: Implement code with TDD following a deterministic state machine (understand → scout → architecture → tdd → simplify → test_quality → complexity → spec → commit). Driven by the issues in docs/specs/<timestamp_slug>/.
---

# Implementation

Implement code with TDD. This skill runs a deterministic state machine driven by the issues registered in a spec folder under `docs/specs/<timestamp_slug>/`.

## Communication

Explain progress and decisions to the user using business language. Describe what was built and why, not how. Avoid code snippets in summaries unless asked.

**The code, tests, commits, and metadata updates always use precise technical language.** Only the conversational explanations presented to the user use business language.

## Language

- **All artifacts** (code, tests, comments, commit messages, metadata updates) must be written in **English**.
- **Chat with the user** must be in the **same language the user uses**. Mirror the user's language.

## State Machine

Each issue runs its own per-issue state machine:

```
idle → understand → scout → architecture → tdd → simplify → test_quality → complexity → spec → commit → idle
```

## Steps

| Step         | Skill                  | What to do                                                                         |
| ------------ | ---------------------- | ---------------------------------------------------------------------------------- |
| understand   | (none)                 | Read the issue file and the spec context                                           |
| scout        | (context-dependent)    | Assess if touched code follows architecture; refactor only what this issue touches |
| architecture | (context-dependent)    | Define structure using the appropriate skill (see below)                           |
| tdd          | praxis:tdd                   | Implement following the architecture's build order                                 |
| simplify     | praxis:code-simplifier       | Simplify the result                                                                |
| test_quality | praxis:test-desiderata       | Check test quality                                                                 |
| complexity   | praxis:complexity-review     | Challenge unnecessary complexity                                                   |
| spec         | praxis:bdd-with-approvals    | Write acceptance specs and verify they pass                                        |
| commit       | (none)                       | Commit the issue's changes                                                         |

**Architecture skill selection**:
- Backend → `praxis:backend-architecture`
- Frontend → `praxis:frontend-architecture`

## Spec Folder Layout

The spec folder produced by `discovery` drives implementation:

```
docs/specs/<timestamp_slug>/
├── metadata.json          # single source of truth: issue status + per-issue phases (as ISO timestamps)
├── SPEC.md                # design document (read-only context)
├── ISSUE-01-<slug>.md     # issue content
├── ISSUE-02-<slug>.md
└── ...
```

- **`metadata.json`** is the single source of truth for issue status and per-issue phase progress.
- The issue files and `SPEC.md` are **content/context** — read them, do not track status in them.

## How to Run

1. **Setup**:
   - Locate the active spec folder under `docs/specs/`. If several exist, work the most recent one with `pending` issues (confirm with the user if ambiguous).
   - Pick the next issue to implement: the first issue in `metadata.json` whose `status` is `pending` and whose `blocked_by` dependencies are all `done`.
   - Create a feature branch if needed.
2. **Understand**: Read the issue file and `SPEC.md` for context. Confirm understanding with the user.
3. **Scout**: Assess the existing code that this issue will touch. Use `praxis:backend-architecture` for backend or `praxis:frontend-architecture` for frontend to evaluate alignment. If the code already follows the architecture, use the skip protocol. If not, refactor **only the code this issue touches** with a dedicated `refactor(scope): ...` commit before continuing.
4. **Architecture**: Use the Skill tool to invoke the appropriate skill based on context — `skill: "praxis:backend-architecture"` for backend, `skill: "praxis:frontend-architecture"` for frontend. This is MANDATORY — do NOT attempt to perform the step yourself without loading the sub-skill first. The sub-skill contains specific methodology, formats, and checklists that must be followed.
5. **TDD**: Use the Skill tool to invoke `skill: "praxis:tdd"` to implement inside-out — domain first, then ports, then adapters.
6. **Simplify**: Use the Skill tool to invoke `skill: "praxis:code-simplifier"` to simplify the result.
7. **Test quality**: Use the Skill tool to invoke `skill: "praxis:test-desiderata"` to check test quality.
8. **Complexity**: Use the Skill tool to invoke `skill: "praxis:complexity-review"` to challenge unnecessary complexity.
9. **Spec**: Use the Skill tool to invoke `skill: "praxis:bdd-with-approvals"` to write acceptance specs and verify they pass.
10. **Commit**: Commit the issue's changes. Set the issue's `status` to `done` in `metadata.json`.
11. **When all issues are done**: Create the pull request.

Each completed step sets its phase to the current ISO 8601 timestamp inside the issue's `phases` object in `metadata.json`.

## State Tracking

State lives in `metadata.json`, not in frontmatter. Each issue carries its own `phases` object; each phase is `null` until complete, then holds an ISO 8601 timestamp.

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

Before doing any work in a step, follow this protocol:

1. **Read current state**: read `metadata.json`, pick the active issue, and find its first `null` phase.
2. **Advance one step only**: complete the current phase and set its timestamp. Never jump ahead.
3. **Print progress**: show the user the current position:
   ```
   ▶ ISSUE-NN · step_name (N/total) — Remaining: step1 → step2 → ... → commit
   ```
4. **Skip protocol**: if a step does not apply, do NOT skip silently. Instead:
   - Print: `⏭ step_name — Skip reason: {reason}`
   - Set the phase timestamp and auto-advance immediately. Do not wait for confirmation on skips.
5. **Architecture is mandatory**: Always invoke the architecture skills (`praxis:backend-architecture` for backend, `praxis:frontend-architecture` for frontend) even when the code is simple. The goal is to set a precedent of organized code from the start. Never skip architecture steps citing simplicity.

## Contextual Skills

Use the Skill tool to invoke these when relevant during implementation:
- `praxis:dockerfile-review` — when working with Dockerfiles
- `praxis:expand-contract` — when making breaking changes (DB migrations, API changes)
- `praxis:thinkies` — when stuck or exploring alternatives

## Rules

- **Wait for user confirmation** before advancing only when there are open questions or decisions needed. Auto-advance when a step completes cleanly or is skipped.
- **Never skip steps.** Follow the state machine order exactly. Use the skip protocol when a step does not apply.
- **Open questions block progress.** Resolve all before completing a step.
- **Implementation only modifies issue tracking in `metadata.json`** — update `status` and per-issue `phases`. Do not edit `SPEC.md` or the issue content files.
- **Each issue ends with a commit**, not a PR. The PR is created once all issues in the spec are done.
- **Test data must always be anonymous.** Never use real names, emails, or any personally identifiable information in tests. Use generic placeholders like `user@example.com`, `John Doe`, etc.
