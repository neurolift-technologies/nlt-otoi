# NeuroLift OTOI Framework

**Orchestrated Terms of Interaction (OTOI)**: User-defined Terms of Interaction for AI systems. Enables neurodivergent-friendly multi-agent orchestration with privacy-first governance. Open standard for human-controlled AI collaboration.

## 🌟 What is OTOI?

The OTOI (Orchestrated Terms of Interaction) framework is a revolutionary approach to human-AI interaction that puts users in complete control of their AI collaborations. It provides a structured way to define Terms of Interaction (TOI) that ensure AI systems work exactly how you need them to, respecting your cognitive preferences, privacy requirements, and collaboration style.

### Key Principles

- **User-Controlled**: You define exactly how AI should interact with you
- **Neurodivergent-Friendly**: Built with diverse cognitive needs in mind
- **Privacy-First**: Your data and preferences stay under your control
- **Flexible**: Adapt to any workflow or collaboration style
- **Transparent**: Clear, understandable interaction rules

## 🚀 Quick Start

### For Non-Technical Users

1. Start with the [Personal TOI Template](/templates/personal-toi-template.md)
2. Fill in your preferences and requirements
3. Share your TOI with AI systems or collaborators
4. Enjoy personalized, respectful AI interactions

> **Note:** The root templates are legacy-friendly worksheets. New machine-readable
> integrations should migrate the answers into the canonical `.toi` format.

### For Technical Users

1. Use [`@neurolift/toi`](https://www.npmjs.com/package/@neurolift/toi) as the
   canonical `.toi` validator and resolver for interaction preference documents.
2. Use [`@neurolift/otoi`](/packages/otoi/README.md) for the `.otoi`
   orchestration layer: charter parsing, policy honoring, conflict handling, and
   per-agent propagation.
3. Use the [canonical TOI migration guide](/docs/canonical-toi-migration.md) when
   upgrading older documents that use `version` / `metadata` /
   `communication` / `cognitive` / `privacy`.
4. Contribute to the standard through our
   [development process](/docs/development-process.md).

## Canonical `.toi` and `.otoi` standard

PR #27 adopted the canonical **`.toi`** standard as the source of truth for
individual Terms of Interaction:

- **`.toi` (`@neurolift/toi`)**: the portable, signable interaction preference
  document format. It owns the document shape, tiers, resolution semantics, and
  validation rules.
- **`.otoi` (`@neurolift/otoi`)**: the in-repo TypeScript package that consumes a
  stack of `.toi` documents, resolves them into one effective policy, detects
  same-tier conflicts, and propagates the result to declared agents.
- **Legacy root schemas**: `schemas/personal-toi.schema.json` and
  `schemas/collaborative-charter.schema.json` remain for pre-existing documents
  only and are marked deprecated. See
  [`docs/canonical-toi-migration.md`](/docs/canonical-toi-migration.md).

## 📁 Repository Structure

```
/src/              # Python implementation
├── fusion/        # TOI-OTOI governance layer
│   ├── toi_parser.py        # Parse & validate TOI documents
│   ├── otoi_orchestrator.py # Multi-agent coordination
│   └── privacy_guardian.py  # Privacy-first enforcement

/packages/otoi/    # TypeScript .otoi reference package
├── README.md      # Install, quick start, and API guide
├── SPEC.md        # Normative .otoi charter specification
├── src/           # Zod schema, honoring, conflict, propagation logic
└── test/          # Vitest coverage for charter honoring behavior

/schemas/          # Deprecated legacy JSON schemas
├── personal-toi.schema.json          # Legacy personal shape
└── collaborative-charter.schema.json # Legacy collaborative shape

/templates/        # User-friendly templates
├── personal-toi-template.md
├── collaborative-charter-template.md
└── quick-start-template.md

/examples/         # Real-world examples
├── neurodivergent-examples/
├── neuroLift/     # NeuroLift integration patterns
└── team-collaboration/

/index.html        # GitHub Pages landing page
/agent-solidarity-kit.json # Agent governance + integration contract

/docs/            # Comprehensive documentation
├── canonical-toi-migration.md
├── framework-overview.md
├── development-process.md
├── implementation-guide.md
├── best-practices.md
├── active-threads.md
└── agent-log/
    ├── README.md
    ├── registrations/
    └── handoffs/
```

## 🧭 GitHub Pages and Solidarity Kit Maintenance

The repository includes a public landing page (`index.html`) and a governance
contract (`agent-solidarity-kit.json`). Keep them synchronized:

1. Treat `agent-solidarity-kit.json` as the source of truth.
2. Mirror user-facing fields in `index.html` (version, model details, and
   architecture labels) when they change.
3. Use `docs/development-process.md` for the operational runbook and validation
   commands.
4. Track work lifecycle in `docs/active-threads.md` and session records in
   `docs/agent-log/`.

## 🎯 Core Components

### Personal TOI (Terms of Interaction)

Your personal TOI defines how AI systems should interact with you individually.
For new technical integrations, represent this as a canonical `.toi` document
validated by `@neurolift/toi`. It includes:

- Communication preferences (direct vs. indirect, formal vs. casual)
- Cognitive accessibility needs (processing time, information structure)
- Privacy and data handling requirements
- Feedback and correction preferences
- Energy and attention management

### Collaborative Charter

For team or multi-user scenarios, legacy Collaborative Charters are replaced by
`.toi` documents at `community` or `project` tier plus an `.otoi` charter. The
`.otoi` charter establishes:

- The agent mesh bound to the policy
- The `.toi` sources in force
- Same-tier conflict disposition
- Unsupported-preference handling
- Per-agent policy propagation

## 🌈 Neurodivergent-Friendly Features

- **Sensory Considerations**: Control information density and presentation
- **Executive Function Support**: Structured decision trees and clear processes
- **Social Communication**: Explicit expectations and interaction patterns
- **Cognitive Load Management**: Customizable complexity levels
- **Routine and Predictability**: Consistent interaction patterns

## 🔒 Privacy & Security

- **Local Control**: Your TOI documents stay on your systems
- **Minimal Data**: Only necessary information is shared
- **Transparent Processing**: Clear rules about data handling
- **Revocable Consent**: Easy to modify or withdraw permissions
- **Standards-Based**: Open protocols, no vendor lock-in

## 🤝 Contributing

We welcome contributions from everyone! Whether you're:

- A neurodivergent individual sharing your needs
- A developer implementing the standard
- A researcher studying human-AI interaction
- An organization adopting OTOI

See our [Contributing Guidelines](CONTRIBUTING.md) for how to get involved.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌍 Community

- **Issues**: Report bugs or request features
- **Discussions**: Share experiences and ask questions
- **Examples**: Contribute real-world TOI documents
- **Documentation**: Help improve our guides and tutorials

## 🔗 Related Projects

- [@neurolift/otoi](/packages/otoi/README.md) — TypeScript `.otoi` reference implementation
- [Canonical TOI Migration Guide](/docs/canonical-toi-migration.md)
- [OTOI Browser Extension](#) (Coming Soon)
- [OTOI for Teams](#) (Coming Soon)

## 📖 Deep Dive

For a comprehensive technical overview of the TOI-OTOI framework, including framework philosophy, architecture layers, and development roadmap, see our [Framework Overview](/docs/framework-overview.md).

---

**Made with ❤️ for the neurodivergent community and everyone who values respectful human-AI collaboration.**
