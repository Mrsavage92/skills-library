# Phase 0 — Orient + GitHub Repo + Notion Doc

## Phase 0 — Orient

Read these files in full — they are the source of truth for the entire build. Run all reads in parallel:
1. `~/.claude/commands/premium-website.md` — all suite rules, landing page non-negotiables, performance requirements, per-page quality bar, and pre-deploy checklist. Everything in that file applies automatically to every phase below.
2. `~/.claude/web-system-prompt.md` — Design DNA. Read before generating any UI.
3. `~/.claude/commands/web-animations.md` — Framer Motion patterns. Technique 3 STAGGER is mandatory for the hero. Read before writing any animated component.
4. `CLAUDE.md` (project root, if exists) — project-specific overrides.
5. `DESIGN-BRIEF.md` (project root, if exists) — locked color system, typography, marketing tier, and component decisions from Phase 0.5. If this file exists, all design decisions are already made — do NOT re-decide them.
6. `SCOPE.md` (project root, if exists) — page inventory and design decisions.

**Monorepo detection:** Check if the working directory contains `turbo.json` or an `apps/` directory. If yes, this is a monorepo build.
- In monorepo mode: the frontend lives in `apps/[product-slug]/`. All Phase 2-6 file operations target that subdirectory.
- The backend is the shared FastAPI service at `services/api/` — do NOT scaffold a new backend or create a new Railway service. Note the existing Railway URL from `CLAUDE.md` for VITE_API_URL.
- If `apps/[product-slug]/` already exists (created by `/product-add`): skip Phase 2 directory creation, only fill in the files.
- If `apps/[product-slug]/` does not exist: run `/product-add` first, then scaffold.
- **Scaffold copy cleanup (MANDATORY if the app directory was created by copying another product's directory):** Before writing any content, run these checks in `apps/[product-slug]/`:
  1. Delete `.vercel/project.json` if it exists — it points to the source product's Vercel project and will silently deploy to the wrong project on first deploy. Vercel creates a fresh `project.json` automatically on next deploy.
  2. Grep for the source product's `product_id` string (e.g. `whs-psychosocial`) across all src files and replace all occurrences with the new product's id.
  3. Check `src/styles/index.css` for the old `--brand:` HSL value and replace with the new product's brand colour.
  4. Grep `src/pages/*.tsx` for any imported type names that have been removed from `src/types/index.ts`. TypeScript compiles ALL files in the project, not just routes imported in App.tsx — orphan pages with deleted type imports will fail `tsc --noEmit` even if they are unreachable at runtime. Stub those files to `// Unused - replaced by [NewPage].tsx\nexport {}` immediately.

Check if BUILD-LOG.md exists in the project root (or `apps/[product-slug]/BUILD-LOG.md` in monorepo). This is the primary resume signal — not git log.

If BUILD-LOG.md does not exist: this is a fresh start. Begin at Phase 0.25.
If BUILD-LOG.md exists: read it to identify the last completed phase, then continue from the next one. If resuming from Phase 1 or later, verify DESIGN-BRIEF.md exists — if missing, run Phase 0.5 before continuing. Also verify MARKET-BRIEF.md exists — if missing, run Phase 0.25 before continuing.

**If resuming (BUILD-LOG.md exists): also run `/project-refresh` PULL now before continuing.** Pull Notion state into context — decisions, blockers, and credential status may have changed since the last session.

Log every phase start and completion to `BUILD-LOG.md` in the project root (or `apps/[product-slug]/BUILD-LOG.md` in monorepo mode).

---

## Phase 0 — GitHub Repo + Notion Doc (fresh builds only)

**For fresh builds (no BUILD-LOG.md), do this before Phase 0.25. For resuming builds, verify these exist and skip if already done.**

**Step A — Create GitHub repo:**

Check if a repo exists for this product:
```
mcp__github__search_repositories({ query: "[product-slug] user:Mrsavage92" })
```

If no repo found: create it using the MCP tool (preferred) with fallback to GitHub API:

**Method 1 — GitHub MCP (preferred):**
```
mcp__github__create_repository({ name: "[product-slug]", description: "[product name]", private: true, autoInit: false })
```

**Method 2 — GitHub API via curl (fallback if MCP unavailable):**
```bash
TOKEN=$(git credential fill <<< 'protocol=https
host=github.com' 2>/dev/null | grep password | cut -d= -f2)
curl -s -X POST -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  https://api.github.com/user/repos \
  -d '{"name":"[product-slug]","private":true,"description":"[product name]"}'
```

**Method 3 — gh CLI (final fallback):**
```bash
gh repo create Mrsavage92/[product-slug] --private --source=. --push
```

After creation: set the remote and push immediately:
```bash
git remote add origin https://github.com/Mrsavage92/[product-slug].git 2>/dev/null || git remote set-url origin https://github.com/Mrsavage92/[product-slug].git
git push -u origin main || git push -u origin master
```

**Verify the push succeeded** — if `git push` returns "Repository not found", the repo creation failed. Try the next fallback method. Do NOT continue the build without a working GitHub repo.

In monorepo mode: skip repo creation — the monorepo (`saas-platform` or `au-compliance-platform`) is already the repo. Just verify the `apps/[product-slug]/` directory will be committed there.

Write the repo URL to BUILD-LOG.md and the project memory file as `github_repo`.

**Step B — Create Notion project doc:**

Run `/project-doc` with the product name and brief. This creates the Notion master doc under the Projects hub.

Write the Notion URL to BUILD-LOG.md and the project memory file as `notion_url`.

**Step C — Create project memory file:**

Check if `~/.claude/projects/.../memory/project_[slug].md` exists. If not, create it now:
```markdown
---
name: [Product Name]
description: [one-line product description]
type: project
---

[Product Name] — [brief description]

**Why:** [product rationale]
**How to apply:** Next session = continue from last BUILD-LOG.md phase.

GitHub: [repo URL]
Notion: [notion URL]
Build state: Phase 0 started [date]
```

Add the memory file to MEMORY.md index.

After Steps A-C complete: commit the initial files (BUILD-LOG.md, memory file) and push to GitHub:
```bash
git add BUILD-LOG.md && git commit -m "init: [product-name] saas-build started" && git push origin main
```

Log: "Phase 0 complete — context loaded, repo created, Notion doc created" to BUILD-LOG.md.

---

## Phase Completion Protocol (applies to every phase)

Every time a "Log: Phase X complete" line is reached:
1. Write the log entry to BUILD-LOG.md
2. `git add -A && git commit -m "phase X: [one-line description]" && git push origin main`
3. Run `/project-refresh` PUSH with phase name + what was built + any new NEEDS_HUMAN items

This is not optional. A phase not committed and not in Notion does not exist from the next session's perspective.

In monorepo mode: commit from the monorepo root (`C:/Users/Adam/Documents/au-compliance-platform`), not the app subdirectory.
