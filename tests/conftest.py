"""Shared test helpers — locate the verbatim npm test corpus copied from the
reference implementation (``@neurolift-technologies/otoi``)."""
from __future__ import annotations

from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
NPM_TESTS_DIR = FIXTURES / "npm"
