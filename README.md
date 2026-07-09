# ollama-actions-week

**Student:** Stephen McKitrick ([@Bigessfour](https://github.com/Bigessfour))  
**Cohort:** Echo  
**Challenges:** Week 11 Day 1 (GitHub Actions) + Day 2 (Ollama AI PR review)

![Push Workflow Status](https://github.com/Bigessfour/ollama-actions-week/actions/workflows/push-workflow.yml/badge.svg)
![AI PR Review Status](https://github.com/Bigessfour/ollama-actions-week/actions/workflows/ai-pr-review.yml/badge.svg)

## Workflows

| File | Trigger | Purpose |
|------|---------|---------|
| `push-workflow.yml` | Push to `main` | Multi-job pipeline, env vars, conditionals, matrix |
| `scheduled-workflow.yml` | Friday cron + manual | Scheduled log generation |
| `pr-workflow.yml` | Pull requests to `main` | File validation and automated PR comment |
| `ai-pr-review.yml` | PR opened/synchronize → `main` | Ollama AI documentation review (Day 2) |

## Day 2 — AI-powered PR documentation review

`ai-pr-review.yml` upgrades the Day 1 automation with local LLM analysis via Ollama (`llama3.2:1b` primary; matrix also exercises `llama3.2:3b`).

### Pipeline jobs

1. **setup** — Install Ollama, pull model, report model version + disk space  
2. **analysis** — README quality, repo structure, improvements, personal file feedback, conditionals  
3. **synthesis** — Executive summary + overall score + top 3 priorities  
4. **report** — `$GITHUB_STEP_SUMMARY` dashboard + `gh pr comment` markdown review  
5. **matrix-analysis** — Models × prompt styles (`concise` / `detailed` / `technical`), `fail-fast: false`  
6. **matrix-compare** — Downloads matrix artifacts and writes a comparison summary  

### Model choices

| Model | Why |
|-------|-----|
| `llama3.2:1b` | Fast enough for free GitHub-hosted runners; good default for CI feedback loops |
| `llama3.2:3b` | Slightly stronger reasoning when runner RAM allows; used in matrix only |

### AI configuration (env)

- `AI_MODEL`, `AI_TEMPERATURE`, `MAX_TOKENS`, `ANALYSIS_TYPE` (workflow-level)  
- `PROMPT_STYLE` (job-level on analysis)  
- PR context: number, title, author, source branch  

## Day 1 notes

The push workflow chains setup → build → report with env vars, conditionals, artifacts, and an OS × environment matrix. The PR workflow validates `name.txt` / `devops.txt` and comments a summary (requires `pull-requests: write`).

## Cron schedule

`0 0 * * 5` — midnight UTC every Friday. Use `gh workflow run scheduled-workflow.yml` to test immediately.

## Challenge briefs

- Day 1: https://github.com/codeplatoon-devops/aico-challenges-w11/blob/main/day-1-github-actions-intro/challenge-1-git-basics-and-github-actions.md  
- Day 2: https://github.com/codeplatoon-devops/aico-challenges-w11/blob/main/day-2-ollama-and-github-actions/challenge-1-ai-powered-pull-request-documentation-review.md  
