"""Canonical ``.otoi`` v1.0.0 charter schema — the single source of truth for
the orchestration layer.

An ``.otoi`` charter is declarative, like a ``.toi`` document: it never contains
code or prompts. It names the ``.toi`` sources in force, the agents bound to
honor them, and the enforcement policy. The actual interaction preferences live
in the referenced ``.toi`` documents and are validated by ``nlt_toi`` — this
schema deliberately treats inline ``.toi`` payloads as opaque (``unknown``) and
defers to ``parse_toi`` at honor time, so there is exactly one validator for the
``.toi`` shape.

Every object is *open* (a Zod ``looseObject`` in the reference) for the same
additive forward-compatibility the ``.toi`` standard guarantees: unknown keys are
preserved, never rejected.

This module mirrors ``@neurolift-technologies/otoi`` ``src/schema.ts``. Because
Python has no Zod, the same constraints are expressed as a hand-written validator
that returns a list of :class:`OtoiIssue` (empty when valid) and a parser that
applies the schema's defaults — reproducing Zod's ``.default([])`` behavior.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from nlt_toi import TOI_TIERS

from .constants import (
    OTOI_CONFLICT_STRATEGIES,
    OTOI_ENFORCEMENT_MODES,
    OTOI_UNSUPPORTED_STRATEGIES,
)
from .errors import OtoiIssue

# Semantic version, e.g. ``1.0.0``, ``1.2.0-rc.1``.
_SEMVER = re.compile(
    r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
# ISO 8601 calendar date or date-time (offset optional).
_ISO_DATETIME = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?)?$"
)
# RFC 4122 version-4 UUID.
_UUID_V4 = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _is_object(value: Any) -> bool:
    return isinstance(value, dict)


def _is_array(value: Any) -> bool:
    return isinstance(value, list)


def _is_string(value: Any) -> bool:
    # bool is a subclass of int but never str; only true strings count.
    return isinstance(value, str)


def _push(issues: List[OtoiIssue], path: str, message: str) -> None:
    issues.append(OtoiIssue(path=path, message=message))


def _join(prefix: str, key: str) -> str:
    return f"{prefix}.{key}" if prefix else key


def _validate_agent(agent: Any, path: str, issues: List[OtoiIssue]) -> None:
    if not _is_object(agent):
        _push(issues, path, "Invalid input: expected object")
        return
    aid = agent.get("id")
    if not _is_string(aid):
        _push(issues, _join(path, "id"), "Invalid input: expected string")
    elif len(aid) < 1:
        _push(issues, _join(path, "id"), "Too small: expected string to have >=1 characters")
    if "role" in agent and agent["role"] is not None and not _is_string(agent["role"]):
        _push(issues, _join(path, "role"), "Invalid input: expected string")
    for field in ("modalities", "affordances"):
        if field in agent and agent[field] is not None:
            arr = agent[field]
            if not _is_array(arr):
                _push(issues, _join(path, field), "Invalid input: expected array")
            else:
                for i, item in enumerate(arr):
                    if not _is_string(item):
                        _push(issues, _join(path, f"{field}.{i}"), "Invalid input: expected string")


def _validate_source(source: Any, path: str, issues: List[OtoiIssue]) -> None:
    if not _is_object(source):
        _push(issues, path, "Invalid input: expected object")
        return
    tier = source.get("tier")
    if tier not in TOI_TIERS:
        _push(
            issues,
            _join(path, "tier"),
            f"Invalid option: expected one of {_quoted(TOI_TIERS)}",
        )
    if "uri" in source and source["uri"] is not None and not _is_string(source["uri"]):
        _push(issues, _join(path, "uri"), "Invalid input: expected string")
    has_uri = source.get("uri") is not None
    has_inline = source.get("inline") is not None
    # ``.refine``: a toi_source must provide exactly one of ``uri`` or ``inline``.
    if has_uri == has_inline:
        _push(issues, path, "a toi_source must provide exactly one of `uri` or `inline`")


def _validate_enforcement(enf: Any, path: str, issues: List[OtoiIssue]) -> None:
    if not _is_object(enf):
        _push(issues, path, "Invalid input: expected object")
        return
    _enum_field(enf, "mode", OTOI_ENFORCEMENT_MODES, path, issues)
    _enum_field(enf, "on_conflict", OTOI_CONFLICT_STRATEGIES, path, issues)
    _enum_field(enf, "on_unsupported", OTOI_UNSUPPORTED_STRATEGIES, path, issues)
    if "audit" in enf and enf["audit"] is not None and not isinstance(enf["audit"], bool):
        _push(issues, _join(path, "audit"), "Invalid input: expected boolean")


def _enum_field(obj: Dict[str, Any], key: str, options, path: str, issues: List[OtoiIssue]) -> None:
    if key in obj and obj[key] is not None and obj[key] not in options:
        _push(
            issues,
            _join(path, key),
            f"Invalid option: expected one of {_quoted(options)}",
        )


def _quoted(options) -> str:
    return "|".join(f'"{o}"' for o in options)


def schema_issues(charter: Any) -> List[OtoiIssue]:
    """Validate a candidate charter against the ``.otoi`` v1.0.0 schema.

    Returns an empty list when valid; otherwise one :class:`OtoiIssue` per
    violation, each with a dotted path mirroring the reference's flattened Zod
    issues. The caller (``parse_charter``) raises an
    :class:`~nlt_otoi.errors.OtoiValidationError` from these.
    """
    issues: List[OtoiIssue] = []
    if not _is_object(charter):
        _push(issues, "", "Invalid input: expected object")
        return issues

    # Reserved namespace.
    otoi = charter.get("$otoi")
    if "$otoi" not in charter or otoi is None:
        _push(issues, "$otoi", "Invalid input: expected string")
    elif not _is_string(otoi):
        _push(issues, "$otoi", "Invalid input: expected string")
    elif not _SEMVER.match(otoi):
        _push(issues, "$otoi", "must be a semantic version (MAJOR.MINOR.PATCH)")

    if "$id" in charter and charter["$id"] is not None:
        if not _is_string(charter["$id"]) or not _UUID_V4.match(charter["$id"]):
            _push(issues, "$id", "must be a version-4 UUID")

    for key in ("$created", "$updated"):
        if key in charter and charter[key] is not None:
            val = charter[key]
            if not _is_string(val) or not _ISO_DATETIME.match(val):
                _push(issues, key, "must be an ISO 8601 date or date-time")

    if "identity" in charter and charter["identity"] is not None:
        identity = charter["identity"]
        if not _is_object(identity):
            _push(issues, "identity", "Invalid input: expected object")
        else:
            author = identity.get("author")
            if not _is_string(author):
                _push(issues, "identity.author", "Invalid input: expected string")
            elif len(author) < 1:
                _push(issues, "identity.author", "Too small: expected string to have >=1 characters")

    if "agents" in charter and charter["agents"] is not None:
        agents = charter["agents"]
        if not _is_array(agents):
            _push(issues, "agents", "Invalid input: expected array")
        else:
            for i, agent in enumerate(agents):
                _validate_agent(agent, f"agents.{i}", issues)

    if "enforcement" in charter and charter["enforcement"] is not None:
        _validate_enforcement(charter["enforcement"], "enforcement", issues)

    if "toi_sources" in charter and charter["toi_sources"] is not None:
        sources = charter["toi_sources"]
        if not _is_array(sources):
            _push(issues, "toi_sources", "Invalid input: expected array")
        else:
            for i, source in enumerate(sources):
                _validate_source(source, f"toi_sources.{i}", issues)

    return issues


def parse_with_defaults(charter: Dict[str, Any]) -> Dict[str, Any]:
    """Return a shallow copy of *charter* with the schema's defaults applied.

    Mirrors Zod's ``.default([])`` on ``agents`` and ``toi_sources``: when those
    keys are absent (or ``None``) the parsed charter carries an empty list, so
    downstream code can iterate unconditionally. Unknown keys are preserved
    (``looseObject``).
    """
    result = dict(charter)
    if result.get("agents") is None:
        result["agents"] = []
    if result.get("toi_sources") is None:
        result["toi_sources"] = []
    return result
