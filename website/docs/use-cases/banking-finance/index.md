---
sidebar_position: 1
title: Banking & Finance
description: Five finance use cases — credit risk assessment, investment scenario planning, regulatory compliance, financial narrative generation, and fraud investigation.
---

# Banking & Finance

Five use cases for banks, fintechs, and investment teams. These examples show how structured context engineering replaces inconsistent, hard-to-audit ad-hoc prompts with repeatable, measurable workflows.

| Use Case | Patterns | Integration |
|----------|---------|-------------|
| [Credit Risk Assessment](./credit-risk) | RiskAssessor + RiskMitigator + ImpactAssessor + CausalReasoner | Blueprint + to_openai() |
| [Investment Scenario Planning](./investment-planning) | FutureScenarioPlanner + MultiObjectiveOptimizer + DecisionFramework | CrewAI multi-agent |
| [Regulatory Compliance Audit](./compliance-audit) | SystemHealthAuditor + AnomalyDetector + EthicalFrameworkAnalyzer | LangChain + LlamaIndex RAG |
| [Financial Report Narrative](./financial-narrative) | DataAnalyzer + SynthesisBuilder + NarrativeBuilder | Blueprint + Markdown export |
| [Fraud Pattern Investigation](./fraud-investigation) | AnomalyDetector + PatternRecognitionEngine + CausalReasoner | AutoGen investigator chain |
