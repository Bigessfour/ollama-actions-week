# Day 3 — Production-ready testing infrastructure

**Solo submission:** Member 1 work by Stephen McKitrick. Members 2 and 3 were **simulated** in one PR (`day3-solo-simulated-team`) because teammates were unavailable. File ownership from the brief is preserved in separate modules:

| Simulated member | Files |
|------------------|-------|
| Member 1 | `tests/conftest.py`, `tests/test_ollama_service.py` |
| Member 2 (simulated) | `tests/test_performance.py`, `requirements.txt` |
| Member 3 (simulated) | `tests/test_reliability.py`, `.github/workflows/ollama-basic.yml` |

**Local setup:**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OLLAMA_MODELS="${OLLAMA_MODELS:-$HOME/.ollama/models}"
ollama serve   # separate terminal; ollama pull llama3.2:1b
pytest tests/ -v
```

**Challenges evidence:** `w11d3-challenges` on `Bigessfour/aico-challenges-w11`.