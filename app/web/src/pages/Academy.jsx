import { useState } from "react";
import { Link } from "react-router-dom";
import "./Academy.css";

const TRACKS = [
  {
    icon: "\u{1F680}",
    title: "Getting Started",
    desc: "From zero to structured context in 5 minutes. Install the SDK, build your first context, and send it to an LLM.",
  },
  {
    icon: "\u{1F4DA}",
    title: "Pattern Deep Dives",
    desc: "Walkthroughs for each cognitive pattern \u2014 when to use it, what parameters matter, and real-world examples.",
  },
  {
    icon: "\u{1F517}",
    title: "Chain Composition",
    desc: "Learn to compose multi-pattern chains that deliver temporal + diagnostic + scenario + synthesis analysis.",
  },
  {
    icon: "\u{1F4CA}",
    title: "Quality & CAI",
    desc: "Use Quality Metrics to score contexts before sending. Use CAI to prove templates produce better LLM output.",
  },
  {
    icon: "\u{1F9E9}",
    title: "Framework Integrations",
    desc: "Plug mycontext into LangChain, CrewAI, AutoGen, smolagents, and more. Patterns as tools, contexts as agents.",
  },
  {
    icon: "\u{1F4D3}",
    title: "Example Notebooks",
    desc: "Jupyter notebooks covering data analysis, code review, strategic planning, and end-to-end agent workflows.",
  },
];

const CONCEPTS = [
  { term: "Pattern", def: "A reusable cognitive template grounded in research. Each pattern defines structure, inputs, and expected outputs. Examples: Root Cause Analyzer, Decision Framework." },
  { term: "Context", def: "The complete structured prompt combining Guidance + Directive + Constraints. This is what gets sent to the LLM." },
  { term: "Guidance", def: "System-level instructions: who the model acts as (Role), how it behaves (Rules), and communication tone (Style)." },
  { term: "Directive", def: "The specific task instruction \u2014 the \u2018what\u2019. Contains the main question or instruction with parameter slots." },
  { term: "Constraints", def: "Hard boundaries: what must appear in the output (must_include), what must not (must_not_include), and formatting rules." },
  { term: "Export Format", def: "The output format for your context. Supports 13 formats: Markdown, JSON, YAML, OpenAI, Anthropic, Google, LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, XML." },
  { term: "Quality Score", def: "A 0\u2013100 score across 6 dimensions: clarity, completeness, specificity, relevance, structure, efficiency. Available in fast (heuristic) and accurate (LLM) modes." },
];

const FAQ = [
  { q: "How do I get started?", a: "Go to Templates, pick a pattern, fill in the parameters, and click Build. That\u2019s it \u2014 your structured context is ready to download." },
  { q: "What\u2019s the difference between Templates and Custom?", a: "Templates are pre-built, research-backed patterns (85 total). Custom lets you create your own templates from scratch using a step-by-step wizard." },
  { q: "How does quality scoring work?", a: "Fast mode uses heuristics (no API key needed). Accurate mode uses an LLM to semantically evaluate your context across 6 dimensions. Add an API key in Account settings." },
  { q: "What is Enterprise?", a: "Enterprise adds 69 advanced patterns for decision-making, systems thinking, ethical reasoning, metacognition, and more. Enter a license key in your Account." },
  { q: "Can I export to my LLM framework?", a: "Yes. We support OpenAI, Anthropic, Google, LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, and raw formats (JSON, YAML, Markdown)." },
  { q: "Is there a Python SDK?", a: "Yes. Install with: pip install mycontext-ai. See the PyPI page for documentation." },
];

export default function Academy() {
  const [expandedFaq, setExpandedFaq] = useState(null);

  return (
    <div className="academy-page">
      <div className="academy-header">
        <span className="academy-header-icon">{"\uD83C\uDF93"}</span>
        <div>
          <h1>Sadhira Academy</h1>
          <p className="academy-intro">
            Tutorials, reference, and everything you need to master context engineering.
          </p>
        </div>
      </div>

      {/* Learning Tracks */}
      <section className="academy-section">
        <h2>Learning Tracks</h2>
        <p className="academy-section-sub">
          Each track takes you from concept to working code. Start with Getting Started, then explore any track that fits your use case.
        </p>
        <div className="academy-grid">
          {TRACKS.map((t) => (
            <div key={t.title} className="academy-card">
              <span className="academy-badge soon">Coming Soon</span>
              <span className="academy-card-icon">{t.icon}</span>
              <h3>{t.title}</h3>
              <p>{t.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Core Concepts */}
      <section className="academy-section">
        <h2>Core Concepts</h2>
        <div className="academy-concepts-grid">
          {CONCEPTS.map((c) => (
            <div key={c.term} className="academy-concept">
              <h3>{c.term}</h3>
              <p>{c.def}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="academy-section">
        <h2>Frequently Asked Questions</h2>
        <div className="academy-faq">
          {FAQ.map((f, i) => (
            <button
              key={i}
              type="button"
              className={`academy-faq-item${expandedFaq === i ? " open" : ""}`}
              onClick={() => setExpandedFaq(expandedFaq === i ? null : i)}
            >
              <div className="academy-faq-q">
                <span>{f.q}</span>
                <span className="academy-faq-chevron">{expandedFaq === i ? "\u2212" : "+"}</span>
              </div>
              {expandedFaq === i && <p className="academy-faq-a">{f.a}</p>}
            </button>
          ))}
        </div>
      </section>

      {/* Quick Links */}
      <section className="academy-section">
        <h2>Quick Links</h2>
        <div className="academy-grid">
          <a href="https://pypi.org/project/mycontext-ai/" target="_blank" rel="noopener noreferrer" className="academy-card">
            <span className="academy-card-icon">{"\u{1F4E6}"}</span>
            <h3>Python SDK on PyPI</h3>
            <p>pip install mycontext-ai</p>
          </a>
          <Link to="/templates" className="academy-card">
            <span className="academy-card-icon">{"\u{1F9E0}"}</span>
            <h3>Cognitive Studio</h3>
            <p>Browse all 85 cognitive patterns</p>
          </Link>
          <Link to="/chains" className="academy-card">
            <span className="academy-card-icon">{"\u26D3\uFE0F"}</span>
            <h3>Chain Composer</h3>
            <p>Build multi-pattern workflows</p>
          </Link>
          <Link to="/custom" className="academy-card">
            <span className="academy-card-icon">{"\u{270F}\uFE0F"}</span>
            <h3>Context Studio</h3>
            <p>Create your own templates</p>
          </Link>
        </div>
      </section>

      <div className="academy-cta">
        <h3>Tutorials and examples are on the way</h3>
        <p>We are building step-by-step guides and Jupyter notebooks. Check back soon or explore the Cognitive Studio in the meantime.</p>
      </div>
    </div>
  );
}
