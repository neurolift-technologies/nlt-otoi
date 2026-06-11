/**
 * Canonical `.otoi` v1.0.0 charter schema — the single source of truth for the
 * orchestration layer.
 *
 * An `.otoi` charter is declarative, like a `.toi` document: it never contains
 * code or prompts. It names the `.toi` sources in force, the agents bound to
 * honor them, and the enforcement policy. The actual interaction preferences
 * live in the referenced `.toi` documents and are validated by `@neurolift/toi`
 * — this schema deliberately treats inline `.toi` payloads as opaque
 * (`unknown`) and defers to `parseToi` at honor time, so there is exactly one
 * validator for the `.toi` shape.
 *
 * Every object is a `looseObject` for the same additive forward-compatibility
 * the `.toi` standard guarantees: unknown keys are preserved, never rejected.
 */
import { z } from "zod";
import { TOI_TIERS } from "@neurolift/toi";
import {
  OTOI_CONFLICT_STRATEGIES,
  OTOI_ENFORCEMENT_MODES,
  OTOI_UNSUPPORTED_STRATEGIES,
} from "./constants.js";

/** Semantic version, e.g. `1.0.0`, `1.2.0-rc.1`. */
const semver = z
  .string()
  .regex(
    /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/,
    "must be a semantic version (MAJOR.MINOR.PATCH)",
  );

/** ISO 8601 calendar date or date-time (offset optional). */
const isoDateTime = z
  .string()
  .regex(
    /^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?)?$/,
    "must be an ISO 8601 date or date-time",
  );

/** RFC 4122 version-4 UUID. */
const uuidV4 = z
  .string()
  .regex(
    /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
    "must be a version-4 UUID",
  );

/** A participant in the mesh that must honor the resolved `.toi` preferences. */
export const otoiAgentSchema = z.looseObject({
  id: z.string().min(1),
  role: z.string().optional(),
  modalities: z.array(z.string()).optional(),
  affordances: z.array(z.string()).optional(),
});

/**
 * A reference to one `.toi` document that participates in resolution. A source
 * MUST provide either a `uri` to load or an `inline` document; `inline` is left
 * opaque here and validated by `@neurolift/toi` at honor time.
 */
export const otoiSourceSchema = z
  .looseObject({
    tier: z.enum(TOI_TIERS),
    uri: z.string().optional(),
    inline: z.unknown().optional(),
  })
  .refine((s) => (s.uri !== undefined) !== (s.inline !== undefined), {
    message: "a toi_source must provide exactly one of `uri` or `inline`",
  });

/** How preferences are propagated and what happens on conflict / unsupported. */
export const otoiEnforcementSchema = z.looseObject({
  mode: z.enum(OTOI_ENFORCEMENT_MODES).optional(),
  on_conflict: z.enum(OTOI_CONFLICT_STRATEGIES).optional(),
  on_unsupported: z.enum(OTOI_UNSUPPORTED_STRATEGIES).optional(),
  audit: z.boolean().optional(),
});

/** The canonical `.otoi` charter schema. */
export const otoiCharterSchema = z.looseObject({
  // Reserved namespace.
  $otoi: semver,
  $id: uuidV4.optional(),
  $created: isoDateTime.optional(),
  $updated: isoDateTime.optional(),

  // Who authored the charter (distinct from the .toi authors it honors).
  identity: z.looseObject({ author: z.string().min(1) }).optional(),

  // The mesh and how it honors preferences.
  agents: z.array(otoiAgentSchema).default([]),
  enforcement: otoiEnforcementSchema.optional(),
  toi_sources: z.array(otoiSourceSchema).default([]),
});
