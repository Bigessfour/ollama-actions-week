# Day 3 — Production-ready testing infrastructure

**Branch order (solo catch-up):**

1. `test-infra-skeleton` → merge (this PR)
2. `member-1-service-tests` → `tests/test_ollama_service.py`
3. `member-2-performance-tests` → `tests/test_performance.py`
4. `member-3-reliability-workflow` → `tests/test_reliability.py` + `.github/workflows/ollama-basic.yml`

**Local setup:**

```bash
export OLLAMA_MODELS="${OLLAMA_MODELS:-$HOME/.ollama/models}"
ollama serve   # separate terminal
pip install -r requirements.txt
pytest tests/ -v
```

**Challenges submission:** `w11d3-challenges` on `Bigessfour/aico-challenges-w11` (evidence only).