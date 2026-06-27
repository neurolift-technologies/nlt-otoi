"""Public type aliases for ``.otoi`` charters.

In the TypeScript reference these are inferred from the Zod charter schema
(``z.infer<...>``) so they can never drift from validation. Python validates with
a hand-written validator (see :mod:`nlt_otoi.schema`) and represents a parsed
charter as a plain ``dict`` — an *open* JSON object whose unknown keys are
preserved. These aliases document the structural shape; they are not enforced at
runtime beyond what :func:`nlt_otoi.honor.parse_charter` checks.

Ported from ``@neurolift-technologies/otoi`` ``src/types.ts``.
"""
from __future__ import annotations

from typing import Any, Dict

#: A fully-parsed, schema-valid ``.otoi`` charter.
OtoiCharter = Dict[str, Any]

#: A mesh participant bound to honor the resolved preferences.
OtoiAgent = Dict[str, Any]

#: A reference to a ``.toi`` document participating in resolution.
OtoiSource = Dict[str, Any]

#: Raw (pre-default) enforcement settings as authored in the charter.
OtoiEnforcement = Dict[str, Any]
