# Claude Code Skills Library

**314 skills, 59 agents, and 59 commands for Claude Code.**

A production-grade library of Claude Code skills covering SaaS product building, website auditing, marketing, engineering, C-level advisory, regulatory compliance, and more. Originally forked from [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) and significantly expanded with 118 additional skills, 59 agents, and 38 commands.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-314-brightgreen?style=for-the-badge)](#skills-overview)
[![Agents](https://img.shields.io/badge/Agents-59-blue?style=for-the-badge)](#agents)
[![Commands](https://img.shields.io/badge/Commands-59-orange?style=for-the-badge)](#commands)

---

## What's In This Repo

| Type | Count | What they do |
|------|-------|-------------|
| **Skills** | 314 | Domain expertise packages with structured workflows, decision frameworks, and scripts |
| **Agents** | 59 | Autonomous agent definitions — C-suite advisors, engineering specialists, architects |
| **Commands** | 59 | Slash commands that trigger skills from chat (e.g. `/saas-build`, `/autopilot`, `/geo-audit`) |

---

## Skills Overview

### Audit & Analysis Suites (8 suites, 50+ skills)

Full website audit suites that run independently or together via `/full-audit` or `/parallel-audit`.

| Suite | Skills | What it audits |
|-------|--------|----------------|
| **Marketing** | `/market audit`, `copy`, `emails`, `social`, `ads`, `funnel`, `landing`, `gbp`, `proposal`, `brand`, `competitors`, `launch`, `reviews`, `seo`, `report`, `report-pdf` | SEO, copy, funnel, social, email, CTAs, competitors |
| **Technical** | `/techaudit audit`, `accessibility`, `mobile`, `speed`, `report-pdf` | Performance, accessibility, mobile, Core Web Vitals |
| **GEO** | `/geo audit`, `citability`, `schema`, `technical`, `crawlers`, `llmstxt`, `platform-optimizer`, `brand-mentions`, `content`, `report`, `report-pdf` | AI citability, schema, llms.txt, AI crawlers |
| **Security** | `/security audit`, `headers`, `email`, `report-pdf` | Headers, certificates, email auth, CMS hardening |
| **Privacy** | `/privacy audit`, `cookies`, `policy`, `report-pdf` | GDPR/PECR, cookies, privacy policy |
| **Reputation** | `/reputation audit`, `monitor`, `response`, `report-pdf` | Reviews, brand mentions, trust signals |
| **Employer Brand** | `/employer audit`, `careers`, `evp`, `reviews`, `social`, `report-pdf` | Careers page, EVP, Glassdoor, LinkedIn employer |
| **AI Readiness** | `/ai-ready audit`, `adoption`, `automation`, `data`, `report-pdf` | AI maturity, automation opportunities, data readiness |

**Orchestrators:**
- `/full-audit <url>` — runs all 8 suites sequentially, produces combined report
- `/parallel-audit <url>` — runs all 8 suites simultaneously via background agents

---

### Premium Website Suite (16 skills)

Complete SaaS product build pipeline — replaces Lovable. Produces Awwwards/Linear/Stripe quality output.

| Skill | Role |
|-------|------|
| `/web-design-research` | Pre-build competitor research, 21st.dev component sourcing, unique design system |
| `/web-scope` | Define pages, design decisions, architecture — reads DESIGN-BRIEF.md |
| `/web-scaffold` | Bootstrap project: config, design system, routes, AppLayout, Sentry |
| `/web-page` | Build individual pages using Component Lock from DESIGN-BRIEF.md |
| `/web-component` | Build production components (modals, forms, cards) |
| `/web-animations` | Framer Motion patterns — 5 techniques including hero entrance stagger |
| `/web-supabase` | Backend: schema, RLS, auth, TypeScript types |
| `/web-stripe` | Payments: checkout, webhooks, UpgradeButton, Customer Portal |
| `/web-email` | Transactional email: Resend + React Email, 5 templates, trial reminders |
| `/web-onboarding` | Multi-step onboarding wizard with progress bar, trial activation |
| `/web-settings` | Settings page: profile, billing, team management, danger zone |
| `/web-table` | Data tables: TanStack Table v8, sorting, filtering, pagination, bulk actions |
| `/web-review` | Quality gate: 38+/40 required score, fix loop |
| `/web-deploy` | Deploy: Vercel or Railway, bundle audit, smoke test |
| `/web-fix` | Targeted bug fixing with context awareness |
| `/premium-website` | Suite contract — saas-build reads this file to enforce all rules |

**Orchestrators:**
- `/saas-build` — runs the full pipeline autonomously from brief to deploy (8 phases)
- `/saas-improve` — 6-agent parallel improvement swarm for post-launch quality

---

### SaaS Product Tools

| Skill | What it does |
|-------|-------------|
| `saas-build` | Full autonomous SaaS build — 8 phases from idea to deployed product |
| `saas-improve` | 6-agent parallel swarm: scan, prioritise, execute, deploy |
| `autopilot` | Autonomous project progression — keeps building while you're away |
| `dashboard-design` | Enterprise dashboard expert grounded in 40-product research corpus |
| `scaffold` | Project/feature/module scaffolding |
| `product-add` | Add features to existing products |
| `saas-health` | ARR, MRR, churn, CAC, LTV, NRR, quick ratio benchmarking |

---

### Project & Knowledge Management

| Skill | What it does |
|-------|-------------|
| `notion` | Create/update Notion pages with enforced project structure |
| `project-doc` | Create Notion master doc + local memory file for any project |
| `project-refresh` | Re-inject project context mid-conversation from Notion |
| `project-review` | Deep strategic review: competitive landscape, gap analysis, roadmap |
| `project-manager` | Full lifecycle: scope, phases, milestones, UAT, status reporting |
| `project-health` | Portfolio health dashboard and risk matrix |
| `handoff` | Session handoff document for seamless context transfer |
| `sync-knowledge-base` | Sync skills/commands to GitHub + update Notion docs |

---

### Power Platform & Microsoft

| Skill | What it does |
|-------|-------------|
| `dynamics365-crm-architect` | D365 CRM architecture, model-driven apps, configuration |
| `dataverse-data-model` | Dataverse schema design, relationships, choice fields |
| `power-automate-engineer` | Cloud flows, desktop flows, connectors, adaptive cards |
| `power-platform-alm` | Solutions, environment strategy, CI/CD, governance |
| `power-platform-integration` | Integration patterns: MuleSoft, custom connectors, webhooks, Azure Service Bus |

---

### Product & Strategy

| Skill | What it does |
|-------|-------------|
| `prd` | Product Requirements Document generation |
| `code-to-prd` | Reverse-engineer a codebase into a PRD |
| `rice` | RICE framework scoring and ranking |
| `sprint-plan` | Sprint plan with capacity allocation and user stories |
| `sprint-health` | Sprint health scoring with velocity trends |
| `okr` | Cascading OKRs from company to team level |
| `competitive-matrix` | Weighted competitive analysis matrices |
| `customer-journey` | End-to-end journey mapping with touchpoints and pain points |
| `persona` | Data-driven user personas with JTBD |
| `user-story` | INVEST-compliant stories with Given/When/Then |
| `pricing-model` | Pricing strategy, tiers, and page structure |
| `pitch-deck` | Investor pitch deck with narrative arc |

---

### Content & Marketing Commands

| Skill | What it does |
|-------|-------------|
| `linkedin-post` | Viral LinkedIn post with carousel plan |
| `scroll-stop-build` | Apple-style scroll-driven video website |
| `scroll-stop-prompt` | AI prompts for scroll-stopping product content |
| `brand-dna` | Brand reverse-engineering for AI image generation |
| `ad-creative` | AI ad creative prompts (Nano Banana 2 / Higgsfield) |
| `seo-strategy` | Single-article optimisation or site-wide SEO audit |
| `stock-photos` | Free stock photo finder with cultural specificity |
| `job-description` | Inclusive job descriptions |

---

### Engineering & DevOps

| Skill | What it does |
|-------|-------------|
| `senior-frontend` | React 18, Vite, TypeScript, Tailwind, shadcn/ui |
| `senior-backend` | FastAPI, Python, Supabase, PostgreSQL |
| `senior-devops` | Railway, Vercel, GitHub Actions, Docker |
| `senior-qa` | Playwright E2E, Vitest, pytest |
| `code-reviewer` | Deep review: security, performance, logic bugs |
| `incident-commander` | Production incident response |
| `stripe-integration-expert` | Stripe payments, subscriptions, webhooks |
| `a11y-audit` | WCAG 2.2 accessibility audit with auto-fix |
| `tdd` | Test-driven development workflows |
| `tech-debt` | Scan, prioritise, and report technical debt |
| `pipeline` | CI/CD pipeline generation (GitHub Actions, GitLab CI) |
| `architecture` | ADRs, system design docs, tech stack recommendations |
| `api-docs` | API documentation and OpenAPI spec generation |
| `validate` | Stress-test plans and architectures |
| `decide` | Structured technology decision framework |
| `design` | Comprehensive system architecture design |

---

### Inherited from Fork (196 skills)

The following domains were part of the [original repo](https://github.com/alirezarezvani/claude-skills) by Alireza Rezvani:

| Domain | Count | Directory | Highlights |
|--------|-------|-----------|------------|
| **Engineering Team** | 28 | [engineering-team/](engineering-team/) | Senior roles (frontend, backend, fullstack, DevOps, QA, SecOps, ML, data, CV), Playwright pro, self-improving agent, MS365 tenant manager |
| **Engineering (POWERFUL)** | 32 | [engineering/](engineering/) | Agent designer, RAG architect, database designer, Terraform, Helm, dependency auditor, release manager |
| **Marketing** | 46 | [marketing-skill/](marketing-skill/) | Content (8), SEO (5), CRO (6), channels (6), growth (4), intelligence (4), sales (2) |
| **C-Level Advisory** | 30 | [c-level-advisor/](c-level-advisor/) | Full C-suite (CEO to CISO), board meetings, culture, legal, M&A, hiring |
| **Product Team** | 15 | [product-team/](product-team/) | PM toolkit, agile PO, UX researcher, UI design system, SaaS scaffolder |
| **Project Management** | 6 | [project-management/](project-management/) | Senior PM, Scrum master, Jira, Confluence, Atlassian admin |
| **Regulatory & QM** | 12 | [ra-qm-team/](ra-qm-team/) | ISO 13485, MDR 2017/745, FDA 510(k), ISO 27001, GDPR, CAPA |
| **Business Growth** | 6 | [business-growth/](business-growth/) | Customer success, sales engineer, revenue ops, contracts |
| **Finance** | 2 | [finance/](finance/) | Financial analyst, SaaS metrics coach |
| **Web Design** | 4 | [web-design/](web-design/) | Lottie search, web design guidelines |

---

## Agents

59 autonomous agent definitions in [agents/](agents/). Each is a standalone `.md` file that defines an agent's role, expertise, decision framework, and output format.

### C-Suite & Advisory (17)

| Agent | Domain |
|-------|--------|
| `cs-ceo-advisor` | Company vision, fundraising, board prep |
| `cs-cfo-advisor` | Financial modelling, runway, fundraising strategy |
| `cs-cto-advisor` | Tech strategy, engineering scaling, architecture governance |
| `cs-cmo-advisor` | Brand, growth model, marketing budget, CAC/LTV |
| `cs-coo-advisor` | Strategy execution, OKRs, process design |
| `cs-cpo-advisor` | Product portfolio, PMF, north star metrics |
| `cs-cro-advisor` | Revenue forecasting, NRR, pricing, pipeline |
| `cs-chro-advisor` | Hiring, compensation, org structure, retention |
| `cs-ciso-advisor` | Security risk, compliance (SOC 2, ISO 27001, HIPAA) |
| `cs-chief-of-staff` | Multi-role decision routing and synthesis |
| `cs-board-advisor` | Board decks, investor updates, fundraising narratives |
| `cs-founder-coach` | Leadership evolution, delegation, energy management |
| `cs-legal-advisor` | Contracts, NDAs, ToS, privacy policies |
| `cs-ma-advisor` | M&A strategy, due diligence, integration planning |
| `cs-scenario-war-room` | Cross-functional scenario planning for compound risks |
| `cs-partnerships` | Partnership identification, structuring, activation |
| `cs-orchestrator` | Multi-agent task decomposition and parallel delegation |

### Engineering & Architecture (15)

| Agent | Domain |
|-------|--------|
| `cs-senior-engineer` | System design, code review, architecture |
| `cs-devops` | Cloud, Terraform, Kubernetes, CI/CD |
| `cs-sre` | SLOs, error budgets, post-mortems, alert tuning |
| `cs-engineering-lead` | Team coordination, incident response, cross-functional delivery |
| `cto-architect` | New architecture design from scratch |
| `cto-orchestrator` | Routes to architect or mentor based on need |
| `strategic-cto-mentor` | Stress-tests plans through 7-dimension evaluation |
| `systems-architect` | Evidence-based architecture with trade-off analysis |
| `database-designer` | Schema design, indexes, migrations, query optimisation |
| `migration-architect` | Zero-downtime system migrations |
| `observability-designer` | SLI/SLO frameworks, monitoring, runbooks |
| `performance-tuner` | Profiling and bottleneck identification |
| `mcp-server-builder` | REST API to MCP server conversion |
| `rag-architect` | RAG pipeline design (chunking, embeddings, retrieval) |
| `test-engineer` | Comprehensive test strategy across all levels |

### Product & Growth (10)

| Agent | Domain |
|-------|--------|
| `cs-product-manager` | Feature prioritisation, PRDs, sprint stories |
| `cs-product-strategist` | Product vision, market positioning, portfolio strategy |
| `cs-product-analyst` | KPIs, A/B tests, funnel analysis |
| `cs-ux-researcher` | Research planning, personas, journey maps, usability tests |
| `cs-project-manager` | Sprint planning, Jira/Confluence, Scrum ceremonies |
| `cs-growth-strategist` | Pipeline ops, revenue forecasting, GTM strategy |
| `cs-customer-success` | Onboarding, QBRs, health scores, save playbooks |
| `cs-revenue-ops` | Pipeline analysis, forecast accuracy, GTM efficiency |
| `cs-sales-coach` | Scripts, discovery frameworks, objection handling |
| `cs-sales-engineer` | RFP responses, POC planning, technical proposals |

### Marketing & Content (6)

| Agent | Domain |
|-------|--------|
| `cs-content-creator` | Blog posts, social content, brand voice, email copy |
| `cs-demand-gen-specialist` | Paid acquisition, lead gen, campaign optimisation |
| `cs-seo-specialist` | Organic search, GEO, technical SEO, schema |
| `cs-employer-brand` | Careers page CRO, EVP, Glassdoor strategy |
| `cs-reputation-manager` | Review management, monitoring, negative press |
| `cs-data-analyst` | Dashboards, cohort analysis, funnel diagnostics |

### Specialist (11)

| Agent | Domain |
|-------|--------|
| `cs-financial-analyst` | Financial modelling, valuation, budget analysis |
| `cs-ai-advisor` | AI maturity, automation mapping, data readiness |
| `cs-audit-specialist` | Multi-suite website auditing |
| `cs-quality-regulatory` | ISO 13485, EU MDR, FDA 510(k), ISO 27001 |
| `cs-workspace-admin` | Google Workspace automation via gws CLI |
| `agent-designer` | Multi-agent system architecture |
| `api-design-reviewer` | REST API linting, breaking changes, security |
| `codebase-onboarding` | Auto-generate onboarding docs from codebase |
| `pr-review-expert` | Blast radius analysis, security scan, test coverage delta |
| `refactor-expert` | Code smell detection, SOLID principles, modernisation |
| `root-cause-analyzer` | Systematic debugging for complex/recurring issues |

---

## Commands

59 slash commands in [commands/](commands/). These are the user-facing triggers for skills.

<details>
<summary>Full command list</summary>

| Command | What it triggers |
|---------|-----------------|
| `/a11y-audit` | WCAG 2.2 accessibility scan |
| `/ad-creative` | AI ad creative prompts |
| `/agent-brief` | Portable context brief for subagents |
| `/api-docs` | API documentation generation |
| `/architecture` | ADR and system design docs |
| `/brand-dna` | Brand reverse-engineering |
| `/changelog` | Changelog from git history |
| `/code-to-prd` | Codebase to PRD |
| `/competitive-matrix` | Competitive analysis matrix |
| `/customer-journey` | Journey mapping |
| `/decide` | Technology decision framework |
| `/design` | System architecture design |
| `/financial-health` | Financial ratio analysis |
| `/google-workspace` | Google Workspace diagnostics |
| `/handoff` | Session handoff document |
| `/job-description` | Job description writer |
| `/linkedin-post` | LinkedIn post generator |
| `/okr` | OKR generation |
| `/parallel-audit` | Multi-suite parallel audit |
| `/persona` | User persona generation |
| `/pipeline` | CI/CD pipeline generation |
| `/pitch-deck` | Investor pitch deck |
| `/plugin-audit` | Skill/agent quality audit |
| `/prd` | Product Requirements Document |
| `/premium-website` | Web suite reference |
| `/pricing-model` | Pricing strategy design |
| `/product-add` | Add feature to product |
| `/project-health` | Portfolio health dashboard |
| `/retro` | Sprint retrospective analysis |
| `/review` | Code/product review |
| `/rice` | RICE prioritisation |
| `/saas-build` | Full SaaS build pipeline |
| `/saas-health` | SaaS metrics benchmarking |
| `/saas-improve` | Post-launch improvement swarm |
| `/scaffold` | Project scaffolding |
| `/scroll-stop-build` | Scroll-driven video website |
| `/scroll-stop-prompt` | Scroll-stop content prompts |
| `/seo-auditor` | SEO audit |
| `/seo-strategy` | SEO optimisation |
| `/sprint-health` | Sprint health scoring |
| `/sprint-plan` | Sprint planning |
| `/standup` | Async standup formatting |
| `/sync-knowledge-base` | Sync to GitHub + Notion |
| `/tdd` | Test-driven development |
| `/tech-debt` | Technical debt analysis |
| `/usage-report` | Skill usage analytics |
| `/user-story` | User story generation |
| `/validate` | Plan stress-testing |
| `/vercel-react-best-practices` | Vercel + React patterns |
| `/web-animations` | Framer Motion patterns |
| `/web-component` | Component builder |
| `/web-deploy` | Deploy to Vercel/Railway |
| `/web-fix` | Bug fixing |
| `/web-page` | Page builder |
| `/web-review` | Quality gate (38+/40) |
| `/web-scaffold` | Project bootstrap |
| `/web-scope` | Scope definition |
| `/web-stripe` | Stripe integration |
| `/web-supabase` | Supabase backend |

</details>

---

## Installation

### Claude Code

```bash
# Clone the repo
git clone https://github.com/Mrsavage92/skills-library.git

# Copy skills you want to use
cp -r skills-library/skills/autopilot ~/.claude/skills/
cp -r skills-library/skills/saas-build ~/.claude/skills/

# Copy agents
cp skills-library/agents/cs-ceo-advisor.md ~/.claude/agents/

# Copy commands
cp skills-library/commands/saas-build.md ~/.claude/commands/
```

### Install everything

```bash
git clone https://github.com/Mrsavage92/skills-library.git
cp -r skills-library/skills/* ~/.claude/skills/
cp -r skills-library/agents/*.md ~/.claude/agents/
cp -r skills-library/commands/*.md ~/.claude/commands/
```

---

## Repo Structure

```
skills-library/
  skills/               118 skills (audit suites, web pipeline, SaaS tools, Power Platform)
  agents/               59 agent definitions + team-based subdirectories
  commands/             59 slash command triggers
  engineering-team/     28 engineering role skills (from fork)
  engineering/          32 POWERFUL-tier engineering skills (from fork)
  marketing-skill/      46 marketing skills (from fork)
  c-level-advisor/      30 C-suite advisory skills (from fork)
  product-team/         15 product skills (from fork)
  project-management/   6 PM skills (from fork)
  ra-qm-team/          12 regulatory/QM skills (from fork)
  business-growth/      6 business growth skills (from fork)
  finance/              2 finance skills (from fork)
  web-design/           4 web design utilities (from fork)
  docs/                 Documentation site source
  scripts/              Conversion and install scripts
  templates/            Skill authoring templates
  standards/            Quality standards
```

---

## Credits

This repo is a fork of [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) by Alireza Rezvani, which provided the foundational 196 skills across engineering, marketing, C-level advisory, product, project management, regulatory, business growth, and finance domains.

The following were added on top of that foundation:
- 118 skills in `skills/` — audit suites, premium website pipeline, SaaS build/improve, Power Platform, GEO, project management, and more
- 59 agent definitions — full C-suite advisory fleet, engineering specialists, growth and marketing agents
- 38 additional commands — web pipeline, audit orchestrators, content tools

---

## License

MIT — see [LICENSE](LICENSE) for details.
