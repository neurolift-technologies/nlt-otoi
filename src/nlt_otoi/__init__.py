"""``nlt_otoi`` — Python reference implementation of the ``.otoi`` (Orchestrated
Terms of Interaction) honoring layer, ported from ``@neurolift-technologies/otoi``.

``.otoi`` is the multi-agent orchestration standard built **on top of** the
canonical ``.toi`` file type. A ``.toi`` document states a person's preferences;
an ``.otoi`` charter declares how a mesh of agents honors a stack of those
documents at runtime. This package consumes ``nlt_toi`` directly — it does not
redefine the ``.toi`` shape, tiers, or resolution semantics.

The public API mirrors the TypeScript reference in snake_case, so the same
conformance fixtures pass under both implementations.

Example::

    from nlt_otoi import honor, propagate, HonorOptions

    policy = honor(charter, HonorOptions(documents=[personal_toi, project_toi]))
    prefs = propagate(policy, "research-agent")  # effective .toi for that agent
"""
from __future__ import annotations

# Constants and the enforcement/conflict vocabularies.
from .constants import (
    OTOI_CONFLICT_STRATEGIES,
    OTOI_ENFORCEMENT_MODES,
    OTOI_FILE_EXTENSION,
    OTOI_FORMAT_VERSION,
    OTOI_MEDIA_TYPE,
    OTOI_RESERVED_KEYS,
    OTOI_RESERVED_PREFIX,
    OTOI_TARGET_TOI_VERSION,
    OTOI_TOI_VERSION_POLICY,
    OTOI_UNSUPPORTED_STRATEGIES,
    OtoiConflictStrategy,
    OtoiEnforcementMode,
    OtoiUnsupportedStrategy,
)

# Charter schema (single source of truth) and inferred types.
from .schema import parse_with_defaults, schema_issues
from .types import OtoiAgent, OtoiCharter, OtoiEnforcement, OtoiSource

# The honoring layer.
from .honor import (
    EffectivePolicy,
    HonorOptions,
    ResolvedEnforcement,
    detect_conflicts,
    honor,
    parse_charter,
    propagate,
)

# ``.toi`` compatibility guard.
from .compat import assert_toi_compatible, is_toi_compatible

# Error taxonomy.
from .errors import (
    OtoiCompatibilityError,
    OtoiError,
    OtoiErrorCode,
    OtoiHonorError,
    OtoiIssue,
    OtoiParseError,
    OtoiValidationError,
    PolicyConflict,
)

# Re-export the canonical ``.toi`` primitives an ``.otoi`` consumer most often
# needs, so a single import surface covers both layers. The ``.toi`` standard
# remains the source of truth for everything below.
from nlt_toi import (
    TOI_FORMAT_VERSION,
    TOI_TIERS,
    ToiDocument,
    parse_toi,
    resolve_toi,
    safe_parse_toi,
    verify_toi,
)

#: A ``.toi`` interaction tier (``personal`` | ``community`` | ``project``).
#: The TS reference re-exports a ``ToiTier`` type alias; Python tiers are plain
#: strings drawn from :data:`TOI_TIERS`.
ToiTier = str

__version__ = "1.2.0"

__all__ = [
    # constants / vocabularies
    "OTOI_FORMAT_VERSION",
    "OTOI_TOI_VERSION_POLICY",
    "OTOI_TARGET_TOI_VERSION",
    "OTOI_FILE_EXTENSION",
    "OTOI_MEDIA_TYPE",
    "OTOI_RESERVED_PREFIX",
    "OTOI_RESERVED_KEYS",
    "OTOI_ENFORCEMENT_MODES",
    "OTOI_CONFLICT_STRATEGIES",
    "OTOI_UNSUPPORTED_STRATEGIES",
    "OtoiEnforcementMode",
    "OtoiConflictStrategy",
    "OtoiUnsupportedStrategy",
    # schema + types
    "schema_issues",
    "parse_with_defaults",
    "OtoiCharter",
    "OtoiAgent",
    "OtoiSource",
    "OtoiEnforcement",
    # honoring layer
    "parse_charter",
    "honor",
    "propagate",
    "detect_conflicts",
    "HonorOptions",
    "EffectivePolicy",
    "ResolvedEnforcement",
    # compatibility guard
    "assert_toi_compatible",
    "is_toi_compatible",
    # error taxonomy
    "OtoiError",
    "OtoiParseError",
    "OtoiValidationError",
    "OtoiHonorError",
    "OtoiCompatibilityError",
    "OtoiErrorCode",
    "OtoiIssue",
    "PolicyConflict",
    # re-exported `.toi` primitives
    "parse_toi",
    "safe_parse_toi",
    "verify_toi",
    "resolve_toi",
    "TOI_TIERS",
    "TOI_FORMAT_VERSION",
    "ToiDocument",
    "ToiTier",
    "__version__",
]
