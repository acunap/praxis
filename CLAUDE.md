## Process

When the user asks to create or modify code, suggest the appropriate skill instead of doing it directly:

- If there is no spec under `docs/specs/` or the task is a new feature/system, suggest: **"Use `/discovery` to design this before coding"**
- If a spec exists under `docs/specs/<timestamp_slug>/` with pending issues, suggest: **"Use `/implementation` to build the next issue"**

Do not start the process automatically — let the user invoke the skill.
