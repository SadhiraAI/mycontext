---
sidebar_position: 1
title: Software Development
description: Six use cases for software teams — AI code review, incident response, architecture decisions, technical debt, developer onboarding, and AI-assisted testing.
---

# Software Development

Six production-ready use cases for engineering teams. Each one shows how cognitive patterns turn LLM calls from ad-hoc prompts into systematic, quality-assured workflows.

| Use Case | Patterns | Integration |
|----------|---------|-------------|
| [PR Review Pipeline](./pr-review) | CodeReviewer + RiskAssessor + BottleneckIdentifier | LangChain LCEL chain |
| [Incident Response](./incident-response) | RootCauseAnalyzer + DiagnosticRootCauseAnalyzer + SystemHealthAuditor | AutoGen multi-agent |
| [Architecture Decisions](./architecture-decisions) | DecisionFramework + TradeoffAnalyzer + ConstraintOptimizer | Blueprint + Markdown export |
| [Technical Debt Analysis](./technical-debt) | BottleneckIdentifier + DependencyMapper + EfficiencyAnalyzer | Blueprint + quality gate |
| [Developer Onboarding](./onboarding-assistant) | TechnicalTranslator + ScaffoldingFramework + SocraticQuestioner | Agent Skill + LangChain memory |
| [AI-Assisted Testing](./ai-testing) | StepByStepReasoner + ErrorDetectionFramework + RiskAssessor + HypothesisGenerator | CrewAI + Blueprint |

All examples use Python 3.10+. Enterprise patterns require a license key.
