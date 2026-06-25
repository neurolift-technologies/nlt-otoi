"""Error taxonomy for the ``.otoi`` honoring layer, mirroring ``nlt_toi``'s
pattern: every error is an :class:`OtoiError` carrying a discriminating
``code``.

Ported faithfully from ``@neurolift-technologies/otoi`` ``src/errors.ts``.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence, Tuple

#: The closed set of error codes: ``PARSE`` | ``VALIDATION`` | ``HONOR`` |
#: ``COMPAT``.
OtoiErrorCode = str


@dataclass(frozen=True)
class OtoiIssue:
    """A single charter-schema violation, flattened to a dotted path and a
    message."""

    path: str
    message: str


@dataclass(frozen=True)
class PolicyConflict:
    """A same-tier disagreement on a single leaf field across two ``.toi``
    documents."""

    #: The tier whose documents disagree.
    tier: str
    #: Dotted path to the contested leaf (e.g. ``communication.tone``).
    path: str
    #: The distinct values asserted at that path.
    values: Tuple[Any, ...]


class OtoiError(Exception):
    """Base class for every error raised by this library."""

    code: OtoiErrorCode

    def __init__(self, code: OtoiErrorCode, message: str) -> None:
        super().__init__(message)
        self.name = type(self).__name__
        self.code = code


class OtoiParseError(OtoiError):
    """Input was not well-formed JSON, or its root was not a JSON object."""

    def __init__(self, message: str) -> None:
        super().__init__("PARSE", message)


class OtoiValidationError(OtoiError):
    """A charter violated the ``.otoi`` schema."""

    def __init__(self, message: str, issues: Sequence[OtoiIssue]) -> None:
        super().__init__("VALIDATION", message)
        self.issues: Tuple[OtoiIssue, ...] = tuple(issues)


class OtoiHonorError(OtoiError):
    """Honoring could not be completed: no documents to resolve, an unresolved
    conflict under a ``reject`` strategy, or an unsupported preference under
    ``strict`` enforcement."""

    def __init__(self, message: str, conflicts: Sequence[PolicyConflict] = ()) -> None:
        super().__init__("HONOR", message)
        self.conflicts: Tuple[PolicyConflict, ...] = tuple(conflicts)


class OtoiCompatibilityError(OtoiError):
    """The installed ``nlt_toi`` cannot be honored because it declares no valid
    ``.toi`` format version.

    ``.otoi`` is version-agnostic — it accepts a ``.toi`` document of any
    well-formed format version — so this is raised only for a broken or
    pre-``1.0.0`` ``.toi`` install whose runtime contract can't be trusted.
    """

    def __init__(self, message: str) -> None:
        super().__init__("COMPAT", message)
