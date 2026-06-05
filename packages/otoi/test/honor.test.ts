import { describe, expect, it } from "vitest";
import { detectConflicts, honor, parseCharter, propagate } from "../src/index.js";
import type { ToiDocument } from "../src/index.js";

const personal: ToiDocument = {
  $toi: "1.0.0",
  $tier: "personal",
  identity: { author: "josh" },
  communication: { tone: "direct" },
} as ToiDocument;

const project: ToiDocument = {
  $toi: "1.0.0",
  $tier: "project",
  identity: { author: "nlt-redteam" },
  communication: { tone: "professional", verbosity: "concise" },
} as ToiDocument;

const charter = {
  $otoi: "1.0.0",
  agents: [{ id: "research-agent" }],
};

describe("honor", () => {
  it("resolves a stack with terminal personal precedence and project gap-fill", async () => {
    const policy = await honor(charter, { documents: [project, personal] });
    // personal is terminal for tone; project only fills the gap (verbosity).
    expect(policy.effective.communication?.tone).toBe("direct");
    expect(policy.effective.communication?.verbosity).toBe("concise");
    expect(policy.tiers).toEqual(["personal", "project"]);
    expect(policy.conflicts).toEqual([]);
  });

  it("requires at least one document", async () => {
    await expect(honor(charter, {})).rejects.toThrow(/at least one .toi document/);
  });

  it("loads uri-backed sources via loadSource", async () => {
    const withSource = {
      $otoi: "1.0.0",
      toi_sources: [{ tier: "personal", uri: "me.toi" }],
    };
    const policy = await honor(withSource, {
      loadSource: () => JSON.stringify(personal),
    });
    expect(policy.effective.identity.author).toBe("josh");
  });

  it("rejects a uri source when no loader is supplied", async () => {
    const withSource = { $otoi: "1.0.0", toi_sources: [{ tier: "personal", uri: "me.toi" }] };
    await expect(honor(withSource, {})).rejects.toThrow(/no loadSource/);
  });
});

describe("detectConflicts", () => {
  it("finds same-tier leaf disagreements", () => {
    // Same author (no conflict there); only `communication.tone` disagrees.
    const a: ToiDocument = { $toi: "1.0.0", $tier: "project", identity: { author: "team" }, communication: { tone: "formal" } } as ToiDocument;
    const b: ToiDocument = { $toi: "1.0.0", $tier: "project", identity: { author: "team" }, communication: { tone: "casual" } } as ToiDocument;
    const conflicts = detectConflicts([a, b]);
    expect(conflicts).toHaveLength(1);
    expect(conflicts[0]?.path).toBe("communication.tone");
  });

  it("does not treat cross-tier differences as conflicts", () => {
    expect(detectConflicts([personal, project])).toEqual([]);
  });

  it("on_conflict=reject turns a same-tier conflict into a thrown error", async () => {
    const a: ToiDocument = { $toi: "1.0.0", $tier: "project", identity: { author: "a" }, communication: { tone: "formal" } } as ToiDocument;
    const b: ToiDocument = { $toi: "1.0.0", $tier: "project", identity: { author: "b" }, communication: { tone: "casual" } } as ToiDocument;
    const strictCharter = { $otoi: "1.0.0", enforcement: { on_conflict: "reject" } };
    await expect(honor(strictCharter, { documents: [a, b] })).rejects.toThrow(/conflict/i);
  });
});

describe("propagate", () => {
  it("returns the effective policy for a declared agent", async () => {
    const policy = await honor(charter, { documents: [personal] });
    expect(propagate(policy, "research-agent")).toBe(policy.effective);
  });

  it("refuses an unknown agent under strict enforcement", async () => {
    const strict = { $otoi: "1.0.0", agents: [{ id: "known" }], enforcement: { mode: "strict" } };
    const policy = await honor(strict, { documents: [personal] });
    expect(() => propagate(policy, "stranger")).toThrow(/strict enforcement/);
  });
});

describe("parseCharter", () => {
  it("rejects a non-object root", () => {
    expect(() => parseCharter("[]")).toThrow(/must be a JSON object/);
  });

  it("rejects a charter missing $otoi", () => {
    expect(() => parseCharter({ agents: [] })).toThrow(/Invalid .otoi charter/);
  });
});
