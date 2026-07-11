"""Member 1 — Ollama service health tests."""

from __future__ import annotations

import subprocess

import pytest


@pytest.mark.critical
def test_ollama_installed():
    """Ollama CLI is installed and reports a version string."""
    result = subprocess.run(
        ["ollama", "--version"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, f"ollama --version failed: {result.stderr}"
    assert "ollama" in (result.stdout + result.stderr).lower()


@pytest.mark.critical
def test_ollama_service_responding(ollama_available):
    """Ollama service responds to ollama list."""
    if not ollama_available:
        pytest.skip("Ollama service not available (start with: ollama serve)")
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, f"ollama list failed: {result.stderr}"


@pytest.mark.critical
def test_model_available(model_name, ollama_available):
    """Required model appears in ollama list output."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0
    assert model_name in result.stdout, (
        f"Model {model_name} not in ollama list. Pull with: ollama pull {model_name}"
    )


@pytest.mark.critical
def test_model_loads_successfully(model_name, sample_prompt, ollama_available, ollama_run):
    """Model can process a minimal prompt and return non-empty output."""
    if not ollama_available:
        pytest.skip("Ollama service not available")
    result = ollama_run(model_name, sample_prompt, timeout=120)
    assert result.returncode == 0, f"ollama run failed: {result.stderr}"
    assert result.stdout.strip(), "Expected non-empty model response"


@pytest.mark.advisory
def test_cache_directory_exists(ollama_models_dir):
    """Configured OLLAMA_MODELS directory exists (advisory for fresh installs)."""
    assert ollama_models_dir.exists(), (
        f"Model directory missing: {ollama_models_dir}. Set OLLAMA_MODELS if using a custom path."
    )