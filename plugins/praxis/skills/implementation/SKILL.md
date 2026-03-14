---
name: implementation
description: Implement code with TDD following a deterministic state machine (understand → scout → architecture → tdd → simplify → test_quality → complexity → spec → commit). Driven by issues in plan.md.
argument-hint: "[tech]"
---

# Implementation

Implement code with TDD. This skill runs a deterministic state machine driven by issues in `plan.md`.

## Audience Mode

If `$ARGUMENTS` is `tech`, use tech tone. Otherwise, default to non-tech.

- **Default (no argument)**: Explain progress and decisions using business language. Describe what was built and why, not how. Avoid code snippets in summaries unless asked.
- **`tech`**: Use tech language — code references, architecture terms, test results, etc.

**The code, tests, commits, and plan updates are identical regardless of mode.** Only the conversational explanations presented to the user change.

## Language

- **All artifacts** (code, tests, comments, commit messages, plan updates) must be written in **English**.
- **Chat with the user** must be in the **same language the user uses**. Mirror the user's language.

## State Machine

```
idle → understand → scout → architecture → tdd → simplify → test_quality → complexity → spec → commit → idle
```

## Steps

| Step         | Skill                  | What to do                                                                         |
| ------------ | ---------------------- | ---------------------------------------------------------------------------------- |
| understand   | (none)                 | Read the issue in `plan.md` and its surrounding context                            |
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

## How to Run

1. **Setup**: Identify which issue to implement from `## Issues` in `plan.md`. Create a feature branch if needed. Update the frontmatter: `state: understand`, `type: implementation`.
2. **Understand**: Read the issue and the rest of the plan for context. Confirm understanding with the user.
3. **Scout**: Assess the existing code that this issue will touch. Use `praxis:backend-architecture` for backend or `praxis:frontend-architecture` for frontend to evaluate alignment. If the code already follows the architecture, use the skip protocol. If not, refactor **only the code this issue touches** with a dedicated `refactor(scope): ...` commit before continuing.
4. **Architecture**: Use the Skill tool to invoke the appropriate skill based on context — `skill: "praxis:backend-architecture"` for backend, `skill: "praxis:frontend-architecture"` for frontend. This is MANDATORY — do NOT attempt to perform the step yourself without loading the sub-skill first. The sub-skill contains specific methodology, formats, and checklists that must be followed.
5. **TDD**: Use the Skill tool to invoke `skill: "praxis:tdd"` to implement inside-out — domain first, then ports, then adapters.
6. **Simplify**: Use the Skill tool to invoke `skill: "praxis:code-simplifier"` to simplify the result.
7. **Test quality**: Use the Skill tool to invoke `skill: "praxis:test-desiderata"` to check test quality.
8. **Complexity**: Use the Skill tool to invoke `skill: "praxis:complexity-review"` to challenge unnecessary complexity.
9. **Spec**: Use the Skill tool to invoke `skill: "praxis:bdd-with-approvals"` to write acceptance specs and verify they pass.
10. **Commit**: Commit the issue's changes. Mark issue status as `done`.
11. **When all issues are done**: Create the pull request.

## State Transition Protocol

Before doing any work in a step, follow this protocol:

1. **Read current state**: Read `state` from plan.md frontmatter.
2. **Advance one step only**: Update `state` to the **immediately next** step in the state machine. Never jump ahead.
3. **Print progress**: Show the user the current position:
   ```
   ▶ step_name (N/total) — Remaining: step1 → step2 → ... → commit
   ```
4. **Skip protocol**: If a step does not apply, do NOT skip silently. Instead:
   - Print: `⏭ step_name — Skip reason: {reason}`
   - Auto-advance to the next step immediately. Do not wait for confirmation on skips.
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
- **Implementation only modifies issue Status** — update from `pending` to `done` when implementation is complete. No other plan modifications.
- **Each issue ends with a commit**, not a PR. The PR is created once all issues in the plan are done.
- **Test data must always be anonymous.** Never use real names, emails, or any personally identifiable information in tests. Use generic placeholders like `user@example.com`, `John Doe`, etc.
