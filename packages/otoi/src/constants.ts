/**
 * Canonical constants for the `.otoi` (Orchestrated Terms of Interaction)
 * honoring layer.
 *
 * `.otoi` is the orchestration standard that sits on top of the canonical
 * `.toi` file type ({@link https://www.npmjs.com/package/@neurolift-technologies/toi}). A
 * `.toi` document states a person's interaction preferences; an `.otoi` charter
 * describes how a multi-agent system *honors* those preferences at runtime —
 * which agents are bound, how a stack of `.toi` documents resolves, and what
 * happens on conflict or on an unsupported preference.
 *
 * The `.toi`-level constants (tiers, format version, file extension) are NOT
 * re-declared here — they are imported from `@neurolift-technologies/toi`, the single source
 * of truth, exactly as that package's `constants.ts` anticipates.
 */
import { TOI_FORMAT_VERSION } from "@neurolift-technologies/toi";

/** Format version of the `.otoi` specification this library implements. */
export const OTOI_FORMAT_VERSION = "1.0.0";

/** The `.toi` format version this `.otoi` version is designed to honor. */
export const OTOI_TARGET_TOI_VERSION = TOI_FORMAT_VERSION;

/** Canonical file extension for an Orchestrated Terms of Interaction charter. */
export const OTOI_FILE_EXTENSION = ".otoi";

/** Registered media (MIME) type for `.otoi` charters (structured-syntax suffix per RFC 6839). */
export const OTOI_MEDIA_TYPE = "application/otoi+json";

/** Prefix marking the reserved namespace. Every `$`-prefixed key is reserved. */
export const OTOI_RESERVED_PREFIX = "$";

/** Reserved top-level keys defined by v1.0.0. Unknown `$`-keys are reserved-and-preserved. */
export const OTOI_RESERVED_KEYS = ["$otoi", "$id", "$created", "$updated"] as const;

/**
 * Enforcement modes, in ascending order of strictness.
 * - `advisory`: agents are informed of preferences but not held to them.
 * - `enforced`: agents must honor resolved preferences; unsupported ones degrade.
 * - `strict`: any unsupported preference or unknown agent is a hard failure.
 */
export const OTOI_ENFORCEMENT_MODES = ["advisory", "enforced", "strict"] as const;
export type OtoiEnforcementMode = (typeof OTOI_ENFORCEMENT_MODES)[number];

/** How to handle two same-tier documents that disagree on the same leaf. */
export const OTOI_CONFLICT_STRATEGIES = ["highest-tier-wins", "reject", "escalate"] as const;
export type OtoiConflictStrategy = (typeof OTOI_CONFLICT_STRATEGIES)[number];

/** How to handle a stated preference no agent in the mesh can satisfy. */
export const OTOI_UNSUPPORTED_STRATEGIES = ["ignore", "degrade", "reject"] as const;
export type OtoiUnsupportedStrategy = (typeof OTOI_UNSUPPORTED_STRATEGIES)[number];
