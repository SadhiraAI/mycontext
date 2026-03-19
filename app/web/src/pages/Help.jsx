import { Link } from "react-router-dom";
import "./Help.css";

const CONCEPTS = [
  { term: "Pattern", def: "A reusable cognitive template grounded in research. Each pattern defines structure, inputs, and expected outputs. Examples: Root Cause Analyzer, Decision Framework." },
  { term: "Context", def: "The complete structured prompt combining Guidance + Directive + Constraints. This is what gets sent to the LLM." },
  { term: "Guidance", def: "System-level instructions: who the model acts as (Role), how it behaves (Rules), and communication tone (Style)." },
  { term: "Directive", def: "The specific task instruction — the 'what'. Contains the main question or instruction with parameter slots." },
  { term: "Constraints", def: "Hard boundaries: what must appear in the output (must_include), what must not (must_not_include), and formatting rules." },
  { term: "Export Format", def: "The output format for your context. Supports 13 formats: Markdown, JSON, YAML, OpenAI, Anthropic, Google, LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, XML." },
  { term: "Quality Score", def: "A 0-100 score across 6 dimensions: clarity, completeness, specificity, relevance, structure, efficiency. Available in fast (heuristic) and accurate (LLM) modes." },
];

const FAQ = [
  { q: "How do I get started?", a: "Go to Templates, pick a pattern, fill in the parameters, and click Build. That's it — your structured context is ready to download." },
  { q: "What's the difference between Templates and Custom?", a: "Templates are pre-built, research-backed patterns (87 total). Custom lets you create your own templates from scratch using a step-by-step wizard." },
  { q: "How does quality scoring work?", a: "Fast mode uses heuristics (no API key needed). Accurate mode uses an LLM to semantically evaluate your context across 6 dimensions. Add an API key in Account settings." },
  { q: "What is Enterprise?", a: "Enterprise adds 71 advanced patterns for decision-making, systems thinking, ethical reasoning, metacognition, and more. Enter a license key in your Account." },
  { q: "Can I export to my LLM framework?", a: "Yes. We support OpenAI, Anthropic, Google, LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, Semantic Kernel, and raw formats (JSON, YAML, Markdown)." },
  { q: "Is there a Python SDK?", a: "Yes. Install with: pip install mycontext-ai. See the PyPI page for documentation." },
];

export default function Help() {
  return (
    <div className="help-page">
      <h1>Help &amp; Reference</h1>
      <p className="help-intro">Everything you need to know about context engineering with mycontext.</p>

      <section className="help-section">
        <h2>Core Concepts</h2>
        <div className="help-concepts">
          {CONCEPTS.map((c) => (
            <div key={c.term} className="help-concept">
              <h3>{c.term}</h3>
              <p>{c.def}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="help-section">
        <h2>Frequently Asked Questions</h2>
        <div className="help-faq">
          {FAQ.map((f, i) => (
            <details key={i} className="help-faq-item">
              <summary>{f.q}</summary>
              <p>{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      <section className="help-section">
        <h2>Developer Resources</h2>
        <div className="help-links">
          <a href="https://pypi.org/project/mycontext-ai/" target="_blank" rel="noopener noreferrer" className="help-link-card">
            <strong>Python SDK on PyPI</strong>
            <p>pip install mycontext-ai</p>
          </a>
          <Link to="/templates" className="help-link-card">
            <strong>Browse Templates</strong>
            <p>87 research-backed patterns</p>
          </Link>
          <Link to="/custom" className="help-link-card">
            <strong>Build Custom</strong>
            <p>Create your own templates</p>
          </Link>
        </div>
      </section>
    </div>
  );
}
