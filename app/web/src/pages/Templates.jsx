import { useState, useEffect, useCallback, useRef, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import * as api from "../api/client";
import Toast from "../components/Toast";
import MarkdownContent from "../components/MarkdownContent";
import { modelsForProvider, PROVIDERS } from "../config/models";
import useActiveProvider from "../hooks/useActiveProvider";
import "./Templates.css";

const FORMAT_LABELS = {
  markdown: "Markdown", json: "JSON", yaml: "YAML",
  openai: "OpenAI", anthropic: "Anthropic", google: "Google",
  langchain: "LangChain", llamaindex: "LlamaIndex",
};

const FORMAT_ORDER = ["markdown", "json", "yaml", "openai", "anthropic", "google", "langchain", "llamaindex"];

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
  const hasEnterprise = user?.enterprise_license === true;

  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [licenseFilter, setLicenseFilter] = useState("all");
  const [selected, setSelected] = useState(null);
  const [selectorOpen, setSelectorOpen] = useState(true);
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

  const [actionMode, setActionMode] = useState(null); // null | "generic" | "template"
  const [genericQuestion, setGenericQuestion] = useState("");
  const [genericLoading, setGenericLoading] = useState(false);
  const [genericResult, setGenericResult] = useState(null);

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
        primary,
        hasExamples: Object.keys(examples).length > 0,
        description: p.description,
        useCases: p.use_cases || [],
        useCasePrompts: p.use_case_prompts || {},
        paramDescriptions: p.parameter_descriptions || {},
        researchBasis: p.research_basis || "",
        theme: p.theme || "",
      });
    }).catch(() => setParams({}));
    setBuilt(null);
    setGenericResult(null);
    setGenericQuestion("");
    setActionMode(null);
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
    } catch (e) {
      setError(e.message);
    } finally {
      setGenericLoading(false);
    }
  }

  async function handleBuild() {
    if (!selected) return;
    setBuilding(true);
    setBuilt(null);
    try {
      const res = await api.buildTemplate(selected, params);
      setBuilt(res);
      setActiveTab("markdown");
    } catch (e) {
      setError(e.message);
    } finally {
      setBuilding(false);
    }
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
    if (typeof content === "object") {
      const pretty = JSON.stringify(content, null, 2);
      return pretty.replace(/\\n/g, "\n").replace(/\\t/g, "  ");
    }
    let str = String(content);
    return str.replace(/\\n/g, "\n").replace(/\\t/g, "  ");
  }

  function downloadFormat(format) {
    const content = getExportContent(format);
    if (!content) return;
    let ext = "txt";
    let mime = "text/plain";
    if (typeof built.exports[format] === "object" || ["openai", "anthropic", "google", "langchain", "llamaindex"].includes(format)) {
      ext = "json"; mime = "application/json";
    } else if (format === "yaml") { ext = "yaml"; }
    else if (format === "markdown") { ext = "md"; }
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `context_${selected}_${format}.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
    setToast(`Downloaded ${FORMAT_LABELS[format] || format}`);
  }

  async function copyFormat(format) {
    const content = getExportContent(format);
    if (!content) return;
    try {
      await navigator.clipboard.writeText(content);
      setToast(`Copied ${FORMAT_LABELS[format] || format}`);
    } catch {
      setToast("Copy failed");
    }
  }

  const themes = useMemo(() => {
    const set = new Set();
    templates.forEach((t) => { if (t.theme) set.add(t.theme); });
    return Array.from(set).sort();
  }, [templates]);

  const [themeFilter, setThemeFilter] = useState("all");

  const filtered = useMemo(() => {
    let list = templates;
    if (licenseFilter === "free") list = list.filter((t) => t.license !== "enterprise");
    else if (licenseFilter === "enterprise") list = list.filter((t) => t.license === "enterprise");
    if (themeFilter !== "all") list = list.filter((t) => t.theme === themeFilter);
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
  }, [templates, licenseFilter, themeFilter, search]);

  const selectedTpl = selected ? templates.find((t) => t.name === selected) : null;
  const isEnterpriseLocked = selectedTpl?.license === "enterprise" && !hasEnterprise;

  function handleSelectTemplate(name) {
    setSelected(name);
    setSelectorOpen(false);
    setTimeout(() => detailRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
  }

  return (
    <div className="templates-page">
      <div className="templates-header">
        <div className="page-header-styled">
          <span className="page-header-icon">{"\uD83E\uDDE0"}</span>
          <div>
            <h1>Cognitive Studio</h1>
            <p className="page-header-sub">85 research-backed cognitive frameworks. Master the patterns that amplify your AI.</p>
          </div>
        </div>
        <blockquote className="page-epigraph">
          &ldquo;Cognitive scaffolding improves LLM output by up to 66.7%&rdquo;
          <cite>— Cognitive Foundations for Reasoning, arxiv 2511.16660</cite>
        </blockquote>
        <div className="tpl-intro">
          <p>
            <strong>What is a Pattern?</strong> — A pattern is a ready-made thinking structure that tells the AI <em>how</em> to reason
            about your question. Instead of writing a long prompt yourself, you pick a pattern (e.g.&nbsp;"Root Cause Analyzer")
            and it adds the right analytical steps, evaluation criteria, and output structure automatically.
          </p>
          <p>
            <strong>How to use it:</strong> Filter by category below, pick a pattern, browse its use cases, then copy an example prompt
            or write your own. You have two generation options:
          </p>
          <ul className="tpl-intro-options">
            <li><strong>Generic Prompt</strong> — A pre-written, ready-to-paste prompt. Zero cost, works with any AI. Great for quick use.</li>
            <li><strong>Cognitive Context</strong> — A full structured context assembled from peer-reviewed cognitive research with your specific inputs. Exports to Markdown, JSON, YAML, and major AI platforms.</li>
          </ul>
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
        <>
          {/* ── Template Selector ───────────────────────── */}
          <div className="tpl-selector">
            <div className="tpl-selector-bar">
              <button
                type="button"
                className="tpl-selector-toggle"
                onClick={() => setSelectorOpen(!selectorOpen)}
              >
                {selected ? (
                  <span className="tpl-selector-chosen">
                    <span className="tpl-selector-chosen-name">{selected.replace(/_/g, " ")}</span>
                    {selectedTpl?.license === "enterprise" && <span className="tpl-badge-ent">Enterprise</span>}
                    <span className="tpl-selector-change">Change</span>
                  </span>
                ) : (
                  <span className="tpl-selector-placeholder">Select a cognitive pattern...</span>
                )}
                <span className="tpl-selector-chevron">{selectorOpen ? "\u25B2" : "\u25BC"}</span>
              </button>
            </div>

            {selectorOpen && (
              <div className="tpl-selector-panel fade-in">
                <div className="tpl-selector-filters">
                  <select
                    value={licenseFilter}
                    onChange={(e) => setLicenseFilter(e.target.value)}
                    className="tpl-filter-select"
                  >
                    <option value="all">All Templates (85)</option>
                    <option value="free">Free (16)</option>
                    <option value="enterprise">Enterprise (69)</option>
                  </select>
                  <select
                    value={themeFilter}
                    onChange={(e) => setThemeFilter(e.target.value)}
                    className="tpl-filter-select"
                  >
                    <option value="all">All Categories</option>
                    {themes.map((t) => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                  </select>
                  <input
                    type="text"
                    placeholder="Search by name, description, or use case..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="tpl-filter-search"
                  />
                </div>

                <div className="tpl-selector-count">{filtered.length} template{filtered.length !== 1 ? "s" : ""}</div>

                <div className="tpl-selector-list">
                  {filtered.map((t) => {
                    const locked = t.license === "enterprise" && !hasEnterprise;
                    return (
                      <button
                        key={t.name}
                        type="button"
                        className={`tpl-selector-item ${selected === t.name ? "active" : ""} ${locked ? "locked" : ""}`}
                        onClick={() => handleSelectTemplate(t.name)}
                      >
                        <div className="tpl-selector-item-top">
                          <span className="tpl-selector-item-name">{t.name.replace(/_/g, " ")}</span>
                          {t.license === "enterprise" && <span className="tpl-badge-ent">Enterprise</span>}
                          {locked && <span className="tpl-badge-lock">{"\uD83D\uDD12"}</span>}
                          {t.has_generic_prompt && <span className="tpl-badge-generic" title="Generic prompt available">{"\u26A1"}</span>}
                        </div>
                        <span className="tpl-selector-item-desc">{t.description || "Research-backed cognitive pattern"}</span>
                        {t.theme && <span className="tpl-selector-item-cat">{t.theme}</span>}
                      </button>
                    );
                  })}
                  {filtered.length === 0 && (
                    <p className="tpl-selector-empty">No templates match your filters.</p>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* ── Action Panel ────────────────────────────── */}
          {selected && (
            <div ref={detailRef} className="tpl-action-panel fade-in">
              <div className="tpl-action-header">
                <div>
                  <h2>{selected.replace(/_/g, " ")}</h2>
                  {selectedTpl?.license === "enterprise" && (
                    <span className="tpl-detail-category">Enterprise</span>
                  )}
                  {(paramMeta.theme || selectedTpl?.theme) && (
                    <span className="tpl-detail-theme">{paramMeta.theme || selectedTpl.theme}</span>
                  )}
                </div>
                <button type="button" className="tpl-action-close" onClick={() => { setSelected(null); setSelectorOpen(true); setActionMode(null); }} aria-label="Close">
                  &times;
                </button>
              </div>

              {/* ── About This Pattern (always visible) ── */}
              {(paramMeta.description || selectedTpl?.description) && (
                <div className="tpl-detail-about">
                  <h3>About This Pattern</h3>
                  <p>{paramMeta.description || selectedTpl?.description}</p>
                  {paramMeta.researchBasis && (
                    <p className="tpl-detail-research"><strong>Research Basis:</strong> {paramMeta.researchBasis}</p>
                  )}
                </div>
              )}

              {/* ── Use Cases & Example Prompts Table (always visible) ── */}
              {(() => {
                const useCases = paramMeta.useCases?.length ? paramMeta.useCases : selectedTpl?.use_cases || [];
                const prompts = Object.keys(paramMeta.useCasePrompts || {}).length
                  ? paramMeta.useCasePrompts
                  : selectedTpl?.use_case_prompts || {};
                if (!useCases.length) return null;
                return (
                  <div className="tpl-detail-usecases">
                    <h3>Industry Use Cases &amp; Example Prompts</h3>
                    <p className="tpl-usecase-hint">Copy any prompt below and paste it into the Generic Prompt or Cognitive Context panel.</p>
                    <div className="tpl-usecase-table-wrap">
                      <table className="tpl-usecase-table">
                        <thead>
                          <tr>
                            <th>Use Case</th>
                            <th>Example Prompt</th>
                            <th></th>
                          </tr>
                        </thead>
                        <tbody>
                          {useCases.map((uc, i) => {
                            const prompt = prompts[uc] || "";
                            return (
                              <tr key={i}>
                                <td className="tpl-uc-name">{uc}</td>
                                <td className="tpl-uc-prompt">{prompt || <span className="tpl-uc-na">—</span>}</td>
                                <td className="tpl-uc-action">
                                  {prompt && (
                                    <button
                                      type="button"
                                      className="tpl-uc-copy"
                                      title="Copy prompt"
                                      onClick={async () => {
                                        try {
                                          await navigator.clipboard.writeText(prompt);
                                          setToast("Copied to clipboard");
                                        } catch { setToast("Copy failed"); }
                                      }}
                                    >
                                      Copy
                                    </button>
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

              {isEnterpriseLocked && (
                <div className="tpl-locked-banner">
                  <span className="tpl-locked-icon">{"\uD83D\uDD12"}</span>
                  <div>
                    <strong>Enterprise License Required</strong>
                    <p>Upgrade to generate prompts and context from this pattern.</p>
                  </div>
                  <button
                    type="button"
                    className="tpl-unlock-btn"
                    onClick={() => navigate("/settings", { state: { tab: "License" } })}
                  >
                    Enter License Key
                  </button>
                </div>
              )}

              {!isEnterpriseLocked && (
                <>
                  {/* ── Context Create Options ─────────── */}
                  {!actionMode && (
                    <div className="tpl-action-choices">
                      <h3 className="tpl-action-choices-title">Context Create Options</h3>
                      <div className="tpl-action-cards">
                        {selectedTpl?.has_generic_prompt && (
                          <button
                            type="button"
                            className="tpl-action-card tpl-action-card--generic"
                            onClick={() => setActionMode("generic")}
                          >
                            <span className="tpl-action-card-icon">{"\u26A1"}</span>
                            <span className="tpl-action-card-title">Generate Generic Prompt</span>
                            <span className="tpl-action-card-sub">Pre-authored cognitive prompt — instant, zero LLM calls</span>
                            <span className="tpl-action-card-cost">0 cost</span>
                          </button>
                        )}
                        <button
                          type="button"
                          className="tpl-action-card tpl-action-card--template"
                          onClick={() => setActionMode("template")}
                        >
                          <span className="tpl-action-card-icon">{"\uD83E\uDDE0"}</span>
                          <span className="tpl-action-card-title">Generate Cognitive Context</span>
                          <span className="tpl-action-card-sub">Research-based cognitive context with your inputs, multi-format export</span>
                          <span className="tpl-action-card-cost">Research-driven</span>
                        </button>
                      </div>
                    </div>
                  )}

                  {/* ── Generic Prompt Mode ──────────────── */}
                  {actionMode === "generic" && (
                    <div className="tpl-generic-mode">
                      <button type="button" className="tpl-back-btn" onClick={() => { setActionMode(null); setGenericResult(null); }}>
                        &larr; Back to options
                      </button>
                      <h3>Generic Prompt</h3>
                      <p className="tpl-generic-info">
                        Enter your question and get a pre-authored cognitive prompt instantly — no LLM calls needed.
                      </p>
                      <div className="tpl-generic-form">
                        <textarea
                          value={genericQuestion}
                          onChange={(e) => setGenericQuestion(e.target.value)}
                          rows={3}
                          placeholder="e.g. Why did our conversion rate drop 25% this quarter?"
                          className="tpl-generic-input"
                        />
                        <button
                          type="button"
                          onClick={handleGenericPrompt}
                          disabled={genericLoading || !genericQuestion.trim()}
                          className="tpl-primary-btn"
                        >
                          {genericLoading ? "Generating..." : "Get Generic Prompt"}
                        </button>
                      </div>
                      {genericResult && (
                        <div className="tpl-generic-result">
                          <div className="tpl-result-header">
                            <h4>Generic Prompt</h4>
                            <div className="tpl-result-actions">
                              <span className="tpl-result-meta">{genericResult.chars} chars</span>
                              <button
                                type="button"
                                className="tpl-copy-btn"
                                onClick={async () => {
                                  try {
                                    await navigator.clipboard.writeText(genericResult.prompt);
                                    setToast("Copied to clipboard");
                                  } catch { setToast("Copy failed"); }
                                }}
                              >
                                Copy
                              </button>
                              <button
                                type="button"
                                className="tpl-download-btn"
                                onClick={() => {
                                  const blob = new Blob([genericResult.prompt], { type: "text/plain" });
                                  const url = URL.createObjectURL(blob);
                                  const a = document.createElement("a");
                                  a.href = url;
                                  a.download = `generic_prompt_${selected}.txt`;
                                  a.click();
                                  URL.revokeObjectURL(url);
                                  setToast("Downloaded");
                                }}
                              >
                                Download
                              </button>
                            </div>
                          </div>
                          <pre className="tpl-generic-preview">{genericResult.prompt}</pre>
                        </div>
                      )}
                    </div>
                  )}

                  {/* ── Cognitive Context Mode ────────────── */}
                  {actionMode === "template" && (
                    <div className="tpl-template-mode">
                      <button type="button" className="tpl-back-btn" onClick={() => { setActionMode(null); setBuilt(null); }}>
                        &larr; Back to options
                      </button>
                      <h3>Cognitive Context</h3>

                      <div className="tpl-template-controls">
                        {paramMeta.hasExamples && (
                          <button type="button" onClick={loadExample} className="tpl-example-btn">
                            Load example values
                          </button>
                        )}
                      </div>

                      <div className="tpl-template-form">
                        {Object.entries(params).map(([key, val]) => (
                          <div key={key} className="tpl-template-param">
                            <label>
                              <span className="tpl-param-label">{key}</span>
                              {paramMeta.paramDescriptions?.[key] && (
                                <span className="tpl-param-hint">{paramMeta.paramDescriptions[key]}</span>
                              )}
                            </label>
                            <textarea
                              value={toDisplayVal(val)}
                              onChange={(e) => setParams((p) => ({ ...p, [key]: fromDisplayVal(e.target.value, val) }))}
                              rows={key === "problem" || key === "text" || key === "input" || key === "symptoms" || key === "data" || key === "code" ? 4 : 2}
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
                            {modelsForProvider(userProvider).map((m) => (
                              <option key={m.id} value={m.id}>{m.label} ({m.tier})</option>
                            ))}
                          </select>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={handleBuild}
                        disabled={building}
                        className="tpl-primary-btn"
                      >
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
                              <button
                                key={fmt}
                                type="button"
                                className={`tpl-format-tab ${activeTab === fmt ? "active" : ""}`}
                                onClick={() => setActiveTab(fmt)}
                              >
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
                        </div>
                      )}
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </>
      )}
      {toast && <Toast message={toast} onClose={() => setToast("")} />}
    </div>
  );
}
