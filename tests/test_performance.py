"""Member 2 (simulated) — performance baselines and timing reports."""

from __future__ import annotations

import json
import time

import pytest

MAX_SIMPLE_QUERY_S = 30
OPTIMAL_SIMPLE_QUERY_S = 15
MAX_COLD_START_S = 45


@pytest.mark.critical
def test_ai_response_time(model_name, sample_prompt, ollama_available, ollama_run, test_output_dir):
    """Simple query completes within the team maximum threshold (30s)."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    start = time.time()
    result = ollama_run(model_name, sample_prompt, timeout=MAX_SIMPLE_QUERY_S + 15)
    duration = time.time() - start
    report = {"test": "test_ai_response_time", "duration_s": round(duration, 2)}
    (test_output_dir / "timing.json").write_text(json.dumps(report), encoding="utf-8")
    assert result.returncode == 0, result.stderr
    assert duration < MAX_SIMPLE_QUERY_S, f"Query took {duration:.1f}s (max {MAX_SIMPLE_QUERY_S}s)"


@pytest.mark.advisory
def test_ai_response_time_warning(model_name, sample_prompt, ollama_available, ollama_run):
    """Warn (advisory) when query exceeds optimal 15s but still under max."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    start = time.time()
    result = ollama_run(model_name, sample_prompt, timeout=MAX_SIMPLE_QUERY_S + 15)
    duration = time.time() - start
    assert result.returncode == 0
    if duration > OPTIMAL_SIMPLE_QUERY_S:
        print(f"ADVISORY: response {duration:.1f}s > optimal {OPTIMAL_SIMPLE_QUERY_S}s")


@pytest.mark.critical
def test_model_load_time(model_name, ollama_available, ollama_run, test_output_dir):
    """Cold-style prompt completes within maximum cold-start threshold."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    prompt = "Respond with one word: READY"
    start = time.time()
    result = ollama_run(model_name, prompt, timeout=MAX_COLD_START_S + 15)
    duration = time.time() - start
    report = {"test": "test_model_load_time", "duration_s": round(duration, 2)}
    path = test_output_dir / "timing-report.json"
    existing = []
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
    existing.append(report)
    path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    assert result.returncode == 0
    assert duration < MAX_COLD_START_S, f"Cold query took {duration:.1f}s (max {MAX_COLD_START_S}s)"


@pytest.mark.advisory
def test_cache_improves_performance(model_name, ollama_available, ollama_run):
    """Second query is usually faster than first (advisory; runner load may invert)."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    prompt = "Say hello in exactly three words."
    t0 = time.time()
    r1 = ollama_run(model_name, prompt, timeout=MAX_SIMPLE_QUERY_S + 15)
    d1 = time.time() - t0
    t1 = time.time()
    r2 = ollama_run(model_name, prompt, timeout=MAX_SIMPLE_QUERY_S + 15)
    d2 = time.time() - t1
    assert r1.returncode == 0 and r2.returncode == 0
    if d2 >= d1:
        print(f"ADVISORY: second query not faster ({d2:.1f}s vs {d1:.1f}s)")


@pytest.mark.critical
def test_response_not_empty(model_name, sample_prompt, ollama_available, ollama_run):
    """AI response contains actual content."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    result = ollama_run(model_name, sample_prompt, timeout=MAX_SIMPLE_QUERY_S + 15)
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 3, "Response too short to be meaningful"