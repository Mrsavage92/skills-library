---
name: web-design-research
description: >
  Pre-build design research for SaaS products. Researches competitors, runs targeted MCP queries
  for every mandatory landing page section, locks specific 21st.dev component choices per product
  type, defines a unique design system, and outputs DESIGN-BRIEF.md as the single source of truth.
  Runs BEFORE web-scope. Build skills (web-scaffold, web-page) read the Component Lock from
  DESIGN-BRIEF.md and do NOT re-run MCP queries. Every product must look genuinely different.
---

# Skill: /web-design-research

**Runs BEFORE /web-scope on every new product. Not optional.**

This skill is the only place MCP component decisions are made. Build skills execute the locked plan — they do not re-research. If this step is skipped, every product gets the same structure with different colors. That is not acceptable.

---

## The Problem This Solves

Two failure modes destroy landing page quality:

1. **Vague MCP calls during build** — "search for features section" at scaffold time returns whatever comes first, under time pressure. The build skill picks the top result and moves on. Every product gets Features 4.

2. **Re-running MCP per session** — different sessions make different choices for the same product. The hero section was BentoGrid in one session, Features 4 in the next. Incoherent result.

This skill front-loads all component decisions in one dedicated research session. DESIGN-BRIEF.md becomes the locked contract. Build skills execute it.

---

## Step 1 — Product Personality Classification

Map this product to ONE of 8 personalities. This drives every downstream decision.

| Personality | Industries | Emotional register | User type |
|---|---|---|---|
| **Enterprise Authority** | Compliance, legal, audit, regulation, finance | Trust, seriousness, stability | Accountants, lawyers, compliance officers |
| **Data Intelligence** | Analytics, CI, monitoring, business intelligence | Precision, depth, insight | Analysts, ops teams, growth teams |
| **Trusted Productivity** | HR, project management, CRM, scheduling | Collaboration, clarity, momentum | Team leads, PMs, HR managers |
| **Premium Professional** | Property, consulting, advisory, wealth management | Sophistication, value, status | Executives, advisors, high-net-worth users |
| **Bold Operator** | Trades, construction, logistics, field service | Reliability, action, strength | Tradespeople, site managers, supervisors |
| **Health & Care** | Aged care, NDIS, health, disability services | Warmth, human connection, safety | Carers, families, clinical staff |
| **Growth Engine** | Marketing SaaS, sales tools, creator tools | Energy, momentum, ambition | Founders, marketers, growth leads |
| **Civic/Government** | Migration, public records, government services | Authority, clarity, accessibility | Citizens, agents, administrators |

Answer these three before proceeding:
1. **Personality type:** [one of the 8 above]
2. **User emotion on open:** What is the user feeling when they arrive? (e.g. "Stressed about a compliance deadline", "Looking for competitive edge", "Worried about a client outcome")
3. **3-second message:** What must the design communicate before the user reads a word? (e.g. "This is official and trustworthy", "This is powerful and fast", "This is safe and caring")

---

## Step 2 — Competitor Design Research

**First: check if MARKET-BRIEF.md exists in the project root.** If it does, read the "Top 3 competitors" and "Features users consistently request" sections — these contain pre-fetched competitor data from Phase 0.25. Skip the WebSearch queries below and proceed directly to the analysis step. Do not duplicate research.

If MARKET-BRIEF.md does not exist, run these 4 WebSearch queries:

```
WebSearch: "[product category] SaaS website design 2025"
WebSearch: "[closest competitor] landing page hero"
WebSearch: "[closest competitor 2] landing page hero"
WebSearch: "best [industry] software landing page design"
```

From results, identify and document both angles:

**What's working (adopt or adapt):**
- Proven hero patterns — what are the top 2-3 competitors doing above the fold?
- Social proof formats that appear across multiple competitors
- CTA patterns — what's the dominant first CTA?

**What to avoid:**
- Dominant colors in this category
- Dark vs light prevalence
- Overused design motifs
- One visual gap — something no competitor is doing

Document in 5-6 sentences. This informs Step 3 (color), Step 4 (hero architecture), and component choices.

---

## Step 3 — Color System

Read `references/color-palettes.md` for the full palette library by personality type. Select based on personality + competitor research. Adjust hue/lightness slightly to create distance from any competitor using the same base.

**Hard rules (enforced here, not in the reference):**
- `hsl(213 94% 58%)` (electric blue) is banned unless this is a developer infrastructure tool
- Every color must have a written reason tied to the product's personality
- Mode (dark/light first) must match user environment

---

## Step 4 — Typography Lock

Read `references/typography-library.md` for font pairings by personality type and the full heading scale. Lock the chosen pair and heading scale in DESIGN-BRIEF.md.

---

## Step 5 — Hero Architecture Decision

Choose the hero layout pattern before calling MCP. The pattern drives the hero MCP query in Step 6.

| Pattern | Best for | Description |
|---|---|---|
| **Centered** | Enterprise Authority, Trusted Productivity, Civic | Headline centered, subheadline centered, CTAs centered, product mockup full-width below fold |
| **Split-pane** | Data Intelligence, AI products, Growth Engine | Text block left (40%), animated product output right (60%) — typewriter or live data |
| **Full-screen immersive** | Bold Operator, Premium Professional | Background fills viewport, headline overlaid large, single CTA, product mockup inset — add subtle film grain overlay (opacity 0.03-0.05) for texture |
| **Minimal editorial** | Premium Professional (alternative), Health & Care | Giant display typography dominant, minimal visual, emotional photography or soft illustration |

Lock this choice in DESIGN-BRIEF.md.

---

## Step 6 — 21st.dev Component Lock

Read `references/component-selection.md` for the full selection criteria tables and all 11 MCP search queries. Run every query using `mcp__magic__21st_magic_component_inspiration`. Lock every choice in DESIGN-BRIEF.md.

**Tool usage rule:** Only `mcp__magic__21st_magic_component_inspiration` is called here. `mcp__magic__21st_magic_component_builder` is NEVER called in research — it is called by build skills (web-scaffold, web-page) when constructing the actual component.

---

## Step 7 — LottieFiles Animation Research

Find 3 product-specific animations for empty states, success moments, and loading states.

```
WebSearch: "lottiefiles [product keyword] free animation"
WebSearch: "lottiefiles [core action of product] animation loop"
```

Target placements:
1. **Empty state (primary feature page)** — shown when user has no data yet (100-120px)
2. **Success/completion state** — onboarding finish, form submitted, action confirmed (160-200px)
3. **Processing state** — AI generating, analysis running, search in progress (80-100px)

Integration:
```tsx
import { Player } from '@lottiefiles/react-lottie-player'
import { useReducedMotion } from 'framer-motion'

function LottieEmptyState({ src, height = 120 }: { src: string; height?: number }) {
  const shouldReduce = useReducedMotion()
  if (shouldReduce) return null
  return <Player autoplay loop src={src} style={{ height: `${height}px` }} />
}
```

If no exact match found: note the search terms used and closest alternatives. Never skip.

---

## Step 8 — Differentiation Audit

Use Glob with pattern `~/.claude/projects/*/memory/*.md` to find all project memory files. Read any that reference a SaaS product built with this suite — identify the last 2-3 products and their recorded color choices.

If memory files exist but contain no color data: check for `DESIGN-BRIEF.md` files in sibling project directories. If none found, document "no prior builds found" and continue.

For each of these 5 dimensions, confirm this product makes a **different choice** from recent builds:

| Dimension | This product's choice | Different from recent builds? |
|---|---|---|
| Primary color hue | `hsl([H] ...)` | Yes / No — [name the conflict if No] |
| Background mode | dark-first / light-first | Yes / No |
| Hero pattern | Centered / Split-pane / Full-screen / Minimal | Yes / No |
| Features layout | Border-grid / BentoGrid / List / Editorial | Yes / No |
| Section count | Micro (5) / Standard (9) / Full (11) | Yes / No |

If any dimension conflicts: change this product's choice before locking. See `references/color-palettes.md` for hue-shift guidance.

---

## Step 9 — Marketing Site Structure

Choose tier based on product complexity and competitive environment:

### Tier 1 — Micro SaaS (simple utility, under 5 features)
```
/         Hero + stats + 3 features + pricing + CTA (single scroll)
/auth   Auth
```

### Tier 2 — Standard SaaS (most products — default)
```
/             Hero page (full section stack: hero → logos → stats → features → testimonials → pricing → FAQ → CTA → footer)
/features     Deep feature breakdown + how-it-works steps + comparisons
/pricing      Dedicated pricing page + feature comparison table + FAQ + guarantee
/auth       Auth
```

### Tier 3 — Full Marketing Site (crowded market, SEO priority)
```
/              Hero page
/features      Feature deep dive
/how-it-works  Illustrated workflow walkthrough
/pricing       Full pricing + comparison + FAQ
/blog          SEO content hub
/about         Founder story + credibility
/auth          Auth (signup / login via tabs)
/signin        Login shortcut (redirects to /auth?tab=login)
```

Default: Tier 2. The single-scroll landing page era is over.

---

## Step 9b — Dashboard Design

If the marketing site structure includes a `/dashboard` route, run the `dashboard-design` skill now to lock the dashboard layout before build starts.

Read `~/.claude/skills/dashboard-design/SKILL.md` and complete:
1. Category classification (Analytics, Operations, Finance, HR, CRM, DevOps, Health, Civic)
2. Layout pattern — Sidebar nav or Top nav? Single-panel or split-panel?
3. KPI card spec — how many KPI cards? What metric + sparkline per card?
4. Primary chart type (Area, Bar, Funnel, Heatmap, Table)
5. Empty state design — what does a brand new user see? Must have a CTA.

Add a `## Dashboard Design` section to DESIGN-BRIEF.md with these 5 decisions locked.

---

## Step 10 — Write DESIGN-BRIEF.md

Read `references/design-brief-template.md` for the full template. Write the completed file to the project root.

This file is the single source of truth. Build skills read it — they do not re-research.

---

## Anti-Patterns

- **Generic MCP calls** — never use vague queries like "features section". Always use personality-specific queries from `references/component-selection.md`.
- **Re-running design research** — if DESIGN-BRIEF.md already exists in the project root, do not run this skill again. Read the existing brief and continue.
- **Electric blue `hsl(213 94% 58%)`** — banned for all non-developer-infrastructure products. No exceptions.
- **Picking components by personal preference** — every component choice must be justified by personality type and product criteria from `references/component-selection.md`.

---

## Completion Checklist

Before handoff to `/web-scope`:

- [ ] Personality type identified and justified
- [ ] 4 WebSearch competitor queries run — findings documented (color, mode, clichés)
- [ ] Color palette selected with explicit rejection of defaults + reasons
- [ ] Typography pair locked (not just "Inter")
- [ ] Hero architecture pattern chosen (Centered / Split-pane / Full-screen / Minimal)
- [ ] All 11 MCP queries run — one per mandatory section
- [ ] Each component choice recorded with query used + product-specific reason
- [ ] 3 LottieFiles animations found (or closest alternatives noted)
- [ ] Differentiation audit passed — 3+ dimensions differ from last build
- [ ] Marketing tier chosen (1/2/3)
- [ ] DESIGN-BRIEF.md written to project root with Component Lock table complete

**If any item is unchecked: do not hand off. Complete it first.**

---

## Handoff to /web-scope

Output this summary:

```
DESIGN-BRIEF.md written and locked.

Product: [name]
Personality: [type]
Mode: [dark/light]-first
Primary: hsl([value]) — [name]
Hero pattern: [Centered | Split-pane | Full-screen | Minimal]
Marketing tier: [1/2/3] — [N] public + [N] app pages

Component Lock summary:
- Background: [component]
- Hero: [component]
- Features: [component] — [BentoGrid or Features 4 and why]
- Testimonials: [component]
- Pricing: [component]
- FAQ: [component]

Differentiation vs last build:
- Color: [this product] vs [last product]
- Hero: [this pattern] vs [last pattern]
- Features: [this layout] vs [last layout]

Lottie animations:
- Empty state ([page]): [URL/description]
- Success state: [URL/description]
- Processing state: [URL/description]

Next: /web-scope reads DESIGN-BRIEF.md as its primary input.
web-scaffold reads Component Lock table — does NOT re-run MCP.
```

---

## Related Skills

- `/web-scope` — reads DESIGN-BRIEF.md to plan the build
- `/web-scaffold` — reads Component Lock table, does not re-run MCP
- `/web-page` — reads Component Lock, builds individual pages
- `/dashboard-design` — locks dashboard layout (called from Step 9b)
