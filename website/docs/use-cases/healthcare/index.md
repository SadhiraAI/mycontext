---
sidebar_position: 1
title: Healthcare
description: Five healthcare use cases — differential diagnosis support, patient communication, medical literature synthesis, ethics consultation, and clinical note error detection.
---

# Healthcare

Five use cases for clinical, research, and health-tech teams. These examples are for decision support and documentation assistance — not for replacing clinical judgment.

:::warning Medical Disclaimer
These examples are for illustrative purposes only. AI outputs must always be reviewed by qualified healthcare professionals before influencing clinical decisions.
:::

| Use Case | Patterns | Integration |
|----------|---------|-------------|
| [Differential Diagnosis Support](./differential-diagnosis) | DifferentialDiagnoser + RiskMitigator + AnomalyDetector | Raw Context + quality gate |
| [Patient Communication Simplifier](./patient-communication) | SimplificationEngine + AudienceAdapter + ClarityOptimizer | LangChain streaming |
| [Medical Literature Synthesis](./literature-synthesis) | SynthesisBuilder + CrossDomainSynthesizer + PatternRecognitionEngine | LlamaIndex RAG |
| [Clinical Ethics Consultation](./ethics-consultation) | EthicalFrameworkAnalyzer + MoralDilemmaResolver + StakeholderEthicsAssessor | CrewAI multi-agent |
| [Clinical Note Error Detection](./note-error-detection) | ErrorDetectionFramework + DiagnosticRootCauseAnalyzer + SystemHealthAuditor | Blueprint + OutputEvaluator |
