import { Link } from "react-router-dom";
import "./Guidebooks.css";

const GUIDEBOOKS = [
  {
    id: "prompt-engineering",
    title: "Stop Guessing. Start Contextualizing Prompts.",
    subtitle: "The Complete Prompt Engineering Guidebook",
    description:
      "The 9-Section Architecture that separates professionals from guessers. Role, Goal, Rules, Style, Reasoning, Examples, Output Contract, Guard Rails, Task — every section explained with formulas, examples, and the science behind why it works.",
    tags: ["Prompt Engineering", "9-Section Architecture", "LLM Best Practices"],
    chapters: 9,
    readTime: "35 min",
    level: "All levels",
    icon: "✦",
    color: "#3d8b80",
    href: "/guidebooks/prompt-engineering.html",
  },
  {
    id: "cursor-guide",
    title: "The Only Cursor Guide You'll Ever Need",
    subtitle: "Every Configuration File. Every Capability.",
    description:
      "Rules, Skills, Subagents, MCP servers, Hooks, Plugins, Browser automation, Worktrees, Model selection, and Cost optimization. From zero to a fully autonomous AI development environment — in one document.",
    tags: ["Cursor IDE", "MCP Servers", "AI Workflows", "Developer Setup"],
    chapters: 12,
    readTime: "45 min",
    level: "Beginner → Advanced",
    icon: "⌘",
    color: "#7c3aed",
    href: "/guidebooks/cursor-guide.html",
  },
];

export default function Guidebooks() {
  return (
    <div className="gb-root">
      {/* ── Nav ── */}
      <nav className="gb-nav">
        <Link to="/" className="gb-nav-logo">
          <span className="gb-nav-logo-mark">◈</span>
          <span>mycontext</span>
        </Link>
        <div className="gb-nav-links">
          <Link to="/login" className="gb-nav-link">Sign in</Link>
          <Link to="/signup" className="gb-nav-cta">Get started free</Link>
        </div>
      </nav>

      {/* ── Hero ── */}
      <header className="gb-hero">
        <div className="gb-hero-bg" />
        <div className="gb-hero-inner">
          <span className="gb-hero-label">Free Guides · Sadhira AI</span>
          <h1 className="gb-hero-title">
            Guidebooks
          </h1>
          <p className="gb-hero-sub">
            Comprehensive, downloadable guides on AI prompting, tooling, and workflows.
            Every guide is free — no signup required. Open, read, download as PDF.
          </p>
        </div>
      </header>

      {/* ── Grid ── */}
      <main className="gb-main">
        <div className="gb-grid">
          {GUIDEBOOKS.map((g) => (
            <a
              key={g.id}
              href={g.href}
              target="_blank"
              rel="noopener noreferrer"
              className="gb-card"
            >
              <div className="gb-card-top">
                <span className="gb-card-icon" style={{ color: g.color }}>
                  {g.icon}
                </span>
                <div className="gb-card-meta">
                  <span className="gb-card-chapters">{g.chapters} chapters</span>
                  <span className="gb-card-dot">·</span>
                  <span className="gb-card-read">{g.readTime} read</span>
                  <span className="gb-card-dot">·</span>
                  <span className="gb-card-level">{g.level}</span>
                </div>
              </div>

              <h2 className="gb-card-title">{g.title}</h2>
              <p className="gb-card-subtitle">{g.subtitle}</p>
              <p className="gb-card-desc">{g.description}</p>

              <div className="gb-card-tags">
                {g.tags.map((t) => (
                  <span key={t} className="gb-card-tag">{t}</span>
                ))}
              </div>

              <div className="gb-card-footer">
                <span className="gb-card-open">Open guide →</span>
                <span className="gb-card-pdf">↓ Download PDF</span>
              </div>
            </a>
          ))}
        </div>

        {/* ── Coming soon placeholder ── */}
        <div className="gb-coming-soon">
          <span className="gb-cs-icon">📖</span>
          <h3>More guidebooks coming soon</h3>
          <p>Chain Composer patterns, Cognitive template design, LLM provider comparison, and more. <a href="/signup">Sign up</a> to get notified.</p>
        </div>
      </main>

      {/* ── Footer ── */}
      <footer className="gb-footer">
        <span>Free guides published by <a href="https://sadhiraai.com" target="_blank" rel="noopener noreferrer">Sadhira AI</a></span>
        <Link to="/">← Back to mycontext</Link>
      </footer>
    </div>
  );
}
