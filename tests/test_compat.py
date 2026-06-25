"""Port of ``@neurolift-technologies/otoi`` ``test/compat.test.ts`` and
``test/compat.broken-toi.test.ts`` to pytest.

The ``.toi`` compatibility guard must accept any well-formed semantic version and
fail closed only when the installed ``.toi`` declares no usable version — the
same behavior the TypeScript reference asserts.
"""
from __future__ import annotations

import pytest

import nlt_toi
from nlt_otoi import (
    OTOI_TOI_VERSION_POLICY,
    TOI_FORMAT_VERSION,
    OtoiCompatibilityError,
    assert_toi_compatible,
    is_toi_compatible,
)

# A `.toi` install that exports no format version surfaces at runtime as a
# non-string `TOI_FORMAT_VERSION`. The TS suite casts a runtime non-string
# through the `string` type; here we pass `None` directly.
MISSING_VERSION = None


class TestAssertToiCompatible:
    def test_accepts_any_well_formed_version_no_pin(self):
        assert assert_toi_compatible("1.0.0") == "1.0.0"
        assert assert_toi_compatible("1.5.2") == "1.5.2"
        assert assert_toi_compatible("2.0.0") == "2.0.0"
        assert assert_toi_compatible("1.0.0-rc.1") == "1.0.0-rc.1"
        assert assert_toi_compatible("1.2.3+build.4") == "1.2.3+build.4"

    def test_defaults_to_installed_version_which_is_valid(self):
        assert assert_toi_compatible() == TOI_FORMAT_VERSION

    def test_throws_when_installed_toi_declares_no_version(self):
        with pytest.raises(OtoiCompatibilityError):
            assert_toi_compatible(MISSING_VERSION)
        with pytest.raises(OtoiCompatibilityError, match=r"declares no TOI_FORMAT_VERSION"):
            assert_toi_compatible(MISSING_VERSION)
        with pytest.raises(OtoiCompatibilityError):
            assert_toi_compatible("")
        with pytest.raises(OtoiCompatibilityError, match=r"declares no TOI_FORMAT_VERSION"):
            assert_toi_compatible("   ")

    def test_throws_when_version_is_not_semver(self):
        with pytest.raises(OtoiCompatibilityError, match=r"not a semantic version"):
            assert_toi_compatible("1.0")
        with pytest.raises(OtoiCompatibilityError):
            assert_toi_compatible("latest")
        with pytest.raises(OtoiCompatibilityError, match=r"not a semantic version"):
            assert_toi_compatible("v1.0.0")

    def test_carries_compat_discriminating_code(self):
        with pytest.raises(OtoiCompatibilityError) as exc_info:
            assert_toi_compatible(MISSING_VERSION)
        assert exc_info.value.code == "COMPAT"


class TestIsToiCompatible:
    def test_true_for_valid_false_for_missing_or_malformed(self):
        assert is_toi_compatible("1.0.0") is True
        assert is_toi_compatible("9.9.9") is True
        assert is_toi_compatible() is True  # installed version is valid
        assert is_toi_compatible(MISSING_VERSION) is False
        assert is_toi_compatible("") is False
        assert is_toi_compatible("nope") is False


class TestOtoiToiVersionPolicy:
    def test_declares_version_agnostic_policy(self):
        assert OTOI_TOI_VERSION_POLICY == "any"


class TestBrokenToiInstall:
    """Mirrors ``test/compat.broken-toi.test.ts``: a resolvable ``.toi`` package
    that exports no ``TOI_FORMAT_VERSION``. The no-argument call (as ``honor()``
    makes it) must fail closed."""

    def test_fails_closed_on_no_argument_call(self, monkeypatch):
        monkeypatch.setattr(nlt_toi, "TOI_FORMAT_VERSION", None, raising=False)
        with pytest.raises(OtoiCompatibilityError, match=r"declares no TOI_FORMAT_VERSION"):
            assert_toi_compatible()

    def test_is_toi_compatible_reports_false(self, monkeypatch):
        monkeypatch.setattr(nlt_toi, "TOI_FORMAT_VERSION", None, raising=False)
        assert is_toi_compatible() is False
