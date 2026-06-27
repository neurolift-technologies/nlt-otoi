/**
 * `.toi` compatibility guard for the `.otoi` honoring layer.
 *
 * `.otoi` honors a `.toi` document of *any* well-formed format version (see
 * {@link OTOI_TOI_VERSION_POLICY}): publishing a new `.toi` release never
 * requires a new `.otoi` release, so there is no per-version allow-list to keep
 * in sync. The one case `.otoi` cannot recover from is a `.toi` package that
 * declares no valid format version at all — a broken or pre-`1.0.1` install
 * whose runtime contract can't be trusted. There we fail closed rather than
 * honor documents against an unknown `.toi` format.
 */
import * as toi from "@neurolift-technologies/toi";
import { OTOI_FORMAT_VERSION } from "./constants.js";
import { OtoiCompatibilityError } from "./errors.js";

/** Matches a Semantic Version (MAJOR.MINOR.PATCH with optional pre-release/build). */
const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;

/**
 * Assert that the installed `@neurolift-technologies/toi` declares a usable `.toi` format
 * version. Any well-formed semantic version is accepted — `.otoi` does not pin a
 * `.toi` version (see {@link OTOI_TOI_VERSION_POLICY}). The only rejection is a
 * missing or malformed version, which signals an unusable `.toi` install.
 *
 * @param version the `.toi` format version to check; defaults to the installed
 *   package's `TOI_FORMAT_VERSION`.
 * @returns the validated version string.
 * @throws {OtoiCompatibilityError} if `version` is missing or not a semantic version.
 */
export function assertToiCompatible(version: string | undefined = toi.TOI_FORMAT_VERSION): string {
  if (typeof version !== "string" || version.trim() === "") {
    throw new OtoiCompatibilityError(
      `The installed @neurolift-technologies/toi package declares no TOI_FORMAT_VERSION. ` +
        `.otoi v${OTOI_FORMAT_VERSION} honors any valid .toi format version, but the toi ` +
        `package must export one — install @neurolift-technologies/toi >= 1.0.1.`,
    );
  }
  if (!SEMVER.test(version)) {
    throw new OtoiCompatibilityError(
      `The installed @neurolift-technologies/toi reports TOI_FORMAT_VERSION "${version}", which is ` +
        `not a semantic version; .otoi cannot honor .toi documents against it.`,
    );
  }
  return version;
}

/**
 * Non-throwing form of {@link assertToiCompatible}: returns whether the given
 * `.toi` format version (default: the installed one) is usable by `.otoi`.
 */
export function isToiCompatible(version: string | undefined = toi.TOI_FORMAT_VERSION): boolean {
  return typeof version === "string" && SEMVER.test(version);
}
