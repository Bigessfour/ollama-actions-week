"""Shared fixtures for Day 3 Ollama test infrastructure (Member 1)."""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
from pathlib import Path

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical (must pass)")
    config.addinivalue_line("markers", "advisory: mark test as advisory (can warn)")


@pytest.fixture
def ollama_models_dir() -> Path:
    """Model directory used by tests; align with OLLAMA_MODELS in CI."""
    raw = os.environ.get("OLLAMA_MODELS", os.path.expanduser("~/.ollama/models"))
    return Path(raw).expanduser()


@pytest.fixture
def model_name() -> str:
    return os.environ.get("OLLAMA_TEST_MODEL", "llama3.2:1b")


@pytest.fixture
def sample_prompt() -> str:
    return "Respond with exactly: OLLAMA_TEST_OK"


@pytest.fixture
def test_output_dir():
    with tempfile.TemporaryDirectory(prefix="ollama-test-") as tmp:
        yield Path(tmp)


@pytest.fixture
def ollama_available() -> bool:
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def run_ollama_prompt(model_name: str, prompt: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run a single Ollama generate via CLI."""
    return subprocess.run(
        ["ollama", "run", model_name, prompt],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


@pytest.fixture
def ollama_run():
    return run_ollama_prompt