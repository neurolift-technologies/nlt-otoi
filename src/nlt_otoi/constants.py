"""Canonical constants for the ``.otoi`` (Orchestrated Terms of Interaction)
honoring layer.

``.otoi`` is the orchestration standard that sits on top of the canonical
``.toi`` file type (``nlt-toi`` / ``@neurolift-technologies/toi``). A ``.toi``
document states a person's interaction preferences; an ``.otoi`` charter
describes how a multi-agent system *honors* those preferences at runtime — which
agents are bound, how a stack of ``.toi`` documents resolves, and what happens on
conflict or on an unsupported preference.

The ``.toi``-level constants (tiers, format version, file extension) are NOT
re-declared here — they are imported from ``nlt_toi``, the single source of
truth, exactly as that package's ``constants`` module anticipates.

Ported faithfully from ``@neurolift-technologies/otoi`` ``src/constants.ts``.
"""
from __future__ import annotations

from typing import Optional, Tuple

import nlt_toi

#: Format version of the ``.otoi`` specification this library implements.
OTOI_FORMAT_VERSION = "1.0.0"

#: ``.otoi``'s compatibility policy toward the ``.toi`` format.
#:
#: ``.otoi`` is deliberately **version-agnostic**: it honors a ``.toi`` document
#: of *any* well-formed format version, so publishing a new ``.toi`` release never
#: forces a new ``.otoi`` release. The only ``.toi`` install ``.otoi`` refuses is
#: one that declares no valid format version at all — see
#: :func:`nlt_otoi.compat.assert_toi_compatible`.
OTOI_TOI_VERSION_POLICY = "any"

#: The ``.toi`` format version the installed ``nlt_toi`` reports — read from that
#: package, the single source of truth.
#:
#: This is **informational, not a pin**: ``.otoi`` accepts any valid ``.toi``
#: version (:data:`OTOI_TOI_VERSION_POLICY`), so this value just tells you which
#: ``.toi`` format the current install resolves to. It is read with ``getattr``
#: rather than a ``from nlt_toi import TOI_FORMAT_VERSION``, so importing
#: ``nlt_otoi`` never crashes against a broken or pre-``1.0.0`` ``.toi`` package
#: that exports no format version — such an install simply leaves this ``None``,
#: and the compatibility guard (:func:`nlt_otoi.compat.assert_toi_compatible`)
#: raises a clear :class:`~nlt_otoi.errors.OtoiCompatibilityError` at runtime.
OTOI_TARGET_TOI_VERSION: Optional[str] = getattr(nlt_toi, "TOI_FORMAT_VERSION", None)

#: Canonical file extension for an Orchestrated Terms of Interaction charter.
OTOI_FILE_EXTENSION = ".otoi"

#: Registered media (MIME) type for ``.otoi`` charters (structured-syntax suffix
#: per RFC 6839).
OTOI_MEDIA_TYPE = "application/otoi+json"

#: Prefix marking the reserved namespace. Every ``$``-prefixed key is reserved.
OTOI_RESERVED_PREFIX = "$"

#: Reserved top-level keys defined by v1.0.0. Unknown ``$``-keys are
#: reserved-and-preserved.
OTOI_RESERVED_KEYS: Tuple[str, ...] = ("$otoi", "$id", "$created", "$updated")

#: Enforcement modes, in ascending order of strictness.
#:
#: - ``advisory``: agents are informed of preferences but not held to them.
#: - ``enforced``: agents must honor resolved preferences; unsupported ones
#:   degrade.
#: - ``strict``: any unsupported preference or unknown agent is a hard failure.
OTOI_ENFORCEMENT_MODES: Tuple[str, ...] = ("advisory", "enforced", "strict")

#: How to handle two same-tier documents that disagree on the same leaf.
OTOI_CONFLICT_STRATEGIES: Tuple[str, ...] = ("highest-tier-wins", "reject", "escalate")

#: How to handle a stated preference no agent in the mesh can satisfy.
OTOI_UNSUPPORTED_STRATEGIES: Tuple[str, ...] = ("ignore", "degrade", "reject")

#: Type aliases mirroring the TS string-literal union types. Python has no
#: closed-string type at runtime; these document the accepted values.
OtoiEnforcementMode = str  # one of OTOI_ENFORCEMENT_MODES
OtoiConflictStrategy = str  # one of OTOI_CONFLICT_STRATEGIES
OtoiUnsupportedStrategy = str  # one of OTOI_UNSUPPORTED_STRATEGIES
