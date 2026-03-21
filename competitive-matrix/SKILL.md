---
name: competitive-matrix
description: Build weighted competitive analysis matrices with gap analysis and market positioning maps. Use when evaluating competitors, preparing for a product launch, or deciding on feature prioritisation against the market.
version: 1.0
---

# Competitive Matrix Skill

## Purpose

Produces structured, weighted competitive analysis matrices with gap analysis, positioning maps, and strategic recommendations. Focused on the analytical output — use `market-competitors` first if you need raw competitor data gathering.

## When to Use

- Preparing for a product launch and need to map the competitive landscape
- Deciding feature prioritisation based on competitive gaps
- Presenting a competitive strategy to the board or investors
- Evaluating a potential market entry or pivot
- Running a quarterly competitive review

## Workflow

### Step 1 — Define Evaluation Dimensions

Identify 8-15 dimensions relevant to the market. Default set:

**Product dimensions:** Core functionality, UX quality, mobile experience, integrations, performance, customisation
**Commercial dimensions:** Pricing model, free tier, enterprise offer, support quality
**Strategic dimensions:** Brand strength, content/SEO presence, market share, funding/stability, roadmap transparency

### Step 2 — Assign Weights

Weight dimensions by strategic importance (must sum to 100):
- Critical differentiators: 10-15 points each
- Important but table-stakes: 5-8 points each
- Nice-to-have: 2-4 points each

### Step 3 — Score Competitors

Score each competitor 1-5 on each dimension:
- 5 = Best in class / clear leader
- 4 = Strong / above average
- 3 = Adequate / industry standard
- 2 = Weak / below average
- 1 = Missing / critical gap

Calculate weighted score: `sum(dimension_score × dimension_weight) / 100`

### Step 4 — Gap Analysis

For each dimension, identify:
- **Parity gaps** — competitors score ≥4, you score ≤3 → must close
- **Differentiation opportunities** — you score ≥4, competitors score ≤3 → amplify
- **Table-stakes** — everyone scores ≥4 → maintain, don't over-invest
- **Mutual weaknesses** — everyone scores ≤2 → potential category innovation opportunity

### Step 5 — Positioning Map

Plot 2x2 maps on the two dimensions that matter most for your ICP. Common axes:
- Simplicity ↔ Power
- Budget ↔ Premium
- Niche ↔ Broad
- Self-serve ↔ Enterprise

### Step 6 — Strategic Recommendations

Produce:
1. **Close list** — top 3 parity gaps to address in next 2 quarters
2. **Amplify list** — top 3 differentiators to double down on in messaging
3. **Ignore list** — dimensions where you choose not to compete
4. **Positioning statement** — one-paragraph differentiation narrative

## Output Format

```markdown
# Competitive Matrix — [Market] — [Date]

## Weighted Scores
| Dimension | Weight | [You] | [Comp A] | [Comp B] | [Comp C] |
|-----------|--------|-------|----------|----------|----------|
| ...       | ...    | ...   | ...      | ...      | ...      |
| **TOTAL** | 100    | XX.X  | XX.X     | XX.X     | XX.X     |

## Gap Analysis
### Parity Gaps (must close)
### Differentiation Opportunities (amplify)
### Mutual Weaknesses (innovate)

## Positioning Map
[2x2 ASCII or description]

## Strategic Recommendations
### Close (next 2 quarters)
### Amplify (messaging & roadmap)
### Ignore (deliberate non-compete)

## Positioning Statement
```

## Integration

- Feed gap analysis output into `rice` skill for feature prioritisation
- Feed positioning map into `market-copy` for messaging updates
- Feed competitor scores into `market-competitors` for deeper per-competitor profiles
- Use output with `okr` skill to set competitive OKR targets
