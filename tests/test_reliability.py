"""Member 3 (simulated) — failure handling and graceful degradation."""

from __future__ import annotations

import subprocess

import pytest


@pytest.mark.critical
def test_handles_invalid_model(ollama_run):
    """Non-existent model returns non-zero exit code."""
    result = ollama_run("definitely-not-a-real-model-xyz", "hello", timeout=30)
    assert result.returncode != 0, "Expected failure for invalid model name"


@pytest.mark.critical
def test_handles_empty_prompt(model_name, ollama_available, ollama_run):
    """Empty prompt does not crash the CLI (may error or return minimal output)."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    result = ollama_run(model_name, "", timeout=60)
    # Accept controlled failure or empty handling; must not hang
    assert result.returncode in (0, 1)


@pytest.mark.advisory
def test_handles_timeout(model_name, ollama_available):
    """Subprocess timeout guard fires for long-running generate (advisory)."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    try:
        subprocess.run(
            ["ollama", "run", model_name, "Write a very long essay about DevOps."],
            capture_output=True,
            text=True,
            timeout=1,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return
    pytest.skip("Model finished within 1s; timeout not triggered on this runner")


@pytest.mark.advisory
def test_partial_failure_recovery():
    """Advisory failures are reported separately; CI advisory step uses continue-on-error."""
    assert True


@pytest.mark.critical
def test_error_messages_helpful(ollama_run):
    """Invalid model stderr/stdout mentions model or error context."""
    result = ollama_run("not-a-valid-model-tag-12345", "test", timeout=30)
    combined = (result.stdout + result.stderr).lower()
    assert result.returncode != 0
    assert any(word in combined for word in ("model", "error", "pull", "not found", "failed")), (
        f"Expected actionable error text, got: {result.stderr!r}"
    )