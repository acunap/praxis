## Process

When the user asks to create or modify code, suggest the `/praxis` skill instead of doing it directly. It is a single end-to-end workflow (design → build) that reads `docs/specs/<timestamp_slug>/metadata.json` and resumes at the correct step:

- If there is no spec under `docs/specs/` or the task is a new feature/system, suggest: **"Use `/praxis` to design this before coding"** — it starts at discovery.
- If a spec exists under `docs/specs/<timestamp_slug>/` with pending issues, suggest: **"Use `/praxis` to build the next issue"** — it resumes at implementation.

Do not start the process automatically — let the user invoke the skill.
