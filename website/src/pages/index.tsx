import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import CodeBlock from '@theme/CodeBlock';

import styles from './index.module.css';

const installCode = `pip install mycontext-ai`;

const quickStartCode = `from mycontext import Context, Guidance, Directive

ctx = Context(
    guidance=Guidance(
        role="Senior security reviewer",
        rules=["Flag every injection risk", "Suggest concrete fixes"],
        style="concise, actionable",
    ),
    directive=Directive(content="Review this API endpoint for vulnerabilities."),
)

# Export to any LLM — one context, every provider
ctx.to_openai()      # OpenAI Chat API
ctx.to_anthropic()   # Claude
ctx.to_langchain()   # LangChain
ctx.to_google()      # Gemini`;

const intelligenceCode = `from mycontext.intelligence import smart_execute

# One call — auto-selects the right cognitive pattern,
# builds the context, and executes
response, meta = smart_execute(
    "Why did API response times triple after last deploy?",
    provider="openai",
)

print(meta["templates_used"])  # ['root_cause_analyzer']
print(response)                # Structured root cause analysis`;

const qualityCode = `from mycontext.intelligence import QualityMetrics, ContextAmplificationIndex

# Score any context on 6 dimensions
metrics = QualityMetrics()
score = metrics.evaluate(ctx)
print(f"Quality: {score.overall:.2f}")  # 0.87

# Prove templates work with CAI
cai = ContextAmplificationIndex(provider="openai")
result = cai.measure(question, template_name="root_cause_analyzer")
print(f"CAI: {result.cai_overall:.2f}x")  # 1.42x — 42% better output`;

type FeatureItem = {
  title: string;
  icon: string;
  description: ReactNode;
};

const features: FeatureItem[] = [
  {
    title: '85 Cognitive Patterns',
    icon: '🧠',
    description: (
      <>
        Research-backed patterns implementing real cognitive frameworks — Five Whys,
        Socratic method, systems archetypes, ethical reasoning — grounded in 150+
        peer-reviewed papers.
      </>
    ),
  },
  {
    title: '13 Export Formats',
    icon: '🔄',
    description: (
      <>
        Build once, run anywhere. Export to OpenAI, Anthropic, Gemini, LangChain,
        CrewAI, AutoGen, DSPy, Semantic Kernel, YAML, JSON, XML, and more.
      </>
    ),
  },
  {
    title: 'Measurable Quality',
    icon: '📊',
    description: (
      <>
        Score contexts on 6 dimensions. Evaluate LLM outputs on 5 dimensions.
        Prove templates work with the Context Amplification Index (CAI).
      </>
    ),
  },
  {
    title: '3-Tier Execution',
    icon: '⚡',
    description: (
      <>
        Choose your cost/quality tradeoff: Static Generic (zero-cost compilation),
        Dynamic Compiled (LLM-refined), or Full Response (complete execution).
      </>
    ),
  },
  {
    title: '7 Framework Integrations',
    icon: '🔗',
    description: (
      <>
        Drop into LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel,
        or Google ADK. Dedicated helpers for each framework.
      </>
    ),
  },
  {
    title: 'Intelligence Layer',
    icon: '✨',
    description: (
      <>
        Auto-transform questions into perfect contexts. Pattern suggestion,
        multi-template fusion, chain orchestration, and complexity routing — all automatic.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.featureIcon}>{icon}</div>
        <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

function HeroSection() {
  return (
    <header className={styles.hero}>
      <div className="container">
        <div className={styles.heroInner}>
          <div className={styles.heroContent}>
            <div className={styles.heroBadge}>
              Python SDK · v0.3.0
            </div>
            <Heading as="h1" className={styles.heroTitle}>
              Context engineering<br />for LLMs
            </Heading>
            <p className={styles.heroSubtitle}>
              Build structured contexts with research-backed cognitive patterns.
              Export to any LLM. Measure quality. Prove it works.
            </p>
            <div className={styles.heroActions}>
              <Link className={styles.heroPrimary} to="/docs/getting-started/installation">
                Get Started
              </Link>
              <Link className={styles.heroSecondary} to="/docs/getting-started/quickstart">
                Quick Start →
              </Link>
            </div>
            <div className={styles.heroInstall}>
              <code>pip install mycontext-ai</code>
            </div>
          </div>
          <div className={styles.heroCode}>
            <CodeBlock language="python" title="5 lines to your first context">
              {quickStartCode}
            </CodeBlock>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2">Why mycontext-ai</Heading>
          <p>Capabilities that don't exist in any other open-source prompt engineering library.</p>
        </div>
        <div className="row">
          {features.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function IntelligenceSection() {
  return (
    <section className={styles.codeShowcase}>
      <div className="container">
        <div className={styles.showcaseGrid}>
          <div className={styles.showcaseContent}>
            <div className={styles.showcaseBadge}>Intelligence Layer</div>
            <Heading as="h2">One call. Perfect context.</Heading>
            <p>
              Don't know which pattern fits? The intelligence layer analyzes your question,
              selects the optimal cognitive pattern, builds the context, and executes — automatically.
            </p>
            <ul className={styles.showcaseList}>
              <li>Auto-selects from 85 patterns via keyword, LLM, or hybrid matching</li>
              <li>Fuses multiple patterns when your question spans domains</li>
              <li>Builds multi-step workflow chains for complex analysis</li>
              <li>Routes to the optimal cost/quality tier</li>
            </ul>
            <Link className={styles.showcaseLink} to="/docs/intelligence/overview">
              Explore the intelligence layer →
            </Link>
          </div>
          <div className={styles.showcaseCode}>
            <CodeBlock language="python" title="Automatic pattern selection + execution">
              {intelligenceCode}
            </CodeBlock>
          </div>
        </div>
      </div>
    </section>
  );
}

function QualitySection() {
  return (
    <section className={styles.codeShowcase}>
      <div className="container">
        <div className={styles.showcaseGrid}>
          <div className={styles.showcaseCode}>
            <CodeBlock language="python" title="Measure everything">
              {qualityCode}
            </CodeBlock>
          </div>
          <div className={styles.showcaseContent}>
            <div className={styles.showcaseBadge}>Quality & Proof</div>
            <Heading as="h2">No more guessing.</Heading>
            <p>
              Other tools score prompts. mycontext scores prompts <em>and</em> outputs —
              and proves that templates produce measurably better results.
            </p>
            <ul className={styles.showcaseList}>
              <li><strong>Quality Metrics</strong> — 6 dimensions: clarity, completeness, specificity, relevance, structure, efficiency</li>
              <li><strong>Output Evaluator</strong> — 5 dimensions: instruction following, reasoning depth, actionability, structure compliance, cognitive scaffolding</li>
              <li><strong>CAI</strong> — Context Amplification Index proves templates produce better output with a single number</li>
            </ul>
            <Link className={styles.showcaseLink} to="/docs/quality/quality-metrics">
              Learn about quality metrics →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function ComparisonSection() {
  return (
    <section className={styles.comparison}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2">At a Glance</Heading>
          <p>What sets mycontext-ai apart from typical prompt libraries.</p>
        </div>
        <div className={styles.comparisonTable}>
          <table>
            <thead>
              <tr>
                <th>Capability</th>
                <th>mycontext-ai</th>
                <th>Typical prompt libraries</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>Cognitive patterns</td><td className={styles.highlight}>85 research-backed</td><td>10–20 generic</td></tr>
              <tr><td>Zero-cost generic prompts</td><td className={styles.highlight}>85 pre-authored</td><td>None</td></tr>
              <tr><td>Prompt compilation</td><td className={styles.highlight}>3-tier pipeline</td><td>None</td></tr>
              <tr><td>Context quality scoring</td><td className={styles.highlight}>6 dimensions</td><td>None</td></tr>
              <tr><td>Output quality scoring</td><td className={styles.highlight}>5 dimensions</td><td>None</td></tr>
              <tr><td>Template effectiveness proof</td><td className={styles.highlight}>CAI metric</td><td>None</td></tr>
              <tr><td>Export formats</td><td className={styles.highlight}>13</td><td>1–2</td></tr>
              <tr><td>Framework integrations</td><td className={styles.highlight}>7</td><td>0–1</td></tr>
              <tr><td>Research citations</td><td className={styles.highlight}>150+ papers</td><td>0–5</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.cta}>
      <div className="container">
        <div className={styles.ctaInner}>
          <Heading as="h2">The quality of an LLM's output is bounded by the quality of its input.</Heading>
          <p>mycontext engineers that input — and proves it.</p>
          <div className={styles.ctaActions}>
            <Link className={styles.heroPrimary} to="/docs/getting-started/installation">
              Get Started
            </Link>
            <Link className={styles.heroSecondary} to="https://github.com/SadhiraAI/mycontext">
              View on GitHub →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Context Engineering for LLMs"
      description="Build structured contexts with 85 research-backed cognitive patterns. Export to any LLM. Measure quality. Prove it works.">
      <HeroSection />
      <main>
        <FeaturesSection />
        <IntelligenceSection />
        <QualitySection />
        <ComparisonSection />
        <CTASection />
      </main>
    </Layout>
  );
}
