/**
 * Error taxonomy for the `.otoi` honoring layer, mirroring `@neurolift-technologies/toi`'s
 * pattern: every error is an `OtoiError` carrying a discriminating `code`.
 */

export type OtoiErrorCode = "PARSE" | "VALIDATION" | "HONOR";

/** A single charter-schema violation, flattened to a dotted path and a message. */
export interface OtoiIssue {
  readonly path: string;
  readonly message: string;
}

/** A same-tier disagreement on a single leaf field across two `.toi` documents. */
export interface PolicyConflict {
  /** The tier whose documents disagree. */
  readonly tier: string;
  /** Dotted path to the contested leaf (e.g. `communication.tone`). */
  readonly path: string;
  /** The distinct values asserted at that path. */
  readonly values: readonly unknown[];
}

/** Base class for every error raised by this library. */
export class OtoiError extends Error {
  readonly code: OtoiErrorCode;
  constructor(code: OtoiErrorCode, message: string, options?: { cause?: unknown }) {
    super(message, options);
    this.name = new.target.name;
    this.code = code;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

/** Input was not well-formed JSON, or its root was not a JSON object. */
export class OtoiParseError extends OtoiError {
  constructor(message: string, options?: { cause?: unknown }) {
    super("PARSE", message, options);
  }
}

/** A charter violated the `.otoi` schema. */
export class OtoiValidationError extends OtoiError {
  readonly issues: readonly OtoiIssue[];
  constructor(message: string, issues: readonly OtoiIssue[], options?: { cause?: unknown }) {
    super("VALIDATION", message, options);
    this.issues = issues;
  }
}

/**
 * Honoring could not be completed: no documents to resolve, an unresolved
 * conflict under a `reject` strategy, or an unsupported preference under
 * `strict` enforcement.
 */
export class OtoiHonorError extends OtoiError {
  readonly conflicts: readonly PolicyConflict[];
  constructor(message: string, conflicts: readonly PolicyConflict[] = [], options?: { cause?: unknown }) {
    super("HONOR", message, options);
    this.conflicts = conflicts;
  }
}
