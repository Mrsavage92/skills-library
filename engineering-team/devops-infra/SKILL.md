---
name: "devops-infra"
description: "DevOps and infrastructure engineer for cloud architecture, IaC (Terraform/Pulumi), container orchestration (Kubernetes/Docker), CI/CD pipelines, cost optimisation, disaster recovery, and platform engineering. Use when provisioning cloud infrastructure, designing deployment pipelines, setting up Kubernetes, writing Terraform modules, planning DR strategy, or building a developer platform."
Name: "DevOps Infrastructure"
  Tier: "STANDARD"
  Category: "Engineering"
  Dependencies: "None"
  Author: "claude-skills"
  Version: "2.1.2"
---

# DevOps / Infrastructure Engineer

## Overview

Platform and infrastructure engineering enables fast, reliable product delivery. This skill covers the full infrastructure lifecycle: cloud architecture, infrastructure-as-code, container platforms, CI/CD automation, security hardening, and cost governance.

## When to Use

- Provisioning or redesigning cloud infrastructure (AWS/GCP/Azure)
- Writing Terraform, Pulumi, or CDK for infrastructure
- Setting up or optimising a Kubernetes cluster
- Designing or improving CI/CD pipelines
- Planning disaster recovery or multi-region architecture
- Building an internal developer platform (IDP)

## Quick Start

```
# Infrastructure review
Describe your current stack → architecture review + improvement recommendations

# Terraform module
Describe what you need (e.g. EKS cluster with autoscaling) → Terraform module

# CI/CD pipeline
Share your repo structure + deploy target → GitHub Actions or GitLab CI config
```

## Cloud Architecture Principles

### Well-Architected Framework (AWS)
1. **Operational Excellence** — runbooks, CI/CD, observability
2. **Security** — least privilege IAM, encryption at rest/transit, VPC isolation
3. **Reliability** — multi-AZ, auto-scaling, circuit breakers, backups
4. **Performance** — right-size, caching, CDN, async processing
5. **Cost** — reserved capacity, spot, waste elimination
6. **Sustainability** — efficient instance types, auto-scale-to-zero

### Standard Production Architecture (SaaS)
```
Internet → CloudFront/CDN → ALB → ECS/EKS (app) → RDS/Aurora (db)
                                              ↓
                                    ElastiCache (cache)
                                    SQS/SNS (async)
                                    S3 (assets/backups)
```

## Terraform Module Structure
```
module/
├── main.tf          # Resources
├── variables.tf     # Input variables with descriptions + validation
├── outputs.tf       # Output values
├── versions.tf      # Provider version constraints
└── README.md        # Usage, inputs, outputs table
```

## Kubernetes Production Checklist
- [ ] Namespaces per environment (prod, staging, dev)
- [ ] ResourceRequests + Limits on all containers
- [ ] PodDisruptionBudgets for critical services
- [ ] NetworkPolicies (default deny, explicit allow)
- [ ] RBAC with least-privilege ServiceAccounts
- [ ] HorizontalPodAutoscaler configured
- [ ] Liveness + Readiness probes on all pods
- [ ] Secrets via External Secrets Operator (not hardcoded)
- [ ] PodSecurityStandards enforced

## CI/CD Pipeline Design

### GitHub Actions — Production Deploy Pipeline
```yaml
# Triggers: push to main → deploy to prod
# Triggers: push to staging → deploy to staging
# Triggers: PR → run tests only

stages:
  1. lint-and-test   # parallel: lint, unit tests, security scan
  2. build           # docker build + push to ECR
  3. deploy-staging  # helm upgrade --install staging
  4. integration-test# smoke tests against staging
  5. deploy-prod     # manual approval → helm upgrade production
  6. notify          # Slack notification with deploy summary
```

### Deployment Strategies
| Strategy | Zero Downtime | Rollback Speed | Complexity |
|----------|--------------|----------------|------------|
| Rolling update | ✅ | Medium | Low |
| Blue/Green | ✅ | Fast | Medium |
| Canary | ✅ | Fast | High |
| Feature flags | ✅ | Instant | Medium |

## Disaster Recovery

### RTO/RPO Targets by Service Tier
| Tier | Service Type | RTO | RPO |
|------|-------------|-----|-----|
| Critical | Auth, payments | < 1 hour | < 15 min |
| High | Core product | < 4 hours | < 1 hour |
| Medium | Internal tools | < 24 hours | < 4 hours |
| Low | Dev/staging | Best effort | Daily |

### DR Runbook Template
1. **Incident declared** — on-call paged, war room opened
2. **Impact assessed** — which services, how many users
3. **Failover initiated** — DNS switch / replica promotion
4. **Verification** — smoke tests pass, metrics nominal
5. **Communication** — status page updated, stakeholders notified
6. **Post-mortem** — scheduled within 48 hours

## Key Metrics (DORA)
- **Deployment frequency** — daily or more for high performers
- **Lead time for changes** — < 1 day for elite teams
- **Change failure rate** — < 5% for elite teams
- **MTTR** — < 1 hour for elite teams

## Related Skills
- sre
- cloud-cost-optimizer
- observability-designer


<!-- Auto-generated required sections -->

## Name

DevOps Infrastructure

## Description

DevOps and Infrastructure Engineer skill for Claude Code. Provides workflows, templates, and automation tools.

## Features

- Production-ready workflows
- Step-by-step guidance
- Reusable templates
- Best practices embedded

## Usage

Describe your task to Claude and this skill will be applied automatically based on context.

```
# Trigger this skill by describing your need:
"Help me with devops and infrastructure engineer"
```

## Examples

**Example 1:** Ask Claude to apply this skill to your current project.

**Example 2:** Reference the workflows in SKILL.md to guide your implementation.
