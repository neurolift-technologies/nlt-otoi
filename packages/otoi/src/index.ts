/**
 * `@neurolift-technologies/otoi` — reference implementation of the `.otoi` (Orchestrated
 * Terms of Interaction) honoring layer.
 *
 * `.otoi` is the multi-agent orchestration standard built **on top of** the
 * canonical `.toi` file type. A `.toi` document states a person's preferences;
 * an `.otoi` charter declares how a mesh of agents honors a stack of those
 * documents at runtime. This package consumes `@neurolift-technologies/toi` directly — it
 * does not redefine the `.toi` shape, tiers, or resolution semantics.
 *
 * @example
 * ```ts
 * import { honor, propagate } from "@neurolift-technologies/otoi";
 *
 * const policy = await honor(charter, { documents: [personalToi, projectToi] });
 * const prefs = propagate(policy, "research-agent"); // effective .toi for that agent
 * ```
 */

// Constants and the enforcement/conflict vocabularies.
export {
  OTOI_FORMAT_VERSION,
  OTOI_TOI_VERSION_POLICY,
  OTOI_TARGET_TOI_VERSION,
  OTOI_FILE_EXTENSION,
  OTOI_MEDIA_TYPE,
  OTOI_RESERVED_PREFIX,
  OTOI_RESERVED_KEYS,
  OTOI_ENFORCEMENT_MODES,
  OTOI_CONFLICT_STRATEGIES,
  OTOI_UNSUPPORTED_STRATEGIES,
  type OtoiEnforcementMode,
  type OtoiConflictStrategy,
  type OtoiUnsupportedStrategy,
} from "./constants.js";

// Charter schema (single source of truth) and inferred types.
export {
  otoiCharterSchema,
  otoiAgentSchema,
  otoiSourceSchema,
  otoiEnforcementSchema,
} from "./schema.js";
export type { OtoiCharter, OtoiAgent, OtoiSource, OtoiEnforcement } from "./types.js";

// The honoring layer.
export {
  parseCharter,
  honor,
  propagate,
  detectConflicts,
  type HonorOptions,
  type EffectivePolicy,
  type ResolvedEnforcement,
} from "./honor.js";

// `.toi` compatibility guard.
export { assertToiCompatible, isToiCompatible } from "./compat.js";

// Error taxonomy.
export {
  OtoiError,
  OtoiParseError,
  OtoiValidationError,
  OtoiHonorError,
  OtoiCompatibilityError,
  type OtoiErrorCode,
  type OtoiIssue,
  type PolicyConflict,
} from "./errors.js";

// Re-export the canonical `.toi` primitives an `.otoi` consumer most often
// needs, so a single import surface covers both layers. The `.toi` standard
// remains the source of truth for everything below.
export {
  parseToi,
  safeParseToi,
  verifyToi,
  resolveToi,
  TOI_TIERS,
  TOI_FORMAT_VERSION,
  type ToiDocument,
  type ToiTier,
} from "@neurolift-technologies/toi";
