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
