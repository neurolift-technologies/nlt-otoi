"""``.toi`` compatibility guard for the ``.otoi`` honoring layer.

``.otoi`` honors a ``.toi`` document of *any* well-formed format version (see
:data:`~nlt_otoi.constants.OTOI_TOI_VERSION_POLICY`): publishing a new ``.toi``
release never requires a new ``.otoi`` release, so there is no per-version
allow-list to keep in sync. The one case ``.otoi`` cannot recover from is a
``.toi`` package that declares no valid format version at all — a broken or
pre-``1.0.1`` install whose runtime contract can't be trusted. There we fail
closed rather than honor documents against an unknown ``.toi`` format.

Ported faithfully from ``@neurolift-technologies/otoi`` ``src/compat.ts``.
"""
from __future__ import annotations

import re
from typing import Optional

import nlt_toi

from .constants import OTOI_FORMAT_VERSION
from .errors import OtoiCompatibilityError

# Matches a Semantic Version (MAJOR.MINOR.PATCH with optional pre-release/build).
_SEMVER = re.compile(
    r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)

# Sentinel distinguishing "no argument supplied" (read the installed version at
# call time, so a mocked ``nlt_toi`` is honored) from an explicit ``None``.
_UNSET = object()


def assert_toi_compatible(version=_UNSET) -> str:
    """Assert that the installed ``nlt_toi`` declares a usable ``.toi`` format
    version.

    Any well-formed semantic version is accepted — ``.otoi`` does not pin a
    ``.toi`` version (see :data:`~nlt_otoi.constants.OTOI_TOI_VERSION_POLICY`).
    The only rejection is a missing or malformed version, which signals an
    unusable ``.toi`` install.

    Args:
        version: The ``.toi`` format version to check. When omitted, the
            installed package's ``TOI_FORMAT_VERSION`` is read at call time.

    Returns:
        The validated version string.

    Raises:
        OtoiCompatibilityError: if *version* is missing or not a semantic
            version.
    """
    if version is _UNSET:
        version = getattr(nlt_toi, "TOI_FORMAT_VERSION", None)

    if not isinstance(version, str) or version.strip() == "":
        raise OtoiCompatibilityError(
            "The installed nlt-toi package declares no TOI_FORMAT_VERSION. "
            f".otoi v{OTOI_FORMAT_VERSION} honors any valid .toi format version, but the toi "
            "package must export one — install nlt-toi >= 1.0.1."
        )
    if not _SEMVER.match(version):
        raise OtoiCompatibilityError(
            f'The installed nlt-toi reports TOI_FORMAT_VERSION "{version}", which is '
            "not a semantic version; .otoi cannot honor .toi documents against it."
        )
    return version


def is_toi_compatible(version=_UNSET) -> bool:
    """Non-throwing form of :func:`assert_toi_compatible`: returns whether the
    given ``.toi`` format version (default: the installed one) is usable by
    ``.otoi``."""
    if version is _UNSET:
        version = getattr(nlt_toi, "TOI_FORMAT_VERSION", None)
    return isinstance(version, str) and bool(_SEMVER.match(version))
