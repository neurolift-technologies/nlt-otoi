/**
 * Public TypeScript types, inferred from the canonical charter schema so they
 * can never drift from validation.
 */
import type { z } from "zod";
import type {
  otoiAgentSchema,
  otoiCharterSchema,
  otoiEnforcementSchema,
  otoiSourceSchema,
} from "./schema.js";

/** A fully-parsed, schema-valid `.otoi` charter. */
export type OtoiCharter = z.infer<typeof otoiCharterSchema>;

/** A mesh participant bound to honor the resolved preferences. */
export type OtoiAgent = z.infer<typeof otoiAgentSchema>;

/** A reference to a `.toi` document participating in resolution. */
export type OtoiSource = z.infer<typeof otoiSourceSchema>;

/** Raw (pre-default) enforcement settings as authored in the charter. */
export type OtoiEnforcement = z.infer<typeof otoiEnforcementSchema>;
