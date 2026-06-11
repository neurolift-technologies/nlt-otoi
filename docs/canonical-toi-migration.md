# Migrating to the canonical `.toi` standard

This repository now adopts the canonical **`.toi`** file format
([`@neurolift/toi`](https://www.npmjs.com/package/@neurolift/toi)) as the source
of truth for individual interaction preferences, orchestrated by the new
**`.otoi`** layer ([`@neurolift/otoi`](../packages/otoi/README.md)) in this repo.

The legacy JSON Schemas under `schemas/` (`personal-toi.schema.json`,
`collaborative-charter.schema.json`) are **deprecated**. They remain only to
validate pre-existing documents and will be removed in a future major version.

## Why

The old `personal-toi` shape (`version` / `metadata` / `communication` /
`cognitive` / `privacy`) predates the standardized `.toi` format and is not
interoperable with it. The canonical `.toi` format is declarative, signable
(Ed25519 / RFC 8785), tiered (`personal` > `community` > `project`), and is the
shared standard across the NeuroLift Solidarity Framework. Consuming it — rather
than maintaining a parallel shape — is the whole point of this change.

## Shape at a glance

```jsonc
// Legacy (deprecated)                     // Canonical .toi
{                                          {
  "version": "1.0.0",                        "$toi": "1.0.0",
  "metadata": {                              "$tier": "personal",
    "author": "josh",                        "$created": "2026-06-05",
    "created": "2026-06-05T..."              "identity": { "author": "josh" },
  },                                         "communication": { ... },
  "communication": { ... },                  "cognitive_profile": { ... },
  "cognitive": { ... },                      "privacy": { ... }
  "privacy": { ... }                       }
}
```

## Field mapping

| Legacy field | Canonical `.toi` field | Notes |
| --- | --- | --- |
| `version` | `$toi` | Format version; the canonical value is `"1.0.0"`. Also add a `$tier`. |
| *(none)* | `$tier` | **Required.** One of `personal`, `community`, `project`. |
| `metadata.author` | `identity.author` | `identity` is the only required content section. |
| `metadata.created` / `updated` | `$created` / `$updated` | ISO 8601. |
| `communication.style` | `communication.tone` | `formal`/`casual`/`professional`/`friendly`/`adaptive`; `direct` is also a tone. |
| `communication.directness` | `communication.tone: "direct"` | No separate directness axis; fold into `tone` or drop. |
| `communication.explanation_level` | `communication.verbosity` | `minimal`/`concise`/`detailed`/`comprehensive`. |
| `cognitive.information_structure` | `communication.structure` | `linear`/`hierarchical`/`visual`/`bullet-points`/`narrative`. |
| `cognitive.attention_span` | `cognitive_profile.attention_model` | `short-bursts`/`sustained`/`hyperfocus-prone`/`variable`. |
| `cognitive.processing_time` | `cognitive_profile.*` | No 1:1 field; capture via `scaffolding_preference` / `energy_model` or `custom`. |
| `privacy.data_retention` | `privacy.retention` | `session-only`/`short-term`/`long-term`/`permanent`/`user-controlled`. |
| `privacy.sharing_consent` | `privacy.cross_platform_sharing` | `never`/`explicit-only`/`aggregate-only`/`research-approved`. |

Anything the canonical schema does not model goes under the `.toi` `custom`
object (namespaced), never as a new top-level key.

## Collaborative charters

The legacy `collaborative-charter` shape is replaced by **two** canonical
pieces:

1. Express each team/group preference set as a `.toi` document at the
   `community` or `project` tier.
2. Bind them with an **`.otoi` charter** (`@neurolift/otoi`), which resolves the
   tier stack (`personal` > `community` > `project`) and handles same-tier
   conflicts and enforcement. See [`packages/otoi/SPEC.md`](../packages/otoi/SPEC.md).

## Validating canonical documents

- **TypeScript:** `import { parseToi } from "@neurolift/toi"` (throws on invalid).
- **JSON Schema:** validate against `toi-1.0.0.schema.json` shipped in
  `@neurolift/toi` (draft 2020-12), suitable for the Python validators under
  [`nlt-otoi/tools/validators/`](../nlt-otoi/tools/validators/).

## Status of the Python reference implementation

The Python code under `src/fusion/` and `examples/neuroLift/` is retained for
now. Its TypeScript counterpart for the orchestration layer is
`@neurolift/otoi`; a Python port (or a thin `.toi`-schema-validating shim) can
follow as a separate change.
