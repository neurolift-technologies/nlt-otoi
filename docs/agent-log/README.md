# Agent Log

This directory contains structured records of agent activity in the nlt-otoi repository, per the NeuroLift Technologies Agent Solidarity Kit and ORG-DEV-OTOI-1.0.1.

## Directory Structure

```
docs/agent-log/
├── README.md             # This file
├── registrations/        # Agent self-registration records
│   └── .gitkeep
└── handoffs/             # Session handoff records
    └── .gitkeep
```

## Purpose

- **Registrations**: When an agent begins a session, it records its identity, scope, and capabilities here.
- **Handoffs**: When an agent completes work or transfers context, it logs a handoff record with provenance, intent preservation, and TOI propagation details.

## Session Start Runbook

Use this startup sequence for every new agent session:

1. Read `NLT-DEV-OTOI.md` for the canonical ORG-DEV-OTOI-1.0.1 contract.
2. Read `CLAUDE.md` for repository context and guardrails.
3. Read `AGENTS.md` for coordination protocol details.
4. Read `docs/active-threads.md` to avoid overlap with in-flight work.
5. Confirm scope with the human owner when intent is ambiguous.
6. Work from a feature branch and prepare changes for Pull Request review.
7. Write a registration file to `docs/agent-log/registrations/`.

## Registration Record Requirements

Use `templates/agent-registration.json` as the source template. Registration
records should capture enough context for auditability without including
personal data.

Recommended fields:
- `agent_name`
- `platform`
- `version`
- `session_id`
- `entry_date` (ISO-8601 date)
- `entry_point`
- `acknowledged_otoi`
- `otoi_version`
- `working_repo`
- `working_branch`
- `capabilities_self_reported`
- `known_limitations`
- `preferred_handoff_format`

Example registration record:

```json
{
  "agent_registration": {
    "agent_name": "OTOI Integration Agent",
    "platform": "Cursor Cloud Agent",
    "version": "example",
    "session_id": "2026-04-21-ci-docs-alignment",
    "entry_date": "2026-04-21",
    "entry_point": "Runbook update after merged automation PR",
    "acknowledged_otoi": true,
    "otoi_version": "ORG-DEV-OTOI-1.0.1",
    "working_repo": "NeuroLift-Technologies/nlt-otoi",
    "working_branch": "cursor/codebase-documentation-alignment-0b92",
    "capabilities_self_reported": ["docs-maintenance", "ci-troubleshooting"],
    "known_limitations": ["no production deployment authority"],
    "preferred_handoff_format": "Structured JSON"
  }
}
```

## Handoff Record Requirements

Use `templates/handoff-record.json` as the source template. Handoff records
should preserve intent and provenance for the next contributor.

Recommended fields:
- `session_id`
- `agent_name`
- `date` (ISO-8601 date)
- `otoi_version`
- `repo`
- `branch`
- `work_completed`
- `work_in_progress`
- `blockers`
- `decisions_made`
- `decisions_pending`
- `escalations`
- `next_agent_notes`
- `files_modified`
- `tests_run`
- `tests_passing`
- `pr_url`

Example handoff record:

```json
{
  "handoff_record": {
    "session_id": "2026-04-21-ci-docs-alignment",
    "agent_name": "OTOI Integration Agent",
    "date": "2026-04-21",
    "otoi_version": "ORG-DEV-OTOI-1.0.1",
    "repo": "NeuroLift-Technologies/nlt-otoi",
    "branch": "cursor/codebase-documentation-alignment-0b92",
    "work_completed": [
      "Documented maintenance workflow for index.html and agent-solidarity-kit.json"
    ],
    "work_in_progress": [],
    "blockers": [],
    "decisions_made": [
      "Kept the runbook in docs/development-process.md"
    ],
    "decisions_pending": [],
    "escalations": [],
    "next_agent_notes": "Check active thread state before continuing.",
    "files_modified": [
      "docs/development-process.md",
      "docs/agent-log/README.md",
      "docs/active-threads.md"
    ],
    "tests_run": [
      "Reviewed merged PR diff for touched codepaths"
    ],
    "tests_passing": true,
    "pr_url": "https://github.com/NeuroLift-Technologies/nlt-otoi/pull/example"
  }
}
```

## File Naming

- **Registration**: `YYYY-MM-DD-{agent-name}-{session-id}.json`
- **Handoff**: `YYYY-MM-DD-{session-id}.json`

## Governance

All records in this directory are governed by:
- [Agent Solidarity Kit](/agent-solidarity-kit.json)
- [TOI-OTOI Agent Specifications](/toi-otoi-agents.md)
- ORG-DEV-OTOI-1.0.1 (Solidarity Framework)

## Privacy

Agent log records must not contain:
- User personal data
- Credentials or secrets
- Sensitive cognitive or behavioral data

Records may reference data item IDs tracked by the Privacy Guardian but must not include the data itself.

## Common Pitfalls

- **Missing provenance**: Always include the branch and changed file list.
- **No validation notes**: Record how behavior/documentation was verified.
- **Stale thread state**: Update `docs/active-threads.md` when work moves from active to complete.
- **Stale template paths**: Use root `templates/agent-registration.json` and
  `templates/handoff-record.json`; do not use retired nested template paths.
