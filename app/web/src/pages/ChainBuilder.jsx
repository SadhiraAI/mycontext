import { useState, useEffect, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import * as api from "../api/client";
import Toast from "../components/Toast";
import { modelsForProvider, PROVIDERS } from "../config/models";
import useActiveProvider from "../hooks/useActiveProvider";
import "./ChainBuilder.css";

const MODE_INFO = {
  heuristic: {
    label: "Heuristic",
    badge: "Free",
    badgeClass: "",
    icon: "\u{1F50D}",
    title: "Heuristic Context Chaining",
    desc: "Keyword-based pattern matching across all 85 templates. Instant results, no API key required. Best for quick exploration when you want fast suggestions.",
    needsKey: false,
    apiMode: "quick",
  },
  smart: {
    label: "Smart",
    badge: "AI",
    badgeClass: "chain-tab-badge--llm",
    icon: "\u{1F9E0}",
    title: "Smart Chain Composer",
    desc: "Your LLM reasons through all 85 cognitive patterns, analyzes your question's complexity, domain, and structure, then selects the optimal chain with ordering and rationale.",
    needsKey: true,
    apiMode: "smart",
  },
  hybrid: {
    label: "Hybrid",
    badge: "Best",
    badgeClass: "chain-tab-badge--hybrid",
    icon: "\u26A1",
    title: "Hybrid Composer",
    desc: "Combines keyword-based heuristics with LLM reasoning for the most accurate pattern selection. Uses keyword hints to narrow candidates, then LLM picks the best chain.",
    needsKey: true,
    apiMode: "best",
  },
};

const EXAMPLES = [
  { text: "Why did customer churn spike last quarter?", icon: "\uD83D\uDCC9" },
  { text: "Compare AWS vs GCP for our data pipeline", icon: "\u2696\uFE0F" },
  { text: "Our app crashed in production — diagnose what went wrong", icon: "\uD83D\uDD25" },
  { text: "Design an onboarding flow for enterprise clients", icon: "\uD83C\uDFAF" },
  { text: "Evaluate build vs. buy for our auth system", icon: "\uD83D\uDEE0\uFE0F" },
];

export default function ChainBuilder() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const hasEnterprise = user?.enterprise_license === true;

  const [activeTab, setActiveTab] = useState("heuristic");
  const [question, setQuestion] = useState("");
  const active = useActiveProvider();
  const [provider, setProvider] = useState("openai");
  const [selectedModel, setSelectedModel] = useState("");
  const [hasKey, setHasKey] = useState(false);

  const [suggesting, setSuggesting] = useState(false);
  const [suggestError, setSuggestError] = useState("");
  const [result, setResult] = useState(null);

  const [integrating, setIntegrating] = useState(false);
  const [integratedResult, setIntegratedResult] = useState(null);
  const [integrateError, setIntegrateError] = useState("");

  const [toast, setToast] = useState("");
  const [editableChain, setEditableChain] = useState([]);
  const [showAddPicker, setShowAddPicker] = useState(false);
  const [allTemplates, setAllTemplates] = useState([]);
  const [addSearch, setAddSearch] = useState("");

  useEffect(() => {
    api.listKeys().then((keys) => {
      setHasKey(keys.some((k) => k.provider === provider));
    }).catch(() => setHasKey(false));
  }, [provider]);

  useEffect(() => {
    if (active.provider && !active.loading) {
      setProvider(active.provider);
      if (active.model) setSelectedModel(active.model);
    }
  }, [active.provider, active.model, active.loading]);

  useEffect(() => {
    api.listTemplates().then(setAllTemplates).catch(() => {});
  }, []);

  useEffect(() => {
    const ex = location.state?.example;
    if (ex?.targetPage === "chains" && ex?.chainQuestion) {
      setQuestion(ex.chainQuestion);
      setActiveTab("smart");
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state?.example, navigate, location.pathname]);

  function clearResults() {
    setResult(null);
    setIntegratedResult(null);
    setEditableChain([]);
    setSuggestError("");
    setIntegrateError("");
  }

  async function runCompose(q, tab) {
    const query = (q || question).trim();
    const mode = tab || activeTab;
    if (!query) return;
    const info = MODE_INFO[mode];
    if (info.needsKey && !hasKey) {
      setSuggestError(`${info.label} mode requires an API key. Add one in Settings, or try Heuristic mode (free).`);
      return;
    }
    setSuggesting(true);
    setSuggestError("");
    setResult(null);
    setIntegratedResult(null);
    setEditableChain([]);
    try {
      const opts = { mode: info.apiMode, include_enterprise: true };
      if (info.needsKey) opts.provider = provider;
      const res = await api.suggestChain(query, opts);
      setResult(res);
      const chain = res?.chain || [];
      setEditableChain(chain);
      if (chain.length === 0) {
        const backendReason = res?.reasoning || "";
        const isLLMError = /^(Error:|Invalid JSON:)/i.test(backendReason);
        if (isLLMError) {
          setSuggestError(`LLM error: ${backendReason}. Check that your API key is valid in Settings.`);
        } else if (mode === "heuristic") {
          setSuggestError("No keyword matches found. Try the Smart or Hybrid mode for AI-powered analysis, or add patterns manually below.");
        } else {
          setSuggestError("The AI returned an empty chain. Try rephrasing your question or check your API key in Settings.");
        }
      }
    } catch (e) {
      setSuggestError(e.message);
    } finally {
      setSuggesting(false);
    }
  }

  function handleCompose() {
    runCompose();
  }

  function handleExampleClick(text) {
    setQuestion(text);
    clearResults();
    runCompose(text, activeTab);
  }

  function removePattern(name) {
    setEditableChain((prev) => prev.filter((n) => n !== name));
    setIntegratedResult(null);
  }

  function addPattern(name) {
    if (editableChain.includes(name)) return;
    setEditableChain((prev) => [...prev, name]);
    setShowAddPicker(false);
    setAddSearch("");
    setIntegratedResult(null);
  }

  const allReasoning = useMemo(() => {
    return result?.selection_reasoning || {};
  }, [result]);

  const allCategories = useMemo(() => {
    const c = {};
    if (result?.pattern_categories) Object.assign(c, result.pattern_categories);
    allTemplates.forEach((t) => { if (t.category) c[t.name] = t.category; });
    return c;
  }, [result, allTemplates]);

  function hasEnterpriseInSelection() {
    return editableChain.some((t) => (allCategories[t] || "free") === "enterprise");
  }

  const filteredAddTemplates = useMemo(() => {
    const q = addSearch.toLowerCase();
    return allTemplates
      .filter((t) => !editableChain.includes(t.name))
      .filter((t) => !q || t.name.includes(q) || (t.description || "").toLowerCase().includes(q) || (t.theme || "").toLowerCase().includes(q));
  }, [allTemplates, editableChain, addSearch]);

  async function handleIntegrate() {
    if (!hasKey || editableChain.length < 2) return;
    setIntegrating(true);
    setIntegrateError("");
    setIntegratedResult(null);
    try {
      const res = await api.integrateTemplates(question, editableChain, allReasoning, provider);
      setIntegratedResult(res);
    } catch (e) {
      setIntegrateError(e.message);
    } finally {
      setIntegrating(false);
    }
  }

  function copyIntegrated() {
    if (!integratedResult?.integrated_template) return;
    navigator.clipboard.writeText(integratedResult.integrated_template).then(() => setToast("Copied"));
  }

  function downloadIntegrated() {
    if (!integratedResult?.integrated_template) return;
    const blob = new Blob([integratedResult.integrated_template], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "chain_prompt.md";
    a.click();
    URL.revokeObjectURL(url);
    setToast("Downloaded");
  }

  const modeInfo = MODE_INFO[activeTab];
  const canIntegrate = hasKey && editableChain.length >= 2;
  const blockedByEnterprise = !hasEnterprise && hasEnterpriseInSelection();
  const hasResultData = result?.chain != null;
  const isRunning = suggesting;
  const currentError = suggestError;

  return (
    <div className="chain-page">
      {/* ── Header ──────────────────────────────────── */}
      <div className="chain-header">
        <div className="page-header-styled">
          <span className="page-header-icon">{"\uD83E\uDDEC"}</span>
          <div>
            <h1>Chain Composer</h1>
            <p className="page-header-sub">Compose multi-pattern workflows and generate unified chain prompts.</p>
          </div>
        </div>
        <blockquote className="page-epigraph">
          &ldquo;Chaining cognitive patterns yields emergent reasoning that exceeds any single framework&rdquo;
          <cite>— Compositional Reasoning in LLMs, arxiv 2406.01574</cite>
        </blockquote>
      </div>

      {/* ── Intro ───────────────────────────────────── */}
      <div className="chain-intro">
        <p>
          <strong>What is Chain Composition?</strong> — Instead of using one pattern at a time, chain composition
          lets you combine multiple cognitive patterns into a single, unified workflow. The system analyzes your question,
          recommends the best sequence of patterns, and then <em>integrates</em> them into one powerful composite prompt.
        </p>
        <div className="chain-how-it-works">
          <h3>How It Works</h3>
          <ol className="chain-steps">
            <li><strong>Describe your problem</strong> — Enter any question or challenge below.</li>
            <li><strong>Choose a composition mode</strong> — Pick Heuristic (instant, free), Smart (AI-powered), or Hybrid (best of both).</li>
            <li><strong>Review &amp; edit the chain</strong> — The system suggests patterns; you can add, remove, or reorder them.</li>
            <li><strong>Generate integrated prompt</strong> — The Template Integrator merges all patterns into one unified prompt you can copy to any AI.</li>
          </ol>
        </div>
      </div>

      {/* ── Example prompts ───────────────────────── */}
      <div className="chain-examples">
        <span className="chain-examples-label">Try an example:</span>
        {EXAMPLES.map((ex) => (
          <button
            key={ex.text}
            type="button"
            className="chain-example-chip"
            onClick={() => handleExampleClick(ex.text)}
          >
            <span>{ex.icon}</span> {ex.text}
          </button>
        ))}
      </div>

      {/* ── Question Input ──────────────────────────── */}
      <div className="chain-input-section">
        <label className="chain-input-label">Your Question or Problem</label>
        <textarea
          placeholder="e.g. Why did customer churn spike 25% last quarter and what should we do about it?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          className="chain-textarea"
        />
      </div>

      {/* ── Mode Cards ──────────────────────────────── */}
      <div className="chain-modes-section">
        <h2 className="chain-section-title">Choose Composition Mode</h2>
        <div className="chain-mode-cards">
          {Object.entries(MODE_INFO).map(([key, info]) => (
            <button
              key={key}
              type="button"
              className={`chain-mode-card ${activeTab === key ? "active" : ""}`}
              onClick={() => { setActiveTab(key); clearResults(); }}
            >
              <div className="chain-mode-card-top">
                <span className="chain-mode-card-icon">{info.icon}</span>
                <span className={`chain-mode-card-badge ${info.badgeClass}`}>{info.badge}</span>
              </div>
              <span className="chain-mode-card-title">{info.title}</span>
              <span className="chain-mode-card-desc">{info.desc}</span>
              {info.needsKey && <span className="chain-mode-card-req">Requires API key</span>}
              {!info.needsKey && <span className="chain-mode-card-free">No API key needed</span>}
            </button>
          ))}
        </div>
      </div>

      {/* ── Active Mode Panel ───────────────────────── */}
      <div className="chain-active-panel">
        <div className="chain-active-header">
          <span className="chain-active-icon">{modeInfo.icon}</span>
          <h3>{modeInfo.title}</h3>
        </div>

        {modeInfo.needsKey && !hasKey && (
          <div className="chain-key-needed">
            <span className="chain-key-icon">{"\uD83D\uDD11"}</span>
            <div>
              <strong>API key required for {modeInfo.label} mode</strong>
              <p>Add an API key in <span className="chain-link" onClick={() => navigate("/settings")} role="button" tabIndex={0}>Settings</span> to use this mode.</p>
            </div>
          </div>
        )}

        {modeInfo.needsKey && hasKey && (
          <div className="chain-options">
            <div className="chain-option">
              <label>Provider</label>
              <select value={provider} onChange={(e) => { setProvider(e.target.value); setSelectedModel(""); }}>
                {PROVIDERS.map((p) => (<option key={p} value={p}>{p}</option>))}
              </select>
            </div>
            <div className="chain-option">
              <label>Model</label>
              <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                <option value="">Auto (default)</option>
                {modelsForProvider(provider).map((m) => (
                  <option key={m.id} value={m.id}>{m.label} ({m.tier})</option>
                ))}
              </select>
            </div>
          </div>
        )}

        <button
          type="button"
          onClick={handleCompose}
          disabled={isRunning || !question.trim() || (modeInfo.needsKey && !hasKey)}
          className="chain-btn"
        >
          {isRunning
            ? (activeTab === "heuristic" ? "Matching patterns\u2026" : "AI is composing chain (may take 15\u201330s)\u2026")
            : activeTab === "heuristic"
              ? "Suggest Patterns (Instant)"
              : `Compose Chain with ${modeInfo.label} AI`
          }
        </button>

        {isRunning && activeTab !== "heuristic" && (
          <p className="chain-loading-hint">The LLM is analyzing your question, reviewing all 85 patterns, and selecting the optimal chain. This can take 15\u201330 seconds.</p>
        )}

        {currentError && <p className="chain-error">{currentError}</p>}
      </div>

      {/* ── Results ──────────────────────────────────── */}
      {hasResultData && editableChain.length > 0 && (
        <div className="chain-result fade-in">
          <div className="chain-result-top">
            <h3>
              Your Workflow
              <span className="chain-result-count">{editableChain.length} pattern{editableChain.length !== 1 ? "s" : ""}</span>
            </h3>
            {hasEnterpriseInSelection() && (
              <span className="chain-ent-notice">
                {"\uD83D\uDD12"} Contains enterprise patterns
              </span>
            )}
          </div>

          {result?.reasoning && <p className="chain-reasoning">{result.reasoning}</p>}

          {activeTab === "heuristic" && editableChain.length < 3 && (
            <p className="chain-mode-hint">
              Keyword matching found {editableChain.length} pattern{editableChain.length !== 1 ? "s" : ""}. For richer results, try <strong>Smart</strong> or <strong>Hybrid</strong> mode, or add more patterns manually below.
            </p>
          )}

          {result?.question_analysis && activeTab === "smart" && (
            <details className="chain-analysis-details">
              <summary>Question Analysis</summary>
              <pre className="chain-analysis-pre">{typeof result.question_analysis === "string" ? result.question_analysis : JSON.stringify(result.question_analysis, null, 2)}</pre>
            </details>
          )}

          {/* Pipeline cards */}
          <div className="chain-pipeline">
            {editableChain.map((name, i) => {
              const cat = allCategories[name] || "free";
              const isFree = cat !== "enterprise";
              const reason = allReasoning[name];
              const tpl = allTemplates.find((t) => t.name === name);
              return (
                <div key={name} className={`chain-pipeline-card ${!isFree ? "chain-pipeline-card--enterprise" : ""}`}>
                  <div className="chain-pipeline-header">
                    <span className="chain-pipeline-num">{i + 1}</span>
                    <div className="chain-pipeline-info">
                      <span className="chain-pipeline-name">{name.replace(/_/g, " ")}</span>
                      {tpl?.description && <span className="chain-pipeline-desc">{tpl.description}</span>}
                    </div>
                    <span className={`chain-pipeline-badge ${isFree ? "chain-pipeline-badge--free" : "chain-pipeline-badge--ent"}`}>
                      {isFree ? "Free" : "Enterprise"}
                    </span>
                    <button className="chain-pipeline-remove" onClick={() => removePattern(name)} title="Remove">&times;</button>
                  </div>
                  {reason && <p className="chain-pipeline-reason">{reason}</p>}
                  {i < editableChain.length - 1 && <div className="chain-pipeline-arrow" />}
                </div>
              );
            })}
          </div>

          {/* Add pattern */}
          <div className="chain-add-section">
            {!showAddPicker ? (
              <button className="chain-btn chain-btn--add" onClick={() => setShowAddPicker(true)}>
                + Add Pattern
              </button>
            ) : (
              <div className="chain-add-picker">
                <div className="chain-add-picker-header">
                  <input
                    type="text"
                    className="chain-add-search"
                    placeholder="Search templates..."
                    value={addSearch}
                    onChange={(e) => setAddSearch(e.target.value)}
                    autoFocus
                  />
                  <button className="chain-add-close" onClick={() => { setShowAddPicker(false); setAddSearch(""); }}>&times;</button>
                </div>
                <div className="chain-add-list">
                  {filteredAddTemplates.length === 0 && (
                    <p className="chain-add-empty">No matching templates.</p>
                  )}
                  {filteredAddTemplates.slice(0, 20).map((t) => {
                    const isFree = (t.category || "free") !== "enterprise";
                    return (
                      <div key={t.name} className="chain-add-item" onClick={() => addPattern(t.name)} role="button" tabIndex={0}>
                        <div className="chain-add-item-info">
                          <span className="chain-add-item-name">{t.name.replace(/_/g, " ")}</span>
                          {t.description && <span className="chain-add-item-desc">{t.description}</span>}
                        </div>
                        <span className={`chain-pipeline-badge ${isFree ? "chain-pipeline-badge--free" : "chain-pipeline-badge--ent"}`}>
                          {isFree ? "Free" : "Enterprise"}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* ── Template Integrator ─────────────────── */}
          <div className="chain-integrate-section">
            <div className="chain-integrate-header">
              <span className="chain-integrate-icon">{"\uD83E\uDDE9"}</span>
              <div>
                <h4>Template Integrator</h4>
                <p className="chain-integrate-desc">
                  The integrator merges your {editableChain.length} selected patterns into a single, unified composite prompt.
                  It combines roles, rules, directives, and output requirements from each pattern into one cohesive cognitive framework
                  that you can copy and use with any AI.
                </p>
              </div>
            </div>

            {blockedByEnterprise && (
              <div className="chain-integrate-blocked">
                <span>{"\uD83D\uDD12"}</span>
                <div>
                  <strong>Enterprise license required</strong>
                  <p>Your chain includes enterprise patterns ({editableChain.filter((t) => (allCategories[t] || "free") === "enterprise").map((t) => t.replace(/_/g, " ")).join(", ")}).
                  The integrator cannot generate a composite prompt with enterprise templates without a license.</p>
                  <button type="button" className="chain-link-btn" onClick={() => navigate("/settings", { state: { tab: "License" } })}>
                    Enter License Key
                  </button>
                </div>
              </div>
            )}

            {!hasKey && !blockedByEnterprise && (
              <div className="chain-integrate-blocked chain-integrate-blocked--key">
                <span>{"\uD83D\uDD11"}</span>
                <div>
                  <strong>API key required</strong>
                  <p>The Template Integrator uses your LLM to intelligently merge patterns. Add an API key in <span className="chain-link" onClick={() => navigate("/settings")} role="button" tabIndex={0}>Settings</span>.</p>
                </div>
              </div>
            )}

            <button
              type="button"
              onClick={handleIntegrate}
              disabled={integrating || !canIntegrate || blockedByEnterprise}
              className="chain-btn chain-btn--integrate"
            >
              {integrating ? "Integrating patterns\u2026" : `Generate Integrated Prompt (${editableChain.length} patterns)`}
            </button>

            {integrateError && <p className="chain-error">{integrateError}</p>}

            {integratedResult?.integrated_template && (
              <div className="chain-integrated-output fade-in">
                <div className="chain-integrated-header">
                  <h4>Integrated Chain Prompt</h4>
                  <div className="chain-integrated-actions">
                    <button type="button" onClick={copyIntegrated} className="chain-copy-btn">Copy</button>
                    <button type="button" onClick={downloadIntegrated} className="chain-export-btn">Download</button>
                  </div>
                </div>

                {integratedResult.role && (
                  <div className="chain-integrated-meta">
                    <div className="chain-meta-item"><strong>Role:</strong> {integratedResult.role}</div>
                    {integratedResult.directive && <div className="chain-meta-item"><strong>Directive:</strong> {integratedResult.directive}</div>}
                  </div>
                )}

                <pre className="chain-integrated-content">{integratedResult.integrated_template}</pre>

                <div className="chain-integrated-footer">
                  <p className="chain-integrated-sources">
                    Built from: {integratedResult.source_templates?.map((t) => t.replace(/_/g, " ")).join(" \u2192 ")}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {(hasResultData || currentError) && editableChain.length === 0 && !isRunning && (
        <div className="chain-result fade-in">
          <h3>Build Your Workflow Manually</h3>
          <p className="chain-reasoning">
            Add cognitive patterns below to build your chain workflow.
          </p>
          {activeTab === "heuristic" && !currentError && (
            <p className="chain-mode-hint">
              Tip: The Heuristic mode uses keyword matching which can be limited. Switch to <strong>Smart</strong> or <strong>Hybrid</strong> mode for AI-powered pattern selection that understands context and nuance.
            </p>
          )}
          <div className="chain-add-section">
            {!showAddPicker ? (
              <button className="chain-btn chain-btn--add" onClick={() => setShowAddPicker(true)}>
                + Add Pattern Manually
              </button>
            ) : (
              <div className="chain-add-picker">
                <div className="chain-add-picker-header">
                  <input
                    type="text"
                    className="chain-add-search"
                    placeholder="Search templates..."
                    value={addSearch}
                    onChange={(e) => setAddSearch(e.target.value)}
                    autoFocus
                  />
                  <button className="chain-add-close" onClick={() => { setShowAddPicker(false); setAddSearch(""); }}>&times;</button>
                </div>
                <div className="chain-add-list">
                  {filteredAddTemplates.length === 0 && (
                    <p className="chain-add-empty">No matching templates.</p>
                  )}
                  {filteredAddTemplates.slice(0, 20).map((t) => {
                    const isFree = (t.category || "free") !== "enterprise";
                    return (
                      <div key={t.name} className="chain-add-item" onClick={() => addPattern(t.name)} role="button" tabIndex={0}>
                        <div className="chain-add-item-info">
                          <span className="chain-add-item-name">{t.name.replace(/_/g, " ")}</span>
                          {t.description && <span className="chain-add-item-desc">{t.description}</span>}
                        </div>
                        <span className={`chain-pipeline-badge ${isFree ? "chain-pipeline-badge--free" : "chain-pipeline-badge--ent"}`}>
                          {isFree ? "Free" : "Enterprise"}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {toast && <Toast message={toast} onClose={() => setToast("")} />}
    </div>
  );
}
