import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTour } from "../context/TourContext";
import * as api from "../api/client";
import SmartExecutePanel from "../components/SmartExecutePanel";
import useActiveProvider from "../hooks/useActiveProvider";
import "./Dashboard.css";

const JOURNEY = [
  {
    step: "\uD83D\uDCBB",
    title: "Context Studio",
    sub: "Novice",
    desc: "Build your first AI context from scratch with our guided wizard. Role, rules, style, directive, constraints — we walk you through every field.",
    to: "/custom",
    color: "var(--accent)",
  },
  {
    step: "\uD83E\uDDE0",
    title: "Cognitive Studio",
    sub: "Adept",
    desc: "Pick from 87 research-backed cognitive frameworks. Each one is a structured reasoning template — not a generic prompt. Fill parameters, export to any LLM.",
    to: "/templates",
    color: "var(--accent)",
  },
  {
    step: "\uD83E\uDDEC",
    title: "Chain Composer",
    sub: "Architect",
    desc: "Compose multiple cognitive patterns into a single analysis pipeline. Our AI selects and orders the right frameworks for your question.",
    to: "/chains",
    color: "var(--accent)",
  },
];

const CAPABILITIES = [
  { label: "Cognitive Patterns", value: "87", detail: "research-backed reasoning frameworks" },
  { label: "Pattern Categories", value: "16", detail: "analysis, reasoning, creative, and more" },
  { label: "Export Formats", value: "8", detail: "Markdown, JSON, YAML, OpenAI, Anthropic, Google, LangChain, LlamaIndex" },
  { label: "Quality Metrics", value: "6", detail: "dimensions scored for every context you build" },
  { label: "Orchestrators", value: "7", detail: "LangChain, CrewAI, AutoGen, DSPy, and more" },
  { label: "Execution Tiers", value: "3", detail: "Static Generic / Dynamic Compiled / Full Response" },
];

const MILESTONES = [
  { id: "first_context", label: "Build your first context", link: "/custom", icon: "1" },
  { id: "try_pattern", label: "Try a cognitive pattern", link: "/templates", icon: "2" },
  { id: "compose_chain", label: "Compose a pattern chain", link: "/chains", icon: "3" },
  { id: "export_format", label: "Set API keys & license", link: "/account", icon: "4" },
];

export default function Dashboard() {
  const { user } = useAuth();
  const { isTourDone, startTour } = useTour();
  const active = useActiveProvider();
  const [templateCount, setTemplateCount] = useState(87);
  const [customCount, setCustomCount] = useState(0);
  const [milestones, setMilestones] = useState(() => {
    try { return JSON.parse(localStorage.getItem("mc_milestones") || "{}"); } catch { return {}; }
  });

  useEffect(() => {
    api.listTemplates().then(t => setTemplateCount(t.length)).catch(() => {});
    api.listCustomTemplates().then(t => setCustomCount(t.length)).catch(() => {});
  }, []);

  function toggleMilestone(id) {
    setMilestones(prev => {
      const next = { ...prev, [id]: !prev[id] };
      localStorage.setItem("mc_milestones", JSON.stringify(next));
      return next;
    });
  }

  const allDone = MILESTONES.every(m => milestones[m.id]);
  const displayName = user?.email?.split("@")[0] || "there";

  return (
    <div className="launchpad">
      <div className="lp-hero">
        <div className="lp-hero-text">
          <div className="page-header-styled">
            <span className="page-header-icon">{"\uD83C\uDFAF"}</span>
            <div>
              <h1>Welcome back, {displayName}</h1>
              <p className="page-header-sub">Your mission control for context engineering.</p>
            </div>
          </div>
          <blockquote className="page-epigraph">
            &ldquo;The right context turns a language model into a domain expert&rdquo;
            <cite>— Agentic Context Engineering, arxiv 2510.04618</cite>
          </blockquote>
          <p className="lp-hero-sub">
            You have {templateCount} cognitive patterns and {customCount} custom context{customCount !== 1 ? "s" : ""} ready to use.
          </p>
        </div>
        {!isTourDone() && (
          <button type="button" className="lp-tour-btn" onClick={startTour}>
            Take the guided tour
          </button>
        )}
      </div>

      <section className="lp-section">
        <h2>Your Journey</h2>
        <p className="lp-section-sub">Three levels of context engineering mastery. Start at the top, work your way down.</p>
        <div className="lp-journey">
          {JOURNEY.map(j => (
            <Link key={j.to} to={j.to} className="lp-journey-card">
              <div className="lp-journey-step">{j.step}</div>
              <div className="lp-journey-body">
                <h3>{j.title}</h3>
                <span className="lp-journey-tier">{j.sub}</span>
                <p>{j.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="lp-section">
        <h2>Platform at a Glance</h2>
        <div className="lp-stats">
          {CAPABILITIES.map(c => (
            <div key={c.label} className="lp-stat-card">
              <span className="lp-stat-value">{c.value}</span>
              <span className="lp-stat-label">{c.label}</span>
              <span className="lp-stat-detail">{c.detail}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="lp-section">
        <h2>Try Smart Execute</h2>
        <p className="lp-section-sub">
          Ask any question — Smart Execute automatically picks the right cognitive pattern, compiles your context, and runs it.
          The fastest way to experience what mycontext does.
        </p>
        <SmartExecutePanel
          provider={active.provider || "openai"}
          hasKey={active.hasKey}
          compact
        />
        {!active.hasKey && (
          <p className="lp-smart-hint">
            <Link to="/settings">Add an API key in Settings</Link> to try Smart Execute.
          </p>
        )}
      </section>

      {!allDone && (
        <section className="lp-section">
          <h2>Milestones</h2>
          <p className="lp-section-sub">Track your progress as you explore the platform.</p>
          <div className="lp-milestones">
            {MILESTONES.map(m => (
              <div key={m.id} className={`lp-milestone ${milestones[m.id] ? "done" : ""}`}>
                <button type="button" className="lp-milestone-check" onClick={() => toggleMilestone(m.id)}>
                  {milestones[m.id] ? "\u2713" : m.icon}
                </button>
                <Link to={m.link} className="lp-milestone-label">{m.label}</Link>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
