# praxis

Structured practice for software craft — a Claude Code plugin with discovery, implementation, and engineering skills.

## What is this?

Working with AI coding assistants can feel chaotic — you start coding without a clear plan, skip design steps, and end up with inconsistent results. Praxis is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin that brings structure through a single end-to-end workflow, `/praxis:praxis`, with two phases:

1. **Discovery** — Design before code. Clarify the problem, model the domain, and define the architecture. The whole design is then reviewed for unnecessary complexity in a single pass before breaking work into vertical slices.

2. **Implementation** — Code with TDD. For each slice: understand the requirement, define the architecture, implement with test-driven development, simplify, review test quality, challenge complexity, and commit.

It is one skill, not two: the **current step is always derived from `metadata.json`**, so running `/praxis:praxis` resumes exactly where the workflow left off — first designing, then building. The whole thing follows a strict state machine — no skipping steps, no moving forward without confirmation. Open questions must be resolved before progressing.

## Install

Inside a Claude Code session, run:

```
/plugin marketplace add git@github.com:acunap/praxis.git
/plugin install praxis@praxis
```

Once installed, all skills are available as `/praxis:praxis`, `/praxis:tdd`, etc.

A smart process rule is included — it evaluates task complexity and only suggests `/praxis:praxis` when the task warrants it. Simple tasks (bug fixes, small edits) won't trigger any suggestions.

## How it works

1. Install the plugin in any project.
2. Start working — the process rule will suggest `/praxis:praxis` when the task is complex enough.
3. Run `/praxis:praxis`. It reads `docs/specs/<timestamp_slug>/metadata.json` to find the current step and resumes there:
   - **No spec yet?** It starts discovery — clarify, model, architect, and slice the work into issues under `docs/specs/<timestamp_slug>/` (a `SPEC.md`, a `metadata.json`, and one file per issue).
   - **Spec with pending issues?** It moves to implementation, building the next issue with TDD, simplification, and complexity review.
4. Each issue ends with a commit. When all issues are done, it creates a PR.

## Local development

If you're working on praxis itself, skills are available directly as `/praxis`, `/tdd`, etc. — no plugin install needed.

The `CLAUDE.md` at the root handles the local workflow.

## Skills included

| Skill | Purpose |
|-------|---------|
| `praxis` | End-to-end workflow — design (discovery) then build (implementation), driven by `metadata.json` |
| `tdd` | Test-driven development process |
| `collaborative-design` | Visual scenario exploration |
| `event-modeling` | Map behavior as events, commands, views |
| `backend-architecture` | Ports and adapters design |
| `frontend-architecture` | Feature-based React architecture |
| `complexity-review` | Challenge and simplify proposals |
| `expand-contract` | Zero-downtime breaking changes |
| `thinkies` | Kent Beck's pattern-based thinking |
| `dockerfile-review` | Dockerfile optimization |
| `test-desiderata` | Test quality analysis |
| `code-simplifier` | Reduce complexity without changing behavior |
