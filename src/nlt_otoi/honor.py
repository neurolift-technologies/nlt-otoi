"""The ``.otoi`` honoring layer.

This is what makes ``.otoi`` more than a second copy of ``.toi``: it consumes the
canonical ``nlt_toi`` primitives (``parse_toi``, ``resolve_toi``) to turn a
charter plus a stack of ``.toi`` documents into one **effective interaction
policy** that every agent in the mesh honors — and it adds the orchestration
concerns the ``.toi`` standard deliberately leaves out: same-tier conflict
detection, enforcement modes, and per-agent propagation.

Ported faithfully from ``@neurolift-technologies/otoi`` ``src/honor.ts``. The
reference ``honor`` is ``async`` only to await an I/O-bound ``loadSource``; this
port exposes a synchronous ``honor`` whose ``load_source`` callable returns the
``.toi`` text directly, matching Python library idiom and the conformance suite.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

from nlt_toi import TIER_RANK, ToiDocument, parse_toi, resolve_toi

from .compat import assert_toi_compatible
from .constants import (
    OtoiConflictStrategy,
    OtoiEnforcementMode,
    OtoiUnsupportedStrategy,
)
from .errors import (
    OtoiHonorError,
    OtoiIssue,
    OtoiParseError,
    OtoiValidationError,
    PolicyConflict,
)
from .schema import parse_with_defaults, schema_issues
from .types import OtoiAgent, OtoiCharter, OtoiEnforcement


@dataclass
class ResolvedEnforcement:
    """Enforcement settings with every field resolved to a concrete value."""

    mode: OtoiEnforcementMode
    on_conflict: OtoiConflictStrategy
    on_unsupported: OtoiUnsupportedStrategy
    audit: bool


_DEFAULT_ENFORCEMENT = ResolvedEnforcement(
    mode="enforced",
    on_conflict="highest-tier-wins",
    on_unsupported="degrade",
    audit=True,
)


@dataclass
class HonorOptions:
    """Options for :func:`honor`."""

    #: Already-parsed ``.toi`` documents to fold in alongside the charter's
    #: sources.
    documents: Optional[Sequence[ToiDocument]] = None
    #: Lowest-precedence fallback values, applied only where nothing else set a
    #: field.
    platform_defaults: Optional[Mapping[str, Any]] = None
    #: Loader used to resolve ``toi_sources`` that reference a ``uri``.
    load_source: Optional[Callable[[str], str]] = None


@dataclass
class EffectivePolicy:
    """The synthesized result every agent in the mesh honors."""

    #: The resolved effective ``.toi`` view (tier precedence applied).
    effective: ToiDocument
    #: Which tiers contributed, highest precedence first.
    tiers: List[str]
    #: The agents bound by the charter.
    agents: List[OtoiAgent]
    #: The enforcement policy in force.
    enforcement: ResolvedEnforcement
    #: Same-tier conflicts detected during resolution (empty when none).
    conflicts: List[PolicyConflict] = field(default_factory=list)


def parse_charter(input: Any) -> OtoiCharter:
    """Parse and validate an ``.otoi`` charter.

    Raises:
        OtoiParseError: if *input* is not valid JSON or its root is not an
            object.
        OtoiValidationError: if the charter violates the canonical schema.
    """
    json_value = _parse_json(input) if isinstance(input, str) else input
    if not isinstance(json_value, dict):
        raise OtoiParseError("An .otoi charter must be a JSON object")
    issues = schema_issues(json_value)
    if issues:
        raise _to_validation_error(issues)
    return parse_with_defaults(json_value)


def detect_conflicts(documents: Sequence[ToiDocument]) -> List[PolicyConflict]:
    """Detect same-tier conflicts across ``.toi`` documents.

    Cross-tier disagreement is not a conflict — that is what tier precedence is
    for. But two documents at the *same* tier that assign different values to the
    same leaf cannot both be honored, so each such leaf is reported.
    """
    seen_by_tier: Dict[str, Dict[str, Any]] = {}
    # Preserve first-seen order of conflicting (tier, path) keys, like the JS Map.
    working: "Dict[str, _WorkingConflict]" = {}

    for doc in documents:
        tier = doc["$tier"]
        seen = seen_by_tier.setdefault(tier, {})
        leaves: Dict[str, Any] = {}
        _collect_leaves(_content_of(doc), "", leaves)

        for path, value in leaves.items():
            if path not in seen:
                seen[path] = value
                continue
            existing = seen[path]
            if _equal_leaf(existing, value):
                continue
            key = tier + chr(31) + path  # internal map key; unit-separator keeps tier/path unambiguous
            entry = working.get(key)
            if entry is not None:
                if not any(_equal_leaf(v, value) for v in entry.values):
                    entry.values.append(value)
            else:
                working[key] = _WorkingConflict(tier=tier, path=path, values=[existing, value])

    return [PolicyConflict(tier=e.tier, path=e.path, values=tuple(e.values)) for e in working.values()]


def honor(input: Any, options: Optional[HonorOptions] = None) -> EffectivePolicy:
    """Fold a charter and its ``.toi`` sources into one effective policy.

    Resolution delegates tier precedence to ``nlt_toi``'s ``resolve_toi``; this
    function adds source loading, same-tier conflict detection, and enforcement.

    Raises:
        OtoiCompatibilityError: when the installed ``nlt_toi`` declares no valid
            format version (a broken or pre-``1.0.0`` install).
        OtoiHonorError: when there is nothing to resolve, when a ``uri`` source
            is present without a ``load_source``, or when a same-tier conflict is
            found under ``on_conflict="reject"``.
    """
    if options is None:
        options = HonorOptions()
    # Fail closed if the installed ``.toi`` package declares no usable format
    # version. Any valid ``.toi`` version is honored — ``.otoi`` does not pin one.
    assert_toi_compatible()
    charter = parse_charter(input)
    enforcement = _resolve_enforcement(charter.get("enforcement"))
    docs = _gather_documents(charter, options)

    if len(docs) == 0:
        raise OtoiHonorError(
            "honor() requires at least one .toi document "
            "(from the charter's toi_sources or options.documents)"
        )

    conflicts = detect_conflicts(docs)
    if conflicts and enforcement.on_conflict == "reject":
        where = ", ".join(f"{c.tier}:{c.path}" for c in conflicts)
        raise OtoiHonorError(
            f'Unresolved same-tier conflict(s) under on_conflict="reject": {where}',
            conflicts,
        )

    effective = resolve_toi(docs, options.platform_defaults)

    return EffectivePolicy(
        effective=effective,
        tiers=_unique_tiers_by_precedence(docs),
        agents=list(charter.get("agents", [])),
        enforcement=enforcement,
        conflicts=conflicts,
    )


def propagate(policy: EffectivePolicy, agent_id: str) -> ToiDocument:
    """Return the effective preferences a specific agent must honor.

    Under ``strict`` enforcement, an agent that is not declared in the charter
    mesh is refused rather than silently served the policy.
    """
    known = any(a.get("id") == agent_id for a in policy.agents)
    if not known and policy.enforcement.mode == "strict":
        raise OtoiHonorError(
            f'Agent "{agent_id}" is not declared in the charter mesh; '
            "strict enforcement refuses to honor for unknown agents"
        )
    return policy.effective


# --- internals ------------------------------------------------------------


@dataclass
class _WorkingConflict:
    tier: str
    path: str
    values: List[Any]


def _gather_documents(charter: OtoiCharter, options: HonorOptions) -> List[ToiDocument]:
    docs: List[ToiDocument] = []
    for source in charter.get("toi_sources", []):
        doc: Optional[ToiDocument] = None
        if source.get("inline") is not None:
            doc = parse_toi(source["inline"])
        elif source.get("uri") is not None:
            if options.load_source is None:
                raise OtoiHonorError(
                    f'toi_source references uri "{source["uri"]}" but no loadSource was provided'
                )
            doc = parse_toi(options.load_source(source["uri"]))
        if doc is None:
            continue

        # SPEC §4: a source declares the tier it contributes at. The loaded
        # document's own ``$tier`` MUST agree; a mismatch means the source is
        # mislabeled or points at the wrong file, which would silently change
        # precedence. Fail closed rather than trust either side blindly.
        if doc["$tier"] != source["tier"]:
            origin = (
                f'uri "{source["uri"]}"' if source.get("uri") is not None else "inline document"
            )
            raise OtoiHonorError(
                f'toi_source declares tier "{source["tier"]}" but its {origin} '
                f'has $tier "{doc["$tier"]}"'
            )
        docs.append(doc)

    for doc in options.documents or []:
        docs.append(doc)
    return docs


def _resolve_enforcement(e: Optional[OtoiEnforcement]) -> ResolvedEnforcement:
    e = e or {}
    return ResolvedEnforcement(
        mode=_coalesce(e.get("mode"), _DEFAULT_ENFORCEMENT.mode),
        on_conflict=_coalesce(e.get("on_conflict"), _DEFAULT_ENFORCEMENT.on_conflict),
        on_unsupported=_coalesce(e.get("on_unsupported"), _DEFAULT_ENFORCEMENT.on_unsupported),
        audit=_coalesce(e.get("audit"), _DEFAULT_ENFORCEMENT.audit),
    )


def _coalesce(value, default):
    return default if value is None else value


def _unique_tiers_by_precedence(docs: Sequence[ToiDocument]) -> List[str]:
    tiers = {doc["$tier"] for doc in docs}
    return sorted(tiers, key=lambda t: TIER_RANK[t])


def _content_of(doc: ToiDocument) -> Dict[str, Any]:
    """The content (non-reserved) keys of a document."""
    return {k: v for k, v in doc.items() if not k.startswith("$")}


def _collect_leaves(value: Any, prefix: str, into: Dict[str, Any]) -> None:
    """Flatten objects to dotted leaf paths; arrays and scalars are atomic
    leaves."""
    if _is_plain_object(value):
        for key in value.keys():
            _collect_leaves(value[key], f"{prefix}.{key}" if prefix else key, into)
    else:
        into[prefix] = value


def _is_plain_object(value: Any) -> bool:
    return isinstance(value, dict)


def _equal_leaf(a: Any, b: Any) -> bool:
    """Atomic-leaf equality. Leaves are scalars or arrays, so a stable JSON
    compare suffices."""
    if a is b or a == b:
        return True
    return _stable_json(a) == _stable_json(b)


def _stable_json(value: Any) -> str:
    # Mirror JSON.stringify: compact separators, keys in insertion order
    # (objects compared here are arrays/scalars, so key order is irrelevant).
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def _parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (ValueError, TypeError) as err:
        raise OtoiParseError("Input is not valid JSON") from err


def _to_validation_error(issues: Sequence[OtoiIssue]) -> OtoiValidationError:
    summary = "; ".join(f"{i.path}: {i.message}" if i.path else i.message for i in issues)
    return OtoiValidationError(f"Invalid .otoi charter — {summary}", issues)
