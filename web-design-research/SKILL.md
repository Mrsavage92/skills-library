---
name: web-design-research
description: >
  Pre-build design research for SaaS products. Researches competitors, queries 21st.dev
  for product-specific component patterns, finds LottieFiles animations, defines a unique
  design system (color palette, personality, layout), and plans a multi-page marketing
  structure. Runs BEFORE web-scope. Outputs DESIGN-BRIEF.md which all subsequent phases
  read. Every product must look and feel different from every other product.
---

# Skill: /web-design-research

**This runs BEFORE /web-scope on every new product. Not optional.**

Without this phase, every product gets the same dark navy + electric blue template. This skill forces uniqueness by grounding every design decision in the product's specific industry, emotion, and users.

---

## The Problem This Solves

Products look identical when scope picks a color without asking WHY that color fits this product. A compliance platform and a trades licensing tool have completely different emotional registers. Enterprise analytics and aged care management are for completely different people. Generic dark themes are a red flag that no research was done.

This skill produces `DESIGN-BRIEF.md` — a locked design contract that `web-scope`, `web-scaffold`, and every `web-page` call must read and follow.

---

## Step 1 — Product Personality Analysis

Ask and answer these questions internally before touching any design tool:

**What industry/category is this?**
Map to one of these 8 personalities. Pick the ONE that fits best:

| Personality | Industries | Emotional register | User type |
|---|---|---|---|
| **Enterprise Authority** | Compliance, legal, audit, regulation | Trust, seriousness, stability | Accountants, lawyers, compliance officers |
| **Data Intelligence** | Analytics, CI, monitoring, intelligence | Precision, depth, insight | Analysts, ops teams, growth teams |
| **Trusted Productivity** | HR, project management, CRM, operations | Collaboration, clarity, momentum | Team leads, PMs, HR managers |
| **Premium Professional** | Property, consulting, advisory, finance | Sophistication, value, status | Executives, advisors, agents |
| **Bold Operator** | Trades, construction, logistics, field service | Reliability, action, strength | Tradespeople, site managers, supervisors |
| **Health & Care** | Aged care, NDIS, health, disability | Warmth, human connection, safety | Carers, families, clinical staff |
| **Growth Engine** | Marketing, sales, SaaS growth, creative | Energy, momentum, ambition | Founders, marketers, growth leads |
| **Civic/Government** | Migration, government services, public records | Authority, clarity, access | Citizens, agents, administrators |

**What is the user feeling when they open this product?**
(e.g. "Under pressure to comply", "Looking for competitive edge", "Worried about a client", "Trying to win more business")

**What must the design communicate in 3 seconds?**
(e.g. "This is official and trustworthy", "This is powerful and precise", "This is friendly and easy")

Write these answers down — they drive every decision below.

---

## Step 2 — Competitor Design Research

Run 2-3 WebSearch queries relevant to this product category:

```
WebSearch: "[product category] SaaS design 2024 2025"
WebSearch: "[product keyword] platform UI screenshots"
WebSearch: "best [industry] software design inspiration"
```

Scan results for:
- What colors dominate this category?
- Do competitors use dark or light themes?
- What design conventions are so common they're table stakes?
- What would make THIS product stand out as different or more premium?

Document findings: 2-3 sentences. This informs the differentiation choice.

---

## Step 3 — Unique Color System

Based on personality (Step 1) and research (Step 2), select a color system.

**Rules:**
- Never use `hsl(213 94% 58%)` (the default electric blue) unless the product is specifically about technology infrastructure or developer tooling — it has been used for every prior product
- Never use `hsl(220 35% 4%)` dark navy as the background unless research shows competitors actively avoid it (meaning you'd stand out by using it)
- The color must have a REASON tied to the product's personality
- Light-first vs dark-first must match the user type: professionals who work in bright offices (compliance, property, HR) → light-first; data-heavy power users → dark-first

**Palette library by personality:**

### Enterprise Authority (compliance, audit, legal)
```
Primary:     hsl(155 38% 36%)   -- Deep forest green: regulation, stability, growth
Background:  hsl(150 20% 97%)   -- Off-white (light-first — compliance users work in offices)
Background dark alt: hsl(160 18% 8%)
Accent:      hsl(42 85% 52%)    -- Amber for warnings/deadlines (compliance urgency)
Mode: light-first
Reference: Xero.com, MYOB, ServiceNSW design
```

### Data Intelligence (analytics, CI, monitoring)
```
Primary:     hsl(199 92% 52%)   -- Electric cyan: precision, data, technology
Background:  hsl(220 40% 4%)    -- Deep space navy (data analysts work in dark modes)
Surface:     hsl(222 32% 8%)    -- Elevated card surface
Accent:      hsl(142 68% 45%)   -- Green for positive signals
Mode: dark-first
Reference: Datadog, Grafana, Linear.app
```

### Trusted Productivity (HR, PM, CRM)
```
Primary:     hsl(175 55% 42%)   -- Teal: collaboration, trust, forward motion
Background:  hsl(180 20% 97%)   -- Warm white (light-first)
Surface:     hsl(180 15% 100%)
Accent:      hsl(38 90% 55%)    -- Orange for priority/actions
Mode: light-first
Reference: Notion, Asana, Intercom
```

### Premium Professional (property, consulting, advisory)
```
Primary:     hsl(42 82% 48%)    -- Warm gold/amber: value, premium, opportunity
Background:  hsl(220 25% 7%)    -- Dark charcoal (premium dark feel)
Surface:     hsl(220 20% 11%)
Accent:      hsl(0 0% 98%)      -- Near-white text and borders
Mode: dark-first
Reference: Stripe.com, Mercury bank, CBRE
```

### Bold Operator (trades, construction, logistics)
```
Primary:     hsl(25 88% 50%)    -- Strong orange: reliability, action, energy
Background:  hsl(220 18% 8%)    -- Dark charcoal
Surface:     hsl(220 15% 12%)
Accent:      hsl(200 80% 55%)   -- Sky blue for secondary actions
Mode: dark-first (field workers use phones in bright sun — high contrast)
Reference: ServiceNow, SafetyCulture, Procore
```

### Health & Care (aged care, NDIS, health)
```
Primary:     hsl(155 48% 42%)   -- Sage green: life, care, wellbeing
Background:  hsl(150 30% 97%)   -- Soft warm white (light-first — caring, accessible)
Surface:     hsl(0 0% 100%)
Accent:      hsl(200 65% 55%)   -- Calm blue for information
Mode: light-first (accessibility critical — WCAG AA minimum)
Reference: HealthEngine, HotDoc, NDIS Commission site
```

### Growth Engine (marketing, sales, growth)
```
Primary:     hsl(270 75% 58%)   -- Purple: creativity, ambition, premium energy
Background:  hsl(265 30% 6%)    -- Very dark purple-black
Surface:     hsl(265 25% 10%)
Accent:      hsl(340 80% 58%)   -- Hot pink for CTAs and highlights
Mode: dark-first (marketers love dark dashboards)
Reference: Webflow, Figma, Beehiiv
```

### Civic/Government (migration, government services)
```
Primary:     hsl(210 78% 42%)   -- Institutional blue: authority, trust, access
Background:  hsl(0 0% 98%)      -- Clean white (government clarity)
Surface:     hsl(210 20% 97%)
Accent:      hsl(25 80% 50%)    -- Warm orange for actions/urgency
Mode: light-first (must be highly accessible)
Reference: Australia.gov.au, ServiceNSW, MyGov
```

---

## Step 4 — 21st.dev Component Research

Call `mcp__magic__21st_magic_component_inspiration` with 6 targeted queries. Each query must be SPECIFIC to this product's personality and features — not generic "dark SaaS."

**Query formula:**
1. **Hero:** `[personality adjective] [product category] hero section [theme]`
   - Examples: "compliance authority hero section clean light", "data intelligence hero dark cyan animated", "trades management hero bold orange dark"
2. **Feature display:** `[product's primary feature] feature card [personality]`
   - Examples: "audit checklist feature card enterprise", "company intelligence data card dark", "construction license tracker card orange"
3. **Navigation:** `[personality] sidebar navigation [theme]`
   - Examples: "clean enterprise sidebar light green", "data dense dark sidebar with status", "minimal light sidebar teal"
4. **Social proof / trust:** `[industry] trust signals testimonials [theme]`
   - Examples: "legal compliance logo trust section", "analytics platform testimonial dark"
5. **Pricing section:** `[personality] pricing table [theme]`
   - Examples: "enterprise authority pricing cards light", "SaaS dark pricing table highlighted tier"
6. **Lottie/illustration placeholder:** What concept needs an animated illustration in this product? (onboarding, empty states, hero graphic)
   - Examples: "document compliance check animation", "company search magnify animation", "construction blueprint animation"

For each query, study the returned component and note:
- What makes it distinctive?
- Which patterns to adopt (layout, hover effects, border style, icon usage)
- What to avoid

Also call `mcp__magic__21st_magic_component_builder` for the hero animated background with product-specific parameters:
- Compliance: subtle document grid, moving contract lines, gentle opacity
- Intelligence/Analytics: moving data dots/nodes, network graph animation, particle field
- Trades: geometric blueprint grid, subtle angle lines
- Health: soft floating circles/bubbles, wave motion

---

## Step 5 — LottieFiles Animation Research

LottieFiles provides free JSON animations embeddable in React via `@lottiefiles/react-lottie-player`.

Search for 3 animations relevant to this product:

```
WebSearch: "lottiefiles [product keyword] free animation JSON"
WebSearch: "lottiefiles [action word] animation download"
```

Target use cases for animations (by location in the UI):
1. **Hero illustration** — replaces static mockup in cases where no real app exists yet OR supplements it (above/beside the product mockup)
2. **Empty states** — each major empty state should have a small (100-150px) lottie instead of just an icon
3. **Success/completion states** — onboarding wizard completion, form submission success, action confirmed
4. **Loading/processing** — for operations that take 1-3 seconds (not for normal skeleton loaders — for true wait states like "Analyzing..." or "Generating...")

**Integration pattern:**
```tsx
// Install: npm install @lottiefiles/react-lottie-player
import { Player } from '@lottiefiles/react-lottie-player'

// For remote JSON (LottieFiles CDN):
<Player
  autoplay
  loop
  src="https://lottiefiles.com/animations/[id]"
  style={{ height: '180px', width: '180px' }}
/>

// For local JSON (downloaded):
import animationData from '@/assets/animations/empty-search.json'
<Player autoplay loop src={animationData} style={{ height: '120px' }} />
```

**useReducedMotion respect:**
```tsx
import { useReducedMotion } from 'framer-motion'
const shouldReduce = useReducedMotion()
{!shouldReduce && <Player autoplay loop src={...} />}
```

Document the 3 animation URLs/IDs found. If nothing perfect is found, note the search terms and closest alternatives — do not skip this step.

---

## Step 6 — Multi-Page Marketing Structure

**The landing page is NOT a single scrollable page.** It is a set of routes that together form the marketing site.

Choose the right tier based on product complexity:

### Tier 1 — Micro SaaS (simple utility, < 5 features)
```
/ .............. Hero + 3 feature highlights + pricing + CTA (all on one page is acceptable)
/signin ........ Auth
```
→ Use only if the product is genuinely simple. Otherwise use Tier 2.

### Tier 2 — Standard SaaS (most products)
```
/ .............. Hero (headline + subheadline + CTA + product preview) — NO scroll sections
/features ....... Full feature breakdown with detailed cards, how-it-works steps, comparisons
/pricing ........ Dedicated pricing page with plan cards, FAQ, guarantee
/signin ......... Auth (sign in + create account)
```

### Tier 3 — Full Marketing Site (products competing in a crowded market)
```
/ .............. Hero only
/features ....... Feature deep dive
/how-it-works ... Step-by-step workflow with illustrations
/pricing ........ Full pricing + FAQ
/blog ........... SEO content hub (even if initially empty with 1-2 posts)
/about .......... Founder story + credibility
/contact ........ Contact form
/signin ......... Auth
```

**Which tier to use:** Default to Tier 2 for all products in this platform. The single-scroll landing page era is over — Google rewards pages that are focused and deep, not pages with 8 scroll sections.

**Per-page requirements for marketing pages:**

`/` — Hero page:
- Hero: headline + 1-line subheadline + 2 CTAs (primary CTA + secondary "see how it works")
- Single product visual (browser mockup OR lottie animation — not both)
- 3 trust stats (e.g. "10M+ AU entities", "14-day free trial", "No credit card")
- Maximum 2 scroll sections below hero: 1 social proof bar (logos/numbers) + 1 teaser to /features
- Clear nav link to /features and /pricing

`/features` — Features page:
- Section heading + paragraph intro
- 4-6 detailed feature blocks: icon + headline + 2-3 sentences + optional screenshot/mockup
- "How it works" 3-step process (numbered, horizontal on desktop)
- CTA at bottom linking to /pricing

`/pricing` — Pricing page:
- 2-3 plan cards (Tier 1 free/starter, Tier 2 pro highlighted, Tier 3 enterprise/agency)
- Feature comparison table below cards
- FAQ section (4-6 Q&As addressing objections)
- Money-back or "cancel anytime" trust signal
- CTA linking to /signin

---

## Step 7 — Write DESIGN-BRIEF.md

Write this file to the project root (or `apps/[product-slug]/` in monorepo):

```markdown
# [Product Name] — Design Brief

## Product Personality
- **Personality type:** [one of the 8]
- **User emotion on open:** [what they're feeling]
- **3-second message:** [what design communicates immediately]
- **Mode:** dark-first | light-first
- **Why this mode:** [reason tied to user type]

## Color System
- **Primary:** hsl([H] [S]% [L]%) — [name + reason]
- **Background:** hsl([H] [S]% [L]%)
- **Surface:** hsl([H] [S]% [L]%)
- **Accent:** hsl([H] [S]% [L]%) — [use case]
- **Color job:** Primary used ONLY for [X] + [Y]. Accent used for [Z].
- **NOT to use:** hsl(213 94% 58%) [reason it was rejected for this product]

## Typography
- **Font:** [choice + reason]
- **Heading weight:** 700 or 800
- **Tracking:** tight (-0.02em) | normal | wide

## Design References
- **Primary reference:** [site] — borrow [specific elements]
- **Secondary reference:** [site] — borrow [specific elements]
- **What to NOT copy from competitors:** [2-3 clichés in this industry to avoid]

## 21st.dev Components Selected
1. **Hero background:** [component type/description] — [what makes it product-specific]
2. **Feature cards:** [component type] — [why it fits this product's personality]
3. **Navigation:** [component type] — [dark/light, sidebar/top]
4. **[other selected components]**

## LottieFiles Animations
1. **Hero/onboarding illustration:** [URL or description] — location: [hero | onboarding step X]
2. **Empty state - [page name]:** [URL or description] — used when: [condition]
3. **Success state:** [URL or description] — used when: [condition]

## Marketing Site Structure
**Tier:** [1 | 2 | 3]

**Public pages:**
- `/` — [Hero brief]
- `/features` — [Features brief]
- `/pricing` — [Pricing brief]
- `/signin` — Auth

**App pages:**
- [List app routes]

## Design Anti-Patterns (banned for this product)
- [ ] Dark navy background (#0d1117 / hsl(220 35% 4%)) — [if banned, why]
- [ ] Electric blue primary (#3b82f6 equivalent) — [if banned, why]
- [ ] Gradient blobs as hero illustration
- [ ] Generic "3 feature cards with icons" without product-specific imagery
- [ ] Identical card patterns to the previous product built

## Build Order
1. / (Hero page)
2. /features
3. /pricing
4. /signin
5. /setup (onboarding)
6. /dashboard
7. [core feature pages in priority order]
8. /settings (last)
```

---

## Completion Check

Before handing off to `/web-scope`:
- [ ] Personality type identified and documented
- [ ] Competitor research done (2-3 searches) — findings documented
- [ ] Color palette selected with explicit rejection of default colors and documented WHY
- [ ] 6 x 21st.dev queries run — findings documented
- [ ] LottieFiles — 3 animations identified (or closest alternatives noted)
- [ ] Marketing site tier chosen (1/2/3) with multi-page structure
- [ ] DESIGN-BRIEF.md written to project root
- [ ] DESIGN-BRIEF.md explicitly different from previous products (no copy-paste of colors)

**Time budget:** This phase takes 5-10 minutes of research. Do not rush it. A product that looks identical to the last one means this phase was skipped.

---

## Handoff to web-scope

```
DESIGN-BRIEF.md written.

Product: [name]
Personality: [type]
Mode: [dark/light]-first
Primary: hsl([value]) — [name]
Marketing tier: [1/2/3] — [N] public pages + [N] app pages

Key differentiators vs previous builds:
- Color: [completely different from prior product, e.g. "forest green vs prior electric blue"]
- Layout: [what's different structurally]
- Animations: [lottie files to be used]
- 21st.dev: [key components sourced]

Next: /web-scope reads DESIGN-BRIEF.md as its primary input.
```
