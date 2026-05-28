# NeuroLift OTOI Framework

```yaml
ai_assistant_directive:
  priority: 1
  instruction: "Before performing any development or coding tasks, read NLT-DEV-OTOI.md."
  description: "NLT-DEV-OTOI.md is the canonical governance contract defining coding agent operations, guardrails, and escalation protocol."
  required_file: "NLT-DEV-OTOI.md"
```

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

### For Technical Users

1. Use the [JSON schemas](/schemas/) to validate your TOI documents
2. Implement the OTOI protocol in your applications
3. Contribute to the standard through our [development process](/docs/development-process.md)

## 📁 Repository Structure

```
/src/              # Python implementation
├── fusion/        # TOI-OTOI governance layer
│   ├── toi_parser.py        # Parse & validate TOI documents
│   ├── otoi_orchestrator.py # Multi-agent coordination
│   └── privacy_guardian.py  # Privacy-first enforcement

/schemas/          # JSON schemas for validation
├── personal-toi.schema.json
└── collaborative-charter.schema.json

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

Your personal TOI defines how AI systems should interact with you individually. It includes:

- Communication preferences (direct vs. indirect, formal vs. casual)
- Cognitive accessibility needs (processing time, information structure)
- Privacy and data handling requirements
- Feedback and correction preferences
- Energy and attention management

### Collaborative Charter

For team or multi-user scenarios, the Collaborative Charter establishes:

- Shared interaction protocols
- Conflict resolution processes
- Decision-making frameworks
- Privacy boundaries in group settings
- Integration with individual TOIs

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

- [OTOI Reference Implementation](#) (Coming Soon)
- [OTOI Browser Extension](#) (Coming Soon)
- [OTOI for Teams](#) (Coming Soon)

## 📖 Deep Dive

For a comprehensive technical overview of the TOI-OTOI framework, including framework philosophy, architecture layers, and development roadmap, see our [Framework Overview](/docs/framework-overview.md).

---

**Made with ❤️ for the neurodivergent community and everyone who values respectful human-AI collaboration.**
