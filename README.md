# ollama-actions-week

**Student:** Stephen McKitrick ([@Bigessfour](https://github.com/Bigessfour))  
**Cohort:** Echo  
**Challenge:** Week 11 Day 1 — Git Basics and GitHub Actions

![Push Workflow Status](https://github.com/Bigessfour/ollama-actions-week/actions/workflows/push-workflow.yml/badge.svg)

## Workflows

| File | Trigger | Purpose |
|------|---------|---------|
| `push-workflow.yml` | Push to `main` | Multi-job pipeline, env vars, conditionals, matrix |
| `scheduled-workflow.yml` | Friday cron + manual | Scheduled log generation |
| `pr-workflow.yml` | Pull requests to `main` | File validation and automated PR comment |

## Cron schedule

`0 0 * * 5` — midnight UTC every Friday. Use `gh workflow run scheduled-workflow.yml` to test immediately.

## Challenge brief

https://github.com/codeplatoon-devops/aico-challenges-w11/blob/main/day-1-github-actions-intro/challenge-1-git-basics-and-github-actions.md