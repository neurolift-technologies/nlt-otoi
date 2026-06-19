# `@neurolift-technologies/otoi`

Reference implementation of the **`.otoi` (Orchestrated Terms of Interaction)**
honoring layer — the multi-agent orchestration standard built on top of the
canonical [`@neurolift-technologies/toi`](https://www.npmjs.com/package/@neurolift-technologies/toi) file
type.

> A `.toi` document states **a person's** interaction preferences.
> An `.otoi` charter declares **how a mesh of agents honors** a stack of those
> documents at runtime: which agents are bound, how the `.toi` stack resolves,
> and what happens on conflict or on an unsupported preference.

This package **consumes** `@neurolift-technologies/toi` rather than re-implementing it. The
`.toi` shape, tiers, resolution semantics, canonicalization, and signatures all
remain the property of the `.toi` standard; `.otoi` adds only the orchestration
concerns the `.toi` spec deliberately leaves out.

## Install

```bash
npm install @neurolift-technologies/otoi
# @neurolift-technologies/toi is a regular dependency and is installed automatically with it
```

## Quick start

```ts
import { honor, propagate, type ToiDocument } from "@neurolift-technologies/otoi";

const charter = {
  $otoi: "1.0.0",
  agents: [{ id: "research-agent" }, { id: "summary-agent" }],
  enforcement: { mode: "enforced", on_conflict: "highest-tier-wins" },
  toi_sources: [
    { tier: "personal", uri: "users/josh.toi" },
    { tier: "project", inline: { $toi: "1.0.0", $tier: "project", identity: { author: "nlt-redteam" } } },
  ],
};

const policy = await honor(charter, {
  loadSource: (uri) => fs.readFile(uri, "utf8"),
  platformDefaults: { communication: { language: "en" } },
});

// The single effective .toi view every agent honors:
policy.effective;            // resolved ToiDocument
policy.tiers;                // ["personal", "project"]
policy.conflicts;            // same-tier disagreements, if any

// Per-agent propagation (strict mode refuses unknown agents):
const prefs = propagate(policy, "research-agent");
```

## API

| Export | Purpose |
| --- | --- |
| `parseCharter(input)` | Parse + validate an `.otoi` charter (throws `OtoiParseError` / `OtoiValidationError`). |
| `honor(charter, options)` | Resolve the charter's `.toi` sources into one `EffectivePolicy`. |
| `propagate(policy, agentId)` | The effective `.toi` an agent must honor; refuses unknown agents under `strict`. |
| `detectConflicts(documents)` | Report same-tier leaf disagreements (cross-tier differences are *not* conflicts). |
| `otoiCharterSchema` | The Zod source of truth for the charter shape. |
| re-exports | `parseToi`, `resolveToi`, `verifyToi`, `TOI_TIERS`, `ToiDocument`, … from `@neurolift-technologies/toi`. |

## Enforcement model

| Field | Values | Default | Meaning |
| --- | --- | --- | --- |
| `mode` | `advisory` / `enforced` / `strict` | `enforced` | How strictly agents are held to preferences; `strict` also refuses unknown agents. |
| `on_conflict` | `highest-tier-wins` / `reject` / `escalate` | `highest-tier-wins` | What to do with a same-tier disagreement. `reject` throws `OtoiHonorError`. |
| `on_unsupported` | `ignore` / `degrade` / `reject` | `degrade` | What to do with a preference no agent can satisfy. |
| `audit` | boolean | `true` | Whether honoring should be recorded for the audit trail. |

## Relationship to the `.toi` standard

See [`SPEC.md`](./SPEC.md) for the normative `.otoi` specification and the
[`@neurolift-technologies/toi` SPEC](https://www.npmjs.com/package/@neurolift-technologies/toi) for the
underlying file format. Where the two disagree, the `.toi` spec governs the
`.toi` layer and this spec governs orchestration.

## License

This package is MIT licensed; see `packages/otoi/package.json` and the
repository root [`LICENSE`](../../LICENSE). The canonical
`@neurolift-technologies/toi` package that this layer builds on is published
separately and currently declares Apache-2.0 in its own package metadata, so
dependency license notes should cite that package directly rather than infer its
terms from this repository.
