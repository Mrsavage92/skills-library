---
name: "sre"
description: "Site Reliability Engineer for SLO/SLI/SLA definition, error budget management, incident response, on-call runbook design, and chaos engineering. Use when defining reliability targets, investigating production incidents, tuning alerts, designing on-call rotations, or implementing observability for availability guarantees."
Name: "SRE"
  Tier: "STANDARD"
  Category: "Engineering"
  Dependencies: "None"
  Author: "claude-skills"
  Version: "2.1.2"
---

# Site Reliability Engineer

## Overview

SRE bridges development and operations — applying software engineering to reliability problems. This skill covers the full SRE practice: defining service level objectives, managing error budgets, running blameless post-mortems, and designing systems that fail gracefully.

## When to Use

- Defining or reviewing SLOs, SLIs, and SLAs for a service
- Investigating a production incident or outage
- Designing on-call rotations and escalation paths
- Tuning alert thresholds to reduce noise
- Running a blameless post-mortem
- Implementing chaos engineering or game days

## Quick Start

```
# Define SLOs for a service
Describe your service → I'll define SLIs, SLOs, and error budget policy

# Incident response
Paste your incident timeline → I'll structure a blameless post-mortem

# Alert tuning
Share your current alerts + false positive rate → I'll recommend threshold changes
```

## Core Workflows

### 1. SLO Definition
**Step 1:** Identify user-facing journeys (e.g. login, checkout, API call)
**Step 2:** Define SLIs — measurable indicators (latency p99, error rate, availability %)
**Step 3:** Set SLO targets — typically 99.9% availability, p99 < 300ms
**Step 4:** Calculate error budget — (1 - SLO) × time window (e.g. 43.2 min/month for 99.9%)
**Step 5:** Define error budget policy — slow burn vs fast burn alerts, freeze windows

### 2. Incident Response
1. **Detect** — alert fires, on-call paged
2. **Triage** — assess blast radius, customer impact
3. **Mitigate** — rollback, feature flag, traffic shift
4. **Communicate** — status page, stakeholder update every 30 min
5. **Resolve** — root cause fixed or workaround stable
6. **Post-mortem** — blameless, 5 Whys, action items with owners

### 3. Blameless Post-Mortem Template

```markdown
## Incident Summary
- **Date/Time:** 
- **Duration:** 
- **Severity:** P1/P2/P3
- **Impact:** X users affected, $Y revenue impact

## Timeline
| Time | Event |
|------|-------|
| HH:MM | Alert fired |
| HH:MM | On-call paged |
| HH:MM | Mitigated |
| HH:MM | Resolved |

## Root Cause
[5 Whys analysis]

## What Went Well
- 

## What Went Wrong
- 

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
```

### 4. Alert Design Principles
- **Signal over noise** — alert on symptoms (user impact), not causes
- **SLO-based alerts** — burn rate alerts rather than threshold alerts
- **Fast burn** (2% budget in 1hr) → page immediately
- **Slow burn** (5% budget in 6hr) → ticket/notification
- **Runbook link** — every alert must link to a runbook
- **Silence unused alerts** — if it doesn't cause action, remove it

### 5. Error Budget Policy
| Budget Remaining | Action |
|------------------|--------|
| > 50% | Normal development velocity |
| 25–50% | Review risky deployments |
| 10–25% | Freeze non-essential deploys |
| < 10% | All hands on reliability work |

## Key Metrics
- **Availability** = (good_requests / total_requests) × 100
- **MTTR** (Mean Time To Recover) — target < 30 min for P1
- **MTBF** (Mean Time Between Failures) — track trend over quarters
- **Error Budget Burn Rate** = current_error_rate / (1 - SLO)
- **Change Failure Rate** — deploys causing incidents / total deploys (DORA metric)

## Related Skills
- observability-designer
- runbook-generator
- cs-senior-engineer


<!-- Auto-generated required sections -->

## Name

SRE

## Description

Site Reliability Engineer skill for Claude Code. Provides workflows, templates, and automation tools.

## Features

- Production-ready workflows
- Step-by-step guidance
- Reusable templates
- Best practices embedded

## Usage

Describe your task to Claude and this skill will be applied automatically based on context.

```
# Trigger this skill by describing your need:
"Help me with site reliability engineer"
```

## Examples

**Example 1:** Ask Claude to apply this skill to your current project.

**Example 2:** Reference the workflows in SKILL.md to guide your implementation.
