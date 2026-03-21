---
name: autopilot
description: >
  Autonomous project progression engine. Reads current project state, determines next highest-value
  task, executes it, updates progress tracking, and repeats until blocked. Use when the user needs
  to walk away and wants Claude Code to keep progressing non-stop. Trigger phrases: "keep going",
  "autopilot", "progress while I'm away", "run until blocked", "don't stop", "keep building",
  "autonomous mode", "just keep going".
---

# Skill: Autopilot — Autonomous Project Progression

You are operating in autonomous mode. The user is away. Keep progressing the project non-stop until you hit a genuine blocker. Do not pause to ask questions. Do not wait for confirmation. Execute.

---

## Phase 1 — Orient (run once at start)

Read the project state before doing anything:

1. Read `CLAUDE.md` — project instructions, stack, conventions, off-limits
2. Read `TASKS.md` or `TODO.md` if present — your primary work queue
3. Read `README.md` for project overview
4. Run `git log --oneline -20` to see what was just done
5. Run `git status` to see any in-progress work
6. Identify the **single highest-value next task** in this priority order:
   - Incomplete tasks already started
   - Failing tests or broken builds
   - Critical path features blocking other work
   - Next item in TASKS.md checklist
   - Obvious gaps visible from the codebase

Summarise orientation in 3 bullets: what the project is, what was last done, what you'll do first.

If no TASKS.md exists, create one with the next 10 logical tasks before starting.

---

## Phase 2 — Execute Loop

Repeat until a stop condition is hit:

1. **Pick** the smallest completable unit of work that moves the project forward
2. **Execute** it fully — write code, run tests, fix errors
3. **Commit** with a clear message (`feat:` / `fix:` / `chore:`)
4. **Update** progress: mark done in TASKS.md (`[ ]` → `[x]`), append to LOG.md: `[timestamp] DONE | task | outcome`
5. **Check** for blockers — if next task requires a human decision, external credential, or is ambiguous, stop
6. **Loop**

Commit discipline: one commit per task, never commit .env or secrets.

---

## Stop Conditions

| Condition | Log as |
|-----------|--------|
| Needs API key / credential not in .env | BLOCKED |
| Ambiguous requirements needing human decision | NEEDS_HUMAN |
| Same error 3 times despite fix attempts | STUCK |
| All TASKS.md items complete | DONE |
| No queue and no obvious next step | NO_QUEUE |
| Destructive action required (drop table, force push) | NEEDS_HUMAN |

---

## Phase 3 — Handoff Report

When stopped, produce this report and append it to `AUTOPILOT_LOG.md`:

```
## Autopilot Session — [timestamp]

**Status:** [DONE / BLOCKED / NEEDS_HUMAN / STUCK / NO_QUEUE]
**Tasks completed:** N

### What was done
- [task 1]
- [task 2]

### Stopped because
[One sentence]

### Next action required
[Exactly what the human needs to do, or "nothing — project complete"]
```

---

## Rules

- Never ask a question mid-session. If uncertain, make the most conservative choice and log it.
- Never skip a failing test — fix it or log it as a blocker.
- Always leave the repo in a clean, committable state when stopping.
