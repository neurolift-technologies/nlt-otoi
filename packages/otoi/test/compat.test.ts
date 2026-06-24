import { describe, expect, it } from "vitest";
import {
  assertToiCompatible,
  isToiCompatible,
  OtoiCompatibilityError,
  OTOI_TOI_VERSION_POLICY,
  TOI_FORMAT_VERSION,
} from "../src/index.js";

// A `.toi` install that exports no format version surfaces at runtime as a
// non-string `TOI_FORMAT_VERSION`. TypeScript's type says `string`, so we cast a
// runtime non-string through it to exercise that path without a module mock
// (see compat.broken-toi.test.ts for the no-argument, mocked variant).
const missingVersion = null as unknown as string;

describe("assertToiCompatible", () => {
  it("accepts any well-formed .toi format version (no version pin)", () => {
    expect(assertToiCompatible("1.0.0")).toBe("1.0.0");
    expect(assertToiCompatible("1.5.2")).toBe("1.5.2");
    expect(assertToiCompatible("2.0.0")).toBe("2.0.0");
    expect(assertToiCompatible("1.0.0-rc.1")).toBe("1.0.0-rc.1");
    expect(assertToiCompatible("1.2.3+build.4")).toBe("1.2.3+build.4");
  });

  it("defaults to the installed TOI_FORMAT_VERSION, which is valid", () => {
    expect(assertToiCompatible()).toBe(TOI_FORMAT_VERSION);
  });

  it("throws when the installed .toi declares no format version", () => {
    expect(() => assertToiCompatible(missingVersion)).toThrow(OtoiCompatibilityError);
    expect(() => assertToiCompatible(missingVersion)).toThrow(/declares no TOI_FORMAT_VERSION/);
    expect(() => assertToiCompatible("")).toThrow(OtoiCompatibilityError);
    expect(() => assertToiCompatible("   ")).toThrow(/declares no TOI_FORMAT_VERSION/);
  });

  it("throws when the format version is not a semantic version", () => {
    expect(() => assertToiCompatible("1.0")).toThrow(/not a semantic version/);
    expect(() => assertToiCompatible("latest")).toThrow(OtoiCompatibilityError);
    expect(() => assertToiCompatible("v1.0.0")).toThrow(/not a semantic version/);
  });

  it("carries the COMPAT discriminating code", () => {
    try {
      assertToiCompatible(missingVersion);
      expect.unreachable("should have thrown");
    } catch (err) {
      expect(err).toBeInstanceOf(OtoiCompatibilityError);
      expect((err as OtoiCompatibilityError).code).toBe("COMPAT");
    }
  });
});

describe("isToiCompatible", () => {
  it("is true for any valid semantic version, false for a missing/malformed one", () => {
    expect(isToiCompatible("1.0.0")).toBe(true);
    expect(isToiCompatible("9.9.9")).toBe(true);
    expect(isToiCompatible()).toBe(true); // installed version is valid
    expect(isToiCompatible(missingVersion)).toBe(false);
    expect(isToiCompatible("")).toBe(false);
    expect(isToiCompatible("nope")).toBe(false);
  });
});

describe("OTOI_TOI_VERSION_POLICY", () => {
  it("declares the version-agnostic policy", () => {
    expect(OTOI_TOI_VERSION_POLICY).toBe("any");
  });
});
