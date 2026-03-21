---
title: "Best Claude Code Plugins & Skills (2026)"
description: "The 20 best Claude Code plugins and agent skills for engineering, marketing, product, and DevOps. Install in one command."
---

# Best Claude Code Plugins & Skills (2026)

Looking for the best Claude Code plugins to supercharge your workflow? This guide covers 20 production-ready plugins and agent skills — from engineering and DevOps to marketing, product management, and C-level advisory.

All plugins listed here are open-source (MIT), tested in production, and installable in one command.

---

## What's the Difference Between Plugins and Skills?

**Claude Code plugins** use the `.claude-plugin/plugin.json` format and install by copying to `~/.claude/commands/` or `~/.claude/agents/`. **Agent skills** use `SKILL.md` files and work across Claude Code, Codex, Gemini CLI, Cursor, and 8 other coding agents.

This repo provides **both formats** — every skill includes a `.claude-plugin` directory for native Claude Code plugin support, plus a `SKILL.md` for cross-platform compatibility.

---

## Quick Install

```bash
# Install the full marketplace (all 192 skills as Claude Code plugins)
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/://github.com/alirezarezvani/claude-skills

# Install by domain
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/

# Install individual plugins
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/
claude # Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/
```

---

## Top 20 Claude Code Plugins

### Engineering & DevOps

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **frontend-design** | Production-grade UI with high design quality. React, Tailwind, shadcn/ui. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **pr-review-expert** | Multi-pass code review: logic bugs, security, test coverage, architecture. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **autoresearch-agent** | Autonomous experiment loop — optimizes any file by a measurable metric. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **senior-devops** | Infrastructure as Code, CI/CD pipelines, monitoring, incident response. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **docker-development** | Dockerfile optimization, multi-stage builds, container security scanning. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **aws-solution-architect** | AWS architecture design with serverless patterns and IaC templates. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **tdd-guide** | Test-driven development workflows with red-green-refactor cycles. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **database-designer** | Schema design, migrations, indexing strategies, query optimization. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |

### Marketing & Content

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **content-creator** | SEO-optimized content with consistent brand voice and frameworks. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **copywriting** | Marketing copy for landing pages, pricing pages, CTAs. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **email-sequence** | Drip campaigns, nurture sequences, lifecycle email programs. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **app-store-optimization** | ASO keyword research, metadata optimization, A/B testing. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |

### Product & Business

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **research-summarizer** | Structured research → summary → citations for papers and reports. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **agile-product-owner** | User stories, acceptance criteria, sprint planning, velocity tracking. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **ab-test-setup** | A/B test design, hypothesis creation, statistical significance. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **analytics-tracking** | GA4, GTM, conversion tracking, UTM parameters, tracking plans. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |

### C-Level & Strategy

| Plugin | What It Does | Install |
|--------|-------------|---------|
| **cto-advisor** | Tech debt analysis, team scaling, architecture decisions, DORA metrics. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **ceo-advisor** | Strategy, board governance, investor relations, organizational development. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **cfo-advisor** | Financial modeling, fundraising, burn rate analysis, unit economics. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |
| **marketing-strategy-pmm** | Positioning (April Dunford), GTM strategy, competitive intelligence. | `# Skills load automatically from ~/.claude/commands/ and ~/.claude/agents/` |

---

## Why These Plugins?

Unlike single-purpose plugins, these are **POWERFUL-tier** agent skills — each includes:

- **Structured workflows** with slash commands (not just prompts)
- **Python CLI tools** (254 total, zero pip dependencies)
- **Reference documents** — templates, checklists, domain-specific knowledge
- **Cross-platform support** — works on 11 coding agents, not just Claude Code

---

## Cross-Platform Compatibility

Every plugin in this collection works across multiple AI coding agents:

| Tool | Format | Install Method |
|------|--------|---------------|
| Claude Code | `.claude-plugin` | copy to `~/.claude/commands/` |
| OpenAI Codex | `.codex/skills/` | `./scripts/codex-install.sh` |
| Gemini CLI | `.gemini/skills/` | `./scripts/gemini-install.sh` |
| Cursor | `.cursor/skills/` | `./scripts/convert.sh --tool cursor` |
| OpenClaw | `# Available locally in ~/.claude/skills/claude-skills/` | Via Skills Library marketplace |
| Aider, Windsurf, Kilo Code, OpenCode, Augment, Antigravity | Converted formats | `./scripts/convert.sh --tool <name>` |

---

## Related Resources

- [Full Skill Catalog](https://github.com/alirezarezvani/claude-skills) — all 192 skills
- [Agent Skills for Codex](./agent-skills-for-codex.md) — Codex-specific guide
- [Gemini CLI Skills Guide](./gemini-cli-skills-guide.md) — Gemini CLI setup
- [Cursor Skills Guide](./cursor-skills-guide.md) — Cursor integration

---

*Last updated: March 2026 · [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)*
