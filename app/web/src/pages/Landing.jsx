import { useState } from "react";
import { Link } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle";
import "./Landing.css";

const PROBLEMS = [
  {
    icon: "🎲",
    title: "Prompts are ad-hoc",
    body: "Every team writes prompts differently. No structure, no reuse, no way to measure what works.",
  },
  {
    icon: "🔄",
    title: "Results are inconsistent",
    body: "Same question, different prompt, wildly different output. Without cognitive scaffolding, quality is a coin flip.",
  },
  {
    icon: "🔒",
    title: "Every LLM needs a different format",
    body: "OpenAI wants messages, Anthropic wants XML, Google wants parts. Rewriting prompts for each is busywork.",
  },
];

const PRODUCT_SUITE = [
  {
    icon: "\uD83D\uDCBB",
    title: "Context Studio",
    badge: "Novice-friendly",
    desc: "Build prompts step by step with a research-backed 9-section flow. Role, rules, thinking strategy, examples, guardrails — everything in the right order, backed by science.",
    highlights: ["Research-backed prompt flow", "9-step guided wizard", "Two paths: manual or AI-driven"],
    link: "/signup",
    linkText: "Try Context Studio",
    accent: "#0d9488",
  },
  {
    icon: "\uD83E\uDD16",
    title: "Context Copilot",
    badge: "AI-Powered",
    desc: "Tell it what you need in plain English. The Copilot suggests role, rules, thinking strategy, examples, and constraints — one step at a time. You approve, tweak, or skip.",
    highlights: ["Plain English \u2192 structured prompt", "Step-by-step AI guidance", "Works with any LLM provider"],
    link: "/signup",
    linkText: "Meet the Copilot",
    accent: "#6366f1",
  },
  {
    icon: "\uD83E\uDDE0",
    title: "Cognitive Studio",
    badge: "87 Patterns",
    desc: "Research-backed cognitive frameworks — not generic prompt snippets. Root cause analysis, decision frameworks, systems thinking, and 80 more. Grounded in peer-reviewed science.",
    highlights: ["87 reasoning frameworks", "7 categories + enterprise", "Fill params \u2192 export to any LLM"],
    link: "/signup",
    linkText: "Browse all patterns",
    accent: "#0d9488",
  },
  {
    icon: "\uD83E\uDDEC",
    title: "Chain Composer",
    badge: "Multi-Pattern",
    desc: "Compose cognitive patterns into multi-stage analysis pipelines. AI selects and orders the right frameworks automatically. Individual templates are tools — chains are agents.",
    highlights: ["AI-powered chain building", "3 modes: Quick, Hybrid, Smart", "Temporal + diagnostic + scenario analysis"],
    link: "/signup",
    linkText: "Build your first chain",
    accent: "#8b5cf6",
  },
  {
    icon: "\uD83D\uDCE6",
    title: "Python SDK",
    badge: "v0.6.0",
    desc: "Context-as-Code for developers. 22 unique capabilities — context generation, quality scoring, CAI proof, async execution, token-budget assembly, and validated structured output. One context, 13 export formats.",
    highlights: ["pip install mycontext-ai", "22 unique SDK capabilities", "13 export formats · 7 framework integrations"],
    link: "https://mycontext-docs.pages.dev/",
    linkText: "SDK Documentation",
    accent: "#0d9488",
    external: true,
  },
  {
    icon: "\uD83D\uDCCA",
    title: "Quality Metrics",
    badge: "Measure First",
    desc: "Score any context across 6 quality dimensions before you send a single token. Then score the output after. Prove templates work with the Context Amplification Index.",
    highlights: ["6 context quality dimensions", "5 output evaluation dimensions", "CAI: prove templates improve output"],
    link: "/signup",
    linkText: "Measure everything",
    accent: "#f59e0b",
  },
];

const RESEARCH_PROOF = [
  {
    stat: "66.7%",
    claim: "improvement with cognitive scaffolding",
    source: "Cognitive Foundations for Reasoning (arxiv 2511.16660)",
    detail: "LLMs under-utilize cognitive elements correlated with success. Scaffolding with structured reasoning frameworks — exactly what our 87 patterns do — improved performance by up to 66.7% on complex tasks.",
  },
  {
    stat: "25–65%",
    claim: "gain from modular composition",
    source: "DSPy: Compiling Declarative LM Calls (arxiv 2310.03714)",
    detail: "Composing modular LLM calls outperforms monolithic prompts. Our chain composition applies this principle with research-backed cognitive modules, not generic signatures.",
  },
  {
    stat: "+10.6%",
    claim: "from evolving context playbooks",
    source: "Agentic Context Engineering (arxiv 2510.04618)",
    detail: "Treating contexts as structured, evolving artifacts — not throwaway strings — improves agent benchmarks. Our Context-as-Code architecture was built on this principle.",
  },
];

const CHAIN_DEMO = {
  question: "Why did customer churn spike 40% last quarter?",
  steps: [
    { name: "Temporal Sequence Analyzer", role: "Build timeline of events", chars: "4,326" },
    { name: "Root Cause Analyzer", role: "Five Whys + Ishikawa analysis", chars: "8,187" },
    { name: "Future Scenario Planner", role: "2×2 scenario matrix", chars: "6,204" },
    { name: "Holistic Integrator", role: "Multi-perspective synthesis", chars: "9,637" },
  ],
  result: "Temporal + diagnostic + scenario + synthesis analysis — impossible from any single prompt.",
};

const MEASUREMENT_FEATURES = [
  {
    stat: "6",
    label: "Quality Dimensions",
    title: "Quality Metrics",
    desc: "Score any context across clarity, completeness, specificity, relevance, structure, and efficiency — before you send a single token.",
  },
  {
    stat: "CAI",
    label: "Amplification Index",
    title: "Prove Templates Work",
    desc: "CAI compares raw prompts vs. template-built contexts on the same question. A CAI of 1.4x means 40% better output. No opinions — numbers.",
  },
  {
    stat: "5",
    label: "Output Dimensions",
    title: "Output Evaluator",
    desc: "Score LLM responses — not just prompts. Measures instruction following, reasoning depth, actionability, structure compliance, and cognitive scaffolding.",
  },
];

const TOOLS_PROOF = [
  {
    orchestrator: "LangChain / LangGraph",
    desc: "Context.to_langchain() exports to any LangChain workflow. Patterns become graph nodes.",
    status: "Built-in",
  },
  {
    orchestrator: "CrewAI",
    desc: "Context.to_crewai() provides role, goal, and backstory. Each pattern becomes an agent.",
    status: "Built-in",
  },
  {
    orchestrator: "AutoGen",
    desc: "Context.to_autogen() provides system_message. Chain = multi-agent GroupChat.",
    status: "Built-in",
  },
  {
    orchestrator: "DSPy / Semantic Kernel / Google ADK",
    desc: "Dedicated integration helpers for DSPy, Semantic Kernel, and Google ADK out of the box.",
    status: "Built-in",
  },
  {
    orchestrator: "Any LLM API",
    desc: "Context.to_openai(), .to_anthropic(), .to_google(). One context, 13 export formats.",
    status: "Built-in",
  },
];

const FEATURED_TEMPLATES = [
  {
    name: "Root Cause Analyzer",
    category: "Reasoning",
    desc: "Five Whys + Ishikawa-style analysis to find what's really causing the problem.",
    params: ["problem", "context", "symptoms"],
  },
  {
    name: "Decision Framework",
    category: "Decision",
    desc: "Structured decision-making with weighted criteria, options, and clear recommendations.",
    params: ["decision", "options", "depth"],
  },
  {
    name: "Data Analyzer",
    category: "Analysis",
    desc: "Extract patterns, insights, and actionable recommendations from any dataset.",
    params: ["data", "analysis_focus", "context"],
  },
  {
    name: "Comparative Analyzer",
    category: "Decision",
    desc: "Side-by-side comparison with explicit criteria and structured evaluation.",
    params: ["options", "criteria", "context"],
  },
  {
    name: "Code Reviewer",
    category: "Specialized",
    desc: "Systematic code review covering security, performance, maintainability, and best practices.",
    params: ["code", "language", "focus_areas"],
  },
  {
    name: "Idea Generator",
    category: "Creative",
    desc: "Divergent thinking with structured brainstorming and evaluation.",
    params: ["topic", "constraints", "quantity"],
  },
];

const CATEGORIES = [
  "Analysis", "Reasoning", "Creative", "Communication",
  "Planning", "Decision", "Specialized",
];

const PERSONAS = [
  {
    icon: "🏢",
    title: "Product & Business Teams",
    desc: "Turn stakeholder questions into structured analyses. Decision frameworks, root cause analysis, and competitive comparisons — without writing a single prompt.",
    example: "\"Should we build or buy?\" → Decision Framework → structured recommendation",
  },
  {
    icon: "⚙️",
    title: "AI Engineers & Developers",
    desc: "Use cognitive patterns as reusable tools in any orchestrator. Build chains, not agents. Export to any framework.",
    example: "DataAnalyzer as a smolagents Tool → CodeAgent orchestrates → no custom agent code",
  },
  {
    icon: "🔬",
    title: "Researchers & Analysts",
    desc: "Apply cognitive science patterns to your analysis workflows. Chain temporal analysis → root cause → scenarios for depth no single prompt can match.",
    example: "\"Why did churn spike?\" → 4-pattern chain → multi-perspective strategic report",
  },
];

const ENTERPRISE_CATEGORIES = [
  { name: "Systems Thinking", count: 6, examples: "Feedback loops, leverage points, causal loops, emergence" },
  { name: "Problem Solving", count: 6, examples: "Bottleneck identification, constraint optimization, dependency mapping" },
  { name: "Decision Making", count: 5, examples: "Trade-off analysis, multi-objective optimization, cost-benefit" },
  { name: "Metacognition", count: 5, examples: "Self-regulation, cognitive strategy selection, error detection" },
  { name: "Ethical Reasoning", count: 5, examples: "Moral dilemmas, stakeholder ethics, value conflicts" },
  { name: "Diagnostic & Temporal", count: 6, examples: "Root cause diagnosis, scenario planning, timeline analysis" },
  { name: "Learning Science", count: 5, examples: "Scaffolding, spaced repetition, cognitive load management" },
  { name: "Synthesis & Integration", count: 3, examples: "Cross-domain synthesis, pattern recognition, holistic integration" },
];


const DEMO_INPUT = "Why did customer churn spike 40% last quarter?";
const DEMO_OUTPUT = `GUIDANCE
Role: Expert root cause analyst with systems thinking
Rules: Use Five Whys methodology, consider multiple causal paths

DIRECTIVE
Analyze the following problem using structured root cause analysis...
Problem: Why did customer churn spike 40% last quarter?

CONSTRAINTS
Must include: root_causes, contributing_factors, timeline, recommendations
Format: Structured analysis with confidence levels`;

export default function Landing() {
  const [expandedProof, setExpandedProof] = useState(null);

  return (
    <div className="landing">
      <header className="landing-header">
        <span className="landing-brand">
          <svg className="brand-icon-svg" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="url(#brandGradL)" strokeWidth="2.2" strokeLinecap="round"><defs><linearGradient id="brandGradL" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stopColor="#5ba8a0"/><stop offset="100%" stopColor="#8b5cf6"/></linearGradient></defs><path d="M4 6c4-2 12-2 16 0"/><path d="M4 12c4-2 12-2 16 0"/><path d="M4 18c4-2 12-2 16 0"/></svg>
          <span className="brand-my">my</span>
          <span className="brand-context">context</span>
          <span className="brand-dash">-</span>
          <span className="brand-ai">ai</span>
        </span>
        <div className="landing-header-actions">
          <ThemeToggle />
          <Link to="/login" className="landing-btn secondary">Log in</Link>
          <Link to="/signup" className="landing-btn primary">Get started free</Link>
        </div>
      </header>

      <main className="landing-main">
        {/* ── Hero ──────────────────────────────────────── */}
        <section className="landing-hero">
          <div className="landing-hero-badge">The Context Engineering Platform</div>
          <h1 className="landing-headline">
            Don't write prompts.<br />
            Engineer contexts.
          </h1>
          <p className="landing-tagline">
            Research-backed prompt flows. 87 cognitive reasoning frameworks. AI-driven copilot.
            Multi-pattern composition. Quality metrics. One SDK — 13 export formats.
          </p>
          <blockquote className="landing-epigraph">
            &ldquo;Cognitive scaffolding improves LLM performance by up to 66.7%&rdquo;
            <cite>— Cognitive Foundations for Reasoning, arxiv 2511.16660</cite>
          </blockquote>

          <div className="landing-poem">
            <h3 className="landing-poem-title">Basho's Frog Vs Turtle</h3>
            <img src="/front_page.jpg" alt="Pond with turtle" className="landing-poem-img" />
            <blockquote className="landing-poem-text">
              The ancient pond,<br />
              A turtle slinks in:<br />
              Rippleless....
            </blockquote>
            <p className="landing-poem-inspired">
              Inspired by <strong>Matsuo Bash&#x14D;</strong>, Japanese Zen Master
            </p>
          </div>
          <div className="landing-hero-actions">
            <Link to="/signup" className="landing-btn primary large">Let's slink in</Link>
            <Link to="/signup" className="landing-btn secondary large">See all 87 patterns</Link>
          </div>

          <div className="landing-demo">
            <div className="landing-demo-header">
              <span className="landing-demo-dot" />
              <span className="landing-demo-dot" />
              <span className="landing-demo-dot" />
              <span className="landing-demo-title">Live transformation</span>
            </div>
            <div className="landing-demo-body">
              <div className="landing-demo-input">
                <span className="landing-demo-label">Your question</span>
                <p>{DEMO_INPUT}</p>
              </div>
              <div className="landing-demo-arrow">→</div>
              <div className="landing-demo-output">
                <span className="landing-demo-label">Structured context</span>
                <pre>{DEMO_OUTPUT}</pre>
              </div>
            </div>
          </div>
        </section>

        {/* ── Free Guide Download ────────────────────── */}
        <section className="landing-section landing-guide-section">
          <div className="landing-guide-card">
            <div className="landing-guide-content">
              <span className="landing-guide-badge">Free PDF Guide</span>
              <h2 className="landing-guide-title">The Only Cursor Guide You'll Ever Need</h2>
              <p className="landing-guide-desc">
                Every Cursor capability in one document — rules, skills, subagents, MCP servers,
                hooks, plugins, browser automation, and best practices. From zero to a fully
                autonomous development environment.
              </p>
              <ul className="landing-guide-highlights">
                <li>All 8 configuration systems explained with real examples</li>
                <li>20+ free MCP servers categorized by use case</li>
                <li>Step-by-step "How It All Works Together" walkthrough</li>
                <li>Beginner-friendly — works for any codebase, any language</li>
              </ul>
              <div className="landing-guide-meta">
                <span>By Dhiraj Pokhrel</span>
                <span className="landing-guide-sep">·</span>
                <span>1,200+ lines</span>
                <span className="landing-guide-sep">·</span>
                <span>PDF</span>
              </div>
            </div>
            <div className="landing-guide-action">
              <a
                href="/cursor_guide.pdf"
                download="The_Only_Cursor_Guide_Youll_Ever_Need.pdf"
                className="landing-btn primary large landing-guide-download"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download Free PDF
              </a>
              <span className="landing-guide-note">No signup required</span>
            </div>
          </div>
        </section>

        {/* ── Problem ──────────────────────────────────── */}
        <section className="landing-section">
          <h2 className="landing-section-title">The problem with prompt engineering</h2>
          <p className="landing-section-sub">
            Most teams treat prompts as strings. Context engineering treats them as structured, testable, portable artifacts backed by cognitive science.
          </p>
          <div className="landing-problems">
            {PROBLEMS.map((p, i) => (
              <div key={i} className="landing-problem-card">
                <span className="landing-problem-icon">{p.icon}</span>
                <h3>{p.title}</h3>
                <p>{p.body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Research Proof ───────────────────────────── */}
        <section className="landing-section landing-research">
          <h2 className="landing-section-title">Why cognitive patterns work</h2>
          <p className="landing-section-sub">
            This isn't marketing. Peer-reviewed research proves that structured reasoning
            frameworks dramatically improve LLM output quality.
          </p>
          <div className="landing-research-grid">
            {RESEARCH_PROOF.map((r, i) => (
              <button
                key={i}
                type="button"
                className={`landing-research-card ${expandedProof === i ? "expanded" : ""}`}
                onClick={() => setExpandedProof(expandedProof === i ? null : i)}
              >
                <span className="landing-research-stat">{r.stat}</span>
                <span className="landing-research-claim">{r.claim}</span>
                <span className="landing-research-source">{r.source}</span>
                {expandedProof === i && (
                  <p className="landing-research-detail">{r.detail}</p>
                )}
              </button>
            ))}
          </div>
        </section>

        {/* ── Product Suite ────────────────────────────── */}
        <section className="landing-section landing-products-section">
          <h2 className="landing-section-title">Everything you need — nothing you don't</h2>
          <p className="landing-section-sub">
            Six products, one platform. Each one research-backed. Each one designed to make your AI output measurably better.
          </p>
          <div className="landing-products-grid">
            {PRODUCT_SUITE.map((p, i) => (
              <div key={i} className="landing-product-card" style={{ "--product-accent": p.accent }}>
                <div className="landing-product-top">
                  <span className="landing-product-icon">{p.icon}</span>
                  <span className="landing-product-badge" style={{ background: p.accent }}>{p.badge}</span>
                </div>
                <h3>{p.title}</h3>
                <p className="landing-product-desc">{p.desc}</p>
                <ul className="landing-product-highlights">
                  {p.highlights.map((h, hi) => (
                    <li key={hi}>{h}</li>
                  ))}
                </ul>
                {p.external ? (
                  <a href={p.link} target="_blank" rel="noopener noreferrer" className="landing-product-link" style={{ color: p.accent }}>{p.linkText} →</a>
                ) : (
                  <Link to={p.link} className="landing-product-link" style={{ color: p.accent }}>{p.linkText} →</Link>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* ── What makes us different ──────────────────── */}
        <section className="landing-section landing-diff-section">
          <h2 className="landing-section-title">What makes us different</h2>
          <div className="landing-diff-grid">
            <div className="landing-diff-card">
              <span className="landing-diff-icon">{"\uD83D\uDD2C"}</span>
              <h3>Research-backed, not guesswork</h3>
              <p>Every template, every flow, every ordering decision is grounded in peer-reviewed research. We cite our sources.</p>
            </div>
            <div className="landing-diff-card">
              <span className="landing-diff-icon">{"\uD83D\uDCCF"}</span>
              <h3>Measure before you send</h3>
              <p>Score your context across 6 dimensions <em>before</em> calling the LLM. Then score the output. Then prove the template made a difference.</p>
            </div>
            <div className="landing-diff-card">
              <span className="landing-diff-icon">{"\uD83D\uDD17"}</span>
              <h3>Compose, don't rewrite</h3>
              <p>Chain multiple cognitive patterns into multi-stage pipelines. A 4-pattern chain delivers analysis no single prompt can match.</p>
            </div>
            <div className="landing-diff-card">
              <span className="landing-diff-icon">{"\uD83C\uDF10"}</span>
              <h3>One context, every LLM</h3>
              <p>Build once, export to 13 formats. OpenAI, Anthropic, Google, LangChain, CrewAI, AutoGen — no rewriting for each provider.</p>
            </div>
            <div className="landing-diff-card">
              <span className="landing-diff-icon">{"\u2728"}</span>
              <h3>Role + goal → full context</h3>
              <p>Describe your role and objective in plain English. The Context Generator builds rules, examples, output schema, and guard rails automatically — no manual prompt engineering.</p>
            </div>
            <div className="landing-diff-card">
              <span className="landing-diff-icon">{"\uD83D\uDEE1\uFE0F"}</span>
              <h3>Production-ready, not experimental</h3>
              <p>Async execution, token-budget assembly, Pydantic-validated structured output, retry with backoff, and injection prevention — all built in.</p>
            </div>
          </div>
        </section>

        {/* ── Chain Composition ────────────────────────── */}
        <section className="landing-section landing-chain-section">
          <h2 className="landing-section-title">Compose patterns into agents</h2>
          <p className="landing-section-sub">
            Individual templates are tools. Chains of templates are agents.
            No single prompt can deliver temporal + diagnostic + scenario + synthesis analysis. A chain can.
          </p>
          <div className="landing-chain-demo">
            <div className="landing-chain-question">
              <span className="landing-chain-label">Question</span>
              <p>{CHAIN_DEMO.question}</p>
            </div>
            <div className="landing-chain-flow">
              {CHAIN_DEMO.steps.map((step, i) => (
                <div key={i} className="landing-chain-step">
                  <div className="landing-chain-step-num">{i + 1}</div>
                  <div className="landing-chain-step-body">
                    <strong>{step.name}</strong>
                    <span>{step.role}</span>
                    <code>{step.chars} chars</code>
                  </div>
                  {i < CHAIN_DEMO.steps.length - 1 && <div className="landing-chain-arrow">↓</div>}
                </div>
              ))}
            </div>
            <div className="landing-chain-result">
              <span className="landing-chain-label">Result</span>
              <p>{CHAIN_DEMO.result}</p>
            </div>
          </div>
        </section>

        {/* ── Measure Everything ────────────────────────── */}
        <section className="landing-section landing-measure-section">
          <h2 className="landing-section-title">Measure everything</h2>
          <p className="landing-section-sub">
            Other tools generate prompts and hope for the best. mycontext scores your context <em>before</em> you
            call the LLM — and scores the output <em>after</em>. Then proves the template made a measurable difference.
          </p>
          <div className="landing-measure-grid">
            {MEASUREMENT_FEATURES.map((m, i) => (
              <div key={i} className="landing-measure-card">
                <div className="landing-measure-stat">
                  <span className="landing-measure-num">{m.stat}</span>
                  <span className="landing-measure-label">{m.label}</span>
                </div>
                <h3>{m.title}</h3>
                <p>{m.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Templates as Tools ──────────────────────── */}
        <section className="landing-section">
          <h2 className="landing-section-title">Use patterns as tools in any orchestrator</h2>
          <p className="landing-section-sub">
            You don't need to build custom agents. A research-backed template used as a tool
            <em> is </em> an agent capability. Proven with smolagents, built-in for LangChain, CrewAI, AutoGen, and any LLM API.
          </p>
          <div className="landing-tools-grid">
            {TOOLS_PROOF.map((t, i) => (
              <div key={i} className="landing-tool-card">
                <div className="landing-tool-header">
                  <strong>{t.orchestrator}</strong>
                  <span className={`landing-tool-status ${t.status === "Proven" ? "proven" : ""}`}>{t.status}</span>
                </div>
                <p>{t.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Template Showcase ────────────────────────── */}
        <section className="landing-section">
          <h2 className="landing-section-title">87 research-backed cognitive patterns</h2>
          <p className="landing-section-sub">
            Not generic prompt snippets. Reasoning frameworks grounded in cognitive science,
            decision theory, and systems thinking — each backed by peer-reviewed research.
          </p>
          <div className="landing-categories">
            {CATEGORIES.map((c) => (
              <span key={c} className="landing-category-chip">{c}</span>
            ))}
            <span className="landing-category-chip enterprise">+71 Enterprise</span>
          </div>
          <div className="landing-templates-grid">
            {FEATURED_TEMPLATES.map((t) => (
              <div key={t.name} className="landing-template-card">
                <div className="landing-template-header">
                  <span className="landing-template-cat">{t.category}</span>
                </div>
                <h4>{t.name}</h4>
                <p>{t.desc}</p>
                <div className="landing-template-params">
                  {t.params.map((p) => (
                    <code key={p}>{p}</code>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <div className="landing-templates-cta">
            <Link to="/signup" className="landing-btn secondary">Browse all 87 patterns →</Link>
          </div>
        </section>

        {/* ── Three-Tier Execution ─────────────────────── */}
        <section className="landing-section">
          <h2 className="landing-section-title">Three ways to execute — pick your cost/quality trade-off</h2>
          <p className="landing-section-sub">
            Every template ships with a pre-authored generic prompt.
            Use it as-is for zero-cost execution, compile it for richer results, or go full response for maximum depth.
          </p>
          <div className="landing-tiers">
            <div className="landing-tier-card">
              <span className="landing-tier-badge landing-tier-badge--static">0 LLM calls</span>
              <h3>Static Generic</h3>
              <p>Pre-authored cognitive prompts — instant, zero cost. Ideal for chaining, compilation, and lightweight pipelines.</p>
            </div>
            <div className="landing-tier-card landing-tier-card--featured">
              <span className="landing-tier-badge landing-tier-badge--compiled">1-3 LLM calls</span>
              <h3>Dynamic Compiled</h3>
              <p>Templates compiled into one refined prompt. Best balance of cost and quality for complex analysis.</p>
            </div>
            <div className="landing-tier-card">
              <span className="landing-tier-badge landing-tier-badge--full">2-3 LLM calls</span>
              <h3>Full Response</h3>
              <p>Complete template execution with integrated multi-template analysis. Maximum depth and nuance.</p>
            </div>
          </div>
        </section>

        {/* ── Who Benefits ─────────────────────────────── */}
        <section className="landing-section">
          <h2 className="landing-section-title">Built for every team that uses AI</h2>
          <div className="landing-personas">
            {PERSONAS.map((p, i) => (
              <div key={i} className="landing-persona-card">
                <span className="landing-persona-icon">{p.icon}</span>
                <h3>{p.title}</h3>
                <p>{p.desc}</p>
                <div className="landing-persona-example">
                  <code>{p.example}</code>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── Numbers ──────────────────────────────────── */}
        <section className="landing-section landing-stats-section">
          <div className="landing-stats">
            <div className="landing-stat">
              <span className="landing-stat-num">87</span>
              <span className="landing-stat-label">Cognitive Patterns</span>
            </div>
            <div className="landing-stat">
              <span className="landing-stat-num">13</span>
              <span className="landing-stat-label">Export Formats</span>
            </div>
            <div className="landing-stat">
              <span className="landing-stat-num">6+5</span>
              <span className="landing-stat-label">Quality Dimensions (Context + Output)</span>
            </div>
            <div className="landing-stat">
              <span className="landing-stat-num">CAI</span>
              <span className="landing-stat-label">Prove Templates Work</span>
            </div>
            <div className="landing-stat">
              <span className="landing-stat-num">7</span>
              <span className="landing-stat-label">Framework Integrations</span>
            </div>
            <div className="landing-stat">
              <span className="landing-stat-num">22</span>
              <span className="landing-stat-label">Unique SDK Capabilities</span>
            </div>
          </div>
        </section>

        {/* ── Enterprise Teaser ────────────────────────── */}
        <section className="landing-section landing-enterprise">
          <div className="landing-enterprise-content">
            <h2>Enterprise Edition</h2>
            <p className="landing-enterprise-lead">
              71 advanced patterns for teams that need deeper analysis — decision optimization,
              systems thinking, ethical reasoning, metacognition, and more.
            </p>
            <div className="landing-enterprise-cats">
              {ENTERPRISE_CATEGORIES.map((c) => (
                <div key={c.name} className="landing-enterprise-cat">
                  <div className="landing-enterprise-cat-header">
                    <strong>{c.name}</strong>
                    <span className="landing-enterprise-count">{c.count} patterns</span>
                  </div>
                  <p>{c.examples}</p>
                </div>
              ))}
            </div>
            <Link to="/signup" className="landing-btn primary">Start with free edition</Link>
          </div>
        </section>

        {/* ── Footer CTA ──────────────────────────────── */}
        <section className="landing-section landing-final-cta">
          <h2>Start composing better contexts</h2>
          <p>16 free patterns forever. No credit card required.</p>
          <div className="landing-hero-actions">
            <Link to="/signup" className="landing-btn primary large">Get started free</Link>
          </div>
          <p className="landing-dev-link">
            Developers: <a href="https://mycontext-docs.pages.dev/" target="_blank" rel="noopener noreferrer">SDK Docs</a> · <a href="https://pypi.org/project/mycontext-ai/" target="_blank" rel="noopener noreferrer">PyPI</a> · <a href="https://github.com/SadhiraAI/mycontext" target="_blank" rel="noopener noreferrer">GitHub</a>
          </p>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="landing-footer-company">
          <strong>Sadhira AI &amp; Analytics</strong>
          <span className="landing-footer-sep">&middot;</span>
          <span>6912 Hapsburg Lane, Henrico, VA 23231, USA</span>
          <span className="landing-footer-sep">&middot;</span>
          <span>(804) 418-2759</span>
          <span className="landing-footer-sep">&middot;</span>
          <a href="https://contact.sadhiraai.com" target="_blank" rel="noopener noreferrer">contact.sadhiraai.com</a>
        </div>
        <div className="landing-footer-social">
          <a href="#" title="Facebook" className="landing-social-badge" aria-label="Facebook">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="#" title="X / Twitter" className="landing-social-badge" aria-label="X">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </a>
          <a href="#" title="LinkedIn" className="landing-social-badge" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
          <a href="#" title="GitHub" className="landing-social-badge" aria-label="GitHub">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
          </a>
        </div>
        <p className="landing-footer-copy">&copy; {new Date().getFullYear()} Sadhira AI &amp; Analytics. All rights reserved.</p>
      </footer>
    </div>
  );
}
