import React, { useState, useMemo } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './patterns.module.css';

type Tier = 'free' | 'enterprise';

type Pattern = {
  name: string;
  category: string;
  tier: Tier;
  description: string;
  inputs: string[];
  docPath?: string;
};

const PATTERNS: Pattern[] = [
  // ── CORE (16) ────────────────────────────────────────────────────────────
  { name: 'RootCauseAnalyzer', category: 'Reasoning', tier: 'free', description: 'Five Whys + Ishikawa systematic diagnosis', inputs: ['problem', 'depth'], docPath: '/docs/cognitive-patterns/free/root-cause-analyzer' },
  { name: 'StepByStepReasoner', category: 'Reasoning', tier: 'free', description: 'Chain-of-thought with transparent, auditable steps', inputs: ['problem', 'domain'], docPath: '/docs/cognitive-patterns/free/step-by-step-reasoner' },
  { name: 'HypothesisGenerator', category: 'Reasoning', tier: 'free', description: 'Testable hypotheses with experimental design', inputs: ['observation', 'domain'], docPath: '/docs/cognitive-patterns/free/hypothesis-generator' },
  { name: 'DataAnalyzer', category: 'Analysis', tier: 'free', description: '5 intents × 3 investment levels — pattern detection, anomaly identification, and actionable insights', inputs: ['data_description', 'goal', 'intent', 'investment'], docPath: '/docs/cognitive-patterns/free/data-analyzer' },
  { name: 'QuestionAnalyzer', category: 'Analysis', tier: 'free', description: 'Decompose and reframe questions before answering', inputs: ['question', 'depth'], docPath: '/docs/cognitive-patterns/free/question-analyzer' },
  { name: 'Brainstormer', category: 'Creative', tier: 'free', description: 'Divergent ideation followed by convergent selection', inputs: ['topic', 'goal', 'constraints'], docPath: '/docs/cognitive-patterns/free/brainstormer' },
  { name: 'CodeReviewer', category: 'Specialized', tier: 'free', description: 'Security, performance, and maintainability review', inputs: ['code', 'language', 'focus_areas'], docPath: '/docs/cognitive-patterns/free/code-reviewer' },
  { name: 'RiskAssessor', category: 'Specialized', tier: 'free', description: '5-category risk scoring with mitigation paths', inputs: ['decision', 'depth'], docPath: '/docs/cognitive-patterns/free/risk-assessor' },
  { name: 'ScenarioPlanner', category: 'Planning', tier: 'free', description: '4-scenario 2×2 matrix with signpost indicators', inputs: ['topic', 'timeframe'], docPath: '/docs/cognitive-patterns/free/scenario-planner' },
  { name: 'StakeholderMapper', category: 'Planning', tier: 'free', description: 'Power-interest matrix with engagement strategy', inputs: ['project'], docPath: '/docs/cognitive-patterns/free/stakeholder-mapper' },
  { name: 'AudienceAdapter', category: 'Communication', tier: 'free', description: 'Reframe any content for a different audience', inputs: ['message', 'target_audience'], docPath: '/docs/cognitive-patterns/free/audience-adapter' },
  { name: 'TechnicalTranslator', category: 'Communication', tier: 'free', description: 'Jargon to plain language with a translation map', inputs: ['technical_text', 'target_audience'], docPath: '/docs/cognitive-patterns/free/technical-translator' },
  { name: 'SocraticQuestioner', category: 'Specialized', tier: 'free', description: '6-category probing questions on any statement', inputs: ['statement', 'depth'], docPath: '/docs/cognitive-patterns/free/socratic-questioner' },
  { name: 'SynthesisBuilder', category: 'Specialized', tier: 'free', description: 'Integrate multiple sources into a coherent narrative', inputs: ['sources', 'goal'], docPath: '/docs/cognitive-patterns/free/synthesis-builder' },
  { name: 'ConflictResolver', category: 'Specialized', tier: 'free', description: 'Mediate disputes and find win-win resolutions', inputs: ['conflict', 'parties'], docPath: '/docs/cognitive-patterns/free/conflict-resolver' },
  { name: 'IntentRecognizer', category: 'Specialized', tier: 'free', description: 'Uncover the true intent behind any request', inputs: ['input', 'depth'], docPath: '/docs/cognitive-patterns/free/intent-recognizer' },

  // ── ADVANCED (72) ──────────────────────────────────────────────────────
  // Specialized Intelligence (3)
  { name: 'QueryPlanner', category: 'Specialized Intelligence', tier: 'enterprise', description: 'Pre-retrieval query analysis: classify, decompose, and rewrite (HyDE + step-back) before retrieval', inputs: ['query', 'task_type', 'domain'] },
  { name: 'RagAnswerer', category: 'Specialized Intelligence', tier: 'enterprise', description: 'Grounded RAG with citation, abstention, and +15% evidence recall (CRAG/Self-RAG/Chain-of-Note)', inputs: ['question', 'context', 'mode'] },
  { name: 'MemoryCompressor', category: 'Specialized Intelligence', tier: 'enterprise', description: 'Structured state extraction — 2x recall over summarization at scale for agent memory', inputs: ['content', 'intent', 'existing_memory', 'goal'] },
  // Advanced Analysis (4)
  { name: 'TrendIdentifier', category: 'Analysis', tier: 'enterprise', description: 'Detect directional market movements from fragmented signals', inputs: ['data_description', 'context_section'] },
  { name: 'GapAnalyzer', category: 'Analysis', tier: 'enterprise', description: 'Find underserved needs and market white spaces', inputs: ['situation', 'context_section'] },
  { name: 'SWOTAnalyzer', category: 'Analysis', tier: 'enterprise', description: 'Structured strengths, weaknesses, opportunities, threats', inputs: ['situation', 'context_section'] },
  { name: 'AnomalyDetector', category: 'Analysis', tier: 'enterprise', description: 'Surface statistically and behaviourally unusual patterns', inputs: ['data_description', 'context_section'] },
  // Advanced Reasoning (2)
  { name: 'CausalReasoner', category: 'Reasoning', tier: 'enterprise', description: 'Map causal chains from trigger to outcome', inputs: ['phenomenon', 'context_section'] },
  { name: 'AnalogicalReasoner', category: 'Reasoning', tier: 'enterprise', description: 'Draw structural analogies between domains', inputs: ['situation', 'context_section'] },
  // Advanced Creative (4)
  { name: 'IdeaGenerator', category: 'Creative', tier: 'enterprise', description: 'Systematic idea generation beyond obvious solutions', inputs: ['topic', 'constraints'] },
  { name: 'InnovationFramework', category: 'Creative', tier: 'enterprise', description: 'Desirability, feasibility, and viability evaluation', inputs: ['challenge', 'context_section'] },
  { name: 'DesignThinker', category: 'Creative', tier: 'enterprise', description: 'Human-centred design process from empathy to prototype', inputs: ['challenge', 'context_section'] },
  { name: 'MetaphorGenerator', category: 'Creative', tier: 'enterprise', description: 'Vivid, audience-calibrated metaphors for complex concepts', inputs: ['concept', 'context_section'] },
  // Advanced Communication (5)
  { name: 'SimplificationEngine', category: 'Communication', tier: 'enterprise', description: 'Strip jargon without losing precision or accuracy', inputs: ['complex_text', 'context_section'] },
  { name: 'PersuasionFramework', category: 'Communication', tier: 'enterprise', description: 'Structure arguments for maximum persuasive impact', inputs: ['position', 'audience'] },
  { name: 'NarrativeBuilder', category: 'Communication', tier: 'enterprise', description: 'Craft stories that make data and analysis compelling', inputs: ['content', 'context_section'] },
  { name: 'FeedbackComposer', category: 'Communication', tier: 'enterprise', description: 'Structured, specific, developmentally useful feedback', inputs: ['performance', 'context_section'] },
  { name: 'ClarityOptimizer', category: 'Communication', tier: 'enterprise', description: 'Ensure every instruction is unambiguous and actionable', inputs: ['text', 'context_section'] },
  // Advanced Planning (3)
  { name: 'ResourceAllocator', category: 'Planning', tier: 'enterprise', description: 'Optimise resource allocation across competing priorities', inputs: ['project', 'objective'] },
  { name: 'PrioritySetter', category: 'Planning', tier: 'enterprise', description: 'Rank initiatives by value, effort, and strategic fit', inputs: ['items', 'criteria'] },
  { name: 'DeadlineManager', category: 'Planning', tier: 'enterprise', description: 'Sequence tasks with dependency and risk awareness', inputs: ['tasks', 'deadline'] },
  // Advanced Specialized (5)
  { name: 'ContentOutliner', category: 'Specialized', tier: 'enterprise', description: 'Structure long-form content before writing begins', inputs: ['topic', 'audience'] },
  { name: 'AmbiguityResolver', category: 'Specialized', tier: 'enterprise', description: 'Identify and resolve ambiguities before they cause errors', inputs: ['statement', 'context_section'] },
  { name: 'RiskMitigator', category: 'Specialized', tier: 'enterprise', description: 'Propose specific interventions that reduce identified risks', inputs: ['challenge', 'context_section'] },
  { name: 'ImpactAssessor', category: 'Specialized', tier: 'enterprise', description: 'Map direct, indirect, and second-order impacts over time', inputs: ['situation', 'context_section'] },
  { name: 'ConceptExplainer', category: 'Specialized', tier: 'enterprise', description: 'Break complex concepts into layered, structured explanations', inputs: ['concept', 'context_section'] },
  // Decision (5)
  { name: 'DecisionFramework', category: 'Decision', tier: 'enterprise', description: 'Multi-criteria decision analysis with explicit tradeoffs', inputs: ['decision', 'context_section'] },
  { name: 'ComparativeAnalyzer', category: 'Decision', tier: 'enterprise', description: 'Head-to-head comparison across user-defined dimensions', inputs: ['decision', 'context_section'] },
  { name: 'TradeoffAnalyzer', category: 'Decision', tier: 'enterprise', description: 'Explicit tradeoff mapping across competing values', inputs: ['decision', 'context_section'] },
  { name: 'MultiObjectiveOptimizer', category: 'Decision', tier: 'enterprise', description: 'Find solutions satisfying multiple competing objectives', inputs: ['decision', 'context_section'] },
  { name: 'CostBenefitAnalyzer', category: 'Decision', tier: 'enterprise', description: 'Rigorous cost-benefit with distributional effects', inputs: ['decision', 'context_section'] },
  // Problem Solving (6)
  { name: 'ProblemDecomposer', category: 'Problem Solving', tier: 'enterprise', description: 'Break complex problems into independently solvable parts', inputs: ['problem', 'context_section'] },
  { name: 'BottleneckIdentifier', category: 'Problem Solving', tier: 'enterprise', description: 'Find the single constraint limiting the whole system', inputs: ['system', 'process'] },
  { name: 'ConstraintOptimizer', category: 'Problem Solving', tier: 'enterprise', description: 'Distinguish hard constraints from negotiable preferences', inputs: ['problem', 'context_section'] },
  { name: 'DependencyMapper', category: 'Problem Solving', tier: 'enterprise', description: 'Map hidden dependencies that make changes risky', inputs: ['project', 'objective'] },
  { name: 'EfficiencyAnalyzer', category: 'Problem Solving', tier: 'enterprise', description: 'Identify operational and development efficiency costs', inputs: ['process', 'objective'] },
  { name: 'TradeSpaceExplorer', category: 'Problem Solving', tier: 'enterprise', description: 'Map the full solution space before committing to one path', inputs: ['problem', 'context_section'] },
  // Temporal Reasoning (3)
  { name: 'TemporalSequenceAnalyzer', category: 'Temporal', tier: 'enterprise', description: 'Analyse cause-effect chains through time', inputs: ['observation', 'context_section'] },
  { name: 'FutureScenarioPlanner', category: 'Temporal', tier: 'enterprise', description: 'Plausible futures with probability weights and signposts', inputs: ['situation', 'horizon'] },
  { name: 'HistoricalContextMapper', category: 'Temporal', tier: 'enterprise', description: 'Ground present decisions in relevant historical patterns', inputs: ['situation', 'context_section'] },
  // Diagnostic (3)
  { name: 'DiagnosticRootCauseAnalyzer', category: 'Diagnostic', tier: 'enterprise', description: 'Deep diagnostic with differential reasoning', inputs: ['observation', 'system'] },
  { name: 'DifferentialDiagnoser', category: 'Diagnostic', tier: 'enterprise', description: 'Systematic differential analysis with ruled-out alternatives', inputs: ['observation', 'system'] },
  { name: 'SystemHealthAuditor', category: 'Diagnostic', tier: 'enterprise', description: 'Assess completeness and soundness of processes', inputs: ['system', 'observation'] },
  // Synthesis (3)
  { name: 'HolisticIntegrator', category: 'Synthesis', tier: 'enterprise', description: 'Integrate perspectives from multiple frameworks', inputs: ['sources', 'topic'] },
  { name: 'PatternRecognitionEngine', category: 'Synthesis', tier: 'enterprise', description: 'Detect recurring themes and inconsistencies across sources', inputs: ['data_description', 'context_section'] },
  { name: 'CrossDomainSynthesizer', category: 'Synthesis', tier: 'enterprise', description: 'Find connections that span different fields or disciplines', inputs: ['sources', 'topic'] },
  // Systems Thinking (6)
  { name: 'FeedbackLoopIdentifier', category: 'Systems Thinking', tier: 'enterprise', description: 'Map reinforcing and balancing feedback loops', inputs: ['system', 'observation'] },
  { name: 'LeveragePointFinder', category: 'Systems Thinking', tier: 'enterprise', description: 'Find the high-leverage points in a complex system', inputs: ['system', 'observation'] },
  { name: 'EmergenceDetector', category: 'Systems Thinking', tier: 'enterprise', description: 'Identify emergent behaviours from component interactions', inputs: ['system', 'observation'] },
  { name: 'SystemArchetypeAnalyzer', category: 'Systems Thinking', tier: 'enterprise', description: 'Match dysfunction to a known systemic archetype', inputs: ['system', 'observation'] },
  { name: 'CausalLoopDiagrammer', category: 'Systems Thinking', tier: 'enterprise', description: 'Generate causal loop diagrams in structured format', inputs: ['system', 'context_section'] },
  { name: 'StockFlowAnalyzer', category: 'Systems Thinking', tier: 'enterprise', description: 'Model accumulations and flows in dynamic systems', inputs: ['system', 'context_section'] },
  // Metacognition (5)
  { name: 'MetacognitiveMonitor', category: 'Metacognition', tier: 'enterprise', description: 'Observe and regulate the quality of reasoning itself', inputs: ['process', 'context_section'] },
  { name: 'SelfRegulationFramework', category: 'Metacognition', tier: 'enterprise', description: 'Plan, monitor, and adjust cognitive strategies', inputs: ['process', 'context_section'] },
  { name: 'CognitiveStrategySelector', category: 'Metacognition', tier: 'enterprise', description: 'Choose the optimal thinking strategy for a problem type', inputs: ['problem', 'context_section'] },
  { name: 'LearningFromExperience', category: 'Metacognition', tier: 'enterprise', description: 'Turn experience into reusable mental models', inputs: ['situation', 'context_section'] },
  { name: 'ErrorDetectionFramework', category: 'Metacognition', tier: 'enterprise', description: 'Systematically identify errors, omissions, and failure states', inputs: ['process', 'context_section'] },
  // Ethical Reasoning (5)
  { name: 'EthicalFrameworkAnalyzer', category: 'Ethics', tier: 'enterprise', description: 'Apply deontological, consequentialist, and virtue ethics', inputs: ['situation', 'context_section'] },
  { name: 'MoralDilemmaResolver', category: 'Ethics', tier: 'enterprise', description: 'Navigate genuine tensions between competing moral claims', inputs: ['conflict', 'context_section'] },
  { name: 'StakeholderEthicsAssessor', category: 'Ethics', tier: 'enterprise', description: "Map each stakeholder's ethical position and interests", inputs: ['situation', 'context_section'] },
  { name: 'ValueConflictNavigator', category: 'Ethics', tier: 'enterprise', description: 'Resolve situations where core values conflict', inputs: ['situation', 'context_section'] },
  { name: 'ConsequentialistAnalyzer', category: 'Ethics', tier: 'enterprise', description: 'Evaluate net welfare outcomes across all affected groups', inputs: ['situation', 'context_section'] },
  // Learning (5)
  { name: 'ScaffoldingFramework', category: 'Learning', tier: 'enterprise', description: 'Progressive support that withdraws as competence grows', inputs: ['concept', 'learner_level'] },
  { name: 'SpacedRepetitionOptimizer', category: 'Learning', tier: 'enterprise', description: 'Schedule reviews for maximum long-term retention', inputs: ['concept', 'context_section'] },
  { name: 'ZoneOfProximalDevelopment', category: 'Learning', tier: 'enterprise', description: "Target concepts just beyond the learner's current level", inputs: ['concept', 'learner_level'] },
  { name: 'CognitiveLoadManager', category: 'Learning', tier: 'enterprise', description: 'Prevent overload by controlling complexity and pacing', inputs: ['complex_topic', 'learner_level'] },
  { name: 'ConceptualChangeAnalyzer', category: 'Learning', tier: 'enterprise', description: 'Surface and restructure misconceptions before teaching', inputs: ['concept', 'context_section'] },
  // Evaluation (5)
  { name: 'RubricDesigner', category: 'Evaluation', tier: 'enterprise', description: 'Objective, behavioural assessment rubrics aligned to goals', inputs: ['concept', 'learner_level'] },
  { name: 'FormativeAssessmentFramework', category: 'Evaluation', tier: 'enterprise', description: 'Checkpoints that reveal learning progress, not just outcomes', inputs: ['concept', 'learner_level'] },
  { name: 'SummativeEvaluator', category: 'Evaluation', tier: 'enterprise', description: 'Summative assessments measuring deep understanding', inputs: ['concept', 'learner_level'] },
  { name: 'PeerAssessmentStructure', category: 'Evaluation', tier: 'enterprise', description: 'Structured frameworks for calibrated peer review', inputs: ['concept', 'context_section'] },
  { name: 'SelfAssessmentGuide', category: 'Evaluation', tier: 'enterprise', description: 'Guide learners to accurately evaluate their own work', inputs: ['concept', 'context_section'] },
];

const ALL_CATEGORIES = ['All', ...Array.from(new Set(PATTERNS.map(p => p.category))).sort()];

// `tier` is taxonomy only — every pattern is open source. "free" = the 16 core
// patterns, "enterprise" = the 72 advanced patterns. Both ship in every install.
const TIER_LABELS: Record<Tier, string> = {
  free: 'core',
  enterprise: 'advanced',
};

const TIER_COLORS: Record<Tier, string> = {
  free: 'var(--ifm-color-success)',
  enterprise: 'var(--ifm-color-primary)',
};

const CORE_COUNT = PATTERNS.filter(p => p.tier === 'free').length;
const ADVANCED_COUNT = PATTERNS.filter(p => p.tier === 'enterprise').length;
const TOTAL_COUNT = PATTERNS.length;

function PatternCard({ pattern }: { pattern: Pattern }) {
  const card = (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <span className={styles.patternName}>{pattern.name}</span>
        <span
          className={styles.tierBadge}
          style={{ backgroundColor: TIER_COLORS[pattern.tier] }}>
          {TIER_LABELS[pattern.tier]}
        </span>
      </div>
      <span className={styles.categoryBadge}>{pattern.category}</span>
      <p className={styles.description}>{pattern.description}</p>
      <div className={styles.inputs}>
        {pattern.inputs.map(inp => (
          <code key={inp} className={styles.inputChip}>{inp}</code>
        ))}
      </div>
      {pattern.docPath && (
        <span className={styles.docsLink}>View docs →</span>
      )}
    </div>
  );

  return pattern.docPath ? (
    <Link to={pattern.docPath} className={styles.cardLink}>{card}</Link>
  ) : (
    <div className={styles.cardLinkDisabled}>{card}</div>
  );
}

export default function PatternsPage(): JSX.Element {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [tier, setTier] = useState<'all' | 'free' | 'enterprise'>('all');

  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return PATTERNS.filter(p => {
      const matchSearch =
        !q ||
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        p.category.toLowerCase().includes(q) ||
        p.inputs.some(i => i.toLowerCase().includes(q));
      const matchCategory = category === 'All' || p.category === category;
      const matchTier = tier === 'all' || p.tier === tier;
      return matchSearch && matchCategory && matchTier;
    });
  }, [search, category, tier]);

  return (
    <Layout
      title="Pattern Browser"
      description="Browse and filter all 88 cognitive patterns — all open source. Search by name, category, or input.">
      <div className={styles.hero}>
        <div className={styles.heroInner}>
          <h1 className={styles.heroTitle}>Pattern Browser</h1>
          <p className={styles.heroSubtitle}>
            {TOTAL_COUNT} cognitive patterns — all open source. Each one encodes a proven analytical methodology so you bring the problem, not the framework.
          </p>
          <input
            className={styles.searchInput}
            type="text"
            placeholder="Search by name, description, or input..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            autoFocus
          />
        </div>
      </div>

      <div className={styles.controls}>
        <div className={styles.tierToggle}>
          {(['all', 'free', 'enterprise'] as const).map(t => (
            <button
              key={t}
              className={`${styles.tierBtn} ${tier === t ? styles.tierBtnActive : ''}`}
              onClick={() => setTier(t)}>
              {t === 'all'
                ? `All (${TOTAL_COUNT})`
                : t === 'free'
                  ? `Core (${CORE_COUNT})`
                  : `Advanced (${ADVANCED_COUNT})`}
            </button>
          ))}
        </div>

        <div className={styles.categoryPills}>
          {ALL_CATEGORIES.map(cat => (
            <button
              key={cat}
              className={`${styles.pill} ${category === cat ? styles.pillActive : ''}`}
              onClick={() => setCategory(cat)}>
              {cat}
            </button>
          ))}
        </div>
      </div>

      <div className={styles.resultsBar}>
        Showing <strong>{filtered.length}</strong> of <strong>{TOTAL_COUNT}</strong> patterns
        {search && <> matching "<strong>{search}</strong>"</>}
      </div>

      {filtered.length === 0 ? (
        <div className={styles.empty}>
          <p>No patterns match your filters.</p>
          <button className={styles.resetBtn} onClick={() => { setSearch(''); setCategory('All'); setTier('all'); }}>
            Reset filters
          </button>
        </div>
      ) : (
        <div className={styles.grid}>
          {filtered.map(p => <PatternCard key={p.name} pattern={p} />)}
        </div>
      )}

      <div className={styles.footer}>
        <p>
          All {TOTAL_COUNT} patterns are open source and included in every install — no tiers, no license keys.{' '}
          <Link to="/docs/cognitive-patterns/overview">Browse the docs →</Link>
        </p>
        <pre className={styles.installBlock}>pip install mycontext-ai</pre>
      </div>
    </Layout>
  );
}
