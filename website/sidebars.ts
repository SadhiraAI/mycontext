import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const isProduction = process.env.NODE_ENV === 'production';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/installation',
        'getting-started/quickstart',
        'getting-started/core-concepts',
      ],
    },
    {
      type: 'category',
      label: 'Foundations',
      items: [
        'foundations/context-object',
        'foundations/guidance',
        'foundations/directive',
        'foundations/constraints',
        'foundations/task-contract',
        'foundations/research-flow',
        'foundations/patterns',
      ],
    },
    {
      type: 'category',
      label: 'Cognitive Patterns',
      items: [
        'cognitive-patterns/overview',
        {
          type: 'category',
          label: 'Free Patterns (16)',
          items: [
            'cognitive-patterns/free/root-cause-analyzer',
            'cognitive-patterns/free/step-by-step-reasoner',
            'cognitive-patterns/free/hypothesis-generator',
            'cognitive-patterns/free/data-analyzer',
            'cognitive-patterns/free/question-analyzer',
            'cognitive-patterns/free/brainstormer',
            'cognitive-patterns/free/code-reviewer',
            'cognitive-patterns/free/risk-assessor',
            'cognitive-patterns/free/scenario-planner',
            'cognitive-patterns/free/audience-adapter',
            'cognitive-patterns/free/technical-translator',
            'cognitive-patterns/free/socratic-questioner',
            'cognitive-patterns/free/synthesis-builder',
            'cognitive-patterns/free/stakeholder-mapper',
            'cognitive-patterns/free/conflict-resolver',
            'cognitive-patterns/free/intent-recognizer',
          ],
        },
        'cognitive-patterns/enterprise-overview',
        'cognitive-patterns/generic-prompts',
      ],
    },
    {
      type: 'category',
      label: 'Intelligence Layer',
      items: [
        'intelligence/overview',
        'intelligence/transform',
        'intelligence/pattern-suggestion',
        'intelligence/smart-execute',
        'intelligence/prompt-compilation',
        'intelligence/three-tier-execution',
        'intelligence/template-integrator',
        'intelligence/chain-orchestration',
        'intelligence/async-execution',
        'intelligence/token-budget',
        'intelligence/prompt-architect',
        'intelligence/guidance-optimizer',
      ],
    },
    {
      type: 'category',
      label: 'Quality & Metrics',
      items: [
        'quality/quality-metrics',
        'quality/output-evaluator',
        'quality/cai',
        'quality/benchmarking',
        'quality/prompt-optimization-workflow',
        'quality/eval-criteria',
      ],
    },
    {
      type: 'category',
      label: 'Integrations',
      items: [
        'integrations/overview',
        'integrations/langchain',
        'integrations/llamaindex',
        'integrations/crewai',
        'integrations/autogen',
        'integrations/dspy',
        'integrations/semantic-kernel',
        'integrations/google-adk',
      ],
    },
    {
      type: 'category',
      label: 'Export Formats',
      items: [
        'export-formats/overview',
      ],
    },
    {
      type: 'category',
      label: 'Advanced',
      items: [
        'advanced/blueprints',
        'advanced/agent-skills',
        'advanced/output-format',
        'advanced/structured-output',
        'advanced/reliability',
        'advanced/enterprise-license',
      ],
    },
    {
      type: 'category',
      label: 'Use Cases',
      items: [
        'use-cases/overview',
        {
          type: 'category',
          label: 'Software Development',
          items: [
            'use-cases/software-development/index',
            'use-cases/software-development/pr-review',
            'use-cases/software-development/incident-response',
            'use-cases/software-development/architecture-decisions',
            'use-cases/software-development/technical-debt',
            'use-cases/software-development/onboarding-assistant',
            'use-cases/software-development/ai-testing',
          ],
        },
        {
          type: 'category',
          label: 'Healthcare',
          items: [
            'use-cases/healthcare/index',
            'use-cases/healthcare/differential-diagnosis',
            'use-cases/healthcare/patient-communication',
            'use-cases/healthcare/literature-synthesis',
            'use-cases/healthcare/ethics-consultation',
            'use-cases/healthcare/note-error-detection',
          ],
        },
        {
          type: 'category',
          label: 'Banking & Finance',
          items: [
            'use-cases/banking-finance/index',
            'use-cases/banking-finance/credit-risk',
            'use-cases/banking-finance/investment-planning',
            'use-cases/banking-finance/compliance-audit',
            'use-cases/banking-finance/financial-narrative',
            'use-cases/banking-finance/fraud-investigation',
          ],
        },
        {
          type: 'category',
          label: 'Legal',
          items: [
            'use-cases/legal/index',
            'use-cases/legal/contract-risk',
            'use-cases/legal/legal-research',
            'use-cases/legal/case-strategy',
            'use-cases/legal/regulatory-impact',
            'use-cases/legal/client-brief',
          ],
        },
        {
          type: 'category',
          label: 'Education',
          items: [
            'use-cases/education/index',
            'use-cases/education/adaptive-curriculum',
            'use-cases/education/socratic-tutoring',
            'use-cases/education/assessment-rubrics',
            'use-cases/education/concept-explanation',
            'use-cases/education/literature-review',
          ],
        },
        {
          type: 'category',
          label: 'Product & Strategy',
          items: [
            'use-cases/product-strategy/index',
            'use-cases/product-strategy/product-opportunity',
            'use-cases/product-strategy/competitive-intelligence',
            'use-cases/product-strategy/org-bottleneck',
            'use-cases/product-strategy/strategic-roadmap',
          ],
        },
        {
          type: 'category',
          label: 'Government',
          items: [
            'use-cases/government/index',
            'use-cases/government/policy-impact',
            'use-cases/government/public-communication',
            'use-cases/government/compliance-audit',
            'use-cases/government/crisis-response',
            'use-cases/government/budget-allocation',
          ],
        },
        {
          type: 'category',
          label: 'HR & People Ops',
          items: [
            'use-cases/hr-people-ops/index',
            'use-cases/hr-people-ops/performance-review',
            'use-cases/hr-people-ops/job-description',
            'use-cases/hr-people-ops/conflict-mediation',
            'use-cases/hr-people-ops/learning-development',
            'use-cases/hr-people-ops/culture-analysis',
          ],
        },
      ],
    },
    ...(isProduction ? [] : [{
      type: 'category' as const,
      label: 'Research',
      items: [
        'research/overview',
        'research/reasoner-model-comparison',
        'research/data-analyzer-parameterization',
        'research/rag-answerer-grounding',
        'research/memory-compressor-scaling',
      ],
    }]),
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/overview',
      ],
    },
  ],
};

export default sidebars;
