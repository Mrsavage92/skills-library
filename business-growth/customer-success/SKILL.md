---
name: "customer-success"
description: "Customer Success Manager for health scoring, onboarding workflows, churn prediction, retention strategy, QBR preparation, and expansion opportunity identification. Use when building a CS programme, identifying at-risk accounts, planning business reviews, designing onboarding journeys, or scoring expansion opportunities."
Name: "Customer Success"
  Tier: "STANDARD"
  Category: "Business Growth"
  Dependencies: "None"
  Author: "claude-skills"
  Version: "2.1.2"
---

# Customer Success Manager

## Overview

Customer Success is the revenue engine of SaaS — retention and expansion drive NRR above 100%. This skill covers the full CS lifecycle from onboarding to renewal, including health scoring, churn prediction, QBR design, and expansion playbooks.

## When to Use

- Building or improving a customer health scoring model
- Identifying at-risk accounts before they churn
- Designing or improving customer onboarding
- Preparing for a Quarterly Business Review (QBR)
- Identifying upsell/expansion opportunities
- Setting up CS metrics and reporting

## Quick Start

```
# Health scoring
Share your customer data (usage, support tickets, NPS, ARR) → health score model

# At-risk identification
Paste customer metrics → I'll flag red/amber accounts with recommended actions

# QBR preparation
Customer name + goals + usage data → full QBR deck structure
```

## Customer Health Score Model

### Scoring Dimensions (weight to your context)
| Dimension | Weight | Green | Amber | Red |
|-----------|--------|-------|-------|-----|
| Product usage (DAU/MAU) | 30% | > 60% | 30–60% | < 30% |
| Feature adoption (key features used) | 20% | > 70% | 40–70% | < 40% |
| Support ticket volume/severity | 15% | 0–1/mo | 2–3/mo | 4+/mo |
| NPS / CSAT | 15% | > 8 | 6–8 | < 6 |
| Engagement (logins, emails opened) | 10% | Weekly | Monthly | < Monthly |
| Renewal risk signals | 10% | Renewing | Uncertain | At risk |

**Composite score:** Weighted average → Green (70–100), Amber (40–69), Red (0–39)

## Onboarding Workflow

### Phase 1: Kickoff (Day 1–7)
- Confirm success criteria and primary use case
- Identify champion and economic buyer
- Set up integration / data import
- Schedule 30-day check-in

### Phase 2: Activation (Day 7–30)
- Core feature adoption milestone achieved
- First value moment documented (time-to-value)
- Training completed for key users
- Success plan signed off

### Phase 3: Adoption (Day 30–90)
- Breadth of usage across team/seats
- Integration with key workflows confirmed
- Case study / reference discussion initiated

### Phase 4: Retention (Ongoing)
- Monthly/quarterly check-ins
- Usage review against success criteria
- Renewal conversation at 90-day mark

## QBR Template Structure
1. **Executive Summary** — progress vs goals from last QBR
2. **Usage & Adoption** — metrics vs benchmarks
3. **ROI delivered** — quantified business value
4. **Roadmap alignment** — upcoming features relevant to their goals
5. **Goals for next quarter** — 3 specific, measurable outcomes
6. **Risks & mitigations** — blockers to success

## Expansion Playbook
| Signal | Action | Timing |
|--------|--------|--------|
| Hitting usage limits | Upsell to higher tier | Proactive, before friction |
| New team/department | Land-and-expand outreach | When new hire announced |
| Positive NPS (9–10) | Reference/case study + expansion ask | Within 2 weeks of score |
| New use case discovered | Cross-sell or new SKU | During QBR |
| Champion changes jobs | Re-engage at new company | 30 days after departure |

## Key Metrics
- **NRR** (Net Revenue Retention) — target > 110% for growth-stage
- **GRR** (Gross Revenue Retention) — target > 90%
- **Time-to-Value** — days from contract to first value moment
- **Churn rate** — monthly and annual by segment
- **Expansion MRR** — upsell + cross-sell as % of beginning MRR
- **CSM coverage ratio** — ARR per CSM (benchmark: $1–2M per CSM)

## Related Skills
- cs-growth-strategist
- pricing-strategist
- cs-product-analyst


<!-- Auto-generated required sections -->

## Name

Customer Success

## Description

Customer Success Manager skill for Claude Code. Provides workflows, templates, and automation tools.

## Features

- Production-ready workflows
- Step-by-step guidance
- Reusable templates
- Best practices embedded

## Usage

Describe your task to Claude and this skill will be applied automatically based on context.

```
# Trigger this skill by describing your need:
"Help me with customer success manager"
```

## Examples

**Example 1:** Ask Claude to apply this skill to your current project.

**Example 2:** Reference the workflows in SKILL.md to guide your implementation.
