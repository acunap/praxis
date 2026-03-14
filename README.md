# praxis

Structured practice for software craft — a Claude Code plugin with discovery, implementation, and engineering skills.

## What is this?

Working with AI coding assistants can feel chaotic — you start coding without a clear plan, skip design steps, and end up with inconsistent results. Praxis is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin that brings structure through a two-phase workflow:

1. **Discovery** — Design before code. Clarify the problem, model the domain, define the architecture, and break work into vertical slices. Each step is reviewed for unnecessary complexity before moving on.

2. **Implementation** — Code with TDD. For each slice: understand the requirement, define the architecture, implement with test-driven development, simplify, review test quality, challenge complexity, write acceptance specs, and commit.

Both phases follow a strict state machine — no skipping steps, no moving forward without confirmation. Open questions must be resolved before progressing.

## Install

Inside a Claude Code session, run:

```
/plugin marketplace add git@github.com:acunap/praxis.git
/plugin install praxis@praxis
```

Once installed, all skills are available as `/praxis:discovery`, `/praxis:implementation`, `/praxis:tdd`, etc.

A smart process rule is included — it evaluates task complexity and only suggests `/praxis:discovery` or `/praxis:implementation` when the task warrants it. Simple tasks (bug fixes, small edits) won't trigger any suggestions.

## How it works

1. Install the plugin in any project.
2. Start working — the process rule will suggest `/praxis:discovery` when the task is complex enough.
3. Discovery designs the solution step by step: clarify, model, architect, and slice into issues in `plan.md`.
4. Use `/praxis:implementation` to build each issue with TDD, simplification, and complexity review.
5. Each issue ends with a commit. When all issues are done, create a PR.

## Local development

If you're working on praxis itself, skills are available directly as `/discovery`, `/implementation`, etc. — no plugin install needed.

The `CLAUDE.md` at the root handles the local workflow. The `rules/process.md` file is only loaded for plugin consumers.

## Skills included

| Skill | Purpose |
|-------|---------|
| `discovery` | Design before code — clarify, model, architect, slice |
| `implementation` | TDD workflow driven by plan.md issues |
| `tdd` | Test-driven development process |
| `collaborative-design` | Visual scenario exploration |
| `event-modeling` | Map behavior as events, commands, views |
| `hexagonal-architecture` | Ports and adapters design |
| `frontend-architecture` | Feature-based React architecture |
| `complexity-review` | Challenge and simplify proposals |
| `bdd-with-approvals` | BDD tests in domain language |
| `expand-contract` | Zero-downtime breaking changes |
| `thinkies` | Kent Beck's pattern-based thinking |
| `dockerfile-review` | Dockerfile optimization |
| `test-desiderata` | Test quality analysis |
| `code-simplifier` | Reduce complexity without changing behavior |
