# Agent Log

This directory contains structured records of agent activity in the nlt-otoi repository, per the NeuroLift Technologies Agent Solidarity Kit and ORG-DEV-OTOI-1.0.0.

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

1. Read `CLAUDE.md` for repository context and guardrails.
2. Read `docs/active-threads.md` to avoid overlap with in-flight work.
3. If available in this repository version, read `AGENTS.md` for coordination protocol details.
4. Confirm scope with the human owner when intent is ambiguous.
5. Write a registration file to `docs/agent-log/registrations/`.

## Registration Record Requirements

Registration records should capture enough context for auditability without
including personal data.

Recommended fields:
- `agent_name`
- `session_id`
- `started_at` (ISO-8601 UTC timestamp)
- `branch`
- `task_scope`
- `capabilities`
- `constraints`

Example registration record:

```json
{
  "agent_name": "OTOI Integration Agent",
  "session_id": "2026-04-21-ci-docs-alignment",
  "started_at": "2026-04-21T21:50:00Z",
  "branch": "cursor/codebase-documentation-alignment-0b92",
  "task_scope": "Update runbooks for merged GitHub Pages + Solidarity Kit changes",
  "capabilities": ["docs-maintenance", "ci-troubleshooting"],
  "constraints": ["no secrets", "default-deny", "minimal-footprint"]
}
```

## Handoff Record Requirements

Handoff records should preserve intent and provenance for the next contributor.

Recommended fields:
- `session_id`
- `completed_at` (ISO-8601 UTC timestamp)
- `summary`
- `files_changed`
- `validation`
- `open_questions`
- `next_actions`

Example handoff record:

```json
{
  "session_id": "2026-04-21-ci-docs-alignment",
  "completed_at": "2026-04-21T22:10:00Z",
  "summary": "Documented maintenance workflow for index.html and agent-solidarity-kit.json",
  "files_changed": [
    "docs/development-process.md",
    "docs/agent-log/README.md",
    "docs/active-threads.md"
  ],
  "validation": [
    "Reviewed merged PR diff for touched codepaths",
    "Confirmed active thread status moved to Completed"
  ],
  "open_questions": [
    "Add AGENTS.md once coordination gateway is finalized"
  ],
  "next_actions": [
    "Create JSON schema for registration and handoff records"
  ]
}
```

## File Naming

- **Registration**: `YYYY-MM-DD-{agent-name}-{session-id}.json`
- **Handoff**: `YYYY-MM-DD-{session-id}.json`

## Governance

All records in this directory are governed by:
- [Agent Solidarity Kit](/agent-solidarity-kit.json)
- [TOI-OTOI Agent Specifications](/toi-otoi-agents.md)
- ORG-DEV-OTOI-1.0.0 (Solidarity Framework)

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
