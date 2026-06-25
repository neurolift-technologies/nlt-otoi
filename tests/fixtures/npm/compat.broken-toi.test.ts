import { describe, expect, it, vi } from "vitest";

// Simulate a broken or pre-1.0.1 `@neurolift-technologies/toi` install: the package is
// resolvable but exports no `TOI_FORMAT_VERSION`. `assertToiCompatible()` (called
// with no argument, as `honor()` calls it) must fail closed rather than honor
// `.toi` documents against an unknown format contract.
vi.mock("@neurolift-technologies/toi", () => ({ TOI_FORMAT_VERSION: undefined }));

const { assertToiCompatible, isToiCompatible } = await import("../src/compat.js");

describe("assertToiCompatible with a .toi install that declares no version", () => {
  it("fails closed on the no-argument call", () => {
    expect(() => assertToiCompatible()).toThrow(/declares no TOI_FORMAT_VERSION/);
  });

  it("isToiCompatible() reports false", () => {
    expect(isToiCompatible()).toBe(false);
  });
});
