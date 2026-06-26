# Development Process and CI Runbooks

This guide explains how contribution workflows are validated in this repository,
which checks run automatically, and how to troubleshoot common failures.

It is intentionally focused on repository automation and quality gates. For
general contribution rules, see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Local Prerequisites for CI Reproduction

GitHub Actions runners provide `python` (3.11) and tool binaries on `PATH`.
Local machines often differ, so use equivalent commands where needed:

- If `python` is unavailable, use `python3`.
- If `pip` is unavailable, use `python3 -m pip`.
- If `bandit` is not on `PATH`, run it as `python3 -m bandit`.

Minimum local tools for CI parity:
- Python 3.11
- `jsonschema` (schema validation workflow dependency)
- `bandit` (security scan workflow dependency)

## Workflow Architecture

The repository uses four GitHub Actions workflows:

| Workflow | File | Purpose |
| --- | --- | --- |
| Accessibility Check | `.github/workflows/accessibility-check.yml` | Enforces accessibility-focused docs and template checks |
| Schema Validation | `.github/workflows/schema-validation.yml` | Validates schema and template JSON structure |
| Security Scan | `.github/workflows/security-scan.yml` | Runs Bandit and lightweight security heuristics |
| Create Branch Cleanup Issues | `.github/workflows/create-branch-cleanup-issues.yml` | Creates maintenance issues for stale merged branches |

### CI Coverage Map (What Codepaths Each Workflow Exercises)

This section maps workflow behavior to concrete repository paths so contributors
can quickly identify which checks are relevant for a change.

| Workflow | Primary codepaths covered | Notes |
| --- | --- | --- |
| Accessibility Check | `docs/**`, `templates/**`, `schemas/**`, `nlt-otoi/docs/**`, `nlt-otoi/templates/**`, `nlt-otoi/schemas/**` | Also runs template validation via `nlt-otoi/tools/validators/toi-validator.py` and scans `nlt-otoi/tools/` for accessibility terms as a warning signal |
| Schema Validation | `schemas/**`, `nlt-otoi/schemas/**`, `nlt-otoi/templates/**`, `nlt-otoi/tools/validators/**` | Workflow currently enforces JSON parse validity, not full cross-document semantic validation |
| Security Scan | `src/**`, `nlt-otoi/tools/**`, `schemas/**`, `nlt-otoi/schemas/**` | Triggered on every push/PR to `main`/`develop` (no path filter), plus weekly schedule |
| Create Branch Cleanup Issues | `.github/workflows/create-branch-cleanup-issues.yml` | Manual maintenance workflow; does not run on push or PR |

### Source of Truth for CI Definitions

GitHub Actions only executes workflow files from the repository root
`.github/workflows/` directory.

This repository also contains older workflow copies under
`nlt-otoi/.github/workflows/` for historical context. Those nested copies are
not loaded by GitHub Actions and should not be used for CI troubleshooting.

When changing automation behavior, always edit the root workflow files first.
Treat nested workflow copies as archival references, not active automation.

## GitHub Pages + Solidarity Kit Documentation Runbook

PR #17 introduced two repository-level interfaces that require manual alignment:

- `index.html` (GitHub Pages landing page content)
- `agent-solidarity-kit.json` (governance and agent integration contract)

Supporting operational docs were added under:
- `docs/active-threads.md`
- `docs/agent-log/README.md`
- `docs/agent-log/registrations/`
- `docs/agent-log/handoffs/`

### Why this runbook exists

The landing page includes a hand-curated preview of Solidarity Kit fields
(version, governance flags, architecture components, model details, and
principles). There is no generation step between `agent-solidarity-kit.json`
and `index.html`, so drift can occur if one file is updated without the other.

### Maintenance workflow

1. Update `agent-solidarity-kit.json` first (source of truth).
2. Mirror user-visible changes in `index.html` where they are presented:
   - architecture pillar names/layers
   - model metadata shown in the badge and caption
   - JSON preview block under the "Agent Solidarity Kit" section
3. Update thread tracking in `docs/active-threads.md` if the change was part of
   an active workstream.
4. If a session handoff is required, add/update records in
   `docs/agent-log/{registrations,handoffs}/`.

### Local validation checks

Validate JSON syntax:

```bash
python3 -m json.tool agent-solidarity-kit.json > /dev/null
```

Check that key metadata, architecture labels, and principle pills appear in the
landing page:

```bash
python3 - <<'PY'
import json
from pathlib import Path

kit = json.loads(Path("agent-solidarity-kit.json").read_text(encoding="utf-8"))
html = Path("index.html").read_text(encoding="utf-8")

checks = [
    ("kit version", kit["version"]),
    ("default model name", kit["model"]["name"]),
    ("default model parameters", kit["model"]["parameters"]),
    ("default model license", kit["model"]["license"]),
    ("OTOI governance version", kit["governance"]["otoi_version"]),
]

architecture_checks = [
    (f"architecture component: {component['name']}", component["name"])
    for component in kit["architecture"]["components"]
] + [
    (f"architecture layer: {component['layer']}", component["layer"].title())
    for component in kit["architecture"]["components"]
]

principle_labels = [
    ("principle pill: Privacy First", "Privacy First"),
    ("principle pill: Agency Preservation", "Agency Preservation"),
    ("principle pill: Transparency", "Transparency"),
    ("principle pill: Neurodivergent-Centered", "Neurodivergent-Centered"),
    ("principle pill: Escalation Culture", "Escalation Culture"),
    ("principle pill: Minimal Footprint", "Minimal Footprint"),
]

missing = [
    name
    for name, value in (checks + architecture_checks + principle_labels)
    if value not in html
]
if missing:
    raise SystemExit(f"Missing landing-page references: {', '.join(missing)}")
print("Landing page contains expected kit references.")
PY
```

### Common pitfalls

| Pitfall | Symptom | Resolution |
| --- | --- | --- |
| `agent-solidarity-kit.json` updated without `index.html` updates | Landing page advertises stale version/model/principles | Reconcile manual JSON preview and model badge text with current kit values |
| Only model/version checked during parity validation | Architecture or principle content drifts even though quick check passes | Use the full parity script in this runbook, not ad-hoc spot checks |
| Section IDs changed in `index.html` | Navigation links no longer jump to expected sections | Keep `href="#..."` values aligned with section `id` attributes |
| Thread not closed in `docs/active-threads.md` | Team members think completed work is still in progress | Move finished work to the **Completed** table and include PR number |

## License Maintenance Runbook

Use this runbook when a change touches repository license text, copyright
notices, package license metadata, or public docs that describe licensing.

### Current license state

As of the `1.1.0` relicense, the repository and the in-repository
`@neurolift-technologies/otoi` package declare `Apache-2.0`.

- `LICENSE`, `nlt-otoi/LICENSE`, and `packages/otoi/LICENSE` contain the
  Apache License 2.0 text with the NeuroLift Technologies, LLC copyright notice.
- `packages/otoi/package.json` declares `"version": "1.1.0"` and
  `"license": "Apache-2.0"`.
- The package `files` allow-list includes `LICENSE` so npm tarballs ship the
  package-local license copy.
- After the approved package publish, the npm registry should report the same
  package version and license metadata as `packages/otoi/package.json`.
- `agent-solidarity-kit.json` `metadata.nlt_otoi_repo_license` mirrors the
  repository license identifier. `metadata.framework_license` describes the
  Solidarity Kit framework layer and should only change when that framework
  license changes intentionally.

### Source-of-truth map

| Surface | Role | Maintenance note |
| --- | --- | --- |
| `LICENSE` | Authoritative Apache-2.0 license text for this repository | Update only when the repository license text or notice changes |
| `README.md` | Public repository summary | Keep the license section aligned with `LICENSE` and package notes |
| `CONTRIBUTING.md` | Contributor checklist | Keep the licensing checklist and this runbook linked |
| `CHANGELOG.md` | Root release history | Record user-visible license or package metadata changes under the release that introduced them |
| `packages/otoi/package.json` | `@neurolift-technologies/otoi` package metadata | Keep `version`, `license`, and the `files` allow-list aligned with release intent |
| `packages/otoi/LICENSE` | Package-local license copy | Must be included in `packages/otoi/package.json` `files` so published tarballs contain the license |
| `packages/otoi/README.md` | Package-facing license explanation | Cite the package-local `LICENSE`, the root `LICENSE`, and dependency licenses from their own metadata |
| `agent-solidarity-kit.json` | Integration metadata | `metadata.nlt_otoi_repo_license` should match the repository license identifier |
| `nlt-otoi/LICENSE` | Nested project license copy | Keep aligned with repo-wide license changes unless there is an explicit approved reason to diverge |
| `nlt-otoi/README.md`, `nlt-otoi/PROJECT_OVERVIEW.md`, `nlt-otoi/CHANGELOG.md` | Nested project docs | Keep these aligned with `nlt-otoi/LICENSE`, not npm package metadata |

The external `@neurolift-technologies/toi` dependency is a separate published
package. Do not infer its terms from this repository's license; cite the
dependency's own published package metadata when license notes mention it.

### Package release coupling

When license work also changes the npm package release surface, verify these
items together:

1. `packages/otoi/package.json` has the intended `version` and `license`.
2. `packages/otoi/package.json` `files` includes `LICENSE`, `README.md`, and
   `SPEC.md` plus the built `dist` output expected by package consumers.
3. `packages/otoi/README.md` describes the same package license and dependency
   license relationship.
4. `CHANGELOG.md` records the root release, and `nlt-otoi/CHANGELOG.md` records
   any nested-project license history that changed.
5. Publishing remains a separate operation: do not run `npm publish` or any
   production release command without explicit human approval.
6. After an approved publish, verify the registry state with read-only `npm view`
   commands instead of assuming the publish succeeded from repository metadata.

### Local audit checks

Run these checks from the repository root after license-related edits:

```bash
python3 -m json.tool agent-solidarity-kit.json > /dev/null
python3 -m json.tool packages/otoi/package.json > /dev/null
rg -n "MIT|Apache-2.0|license|License|LICENSE" \
  README.md CONTRIBUTING.md CHANGELOG.md packages/otoi/README.md \
  packages/otoi/package.json agent-solidarity-kit.json \
  nlt-otoi/README.md nlt-otoi/PROJECT_OVERVIEW.md nlt-otoi/CHANGELOG.md
```

For notice-year changes, inspect all maintained license copies directly:

```bash
python3 - <<'PY'
from pathlib import Path

for path in ["LICENSE", "nlt-otoi/LICENSE", "packages/otoi/LICENSE"]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()[:5]
    print(f"\n{path}")
    print("\n".join(lines))
PY
```

Check that the package metadata ships the license copy:

```bash
python3 - <<'PY'
import json
from pathlib import Path

package = json.loads(Path("packages/otoi/package.json").read_text(encoding="utf-8"))
required = {"dist", "LICENSE", "README.md", "SPEC.md"}
missing = sorted(required - set(package.get("files", [])))
if package.get("license") != "Apache-2.0":
    raise SystemExit("packages/otoi/package.json license is not Apache-2.0")
if missing:
    raise SystemExit(f"packages/otoi/package.json files missing: {', '.join(missing)}")
print("Package license metadata and files allow-list are aligned.")
PY
```

Run package release-readiness checks from the package directory when package
metadata, exports, license files, or release notes change:

```bash
cd packages/otoi
npm install --no-package-lock
npm run typecheck
npm test
npm pack --dry-run
```

Notes:
- There is no committed `packages/otoi/package-lock.json` in this repository.
  Use `npm install --no-package-lock` for verification unless a separate change
  intentionally introduces a lockfile.
- `npm pack --dry-run` invokes the package `prepack` script, which runs
  `npm run build`. Expect ignored local artifacts such as `packages/otoi/dist/`
  and `packages/otoi/node_modules/`; remove them before committing docs-only
  follow-ups.
- The dry-run tarball should include `LICENSE`, `README.md`, `SPEC.md`, and the
  built `dist/**` entry points declared by `packages/otoi/package.json`.

For post-publish verification only, query npm metadata read-only:

```bash
npm view @neurolift-technologies/otoi version license --json
npm view @neurolift-technologies/toi version license --json
```

Expected state for the Apache-2.0 `1.1.0` package release:
- `@neurolift-technologies/otoi` reports version `1.1.0` and license
  `Apache-2.0`.
- `@neurolift-technologies/toi` reports its own Apache-2.0 license from its own
  package metadata. Do not infer the dependency license from this repository.

### Common pitfalls

| Pitfall | Symptom | Resolution |
| --- | --- | --- |
| Root `LICENSE` changed without README/package notes | Public docs still describe old license text or package assumptions | Update `README.md`, `CONTRIBUTING.md`, and `packages/otoi/README.md` in the same PR |
| Package metadata changed without docs | npm consumers see a different license than the package README describes | Reconcile `packages/otoi/package.json` and `packages/otoi/README.md` before release checks |
| Package `LICENSE` omitted from `files` | npm tarball metadata says Apache-2.0 but the package does not include its license text | Add `LICENSE` to `packages/otoi/package.json` `files` before packaging |
| Nested license copy treated as generated from root | `nlt-otoi/LICENSE` notice text drifts without nested docs explaining it | Inspect the nested copy directly and update nested docs/changelog when it changes |
| Dependency license inferred from repository license | Docs misstate the external `.toi` package terms | Cite `@neurolift-technologies/toi` from its own package metadata |
| Release command run from a docs or metadata PR | Package is published before review, merge, or explicit approval | Stop before `npm publish`; document release-readiness checks and leave publishing to an approved release step |
| Root-only checks treated as package release checks | CI passes but the package build, test suite, or tarball contents were never exercised | Run the package command pack from `packages/otoi/` before marking release docs ready |
| Generated package artifacts committed from dry-run checks | PR includes `dist/`, `node_modules/`, or tarball outputs unrelated to documentation | Remove ignored artifacts after verification and keep docs-only PRs clean |

## Trigger Matrix

### Accessibility Check
- Triggers on `push` and `pull_request` to `main` or `develop`
- Pull requests targeting any other base branch do not run this workflow
- Runs only when changes touch:
  - `docs/**`, `templates/**`, `schemas/**`
  - `nlt-otoi/docs/**`, `nlt-otoi/templates/**`, `nlt-otoi/schemas/**`

### Schema Validation
- Triggers on `push` and `pull_request` to `main` or `develop`
- Pull requests targeting any other base branch do not run this workflow
- Runs only when changes touch:
  - `schemas/**`
  - `nlt-otoi/schemas/**`
  - `nlt-otoi/tools/validators/**`
  - `nlt-otoi/templates/**`

### Security Scan
- Triggers on `push` and `pull_request` to `main` or `develop`
- Pull requests targeting any other base branch do not run this workflow
- Also runs on a weekly schedule: Monday at 02:00 UTC
- Has no `paths` filter, so all file changes on supported branches trigger it

### Create Branch Cleanup Issues
- Manual trigger only (`workflow_dispatch`)
- Input:
  - `dry_run` (boolean, default `false`)

## First Triage When a Workflow Did Not Run

Before deep debugging, verify the run should have triggered at all:

1. Confirm the event type is supported (`push`, `pull_request`, `schedule`, or
   `workflow_dispatch` as defined per workflow).
2. For PR-triggered runs, confirm the PR base branch is `main` or `develop`.
3. Confirm at least one changed file matches that workflow's `paths` filters.

Useful local command for path filter checks:

```bash
git diff --name-only <base_sha>...<head_sha>
```

## Local CI Parity Command Pack

Use these commands from repository root to reproduce the same checks performed
by GitHub Actions.

### Accessibility Check (local parity)

```bash
grep -r "neurodivergent\|ADHD\|autism\|accessibility" docs/ nlt-otoi/docs/
grep -r "clear\|simple\|easy\|understand" docs/ nlt-otoi/docs/
python3 nlt-otoi/tools/validators/toi-validator.py nlt-otoi/templates/personal-toi/adhd-optimized-toi.json
```

Important constraint:
- The validator's default schema lookup currently targets
  `nlt-otoi/schemas/v1.0/personal-toi-v1.json`, which is present in the current
  repository tree.
- The default schema validates the nested legacy personal-TOI template shape
  (`metadata`, `user_profile`, etc.), not the canonical `.toi` package schema.
  Use `--schema` when validating a different TOI shape.

### Schema Validation (local parity)

```bash
python - <<'PY'
import glob, json, sys
paths = glob.glob('schemas/**/*.json', recursive=True)
paths += glob.glob('nlt-otoi/schemas/**/*.json', recursive=True)
paths += glob.glob('nlt-otoi/templates/**/*.json', recursive=True)
errors = []
for path in paths:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
    except Exception as exc:
        errors.append((path, exc))
if errors:
    for path, exc in errors:
        print(f'Invalid JSON: {path}: {exc}')
    sys.exit(1)
print('All schema/template JSON files parse successfully.')
PY
```

### Security Scan (local parity)

```bash
python3 -m pip install bandit
python3 -m bandit -r src/ nlt-otoi/tools/ -f json -o /tmp/bandit-report.json --exit-zero
python3 - <<'PY'
import json, sys
with open('/tmp/bandit-report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)
high = [r for r in report.get('results', []) if r.get('issue_severity') == 'HIGH']
if high:
    print(f'HIGH findings: {len(high)}')
    sys.exit(1)
print('No HIGH Bandit findings.')
PY
```

## Common Failure Signatures and Fast Fixes

Use this table to quickly map common CI outcomes to likely causes:

| Symptom (Actions log/UI) | Likely cause | First action |
| --- | --- | --- |
| Workflow did not appear for a PR | PR base branch is not `main`/`develop`, or changed files did not match `paths` filters | Confirm PR base branch, then run `git diff --name-only <base_sha>...<head_sha>` |
| `❌ Missing accessibility content in documentation` | Accessibility keywords are absent from scanned docs directories | Add explicit accessibility terms in `docs/` or `nlt-otoi/docs/` |
| `❌ Documentation may not use clear language` | Clear-language keywords are missing from scanned docs | Add wording that includes `clear`, `simple`, `easy`, or `understand` |
| `❌ Error: Schema file not found at .../nlt-otoi/schemas/v1.0/personal-toi-v1.json` | The validator default schema was moved, deleted, or not checked out | Restore the tracked schema file, or provide `--schema` with an existing matching schema |
| `❌ Invalid JSON in ...` (schema workflow) | A schema/template file failed JSON parsing | Run `python -m json.tool <file>` and fix syntax |
| `❌ N high-severity security issues found` | Bandit reported one or more HIGH findings | Re-run Bandit locally and remediate flagged code paths |
| `⚠️  Potential hardcoded passwords found — please review` | Grep-based secret heuristic matched literal password assignment pattern | Remove hardcoded credentials or migrate them to environment/secret stores |

Note: warning-level findings do not always fail a workflow. Check each workflow's
explicit `exit` behavior in the root `.github/workflows/` definitions.

## Known Workflow Constraints and Pitfalls

- Accessibility and clear-language checks are keyword-based `grep` checks and
  are case-sensitive.
- Security secret scanning only checks `*.py` and `*.json` for password-style
  assignments and currently warns instead of failing.
- Bandit path scan errors are written into the JSON report `errors` field and
  are not currently used as a fail condition.
- `Create Branch Cleanup Issues` compares `inputs.dry_run` as string values in
  expressions (`'true'` / `'false'`), even though the input is typed as
  boolean.

## Operational Runbooks

### Accessibility Check Runbook

What it does:
1. Checks out the repository and sets up Python 3.11
2. Greps docs for accessibility-related language
3. Validates `nlt-otoi/templates/personal-toi/*.json` with
   `nlt-otoi/tools/validators/toi-validator.py`
4. Greps `nlt-otoi/tools/` for accessibility terms (warning signal)

Behavioral constraints from source:
- The docs grep check is keyword-based, not semantic analysis.
- The grep checks are case-sensitive (`grep -r` without `-i`).
- The workflow expects terms matching:
  - `neurodivergent|ADHD|autism|accessibility`
  - `clear|simple|easy|understand`

Troubleshooting:
- If the check fails after docs edits, confirm the expected terms still appear in
  `docs/` or `nlt-otoi/docs/`.
- Reproduce the keyword checks locally:
  ```bash
  grep -r "neurodivergent\|ADHD\|autism\|accessibility" docs/ nlt-otoi/docs/
  grep -r "clear\|simple\|easy\|understand" docs/ nlt-otoi/docs/
  ```
- If template validation fails, run:
  ```bash
  python3 nlt-otoi/tools/validators/toi-validator.py <template.json>
  ```
- If template validation fails with "Schema file not found", confirm the default
  schema exists at `nlt-otoi/schemas/v1.0/personal-toi-v1.json`. This is a
  path/layout mismatch, not necessarily malformed JSON in the template file.

### Schema Validation Runbook

What it does:
1. Installs `jsonschema`
2. Parses all root schema JSON files in `schemas/**`
3. Parses all JSON files in `nlt-otoi/schemas/**`
4. Parses all JSON templates in `nlt-otoi/templates/**`

Behavioral constraints from source:
- This workflow checks JSON parse validity (not full semantic schema conformance
  across every document in the repo).
- Although it installs `jsonschema`, the current steps only parse JSON files.
- Any invalid JSON causes a hard failure.

Troubleshooting:
- Validate a single file:
  ```bash
  python -m json.tool schemas/personal-toi.schema.json > /dev/null
  ```
- Validate all touched schema/template files before pushing:
  ```bash
  python - <<'PY'
  import glob, json, sys
  paths = glob.glob('schemas/**/*.json', recursive=True)
  paths += glob.glob('nlt-otoi/schemas/**/*.json', recursive=True)
  paths += glob.glob('nlt-otoi/templates/**/*.json', recursive=True)
  bad = []
  for p in paths:
      try:
          with open(p) as f:
              json.load(f)
      except Exception as exc:
          bad.append((p, exc))
  if bad:
      for p, exc in bad:
          print(f'Invalid JSON: {p}: {exc}')
      sys.exit(1)
  print('All schema/template JSON files parse successfully.')
  PY
  ```

### Security Scan Runbook

What it does:
1. Runs Bandit against `src/` and `nlt-otoi/tools/`
2. Fails the workflow only when HIGH-severity Bandit issues exist
3. Runs a simple grep-based secret detection check for hardcoded passwords
4. Scans schemas for `additionalProperties: true` and reports warnings

Behavioral constraints from source:
- Bandit runs with `--exit-zero`, then a Python gate enforces failure only on
  HIGH-severity findings.
- The Bandit JSON report can contain path errors (for example, missing `src/`);
  the current gate does not fail on report `errors` entries.
- The secret check currently warns but does not fail the job.
- Schema permissiveness findings are informational warnings.

Troubleshooting:
- Reproduce Bandit locally:
  ```bash
  python3 -m pip install bandit
  python3 -m bandit -r src/ nlt-otoi/tools/ -f json -o /tmp/bandit-report.json --exit-zero
  ```
- Inspect high-severity findings in `/tmp/bandit-report.json`.
- Also inspect `errors` in `/tmp/bandit-report.json` (missing scan paths show up
  there even when the workflow still passes).
- For hardcoded credential warnings, move secrets to environment variables or
  secret stores and avoid literal password assignments in committed files.

### Branch Cleanup Issue Automation Runbook

What it does:
- Creates GitHub issues (labelled `maintenance` and `branch-cleanup`) to prompt
  deletion of known stale merged branches.

Important constraints:
- This workflow is manual only and does nothing on push/PR events.
- `dry_run=true` prints a summary and does not create issues.
- The workflow currently checks string values (`'true'` / `'false'`) for
  `inputs.dry_run`.
- The stale branch list is hardcoded in
  `.github/workflows/create-branch-cleanup-issues.yml`.
- There is no de-duplication guard; rerunning with `dry_run=false` can create
  duplicate cleanup issues for the same branches.

How to execute:
1. Open **Actions** in GitHub.
2. Run **Create Branch Cleanup Issues**.
3. Set `dry_run=true` first to preview.
4. Re-run with `dry_run=false` to create issues.

## PR Interface and Contributor Workflow

- PR descriptions are standardized by `.github/PULL_REQUEST_TEMPLATE.md`.
- Contributors should include:
  - change type
  - accessibility impact
  - testing notes
  - documentation updates

Recommended pre-push checklist:
1. Ensure changed docs and templates stay accessible and clear.
2. Ensure changed JSON in schemas/templates parses correctly.
3. Review security impact for any tool or policy changes.
4. Confirm PR description follows the template sections.

