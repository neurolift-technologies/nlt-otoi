# The `.otoi` Orchestration Format — Specification

**Version:** 1.0.0
**Status:** Draft
**Media type:** `application/otoi+json` (provisional)
**File extension:** `.otoi`
**Builds on:** the [`.toi` v1.0.0](https://www.npmjs.com/package/@neurolift/toi) standard

> Orchestrated Terms of Interaction (`.otoi`) is an open, declarative file
> format that describes **how a multi-agent system honors** a set of `.toi`
> documents at runtime. Where `.toi` answers "what does this person want?",
> `.otoi` answers "which agents are bound to that, how is a stack of `.toi`
> documents resolved into one effective policy, and what happens on conflict?"

## 1. Status and relationship to `.toi`

The `.toi` specification (§2) explicitly defers orchestration to a separate
`.otoi` standard. This is that standard. It does **not** redefine the `.toi`
document model, tiers, precedence, canonicalization, or signatures; those are
normative in `.toi` and consumed here unchanged. The reference implementation is
[`@neurolift/otoi`](./README.md), which depends on `@neurolift/toi`.

The Zod schema in [`src/schema.ts`](./src/schema.ts) is the machine-readable
source of truth for the charter shape.

## 2. Scope

An `.otoi` **charter** is a declaration, authored by or on behalf of a system
operator, describing the binding between a set of agents (the *mesh*) and a set
of `.toi` documents (the *sources*) they must honor, plus the *enforcement*
policy governing that honoring.

Two properties carry over from `.toi`:

1. **Declarative.** A charter contains no code, prompts, or tool definitions. A
   processor reads it and adapts its own orchestration; it never evaluates it.
2. **Portable.** A charter is plain JSON and may be authored by hand, committed,
   or exchanged with no shared runtime.

A charter MUST NOT inline interaction *instructions*; the preferences it honors
live only in the referenced `.toi` documents, validated by the `.toi` layer.

## 3. Document model

A `.otoi` charter is a single JSON object. Keys beginning with `$` are reserved
(document metadata); all other keys are content.

| Key | Required | Type | Rule |
| --- | --- | --- | --- |
| `$otoi` | **Yes** | string | Charter format version (semver). `"1.0.0"` for this version. |
| `$id` | No | string | A version-4 UUID. |
| `$created` / `$updated` | No | string | ISO 8601 date or date-time. |
| `identity` | No | object | Who authored the charter (`author` required if present). |
| `agents` | No | array | The mesh: objects with a required `id`, optional `role`, `modalities`, `affordances`. |
| `enforcement` | No | object | Enforcement policy (Section 5). |
| `toi_sources` | No | array | `.toi` documents in force (Section 4). |

Like `.toi`, every object is **open**: a processor MUST preserve unknown keys
and MUST NOT reject a document for an unrecognized `$`-prefixed key.

## 4. `toi_sources`

Each source references exactly one `.toi` document and declares the `$tier` it
contributes at:

| Field | Required | Rule |
| --- | --- | --- |
| `tier` | **Yes** | One of the `.toi` tiers (`personal`, `community`, `project`). |
| `uri` | one of | A locator the host resolves to `.toi` text. |
| `inline` | one of | A `.toi` document embedded directly. |

A source MUST provide either `uri` or `inline`. An inline payload is validated
by the `.toi` parser at honor time, not by this schema — there is exactly one
validator for the `.toi` shape.

## 5. Enforcement

| Field | Values | Default | Meaning |
| --- | --- | --- | --- |
| `mode` | `advisory`, `enforced`, `strict` | `enforced` | Strictness of honoring. `strict` additionally refuses to serve the policy to an agent not declared in `agents`. |
| `on_conflict` | `highest-tier-wins`, `reject`, `escalate` | `highest-tier-wins` | Disposition of a **same-tier** disagreement (Section 6). |
| `on_unsupported` | `ignore`, `degrade`, `reject` | `degrade` | Disposition of a preference no agent can satisfy. |
| `audit` | boolean | `true` | Whether honoring is recorded to an audit trail. |

## 6. Resolution and conflicts

Resolution of the `.toi` stack into one **effective** document is performed by
the `.toi` precedence primitive (`resolveToi`): `personal > community > project
> platform defaults`, terminal at the highest tier, gap-filling below.
Cross-tier disagreement is therefore **not** a conflict — precedence resolves
it.

A **conflict** is a disagreement at the **same** tier: two documents that assign
different values to the same leaf path. Conflicts are reported on the resolved
policy. Under `on_conflict: "reject"` a conflict is a hard failure;
`"highest-tier-wins"` lets document order within the tier settle it;
`"escalate"` surfaces the conflict for a human decision.

The effective document is a synthesized *view*: it carries the highest tier's
`$toi`/`$tier`, and per-file metadata (`$id`, `$signature`, …) is not merged
into it, consistent with `.toi` §9.

## 7. Security and privacy considerations

- **Charters are data, not instructions.** A processor MUST NOT treat any field
  as a command or prompt. Orchestration logic is the host's, not the charter's.
- **The `.toi` privacy floor still applies.** Honoring a stack does not relax any
  `privacy` preference in the resolved view; it is a floor, not a ceiling.
- **Signatures.** A charter MAY reference signed `.toi` documents; verification
  is delegated to `@neurolift/toi` (`verifyToi`). Charter-level signing is
  reserved for a future version.

## 8. Versioning

`$otoi` follows Semantic Versioning. A `1.x` processor MUST tolerate a `1.y`
charter for `y > x` by preserving unknown keys (Section 3).

## 9. References

- `@neurolift/toi` SPEC — the `.toi` file format and resolution semantics
- RFC 8259 (JSON), RFC 6839 (`+json`), RFC 4122 (UUID), Semantic Versioning 2.0.0
