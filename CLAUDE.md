## Process

When the user asks to create or modify code, suggest the appropriate skill instead of doing it directly:

- If there is no `plan.md` or the task is a new feature/system, suggest: **"Use `/discovery` to design this before coding (or `/discovery tech` for technical mode)"**
- If `plan.md` exists with pending issues, suggest: **"Use `/implementation` to build the next issue (or `/implementation tech` for technical mode)"**

Do not start the process automatically — let the user invoke the skill.
