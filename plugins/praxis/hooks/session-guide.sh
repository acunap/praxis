#!/bin/sh
cat <<'EOF'
BLOCKING REQUIREMENT: When the user asks to build, design, or add something new and the task involves any of: multiple files/components, ambiguous requirements, architectural decisions, or new domain concepts → you MUST suggest /praxis:discovery to the user BEFORE writing ANY code or creating ANY files. Do NOT proceed to generate code, use Write, Edit, or Bash to create project structure without first suggesting /praxis:discovery and getting the user's decision. This applies even if the task seems straightforward.

BLOCKING REQUIREMENT: When a plan.md exists in the project root with pending issues → you MUST suggest /praxis:implementation to the user BEFORE writing ANY code. Do NOT start implementing features or fixing issues described in plan.md without first suggesting /praxis:implementation and getting the user's decision.

In both cases, do not auto-invoke the skills — suggest them to the user and wait for their decision before proceeding.
EOF
