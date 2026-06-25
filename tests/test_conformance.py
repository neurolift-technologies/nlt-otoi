"""Cross-implementation conformance checks for the ``.otoi`` Python port.

These assertions pin behaviors documented in the reference SPEC.md / README.md
and exercised by the verbatim npm suites under ``tests/fixtures/npm/``. The same
charter objects the TypeScript reference uses must yield the same effective
policy, enforcement defaults, tier order, and conflict reporting here — and the
re-exported ``.toi`` primitives must be the real ``nlt_toi`` functions.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import nlt_toi
from nlt_otoi import (
    OTOI_CONFLICT_STRATEGIES,
    OTOI_ENFORCEMENT_MODES,
    OTOI_FILE_EXTENSION,
    OTOI_FORMAT_VERSION,
    OTOI_MEDIA_TYPE,
    OTOI_RESERVED_KEYS,
    OTOI_UNSUPPORTED_STRATEGIES,
    TOI_FORMAT_VERSION,
    TOI_TIERS,
    HonorOptions,
    OtoiValidationError,
    __version__,
    honor,
    parse_charter,
    parse_toi,
    parse_with_defaults,
    resolve_toi,
    safe_parse_toi,
    verify_toi,
)

from .conftest import NPM_TESTS_DIR

personal = {
    "$toi": "1.0.0",
    "$tier": "personal",
    "identity": {"author": "josh"},
    "communication": {"tone": "direct"},
}
project = {
    "$toi": "1.0.0",
    "$tier": "project",
    "identity": {"author": "nlt-redteam"},
    "communication": {"tone": "professional", "verbosity": "concise"},
}


class TestNpmTestCorpusPresent:
    def test_verbatim_npm_suites_are_vendored(self):
        for name in ("honor.test.ts", "compat.test.ts", "compat.broken-toi.test.ts"):
            path: Path = NPM_TESTS_DIR / name
            assert path.is_file(), f"missing verbatim npm test fixture: {name}"
            assert path.read_text(encoding="utf-8").strip(), f"empty fixture: {name}"


class TestConstantsMatchReference:
    def test_format_and_media_constants(self):
        assert OTOI_FORMAT_VERSION == "1.0.0"
        assert OTOI_FILE_EXTENSION == ".otoi"
        assert OTOI_MEDIA_TYPE == "application/otoi+json"
        assert OTOI_RESERVED_KEYS == ("$otoi", "$id", "$created", "$updated")

    def test_vocabularies(self):
        assert OTOI_ENFORCEMENT_MODES == ("advisory", "enforced", "strict")
        assert OTOI_CONFLICT_STRATEGIES == ("highest-tier-wins", "reject", "escalate")
        assert OTOI_UNSUPPORTED_STRATEGIES == ("ignore", "degrade", "reject")


class TestEnforcementDefaults:
    def test_resolved_enforcement_defaults(self):
        policy = honor({"$otoi": "1.0.0"}, HonorOptions(documents=[personal]))
        assert policy.enforcement.mode == "enforced"
        assert policy.enforcement.on_conflict == "highest-tier-wins"
        assert policy.enforcement.on_unsupported == "degrade"
        assert policy.enforcement.audit is True

    def test_partial_enforcement_fills_remaining_defaults(self):
        charter = {"$otoi": "1.0.0", "enforcement": {"mode": "advisory"}}
        policy = honor(charter, HonorOptions(documents=[personal]))
        assert policy.enforcement.mode == "advisory"
        assert policy.enforcement.on_conflict == "highest-tier-wins"
        assert policy.enforcement.audit is True


class TestParseCharterDefaults:
    def test_agents_and_sources_default_to_empty_lists(self):
        charter = parse_charter({"$otoi": "1.0.0"})
        assert charter["agents"] == []
        assert charter["toi_sources"] == []

    def test_unknown_keys_preserved(self):
        charter = parse_charter({"$otoi": "1.0.0", "$future": {"k": 1}, "x": "y"})
        assert charter["$future"] == {"k": 1}
        assert charter["x"] == "y"

    @pytest.mark.parametrize("field", ["toi_sources", "agents"])
    def test_explicit_null_is_rejected_not_defaulted(self, field):
        # Zod's ``.default([])`` substitutes only for a MISSING key (``undefined``).
        # An explicit JSON ``null`` runs the inner ``z.array`` and is rejected — it
        # must NOT be silently coerced to ``[]``.
        with pytest.raises(OtoiValidationError) as exc_info:
            parse_charter({"$otoi": "1.0.0", field: None})
        assert any(issue.path == field for issue in exc_info.value.issues)

    @pytest.mark.parametrize("field", ["toi_sources", "agents"])
    def test_parse_with_defaults_fills_missing_only_not_null(self, field):
        # Missing key -> default applies.
        assert parse_with_defaults({"$otoi": "1.0.0"})[field] == []
        # Explicit null -> preserved as-is (defaulting must not mask it); the
        # rejection happens in schema validation, not here.
        assert parse_with_defaults({"$otoi": "1.0.0", field: None})[field] is None


class TestResolutionParity:
    def test_terminal_personal_precedence_and_gap_fill(self):
        policy = honor({"$otoi": "1.0.0"}, HonorOptions(documents=[project, personal]))
        assert policy.effective["communication"]["tone"] == "direct"
        assert policy.effective["communication"]["verbosity"] == "concise"
        assert policy.tiers == ["personal", "project"]
        # The synthesized view carries the highest tier's $toi/$tier (SPEC §6).
        assert policy.effective["$tier"] == "personal"
        assert policy.effective["$toi"] == "1.0.0"

    def test_platform_defaults_lowest_precedence(self):
        policy = honor(
            {"$otoi": "1.0.0"},
            HonorOptions(
                documents=[personal],
                platform_defaults={"communication": {"language": "en"}},
            ),
        )
        # personal sets tone; platform default only fills the gap (language).
        assert policy.effective["communication"]["tone"] == "direct"
        assert policy.effective["communication"]["language"] == "en"


class TestReexportedToiPrimitivesAreReal:
    def test_reexports_are_the_nlt_toi_functions(self):
        assert parse_toi is nlt_toi.parse_toi
        assert resolve_toi is nlt_toi.resolve_toi
        assert verify_toi is nlt_toi.verify_toi
        assert safe_parse_toi is nlt_toi.safe_parse_toi
        assert TOI_TIERS is nlt_toi.TOI_TIERS
        assert TOI_FORMAT_VERSION == nlt_toi.TOI_FORMAT_VERSION

    def test_reexported_parse_toi_round_trips(self):
        doc = parse_toi(personal)
        assert doc["$tier"] == "personal"
        # safe_parse_toi reports success on a valid document.
        assert safe_parse_toi(personal).success is True


class TestPackageVersion:
    def test_distribution_version_matches_npm(self):
        # The npm package is 1.2.0; the Python port aligns its version with it.
        assert __version__ == "1.2.0"
