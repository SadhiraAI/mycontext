import { useState, useEffect, useCallback, useRef, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import * as api from "../api/client";
import Toast from "../components/Toast";
import MarkdownContent from "../components/MarkdownContent";
import QualityScore from "../components/QualityScore";
import CAIScoreCard from "../components/CAIScoreCard";
import { modelsForProvider, PROVIDERS } from "../config/models";
import useActiveProvider from "../hooks/useActiveProvider";
import "./Templates.css";

const FORMAT_LABELS = {
  markdown: "Markdown", json: "JSON", yaml: "YAML",
  openai: "OpenAI", anthropic: "Anthropic", google: "Google",
  langchain: "LangChain", llamaindex: "LlamaIndex",
};
const FORMAT_ORDER = ["markdown", "json", "yaml", "openai", "anthropic", "google", "langchain", "llamaindex"];

// Canonical category order for the sidebar
const CATEGORY_ORDER = [
  "Analysis", "Reasoning", "Creative", "Communication", "Planning",
  "Specialized", "Decision", "Problem Solving", "Diagnostic",
  "Synthesis", "Systems Thinking", "Temporal",
  "Metacognition", "Ethical Reasoning", "Learning", "Evaluation",
];

// Map API theme strings to sidebar labels
function themeToCategory(theme) {
  if (!theme) return "Specialized";
  const map = {
    "Data & Analytics": "Analysis",
    "Problem Investigation": "Reasoning",
    "Innovation & Creativity": "Creative",
    "Communication & Clarity": "Communication",
    "Project Management": "Planning",
    "Strategic Thinking": "Analysis",
    "Risk & Compliance": "Specialized",
    "Systems & Complexity": "Systems Thinking",
    "Evaluation & Quality": "Evaluation",
    "Self-Improvement": "Metacognition",
    "Ethics & Governance": "Ethical Reasoning",
    "Learning & Development": "Learning",
  };
  return map[theme] || theme;
}

// Map API license category to sidebar display category using pattern name heuristics
function patternToCategory(t) {
  // Use API category field if present, else derive from theme
  const cat = t.category || "";
  const catMap = {
    reasoning: "Reasoning", analysis: "Analysis", creative: "Creative",
    communication: "Communication", planning: "Planning", specialized: "Specialized",
    decision: "Decision", problem_solving: "Problem Solving", diagnostic: "Diagnostic",
    synthesis: "Synthesis", systems_thinking: "Systems Thinking", temporal: "Temporal",
    metacognition: "Metacognition", ethical_reasoning: "Ethical Reasoning",
    learning: "Learning", evaluation: "Evaluation",
  };
  if (catMap[cat]) return catMap[cat];
  return themeToCategory(t.theme);
}

function toDisplayVal(val) {
  if (Array.isArray(val)) return val.join("\n");
  if (typeof val === "object" && val !== null) return JSON.stringify(val, null, 2);
  return String(val ?? "");
}

function fromDisplayVal(str, original) {
  const s = str.trim();
  if (Array.isArray(original)) return s ? s.split("\n").map((x) => x.trim()).filter(Boolean) : [];
  if (typeof original === "object" && original !== null && !Array.isArray(original)) {
    try { return JSON.parse(s || "{}"); } catch { return original; }
  }
  return s;
}


export default function Templates() {
  const { user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [selected, setSelected] = useState(null);
  const [params, setParams] = useState({});
  const [paramMeta, setParamMeta] = useState({});
  const [building, setBuilding] = useState(false);
  const [built, setBuilt] = useState(null);
  const [activeTab, setActiveTab] = useState("markdown");
  const [toast, setToast] = useState("");
  const [hasKey, setHasKey] = useState(false);
  const active = useActiveProvider();
  const [userProvider, setUserProvider] = useState("openai");
  const [userModel, setUserModel] = useState("");
  const exampleParamsRef = useRef(null);
  const detailRef = useRef(null);

  // Which "tab" is shown in the action panel
  const [actionMode, setActionMode] = useState(null); // null | "generic" | "template"
  const [genericQuestion, setGenericQuestion] = useState("");
  const [genericLoading, setGenericLoading] = useState(false);
  const [genericResult, setGenericResult] = useState(null);

  // Post-build tools
  const [executeLoading, setExecuteLoading] = useState(false);
  const [executeResult, setExecuteResult] = useState(null);
  const [executeError, setExecuteError] = useState("");
  const [showQuality, setShowQuality] = useState(false);
  const [showCAI, setShowCAI] = useState(false);
  const [refineLoading, setRefineLoading] = useState(false);
  const [refineResult, setRefineResult] = useState(null);
  const [refineError, setRefineError] = useState("");


  useEffect(() => {
    api.listTemplates().then(setTemplates).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    api.listKeys().then((keys) => setHasKey(keys.length > 0)).catch(() => setHasKey(false));
  }, []);

  useEffect(() => {
    if (active.provider && !active.loading) {
      setUserProvider(active.provider);
      setHasKey(active.hasKey);
      if (active.model) setUserModel(active.model);
    }
  }, [active.provider, active.model, active.hasKey, active.loading]);

  useEffect(() => {
    const ex = location.state?.example;
    if (ex?.targetPage === "templates" && ex?.templateName && ex?.params) {
      exampleParamsRef.current = ex.params;
      setSelected(ex.templateName);
      setParams(ex.params);
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state?.example, navigate, location.pathname]);

  useEffect(() => {
    if (!selected) return;
    if (exampleParamsRef.current) {
      setParams(exampleParamsRef.current);
      exampleParamsRef.current = null;
      setParamMeta({ primary: "problem", hasExamples: false, description: null, useCases: [], paramDescriptions: {} });
      return;
    }
    api.getTemplateParams(selected).then((p) => {
      const primary = p.primary || "problem";
      const defaults = p.defaults || {};
      const examples = p.example_values || {};
      const initial = Object.keys(examples).length ? { ...defaults, ...examples } : { [primary]: "", ...defaults };
      setParams(initial);
      setParamMeta({
        primary, hasExamples: Object.keys(examples).length > 0,
        description: p.description, useCases: p.use_cases || [],
        useCasePrompts: p.use_case_prompts || {},
        paramDescriptions: p.parameter_descriptions || {},
        researchBasis: p.research_basis || "", theme: p.theme || "",
      });
    }).catch(() => setParams({}));
    setBuilt(null);
    setGenericResult(null);
    setGenericQuestion("");
    setActionMode(null);
    setExecuteResult(null);
    setRefineResult(null);
    setShowQuality(false);
    setShowCAI(false);
  }, [selected]);

  const loadExample = useCallback(() => {
    if (!selected) return;
    api.getTemplateParams(selected).then((p) => {
      const examples = p.example_values || {};
      if (Object.keys(examples).length) {
        setParams((prev) => ({ ...prev, ...examples }));
        setToast("Example values loaded");
      }
    });
  }, [selected]);

  async function handleGenericPrompt() {
    if (!selected || !genericQuestion.trim()) return;
    setGenericLoading(true);
    setGenericResult(null);
    try {
      const res = await api.getGenericPrompt(selected, genericQuestion.trim());
      setGenericResult(res);
    } catch (e) { setError(e.message); }
    finally { setGenericLoading(false); }
  }

  async function handleBuild() {
    if (!selected) return;
    setBuilding(true);
    setBuilt(null);
    setExecuteResult(null);
    setRefineResult(null);
    setShowQuality(false);
    setShowCAI(false);
    try {
      const res = await api.buildTemplate(selected, params);
      setBuilt(res);
      setActiveTab("markdown");
    } catch (e) { setError(e.message); }
    finally { setBuilding(false); }
  }

  async function handleExecute() {
    if (!built?.assembled) return;
    setExecuteLoading(true);
    setExecuteResult(null);
    setExecuteError("");
    try {
      const res = await api.executeContext(built.assembled, userProvider, "", null);
      setExecuteResult(res);
    } catch (e) { setExecuteError(e.message); }
    finally { setExecuteLoading(false); }
  }

  async function handleRefine() {
    if (!built?.assembled) return;
    setRefineLoading(true);
    setRefineResult(null);
    setRefineError("");
    try {
      const res = await api.copilotRefine(built.assembled, userProvider, userModel || null);
      setRefineResult(res);
    } catch (e) { setRefineError(e.message); }
    finally { setRefineLoading(false); }
  }



  function getExportContent(format) {
    if (!built?.exports?.[format]) return "";
    const content = built.exports[format];
    if (typeof content === "object") return JSON.stringify(content, null, 2);
    let str = String(content);
    if (format === "yaml" || format === "markdown") str = str.replace(/\\n/g, "\n");
    return str;
  }

  function getDisplayContent(format) {
    if (!built?.exports?.[format]) return "";
    const content = built.exports[format];
    if (typeof content === "object") return JSON.stringify(content, null, 2).replace(/\\n/g, "\n").replace(/\\t/g, "  ");
    let str = String(content);
    return str.replace(/\\n/g, "\n").replace(/\\t/g, "  ");
  }

  function downloadFormat(format) {
    const content = getExportContent(format);
    if (!content) return;
    let ext = "txt", mime = "text/plain";
    if (typeof built.exports[format] === "object" || ["openai", "anthropic", "google", "langchain", "llamaindex"].includes(format)) {
      ext = "json"; mime = "application/json";
    } else if (format === "yaml") { ext = "yaml"; }
    else if (format === "markdown") { ext = "md"; }
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url;
    a.download = `context_${selected}_${format}.${ext}`; a.click();
    URL.revokeObjectURL(url);
    setToast(`Downloaded ${FORMAT_LABELS[format] || format}`);
  }

  async function copyFormat(format) {
    const content = getExportContent(format);
    if (!content) return;
    try { await navigator.clipboard.writeText(content); setToast(`Copied ${FORMAT_LABELS[format] || format}`); }
    catch { setToast("Copy failed"); }
  }

  // Build category counts from the loaded templates
  const categoryCounts = useMemo(() => {
    const counts = {};
    templates.forEach((t) => {
      const cat = patternToCategory(t);
      counts[cat] = (counts[cat] || 0) + 1;
    });
    return counts;
  }, [templates]);

  const filtered = useMemo(() => {
    let list = templates;
    if (categoryFilter !== "all") list = list.filter((t) => patternToCategory(t) === categoryFilter);
    if (search) {
      const q = search.toLowerCase();
      list = list.filter((t) =>
        t.name.toLowerCase().includes(q) ||
        (t.description || "").toLowerCase().includes(q) ||
        (t.theme || "").toLowerCase().includes(q) ||
        (t.use_cases || []).some((u) => u.toLowerCase().includes(q))
      );
    }
    return list;
  }, [templates, categoryFilter, search]);

  const selectedTpl = selected ? templates.find((t) => t.name === selected) : null;

  function handleSelectTemplate(name) {
    setSelected(name);
    setTimeout(() => detailRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
  }

  return (
    <div className="templates-page">
      <div className="templates-header">
        <div className="page-header-styled">
          <span className="page-header-icon">{"\uD83E\uDDE0"}</span>
          <div>
            <h1>Cognitive Studio</h1>
            <p className="page-header-sub">88 research-backed cognitive frameworks. Master the patterns that amplify your AI.</p>
          </div>
        </div>
        <blockquote className="page-epigraph">
          &ldquo;Cognitive scaffolding improves LLM output by up to 66.7%&rdquo;
          <cite>— Cognitive Foundations for Reasoning, arxiv 2511.16660</cite>
        </blockquote>
        <div className="tpl-intro">
          <p>
            <strong>What is a Pattern?</strong> — A pattern is a ready-made thinking structure that tells the AI <em>how</em> to reason
            about your question. Pick a pattern, fill your inputs, and export to any LLM. To improve an existing prompt,
            use the <strong>Context Studio</strong>.
          </p>
        </div>
      </div>

      {error && (
        <p className="templates-error" role="alert">
          {error}
          <button type="button" onClick={() => { setError(""); setLoading(true); api.listTemplates().then(setTemplates).catch((e) => setError(e.message)).finally(() => setLoading(false)); }} className="templates-retry">Retry</button>
        </p>
      )}

      {loading ? (
        <div className="tpl-selector-loading">Loading templates...</div>
      ) : (
        <div className="tpl-layout">
          {/* ── Left: Category Sidebar ─────────────────── */}
          <aside className="tpl-sidebar">
            <div className="tpl-sidebar-search">
              <input
                type="text"
                placeholder="Search patterns..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="tpl-search-input"
              />
            </div>
            <nav className="tpl-category-nav">
              <button
                type="button"
                className={`tpl-cat-item ${categoryFilter === "all" ? "active" : ""}`}
                onClick={() => setCategoryFilter("all")}
              >
                <span className="tpl-cat-name">All Patterns</span>
                <span className="tpl-cat-count">{templates.length}</span>
              </button>
              {CATEGORY_ORDER.filter((cat) => categoryCounts[cat]).map((cat) => (
                <button
                  key={cat}
                  type="button"
                  className={`tpl-cat-item ${categoryFilter === cat ? "active" : ""}`}
                  onClick={() => setCategoryFilter(cat)}
                >
                  <span className="tpl-cat-name">{cat}</span>
                  <span className="tpl-cat-count">{categoryCounts[cat] || 0}</span>
                </button>
              ))}
            </nav>
          </aside>

          {/* ── Right: Card Grid + Detail ──────────────── */}
          <div className="tpl-main">
            <div className="tpl-grid-header">
              <span className="tpl-grid-count">
                {filtered.length} pattern{filtered.length !== 1 ? "s" : ""}
                {categoryFilter !== "all" ? ` in ${categoryFilter}` : ""}
              </span>
            </div>

            {filtered.length === 0 ? (
              <p className="tpl-selector-empty">No patterns match your filters.</p>
            ) : (
              <div className="tpl-card-grid">
                {filtered.map((t) => {
                  const isActive = selected === t.name;
                  return (
                    <button
                      key={t.name}
                      type="button"
                      className={`tpl-card ${isActive ? "active" : ""}`}
                      onClick={() => handleSelectTemplate(t.name)}
                    >
                      <div className="tpl-card-top">
                        <span className="tpl-card-name">{t.name.replace(/_/g, " ")}</span>
                        <div className="tpl-card-badges">
                          {t.has_generic_prompt && <span className="tpl-badge-generic" title="Generic prompt available">{"\u26A1"}</span>}
                        </div>
                      </div>
                      <span className="tpl-card-desc">{t.description || "Research-backed cognitive pattern"}</span>
                      <span className="tpl-card-cat">{patternToCategory(t)}</span>
                    </button>
                  );
                })}
              </div>
            )}

            {/* ── Detail Panel ──────────────────────────── */}
            {selected && (
              <div ref={detailRef} className="tpl-detail-panel fade-in">
                <div className="tpl-action-header">
                  <div>
                    <h2>{selected.replace(/_/g, " ")}</h2>
                    <div className="tpl-detail-pills">
                      {(paramMeta.theme || selectedTpl?.theme) && <span className="tpl-detail-theme">{paramMeta.theme || selectedTpl.theme}</span>}
                      <span className="tpl-detail-cat-pill">{patternToCategory(selectedTpl || {})}</span>
                    </div>
                  </div>
                  <button type="button" className="tpl-action-close" onClick={() => { setSelected(null); setActionMode(null); }} aria-label="Close">&times;</button>
                </div>

                {(paramMeta.description || selectedTpl?.description) && (
                  <div className="tpl-detail-about">
                    <h3>About This Pattern</h3>
                    <p>{paramMeta.description || selectedTpl?.description}</p>
                    {paramMeta.researchBasis && (
                      <p className="tpl-detail-research"><strong>Research Basis:</strong> {paramMeta.researchBasis}</p>
                    )}
                  </div>
                )}

                {(() => {
                  const useCases = paramMeta.useCases?.length ? paramMeta.useCases : selectedTpl?.use_cases || [];
                  const prompts = Object.keys(paramMeta.useCasePrompts || {}).length ? paramMeta.useCasePrompts : selectedTpl?.use_case_prompts || {};
                  if (!useCases.length) return null;
                  return (
                    <div className="tpl-detail-usecases">
                      <h3>Industry Use Cases &amp; Example Prompts</h3>
                      <p className="tpl-usecase-hint">Copy any prompt below and paste it into the Generic Prompt or Cognitive Context panel.</p>
                      <div className="tpl-usecase-table-wrap">
                        <table className="tpl-usecase-table">
                          <thead><tr><th>Use Case</th><th>Example Prompt</th><th></th></tr></thead>
                          <tbody>
                            {useCases.map((uc, i) => {
                              const prompt = prompts[uc] || "";
                              return (
                                <tr key={i}>
                                  <td className="tpl-uc-name">{uc}</td>
                                  <td className="tpl-uc-prompt">{prompt || <span className="tpl-uc-na">—</span>}</td>
                                  <td className="tpl-uc-action">
                                    {prompt && (
                                      <button type="button" className="tpl-uc-copy" onClick={async () => { try { await navigator.clipboard.writeText(prompt); setToast("Copied to clipboard"); } catch { setToast("Copy failed"); } }}>Copy</button>
                                    )}
                                  </td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  );
                })()}

                {(
                  <>
                    {/* ── Mode Tab Bar ──────────────────────── */}
                    <div className="tpl-mode-tabs">
                      {selectedTpl?.has_generic_prompt && (
                        <button type="button" className={`tpl-mode-tab ${actionMode === "generic" ? "active" : ""}`} onClick={() => setActionMode(actionMode === "generic" ? null : "generic")}>
                          ⚡ Generic Prompt
                        </button>
                      )}
                      <button type="button" className={`tpl-mode-tab ${actionMode === "template" ? "active" : ""}`} onClick={() => setActionMode(actionMode === "template" ? null : "template")}>
                        🧠 Cognitive Context
                      </button>
                    </div>

                    {/* ── Generic Prompt Mode ──────────────── */}
                    {actionMode === "generic" && (
                      <div className="tpl-mode-panel">
                        <p className="tpl-mode-info">Pre-authored cognitive prompt — instant, zero LLM calls.</p>
                        <div className="tpl-generic-form">
                          <textarea
                            value={genericQuestion}
                            onChange={(e) => setGenericQuestion(e.target.value)}
                            rows={3}
                            placeholder="e.g. Why did our conversion rate drop 25% this quarter?"
                            className="tpl-generic-input"
                          />
                          <button type="button" onClick={handleGenericPrompt} disabled={genericLoading || !genericQuestion.trim()} className="tpl-primary-btn">
                            {genericLoading ? "Generating..." : "Get Generic Prompt"}
                          </button>
                        </div>
                        {genericResult && (
                          <div className="tpl-generic-result">
                            <div className="tpl-result-header">
                              <h4>Generic Prompt</h4>
                              <div className="tpl-result-actions">
                                <span className="tpl-result-meta">{genericResult.chars} chars</span>
                                <button type="button" className="tpl-copy-btn" onClick={async () => { try { await navigator.clipboard.writeText(genericResult.prompt); setToast("Copied"); } catch { setToast("Copy failed"); } }}>Copy</button>
                                <button type="button" className="tpl-download-btn" onClick={() => { const blob = new Blob([genericResult.prompt], { type: "text/plain" }); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = `generic_${selected}.txt`; a.click(); URL.revokeObjectURL(url); setToast("Downloaded"); }}>Download</button>
                              </div>
                            </div>
                            <pre className="tpl-generic-preview">{genericResult.prompt}</pre>
                          </div>
                        )}
                      </div>
                    )}

                    {/* ── Cognitive Context Mode ────────────── */}
                    {actionMode === "template" && (
                      <div className="tpl-mode-panel">
                        <p className="tpl-mode-info">Research-based structured context with your inputs — exports to 8 formats.</p>
                        <div className="tpl-template-controls">
                          {paramMeta.hasExamples && (
                            <button type="button" onClick={loadExample} className="tpl-example-btn">Load example values</button>
                          )}
                        </div>
                        <div className="tpl-template-form">
                          {Object.entries(params).map(([key, val]) => (
                            <div key={key} className="tpl-template-param">
                              <label>
                                <span className="tpl-param-label">{key}</span>
                                {paramMeta.paramDescriptions?.[key] && <span className="tpl-param-hint">{paramMeta.paramDescriptions[key]}</span>}
                              </label>
                              <textarea
                                value={toDisplayVal(val)}
                                onChange={(e) => setParams((p) => ({ ...p, [key]: fromDisplayVal(e.target.value, val) }))}
                                rows={["problem", "text", "input", "symptoms", "data", "code", "situation"].includes(key) ? 4 : 2}
                                placeholder={`Enter ${key}...`}
                              />
                            </div>
                          ))}
                        </div>
                        <div className="tpl-template-llm">
                          <div className="tpl-template-llm-row">
                            <label>Provider</label>
                            <select value={userProvider} onChange={(e) => { setUserProvider(e.target.value); setUserModel(""); }}>
                              {PROVIDERS.map((p) => (<option key={p} value={p}>{p}</option>))}
                            </select>
                          </div>
                          <div className="tpl-template-llm-row">
                            <label>Model</label>
                            <select value={userModel} onChange={(e) => setUserModel(e.target.value)}>
                              <option value="">Auto (default)</option>
                              {modelsForProvider(userProvider).map((m) => (<option key={m.id} value={m.id}>{m.label} ({m.tier})</option>))}
                            </select>
                          </div>
                        </div>
                        <button type="button" onClick={handleBuild} disabled={building} className="tpl-primary-btn">
                          {building ? "Building..." : "Build Context"}
                        </button>

                        {built && (
                          <div className="tpl-template-output">
                            <div className="tpl-result-header">
                              <h4>Assembled Context</h4>
                              <div className="tpl-result-actions">
                                <button type="button" onClick={() => downloadFormat(activeTab)} className="tpl-download-btn">Download</button>
                                <button type="button" onClick={() => copyFormat(activeTab)} className="tpl-copy-btn">Copy</button>
                              </div>
                            </div>
                            <div className="tpl-format-tabs">
                              {FORMAT_ORDER.filter((f) => built.exports?.[f]).map((fmt) => (
                                <button key={fmt} type="button" className={`tpl-format-tab ${activeTab === fmt ? "active" : ""}`} onClick={() => setActiveTab(fmt)}>
                                  {FORMAT_LABELS[fmt]}
                                </button>
                              ))}
                            </div>
                            <div className="tpl-output-content">
                              {activeTab === "markdown" ? (
                                <MarkdownContent content={built.assembled || getExportContent("markdown")} />
                              ) : (
                                <pre>{getDisplayContent(activeTab)}</pre>
                              )}
                            </div>

                            {/* ── Post-Build Action Bar ──────────── */}
                            <div className="tpl-postbuild-bar">
                              <span className="tpl-postbuild-label">What next?</span>
                              <div className="tpl-postbuild-actions">
                                <button
                                  type="button"
                                  className={`tpl-postbuild-btn ${executeResult ? "active" : ""}`}
                                  onClick={handleExecute}
                                  disabled={executeLoading || !hasKey}
                                  title={!hasKey ? "Add an API key in Settings" : "Execute with your LLM"}
                                >
                                  {executeLoading ? "Running..." : "▶ Execute"}
                                </button>
                                <button
                                  type="button"
                                  className={`tpl-postbuild-btn ${showQuality ? "active" : ""}`}
                                  onClick={() => { setShowQuality(!showQuality); setShowCAI(false); }}
                                >
                                  📊 Quality Score
                                </button>
                                <button
                                  type="button"
                                  className={`tpl-postbuild-btn ${showCAI ? "active" : ""}`}
                                  onClick={() => { setShowCAI(!showCAI); setShowQuality(false); }}
                                  disabled={!hasKey}
                                  title={!hasKey ? "Add an API key in Settings" : "Measure Context Amplification Index"}
                                >
                                  📈 Measure CAI
                                </button>
                                <button
                                  type="button"
                                  className={`tpl-postbuild-btn ${refineResult ? "active" : ""}`}
                                  onClick={handleRefine}
                                  disabled={refineLoading || !hasKey}
                                  title={!hasKey ? "Add an API key in Settings" : "Quality-gated refinement"}
                                >
                                  {refineLoading ? "Refining..." : "🔁 Refine"}
                                </button>
                              </div>
                            </div>

                            {executeError && <p className="tpl-tool-error">{executeError}</p>}
                            {executeResult && (
                              <div className="tpl-execute-result fade-in">
                                <div className="tpl-result-header">
                                  <h4>LLM Response</h4>
                                  <button type="button" className="tpl-copy-btn" onClick={async () => { try { await navigator.clipboard.writeText(executeResult.response || ""); setToast("Copied"); } catch { setToast("Copy failed"); } }}>Copy</button>
                                </div>
                                <pre className="tpl-execute-output">{executeResult.response}</pre>
                              </div>
                            )}

                            {showQuality && (
                              <div className="tpl-tool-panel fade-in">
                                <h4>Quality Score</h4>
                                <QualityScore assembledContent={built.assembled} provider={userProvider} />
                              </div>
                            )}

                            {showCAI && (
                              <div className="tpl-tool-panel fade-in">
                                <h4>Context Amplification Index</h4>
                                <CAIScoreCard templateName={selected} hasKey={hasKey} provider={userProvider} />
                              </div>
                            )}

                            {refineError && <p className="tpl-tool-error">{refineError}</p>}
                            {refineResult && (
                              <div className="tpl-refine-result fade-in">
                                <div className="tpl-result-header">
                                  <h4>Refinement Result</h4>
                                  <span className="tpl-result-meta">
                                    {refineResult.before_score != null && refineResult.after_score != null
                                      ? `${Math.round(refineResult.before_score * 100)}% → ${Math.round(refineResult.after_score * 100)}%`
                                      : ""}
                                  </span>
                                </div>
                                {refineResult.message && <p className="tpl-refine-message">{refineResult.message}</p>}
                                {refineResult.after && (
                                  <>
                                    <h5>Improved Version</h5>
                                    <pre className="tpl-refine-output">{refineResult.after}</pre>
                                    <button type="button" className="tpl-copy-btn" onClick={async () => { try { await navigator.clipboard.writeText(refineResult.after); setToast("Copied refined prompt"); } catch { setToast("Copy failed"); } }}>Copy Improved</button>
                                  </>
                                )}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}

                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
      {toast && <Toast message={toast} onClose={() => setToast("")} />}
    </div>
  );
}
