import { useState, useEffect, useCallback, useRef } from "react";
import { Link } from "react-router-dom";
import * as api from "../api/client";
import Toast from "../components/Toast";
import QualityScore from "../components/QualityScore";
import MarkdownContent from "../components/MarkdownContent";
import CopilotPanel from "../components/CopilotPanel";
import { STARTER_TEMPLATES, THINKING_STRATEGIES } from "../data/starterTemplates";
import { modelsForProvider, defaultModelForProvider } from "../config/models";
import "./CustomTemplates.css";

/* ── Research references for the prompt flow ──────────── */

const RESEARCH_REFS = [
  { id: 1, short: "Lost in the Middle", authors: "Liu et al.", year: 2023, venue: "TACL 2024", finding: "LLMs recall best from prompt start & end (U-shaped curve). Role + Goal go first; Task goes last.", link: "https://arxiv.org/abs/2307.03172" },
  { id: 2, short: "Serial Position Effects", authors: "Wang et al.", year: 2025, venue: "EMNLP 2025", finding: "Primacy bias dominates — start-placed demos yield up to +6 accuracy points.", link: "https://arxiv.org/abs/2502.04134" },
  { id: 3, short: "Instruction Position Matters", authors: "Li et al.", year: 2023, venue: "Findings of ACL 2024", finding: "Post-instruction (task after context) improves following by +9.7 BLEU.", link: "https://arxiv.org/abs/2308.12097" },
  { id: 4, short: "PASTA", authors: "Zhang et al.", year: 2024, venue: "ICLR 2024", finding: "Emphasis markers (bold/caps) steer attention heads → +22% avg accuracy.", link: "https://arxiv.org/abs/2311.09247" },
  { id: 5, short: "GUIDE", authors: "Zhu et al.", year: 2024, venue: "ICLR 2024", finding: "Tagged emphasis improves instruction-following from 29.4% to 60.4%.", link: "https://arxiv.org/abs/2403.03120" },
  { id: 6, short: "CO-STAR Framework", authors: "GovTech Singapore", year: 2023, venue: "GPT-4 Competition Winner", finding: "Context → Objective → Style → Tone → Audience → Response.", link: null },
  { id: 7, short: "Hard-to-Easy Ordering", authors: "Zhang et al.", year: 2025, venue: "arXiv", finding: "Constraints ordered hard → easy improve compliance across model sizes.", link: "https://arxiv.org/abs/2502.17204" },
  { id: 8, short: "Structured Prompting", authors: "Zheng et al.", year: 2025, venue: "arXiv", finding: "Consistent section structure reduces output variance by ~4%.", link: "https://arxiv.org/abs/2511.20836" },
  { id: 9, short: "The Prompt Report", authors: "Schulhoff et al.", year: 2024, venue: "arXiv", finding: "Systematic survey of 58 prompting techniques — taxonomy & best practices.", link: "https://arxiv.org/abs/2406.06608" },
  { id: 10, short: "The Prompt Canvas", authors: "Hewing & Leinhos", year: 2024, venue: "arXiv", finding: "Unified practitioner framework: Persona → Audience → Context → Task → Output.", link: "https://arxiv.org/abs/2412.05127" },
];

const MEDIUM_ARTICLE_PLACEHOLDER = "https://medium.com/@mycontext/prompt-flow-research";

function ResearchBanner({ onOpen }) {
  return (
    <button type="button" className="ps-research-banner" onClick={onOpen}>
      <div className="ps-research-banner-left">
        <span className="ps-research-banner-badge">Backed by Science</span>
        <span className="ps-research-banner-title">Not just another prompt builder — there's real science behind every section</span>
      </div>
      <div className="ps-research-banner-right">
        <span className="ps-research-banner-stat">{RESEARCH_REFS.length} papers</span>
        <span className="ps-research-banner-cta">See the research →</span>
      </div>
    </button>
  );
}

function ResearchDrawer({ open, onClose }) {
  return (
    <>
      {open && <div className="ps-research-overlay" onClick={onClose} />}
      <div className={`ps-research-panel ${open ? "open" : ""}`}>
        <div className="ps-research-panel-inner">
          <div className="ps-research-header">
            <div>
              <h3>The Science of Prompt Ordering</h3>
              <p className="ps-research-tagline">Why your prompt's section order is its secret weapon</p>
            </div>
            <button type="button" onClick={onClose} className="ps-research-close">×</button>
          </div>

          <p className="ps-research-intro">
            Most prompt builders treat sections as interchangeable blocks. But research shows that <strong>where you place information changes accuracy by up to 76 points</strong> (Sclar et al., ICLR 2024).
            Context Studio uses a structure optimized for how LLMs actually read and process your instructions.
          </p>

          <div className="ps-research-flow">
            <div className="ps-research-zone"><span className="ps-rz-label primacy">Primacy Zone</span> <span className="ps-rz-sections">Role → Goal</span> <span className="ps-rz-why">Strongest recall</span></div>
            <div className="ps-research-zone"><span className="ps-rz-label early">Early</span> <span className="ps-rz-sections">Rules → Style</span> <span className="ps-rz-why">Best instruction compliance</span></div>
            <div className="ps-research-zone"><span className="ps-rz-label middle">Middle</span> <span className="ps-rz-sections">Examples</span> <span className="ps-rz-why">Demos stable here (+6 pts)</span></div>
            <div className="ps-research-zone"><span className="ps-rz-label late">Late</span> <span className="ps-rz-sections">Output Format → Guard Rails</span> <span className="ps-rz-why">Fresh before generating</span></div>
            <div className="ps-research-zone"><span className="ps-rz-label recency">Recency Zone</span> <span className="ps-rz-sections">Reasoning → Task</span> <span className="ps-rz-why">+9.7 BLEU improvement</span></div>
          </div>

          <div className="ps-research-article-cta">
            <a href={MEDIUM_ARTICLE_PLACEHOLDER} target="_blank" rel="noopener noreferrer" className="ps-research-article-link">
              Read the full deep dive on Medium →
            </a>
            <span className="ps-research-article-note">Examples, diagrams, and all the evidence in one place</span>
          </div>

          <h4>References ({RESEARCH_REFS.length})</h4>
          <ol className="ps-research-refs">
            {RESEARCH_REFS.map((r) => (
              <li key={r.id}>
                <div className="ps-ref-title">
                  {r.link ? <a href={r.link} target="_blank" rel="noopener noreferrer">{r.short}</a> : <span>{r.short}</span>}
                  <span className="ps-ref-meta"> — {r.authors} ({r.year}), {r.venue}</span>
                </div>
                <p className="ps-ref-finding">{r.finding}</p>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </>
  );
}

const FORMAT_LABELS = { markdown: "Markdown", json: "JSON", yaml: "YAML", openai: "OpenAI", anthropic: "Anthropic", google: "Google", langchain: "LangChain", llamaindex: "LlamaIndex" };
const FORMAT_ORDER = ["markdown", "json", "yaml", "openai", "anthropic", "google", "langchain", "llamaindex"];

// Aligned with The Prompt Guidebook 9-Section Architecture (docs/THE_PROMPT_GUIDEBOOK.md)
const WIZARD_STEPS = [
  { title: "Pick Your Adventure", short: "Adventure", guidebook: null },           // 0
  { title: "Give It a Name", short: "Name", guidebook: "② Goal" },                 // 1 — name, description, goal
  { title: "Who Should It Be?", short: "Who", guidebook: "① Role, ④ Style" },     // 2
  { title: "House Rules", short: "Rules", guidebook: "③ Rules" },                  // 3
  { title: "Teach It to Think", short: "Think", guidebook: "⑧.5 Reasoning, ⑤ Examples" }, // 4
  { title: "Shape the Answer", short: "Answer", guidebook: "⑦ Output Contract" }, // 5
  { title: "Guard Rails", short: "Guards", guidebook: "⑧ Guard Rails" },           // 6
  { title: "The Big Ask", short: "Ask", guidebook: "⑨ Task" },                     // 7
  { title: "Ship It!", short: "Ship!", guidebook: "Review all 9 sections" },       // 8
];

const SECTION_LABELS = {
  role: "① Role", goal: "② Goal", rules: "③ Rules", style: "④ Style",
  examples: "⑤ Examples", reasoning: "⑧.5 Reasoning",
  output_contract: "⑦ Output Contract", guard_rails: "⑧ Guard Rails", task: "⑨ Task",
};

const IMPROVE_PROVIDERS = ["openai", "anthropic", "google"];

const DEFAULT_GUIDANCE = { goal: "", role: "", rules: [], style: "" };
const DEFAULT_SCHEMA = [{ name: "topic", type: "text", default: "" }];
const OUTPUT_TYPES = ["str", "float", "int", "bool", "list"];

const ROLE_EXAMPLES = [
  { template: "SWOT Analyzer", value: "You are a senior strategic analyst and business consultant with Fortune 500 advisory experience." },
  { template: "Root Cause Analyzer", value: "You are a root cause analysis specialist and systems thinker with Six Sigma Black Belt certification." },
  { template: "Technical Translator", value: "You are an expert technical communicator specializing in translating complex systems into plain language for non-technical stakeholders." },
  { template: "Sentiment Analyzer", value: "You are a senior sentiment analysis specialist with 10 years of experience in NLP and product analytics." },
  { template: "Code Reviewer", value: "You are a senior software engineer and security-focused code reviewer with 15 years of experience across Python, JavaScript, and Go." },
];

const RULE_EXAMPLES = [
  { template: "SWOT", value: "Every weakness must be stated directly — never soften or omit a genuine vulnerability." },
  { template: "Root Cause", value: "Always distinguish symptoms from root causes — never list a symptom as a cause." },
  { template: "Root Cause", value: "Every claim must cite specific evidence from the input data." },
  { template: "Translator", value: "Every technical term must be replaced with a common-language equivalent." },
  { template: "Sentiment", value: "Always consider tone, intensity, hedging, sarcasm, and mixed signals before classifying." },
  { template: "Sentiment", value: "Output must be valid JSON — never include text outside the JSON object." },
  { template: "Code Review", value: "Every issue must be categorized by severity: critical, warning, or suggestion." },
  { template: "Code Review", value: "Every issue must include a concrete fix — never say 'consider improving' without showing how." },
];

const STYLE_EXAMPLES = [
  { template: "SWOT", value: "analytical, balanced, strategic" },
  { template: "Root Cause", value: "investigative, thorough, evidence-based" },
  { template: "Translator", value: "clear, accessible, respectful" },
  { template: "Sentiment", value: "consistent, concise, structured" },
  { template: "Code Review", value: "professional, constructive, specific" },
];

const RULE_PLACEHOLDERS = [
  "e.g. Every claim must cite a specific data point from the input.",
  "e.g. Output must be valid JSON — never include text outside the object.",
  "e.g. Never speculate — omit any claim not supported by the input data.",
  "e.g. Confidence scores must always be between 0.0 and 1.0.",
  "Add another rule...",
];

/* ── Helpers ────────────────────────────────────────────── */

function safeRules(rules) { return Array.isArray(rules) ? rules : []; }
function safeArray(arr) { return Array.isArray(arr) ? arr : []; }

function toDisplay(tpl) {
  return (tpl || "").replace(/\{\{\s*(\w+)\s*\}\}/g, "[$1]");
}

function fromDisplay(displayText, varNames) {
  let result = displayText;
  for (const n of varNames) {
    result = result.split("[" + n + "]").join("{{ " + n + " }}");
  }
  return result;
}

function getDisplayContent(raw) {
  if (typeof raw !== "string") return raw;
  try { return raw.replace(/\\n/g, "\n").replace(/\\t/g, "\t"); }
  catch { return raw; }
}

/* ── Small UI components ────────────────────────────────── */

function Tip({ children }) {
  return (
    <div className="ps-protip">
      <span className="ps-protip-icon">💡</span>
      <div><p>{children}</p></div>
    </div>
  );
}

function WalkthroughBox({ title, children, visible = true }) {
  if (!visible) return null;
  return (
    <div className="ps-walkthrough">
      <div className="ps-walkthrough-header">{title}</div>
      <div className="ps-walkthrough-body">{children}</div>
    </div>
  );
}

function ExamplesDrawer({ title, children }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="ps-examples-drawer">
      <button type="button" className="ps-examples-toggle" onClick={() => setOpen(!open)}>
        <span className="ps-examples-arrow">{open ? "▾" : "▸"}</span> {title}
      </button>
      {open && <div className="ps-examples-body">{children}</div>}
    </div>
  );
}

function DirectivePreview({ template, params }) {
  if (!template) return null;
  const parts = [];
  const regex = /\{\{\s*(\w+)\s*\}\}/g;
  let last = 0;
  let m;
  while ((m = regex.exec(template)) !== null) {
    if (m.index > last) parts.push({ type: "text", value: template.slice(last, m.index) });
    const varName = m[1];
    const val = params?.[varName];
    parts.push({ type: "var", name: varName, filled: !!val, value: val || varName });
    last = regex.lastIndex;
  }
  if (last < template.length) parts.push({ type: "text", value: template.slice(last) });
  if (parts.length === 0) return null;
  return (
    <div className="ps-directive-preview">
      {parts.map((p, i) =>
        p.type === "text" ? (
          <span key={i}>{p.value}</span>
        ) : (
          <span key={i} className={`ps-var-chip ${p.filled ? "filled" : ""}`}>
            {p.filled ? p.value : p.name}
          </span>
        )
      )}
    </div>
  );
}

function PreviewPanel({ builderBuilt, building, onRefresh }) {
  return (
    <div className="ps-preview-side">
      <div className="ps-preview-header">
        <h3>Live Preview</h3>
        <button type="button" onClick={onRefresh} disabled={building} className="ps-btn small primary">
          {building ? "Building..." : "See It Live"}
        </button>
      </div>
      <div className="ps-preview-content">
        {builderBuilt ? (
          <pre className="ps-prompt-text">{builderBuilt.assembled || ""}</pre>
        ) : (
          <p className="ps-preview-empty">Click <strong>See It Live</strong> to preview the complete prompt the AI will receive.</p>
        )}
      </div>
    </div>
  );
}

/* ── Main Component ─────────────────────────────────────── */

export default function CustomTemplates() {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [hasKey, setHasKey] = useState(false);

  const [wizardActive, setWizardActive] = useState(false);
  const [researchOpen, setResearchOpen] = useState(false);
  const [step, setStep] = useState(0);
  const [editing, setEditing] = useState(null);
  const [starterUsed, setStarterUsed] = useState(null);
  const [form, setForm] = useState({
    name: "", description: "",
    guidance: { ...DEFAULT_GUIDANCE },
    directive_template: "",
    input_schema: [...DEFAULT_SCHEMA],
    constraints: null,
    outputSchema: [],
    thinking_strategy: "direct",
    examples: [],
  });
  const [params, setParams] = useState({});
  const [building, setBuilding] = useState(false);
  const [builderBuilt, setBuilderBuilt] = useState(null);
  const [finalized, setFinalized] = useState(false);
  const [activeTab, setActiveTab] = useState("markdown");
  const [previewFmt, setPreviewFmt] = useState("markdown");
  const downloadRef = useRef(null);
  const directiveRef = useRef(null);

  const loadTemplates = useCallback(() => {
    api.listCustomTemplates().then(setTemplates).catch((e) => setError(e.message)).finally(() => setLoading(false));
  }, []);

  useEffect(() => { loadTemplates(); }, [loadTemplates]);
  useEffect(() => {
    api.listKeys().then((keys) => setHasKey(keys.length > 0)).catch(() => setHasKey(false));
  }, []);

  const varNames = (form.input_schema || []).map((f) => f.name).filter(Boolean);
  const showWalkthrough = starterUsed && starterUsed !== "blank";

  function resetWizard() {
    setWizardActive(false); setStep(0); setEditing(null); setStarterUsed(null);
    setForm({ name: "", description: "", guidance: { ...DEFAULT_GUIDANCE }, directive_template: "", input_schema: DEFAULT_SCHEMA.map((f) => ({ ...f })), constraints: null, outputSchema: [], thinking_strategy: "direct", examples: [] });
    setParams({}); setBuilderBuilt(null); setFinalized(false); setActiveTab("markdown"); setPreviewFmt("markdown");
  }

  function startFromStarter(starter) {
    setError("");
    setStarterUsed(starter.id);
    const schema = Array.isArray(starter.input_schema) ? starter.input_schema.map((f) => ({ ...f })) : DEFAULT_SCHEMA.map((f) => ({ ...f }));
    const c = starter.constraints && typeof starter.constraints === "object"
      ? { must_include: safeArray(starter.constraints.must_include).map(s => s), must_not_include: safeArray(starter.constraints.must_not_include).map(s => s), format_rules: safeArray(starter.constraints.format_rules).map(s => s) }
      : null;
    setForm({
      name: starter.id === "blank" ? "" : starter.name.toLowerCase().replace(/\s+/g, "_"),
      description: starter.description || "",
      guidance: { goal: starter.guidance?.goal ?? "", role: starter.guidance?.role ?? "", rules: safeRules(starter.guidance?.rules), style: starter.guidance?.style ?? "" },
      directive_template: starter.directive_template ?? "",
      input_schema: schema, constraints: c,
      outputSchema: safeArray(starter.output_schema).map((f) => ({ ...f })),
      thinking_strategy: starter.thinking_strategy || "direct",
      examples: safeArray(starter.examples).map((ex) => ({ ...ex })),
    });
    const p = {};
    schema.forEach((f) => { p[f.name] = f.default ?? ""; });
    setParams(p); setBuilderBuilt(null); setFinalized(false); setEditing("create"); setStep(1); setPreviewFmt("markdown");
  }

  function startEdit(t) {
    setError("");
    setStarterUsed(null);
    const g = t.guidance || {};
    setForm({
      name: t.name, description: t.description || "",
      guidance: { goal: g.goal || "", role: g.role || "", rules: safeRules(g.rules), style: g.style || "" },
      directive_template: t.directive_template || "",
      input_schema: t.input_schema?.length ? t.input_schema.map((f) => ({ ...f })) : DEFAULT_SCHEMA.map((f) => ({ ...f })),
      constraints: t.constraints || null,
      outputSchema: safeArray(t.output_schema).map((f) => ({ ...f })),
      thinking_strategy: t.thinking_strategy || "direct",
      examples: safeArray(t.examples).map((ex) => ({ ...ex })),
    });
    const p = {};
    (t.input_schema || []).forEach((f) => { p[f.name] = f.default ?? ""; });
    setParams(p); setBuilderBuilt(null); setFinalized(false); setEditing(t.id); setWizardActive(true); setStep(1); setPreviewFmt("markdown");
  }

  async function handleDelete(id) {
    if (!confirm("Delete this template?")) return;
    try { await api.deleteCustomTemplate(id); setToast("Template deleted"); loadTemplates(); }
    catch (e) { setError(e.message); }
  }

  async function handleBuildPreview() {
    setBuilding(true); setBuilderBuilt(null);
    try {
      const mc = getMergedConstraints();
      const hasConstraints = mc.must_include.length > 0 || mc.must_not_include.length > 0 || mc.format_rules.length > 0;
      const cleanSchema = safeArray(form.outputSchema).filter((f) => f.name);
      const def = {
        guidance: form.guidance,
        directive_template: form.directive_template,
        input_schema: form.input_schema,
        constraints: hasConstraints ? mc : null,
        thinking_strategy: form.thinking_strategy,
        examples: form.examples.filter((ex) => ex.input?.trim() && ex.output?.trim()),
        output_schema: cleanSchema.length > 0 ? cleanSchema : null,
      };
      const p = {};
      (form.input_schema || []).forEach((f) => { p[f.name] = params[f.name] ?? f.default ?? ""; });
      if (editing && editing !== "create") {
        setBuilderBuilt(await api.buildCustomTemplate(editing, p, "json"));
      } else {
        setBuilderBuilt(await api.buildCustomPreview(def, p, "json"));
      }
    } catch (e) { setError(e.message); }
    finally { setBuilding(false); }
  }

  async function handleFinalize() {
    const name = form.name?.trim();
    if (!name) { setError("Enter a template name."); return; }
    setError(""); setBuilding(true);
    try {
      const mc = getMergedConstraints();
      const hasConstraints = mc.must_include.length > 0 || mc.must_not_include.length > 0 || mc.format_rules.length > 0;
      const cleanExamples = form.examples.filter((ex) => ex.input?.trim() && ex.output?.trim());
      const cleanSchemaForSave = safeArray(form.outputSchema).filter((f) => f.name);
      const payload = {
        name, description: form.description || "",
        guidance: form.guidance || DEFAULT_GUIDANCE,
        directive_template: form.directive_template ?? "",
        input_schema: form.input_schema || DEFAULT_SCHEMA,
        constraints: hasConstraints ? mc : null,
        thinking_strategy: form.thinking_strategy || "direct",
        examples: cleanExamples.length > 0 ? cleanExamples : null,
        output_schema: cleanSchemaForSave.length > 0 ? cleanSchemaForSave : null,
      };
      const p = {};
      (form.input_schema || []).forEach((f) => { if (f && f.name) p[f.name] = params[f.name] ?? f.default ?? ""; });
      let builtResult = builderBuilt;
      if (!builtResult) {
        const cleanSchemaFin = safeArray(form.outputSchema).filter((f) => f.name);
        builtResult = await api.buildCustomPreview({
          guidance: payload.guidance, directive_template: payload.directive_template,
          input_schema: payload.input_schema, constraints: payload.constraints,
          thinking_strategy: payload.thinking_strategy, examples: payload.examples,
          output_schema: cleanSchemaFin.length > 0 ? cleanSchemaFin : null,
        }, p, "json");
        setBuilderBuilt(builtResult);
      }
      if (editing === "create") {
        const created = await api.createCustomTemplate(payload);
        const tid = created?.id != null ? String(created.id) : null;
        setEditing(tid);
        if (tid) { try { setBuilderBuilt(await api.buildCustomTemplate(tid, p, "json")); } catch (_) {} }
      } else {
        await api.updateCustomTemplate(editing, payload);
        try { setBuilderBuilt(await api.buildCustomTemplate(editing, p, "json")); } catch (_) {}
      }
      setFinalized(true); setToast("Template saved!"); loadTemplates();
      setTimeout(() => downloadRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" }), 150);
    } catch (e) { setError(e?.message || "Failed to save."); }
    finally { setBuilding(false); }
  }

  function downloadBuilderFormat(format) {
    if (!builderBuilt?.exports?.[format]) return;
    let content = builderBuilt.exports[format];
    let ext = "txt"; let mime = "text/plain";
    if (typeof content === "object") { content = JSON.stringify(content, null, 2); ext = "json"; mime = "application/json"; }
    else if (format === "yaml") ext = "yaml";
    else if (format === "markdown") ext = "md";
    else if (["openai","anthropic","google","langchain","llamaindex"].includes(format)) ext = "json";
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url;
    a.download = `${(form.name || "template").replace(/\s+/g, "_")}_${format}.${ext}`;
    a.click(); URL.revokeObjectURL(url);
    setToast(`Downloaded ${FORMAT_LABELS[format] || format}`);
  }

  function copyBuilderFormat(format) {
    if (!builderBuilt?.exports?.[format]) return;
    let content = builderBuilt.exports[format];
    if (typeof content === "object") content = JSON.stringify(content, null, 2);
    navigator.clipboard.writeText(content).then(() => setToast(`Copied ${FORMAT_LABELS[format] || format}`));
  }

  function addSchemaField() {
    const newName = `param_${form.input_schema.length + 1}`;
    setForm((f) => ({ ...f, input_schema: [...f.input_schema, { name: newName, type: "text", default: "" }] }));
    setParams((p) => ({ ...p, [newName]: "" }));
  }
  function removeSchemaField(idx) { setForm((f) => ({ ...f, input_schema: f.input_schema.filter((_, i) => i !== idx) })); }
  function updateSchemaField(idx, field) { setForm((f) => ({ ...f, input_schema: f.input_schema.map((x, i) => (i === idx ? { ...x, ...field } : x)) })); }

  function addRule() { setForm((f) => ({ ...f, guidance: { ...f.guidance, rules: [...safeRules(f.guidance?.rules), ""] } })); }
  function removeRule(idx) { setForm((f) => ({ ...f, guidance: { ...f.guidance, rules: safeRules(f.guidance?.rules).filter((_, i) => i !== idx) } })); }
  function updateRule(idx, value) { setForm((f) => ({ ...f, guidance: { ...f.guidance, rules: safeRules(f.guidance?.rules).map((r, i) => (i === idx ? value : r)) } })); }

  function addConstraintItem(field) { setForm((f) => ({ ...f, constraints: { ...(f.constraints || {}), [field]: [...safeArray(f.constraints?.[field]), ""] } })); }
  function removeConstraintItem(field, idx) { setForm((f) => ({ ...f, constraints: { ...(f.constraints || {}), [field]: safeArray(f.constraints?.[field]).filter((_, i) => i !== idx) } })); }
  function updateConstraintItem(field, idx, value) { setForm((f) => ({ ...f, constraints: { ...(f.constraints || {}), [field]: safeArray(f.constraints?.[field]).map((v, i) => (i === idx ? value : v)) } })); }

  function addOutputField() { setForm((f) => ({ ...f, outputSchema: [...safeArray(f.outputSchema), { name: "", type: "str" }] })); }
  function removeOutputField(idx) { setForm((f) => ({ ...f, outputSchema: safeArray(f.outputSchema).filter((_, i) => i !== idx) })); }
  function updateOutputField(idx, field) { setForm((f) => ({ ...f, outputSchema: safeArray(f.outputSchema).map((x, i) => (i === idx ? { ...x, ...field } : x)) })); }

  function addExample() { setForm((f) => ({ ...f, examples: [...safeArray(f.examples), { input: "", output: "" }] })); }
  function removeExample(idx) { setForm((f) => ({ ...f, examples: safeArray(f.examples).filter((_, i) => i !== idx) })); }
  function updateExample(idx, field, value) { setForm((f) => ({ ...f, examples: safeArray(f.examples).map((ex, i) => (i === idx ? { ...ex, [field]: value } : ex)) })); }

  function getMergedConstraints() {
    const base = form.constraints || {};
    return {
      must_include: safeArray(base.must_include).filter(Boolean),
      must_not_include: safeArray(base.must_not_include).filter(Boolean),
      format_rules: safeArray(base.format_rules).filter(Boolean),
    };
  }

  const FIELD_TO_WIZARD_STEP = {
    name: 1, description: 1, goal: 1,
    role: 2, style: 2,
    rules: 3,
    thinking_strategy: 4, examples: 4,
    output_schema: 5,
    constraints_must_include: 6, constraints_must_not_include: 6, constraints_format_rules: 6,
    variables: 7, directive: 7,
  };

  function handleCopilotSuggestion(suggestion) {
    const { field, action, value } = suggestion;

    if (!editing) {
      setEditing("create");
      setWizardActive(true);
    }

    if (field === "name") {
      setForm(f => ({ ...f, name: String(value).trim() }));
    } else if (field === "description") {
      setForm(f => ({ ...f, description: String(value).trim() }));
    } else if (field === "goal") {
      setForm(f => ({ ...f, guidance: { ...f.guidance, goal: value } }));
    } else if (field === "role") {
      setForm(f => ({ ...f, guidance: { ...f.guidance, role: value } }));
    } else if (field === "rules") {
      const items = Array.isArray(value) ? value : [value];
      setForm(f => {
        const existing = safeRules(f.guidance?.rules).filter(Boolean);
        const merged = [...existing, ...items.filter(r => !existing.includes(r))];
        return { ...f, guidance: { ...f.guidance, rules: merged } };
      });
    } else if (field === "style") {
      setForm(f => ({ ...f, guidance: { ...f.guidance, style: value } }));
    } else if (field === "thinking_strategy") {
      const valid = THINKING_STRATEGIES.find(s => s.id === value);
      if (valid) setForm(f => ({ ...f, thinking_strategy: value }));
    } else if (field === "examples") {
      let items = Array.isArray(value) ? value : [];
      if (typeof value === "string") {
        try { items = JSON.parse(value); } catch (_) { items = []; }
      }
      const exs = items.filter(item => item && typeof item === "object" && item.input && item.output);
      if (exs.length > 0) {
        setForm(f => ({ ...f, examples: [...safeArray(f.examples), ...exs] }));
      }
    } else if (field === "variables") {
      let vars = Array.isArray(value) ? value : typeof value === "string" ? value.split(",").map(s => s.trim()).filter(Boolean) : [value];
      vars = vars.map(v => String(v).replace(/[^a-zA-Z0-9_]/g, "").trim()).filter(Boolean);
      setForm(f => {
        const schema = vars.map(v => ({ name: v, type: "text", default: "" }));
        return { ...f, input_schema: schema };
      });
      setParams(p => {
        const newP = { ...p };
        vars.forEach(v => { if (!(v in newP)) newP[v] = ""; });
        return newP;
      });
    } else if (field === "directive") {
      setForm(f => ({ ...f, directive_template: value }));
    } else if (field === "output_schema") {
      let items = Array.isArray(value) ? value : [];
      if (typeof value === "string") {
        try { items = JSON.parse(value); } catch (_) { items = []; }
      }
      const schema = items
        .filter(item => item && typeof item === "object" && item.name)
        .map(item => ({ name: item.name, type: OUTPUT_TYPES.includes(item.type) ? item.type : "str" }));
      if (schema.length > 0) {
        setForm(f => ({ ...f, outputSchema: schema }));
      }
    } else if (field === "constraints_must_include" || field === "constraints_must_not_include" || field === "constraints_format_rules") {
      const subField = field.replace("constraints_", "");
      let items = Array.isArray(value) ? value : typeof value === "string" ? value.split(",").map(s => s.trim()).filter(Boolean) : [value];
      items = items.map(s => String(s).replace(/^["'\s]+|["'\s]+$/g, "")).filter(s => s.length > 0 && s.length < 200);
      setForm(f => {
        const existing = safeArray(f.constraints?.[subField]).filter(Boolean);
        const merged = [...new Set([...existing, ...items])];
        return { ...f, constraints: { ...(f.constraints || {}), [subField]: merged } };
      });
    }

    const targetStep = FIELD_TO_WIZARD_STEP[field];
    if (targetStep !== undefined) {
      setStep(prev => Math.max(prev, targetStep));
    }

    const label = (field || "").replace(/_/g, " ").replace("constraints ", "");
    setToast("Applied " + label);
  }

  function insertVariable(varName) {
    const ta = directiveRef.current;
    const token = "[" + varName + "]";
    if (ta) {
      const display = toDisplay(form.directive_template);
      const start = ta.selectionStart ?? display.length;
      const end = ta.selectionEnd ?? start;
      const newDisplay = display.slice(0, start) + token + display.slice(end);
      setForm((f) => ({ ...f, directive_template: fromDisplay(newDisplay, [...varNames, varName]) }));
      setTimeout(() => { ta.focus(); ta.selectionStart = ta.selectionEnd = start + token.length; }, 0);
    } else {
      const display = toDisplay(form.directive_template) + " " + token;
      setForm((f) => ({ ...f, directive_template: fromDisplay(display, [...varNames, varName]) }));
    }
  }

  function handleDirectiveDisplayChange(displayText) {
    setForm((f) => ({ ...f, directive_template: fromDisplay(displayText, varNames) }));
  }

  function canProceed() {
    if (step === 1) return form.name?.trim();
    if (step === 2) return form.guidance?.role?.trim();
    return true;
  }

  const directiveDisplay = toDisplay(form.directive_template);
  const selectedStrategy = THINKING_STRATEGIES.find(s => s.id === form.thinking_strategy) || THINKING_STRATEGIES[0];

  // When in fullscreen step mode (step > 0) the copilot becomes a FAB
  const [copilotOpen, setCopilotOpen] = useState(false);
  const [copilotMode, setCopilotMode] = useState(false);

  const [improverOpen, setImproverOpen] = useState(false);
  const [improveInput, setImproveInput] = useState("");
  const [parseResult, setParseResult] = useState(null);
  const [parseLoading, setParseLoading] = useState(false);
  const [improveResult, setImproveResult] = useState(null);
  const [improveLoading, setImproveLoading] = useState(false);
  const [improveError, setImproveError] = useState("");
  const [improveProvider, setImproveProvider] = useState("openai");
  const [improveModel, setImproveModel] = useState(""); // empty = Auto (gpt-4o-mini or provider default)

  async function handleParsePrompt() {
    if (!improveInput.trim()) return;
    setParseLoading(true);
    setParseResult(null);
    setImproveResult(null);
    setImproveError("");
    try {
      const res = await api.parsePrompt(improveInput.trim());
      setParseResult(res);
    } catch (e) { setImproveError(e.message); }
    finally { setParseLoading(false); }
  }

  async function handleImprovePrompt() {
    if (!improveInput.trim()) return;
    setImproveLoading(true);
    setImproveResult(null);
    setImproveError("");
    try {
      const res = await api.improvePrompt(improveInput.trim(), improveProvider, improveModel || null);
      setImproveResult(res);
    } catch (e) { setImproveError(e.message); }
    finally { setImproveLoading(false); }
  }

  // ── Render ──────────────────────────────────────────────
  return (
    <div className={`ps-page ${wizardActive && step > 0 ? "ps-page--fullscreen-step" : ""} ${wizardActive && step > 0 && copilotMode ? "ps-page--copilot-active" : ""}`}>
      <div className="ps-page-header">
        <div>
          <div className="page-header-styled">
            <span className="page-header-icon">{"\uD83D\uDCBB"}</span>
            <div>
              <h1>Context Studio</h1>
              <p className="page-header-sub">Build structured AI contexts from scratch. Your first step into context engineering.</p>
            </div>
          </div>
          <blockquote className="page-epigraph">
            &ldquo;Context is the difference between a language model and an intelligent assistant&rdquo;
            <cite>— Agentic Context Engineering, arxiv 2510.04618</cite>
          </blockquote>
          <p className="ps-intro">
            Build your first AI context from scratch — role, goal, rules, examples, constraints, and more.
            Every prompt follows a <strong>research-backed structure</strong> proven to improve LLM performance.
            No prompt engineering experience needed — we walk you through every step.
          </p>
        </div>
        {!wizardActive && (
          <button type="button" onClick={() => { resetWizard(); setWizardActive(true); }} className="ps-btn primary">
            + Create New Prompt
          </button>
        )}
      </div>

      <ResearchBanner onOpen={() => setResearchOpen(true)} />
      <ResearchDrawer open={researchOpen} onClose={() => setResearchOpen(false)} />

      {error && <p className="ps-error">{error}</p>}

      {wizardActive && step === 0 && (
        <div className="ps-adventure-splash fade-in">
          <div className="ps-progress ps-progress-9">
            {WIZARD_STEPS.map((ws, i) => (
              <div key={i} className={`ps-progress-step ${i === step ? "active" : ""} ${i < step ? "done" : ""}`} onClick={() => { if (i < step) setStep(i); }}>
                <span className="ps-step-num">{i < step ? "✓" : i + 1}</span>
                <span className="ps-step-label">{ws.short}</span>
              </div>
            ))}
          </div>

          <div className="ps-splash-hero">
            <h2>Pick Your Adventure</h2>
            <p className="ps-splash-subtitle">Two ways to build your prompt. Pick the one that fits you.</p>
          </div>

          <div className="ps-three-paths">
            {/* ── Manual Path ── */}
            <button
              type="button"
              className="ps-path-card ps-path-manual"
              onClick={() => { setCopilotMode(false); setCopilotOpen(false); startFromStarter(STARTER_TEMPLATES.find(s => s.id === "blank")); }}
            >
              <div className="ps-path-rec">Recommended</div>
              <div className="ps-path-icon">{"\uD83D\uDEE3\uFE0F"}</div>
              <h3>Take the Wheel</h3>
              <p className="ps-path-tagline">You drive. We navigate.</p>
              <p className="ps-path-desc">
                Walk through each step yourself — role, rules, thinking strategy, examples, guardrails, and the final task.
                You'll <strong>understand every nuance</strong> of what makes a great prompt.
              </p>
              <div className="ps-path-steps">
                <span>Name it</span>
                <span className="ps-path-chevron">{"\u203A"}</span>
                <span>Set the role</span>
                <span className="ps-path-chevron">{"\u203A"}</span>
                <span>Add rules</span>
                <span className="ps-path-chevron">{"\u203A"}</span>
                <span>Teach it to think</span>
                <span className="ps-path-chevron">{"\u203A"}</span>
                <span>Ship it!</span>
              </div>
              <p className="ps-path-why">Best if you want to learn prompt engineering while building.</p>
              <span className="ps-path-cta">Start building {"\u2192"}</span>
            </button>

            {/* ── AI-Driven Path ── */}
            <button
              type="button"
              className="ps-path-card ps-path-ai"
              onClick={() => { setCopilotMode(true); setCopilotOpen(true); startFromStarter(STARTER_TEMPLATES.find(s => s.id === "blank")); }}
            >
              <div className="ps-path-icon">{"\uD83E\uDD16"}</div>
              <h3>Let AI Drive</h3>
              <p className="ps-path-tagline">Tell the Copilot what you need. It builds the prompt for you.</p>
              <p className="ps-path-desc">
                Just describe your goal in plain English. The <strong>Context Copilot</strong> will suggest the role,
                rules, thinking strategy, examples, and constraints — one step at a time.
                You approve, tweak, or skip.
              </p>
              <div className="ps-path-road">
                <span className="ps-path-road-label">You say what you want</span>
                <div className="ps-path-road-arrow">{"\u2192"}</div>
                <span className="ps-path-road-label">Copilot frames it</span>
                <div className="ps-path-road-arrow">{"\u2192"}</div>
                <span className="ps-path-road-label">You approve & ship</span>
              </div>
              <div className="ps-path-key-notice">
                <span className="ps-path-key-icon">{"\uD83D\uDD11"}</span>
                <span>
                  The Copilot needs an AI provider key to work.{" "}
                  <Link to="/settings" className="ps-path-key-link" onClick={(e) => e.stopPropagation()}>
                    Add your key in Settings
                  </Link>{" "}
                  (OpenAI, Anthropic, or Google — pick any one).
                </span>
              </div>
              <p className="ps-path-why">Best if you want fast results or aren't sure where to start.</p>
              <span className="ps-path-cta ps-path-cta-ai">Let Copilot guide me {"\u2192"}</span>
            </button>

            {/* ── Pit Stop: Improve Existing Prompt ── */}
            <button
              type="button"
              className="ps-path-card ps-path-improve"
              onClick={() => setImproverOpen(true)}
            >
              <div className="ps-path-icon">{"\uD83D\uDD27"}</div>
              <h3>Pit Stop</h3>
              <p className="ps-path-tagline">Already have a prompt? Tune it up.</p>
              <p className="ps-path-desc">
                Paste any existing prompt — we'll <strong>X-ray it</strong> against the 9-Section Architecture,
                show what's missing, and rewrite it with AI. Free analysis, no key required.
              </p>
              <div className="ps-path-pitstop-flow">
                <span className="ps-path-pitstop-step">Paste prompt</span>
                <div className="ps-path-road-arrow">{"\u2192"}</div>
                <span className="ps-path-pitstop-step">9-Section X-Ray</span>
                <div className="ps-path-road-arrow">{"\u2192"}</div>
                <span className="ps-path-pitstop-step">AI upgrade</span>
              </div>
              <p className="ps-path-why">Best if you already have a prompt and want to level it up.</p>
              <span className="ps-path-cta ps-path-cta-improve">Open Pit Stop {"\u2192"}</span>
            </button>
          </div>

          <div className="ps-splash-pick-label">Pick a starting point</div>

          <div className="ps-starters ps-starters-splash">
            {STARTER_TEMPLATES.map((s) => (
              <button key={s.id} type="button" className="ps-starter-card" onClick={() => { setCopilotMode(false); setCopilotOpen(false); startFromStarter(s); }}>
                <h3>{s.name}</h3>
                <p>{s.description}</p>
                {s.id !== "blank" && <span className="ps-starter-badge">Pre-filled</span>}
                {s.id === "blank" && <span className="ps-starter-badge blank">Guided</span>}
              </button>
            ))}
          </div>

          <div className="ps-first-time-banner">
            <div className="ps-first-time-glow" />
            <span className="ps-first-time-badge">First time?</span>
            <p>
              Pick <strong>Sentiment Analyzer</strong> and go manual — every field is pre-filled so you can see how each step works.
              Switch to Copilot anytime if you want AI to take over!
            </p>
            <span className="ps-first-time-arrow">{"\u2197"}</span>
          </div>

          <div className="ps-nav">
            <button type="button" onClick={() => { resetWizard(); }} className="ps-btn secondary">Cancel</button>
          </div>
        </div>
      )}

      {wizardActive && step > 0 && (
        <div className="ps-workspace">
        <div className="ps-wizard">

          {/* ── Full-page step header ─────────────────── */}
          <div className="ps-step-screen-header">
            <div className="ps-step-screen-progress">
              {WIZARD_STEPS.slice(1).map((ws, i) => {
                const stepNum = i + 1;
                return (
                  <div
                    key={i}
                    className={`ps-step-dot ${stepNum === step ? "active" : ""} ${stepNum < step ? "done" : ""}`}
                    onClick={() => { if (stepNum < step) setStep(stepNum); }}
                    title={ws.title}
                  >
                    <span className="ps-dot-num">{stepNum < step ? "✓" : stepNum}</span>
                  </div>
                );
              })}
            </div>
            <div className="ps-step-screen-meta">
              <span className="ps-step-screen-num">Step {step} of {WIZARD_STEPS.length - 1}</span>
              <span className="ps-step-screen-title">{WIZARD_STEPS[step]?.title}</span>
              {WIZARD_STEPS[step]?.guidebook && (
                <span className="ps-step-screen-guidebook">9-Section Architecture: {WIZARD_STEPS[step].guidebook}</span>
              )}
            </div>
          </div>

          {/* ── Step 1: Name + Goal (② Goal from Guidebook) ── */}
          {step === 1 && (
            <div className="ps-panel fade-in">
              <h2>Give It a Name</h2>
              <p className="ps-hint">Every great prompt starts with a clear mission. Name your template, then define what "done well" looks like.</p>

              <div className="ps-field">
                <label>Template Name <span className="ps-required">*</span></label>
                <p className="ps-field-hint">A short identifier — use underscores instead of spaces. Think of it like a filename.</p>
                <input value={form.name} onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))} placeholder="e.g. sentiment_analyzer" />
              </div>

              <div className="ps-field">
                <label>Description</label>
                <p className="ps-field-hint">One sentence so you remember what this does later.</p>
                <input value={form.description} onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))} placeholder="e.g. Classify product reviews into sentiment categories" />
              </div>

              <div className="ps-field">
                <label>Goal <span className="ps-guidebook-tag">② Goal — What Success Looks Like</span></label>
                <p className="ps-field-hint">
                  Use the <strong>imperative formula</strong> from the Prompt Guidebook: <em>"Your mission: [specific achievement] — accomplish this fully."</em> This tells the AI exactly what "done" looks like. Vague goals like "analyze data" produce vague output.
                </p>
                <textarea value={form.guidance?.goal || ""} onChange={(e) => setForm((f) => ({ ...f, guidance: { ...f.guidance, goal: e.target.value } }))} rows={3} placeholder='e.g. Your mission: Identify every statistically significant anomaly in the Q4 revenue data — accomplish this fully.' />
              </div>

              <WalkthroughBox title="The Guidebook formula for goals" visible={true}>
                <p className="ps-wt-note"><strong>Declarative (weak):</strong> "Goal: Analyze the data."</p>
                <p className="ps-wt-note"><strong>Imperative (strong):</strong> "Your mission: Surface every statistically significant anomaly in the Q4 revenue data — accomplish this fully."</p>
                <p className="ps-wt-note">The imperative form creates a <em>completion criterion</em> — the AI knows what success looks like and can evaluate its own output against it.</p>
                <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>More examples:</strong></div>
                <ul className="ps-wt-list">
                  <li>"Your mission: Classify product reviews into sentiment categories with confidence scores and reasoning — accomplish this fully."</li>
                  <li>"Your mission: Identify every security vulnerability in this authentication module, rank by exploitability, and provide a concrete remediation for each — accomplish this fully."</li>
                </ul>
              </WalkthroughBox>

              <Tip>The phrase "accomplish this fully" is a <strong>completion anchor</strong> — it signals that partial responses are insufficient. Always include it.</Tip>
            </div>
          )}

          {/* ── Step 2: Role + Style (① Role, ④ Style from Guidebook) ── */}
          {step === 2 && (
            <div className="ps-panel fade-in">
              <h2>Who Should It Be?</h2>
              <p className="ps-hint">The Guidebook says: <em>"You are"</em> are the two most powerful words in prompt engineering. They activate an expert persona that shapes every word the AI writes.</p>

              <div className="ps-field">
                <label>Role <span className="ps-required">*</span> <span className="ps-guidebook-tag">① Role — The Expert Identity</span></label>
                <p className="ps-field-hint">
                  Use the formula: <strong>"You are a [seniority] [domain] [specialist] with [specific context]."</strong> This single sentence primes the AI's knowledge, vocabulary, and judgment. Always start with "You are".
                </p>
                <input value={form.guidance?.role || ""} onChange={(e) => setForm((f) => ({ ...f, guidance: { ...f.guidance, role: e.target.value } }))} placeholder='e.g. You are a senior data scientist specializing in NLP sentiment analysis with 10 years of product analytics experience.' />
                <ExamplesDrawer title="See roles from our 87 built-in templates (click to use)">
                  <div className="ps-example-list">
                    {ROLE_EXAMPLES.map((ex, i) => (
                      <div key={i} className="ps-example-item clickable" onClick={() => setForm((f) => ({ ...f, guidance: { ...f.guidance, role: ex.value } }))}>
                        <span className="ps-example-source">{ex.template}</span>
                        <span className="ps-example-value">{ex.value}</span>
                      </div>
                    ))}
                  </div>
                </ExamplesDrawer>
              </div>

              <WalkthroughBox title="The 'You are' formula (from Guidebook)" visible={true}>
                <p className="ps-wt-note"><strong>Weak:</strong> "analyst"</p>
                <p className="ps-wt-note"><strong>Strong:</strong> "You are a senior financial analyst specializing in forensic accounting with SEC investigation experience."</p>
                <p className="ps-wt-note">The "You are" opener triggers <em>persona priming</em> — the AI anchors its vocabulary, reasoning depth, and judgment to the declared expert. Include seniority, domain, and relevant context.</p>
              </WalkthroughBox>

              <div className="ps-field" style={{marginTop:"1.5rem"}}>
                <label>Writing Style <span className="ps-guidebook-tag">④ Style — Persona's Voice</span></label>
                <p className="ps-field-hint">
                  Pick 2–4 adjectives that define the voice: how formal, how concise, how technical. Style is <em>separate</em> from the Role — the same expert can write differently for different audiences.
                </p>
                <input value={form.guidance?.style || ""} onChange={(e) => setForm((f) => ({ ...f, guidance: { ...f.guidance, style: e.target.value } }))} placeholder="e.g. concise, evidence-based, professional" />
                <ExamplesDrawer title="See styles from our built-in templates (click to use)">
                  <div className="ps-example-list">
                    {STYLE_EXAMPLES.map((ex, i) => (
                      <div key={i} className="ps-example-item clickable" onClick={() => setForm((f) => ({ ...f, guidance: { ...f.guidance, style: ex.value } }))}>
                        <span className="ps-example-source">{ex.template}</span>
                        <span className="ps-example-value">{ex.value}</span>
                      </div>
                    ))}
                  </div>
                </ExamplesDrawer>
              </div>

              <Tip>Keep Role and Style separate. The role says <em>who</em> the AI is; the style says <em>how</em> it writes. A "senior security engineer" might write in a "terse, tactical, action-oriented" style — or a "thorough, educational, tutorial" style depending on the audience.</Tip>
            </div>
          )}

          {/* ── Step 3: Rules (③ Rules from Guidebook) ── */}
          {step === 3 && (
            <div className="ps-panel fade-in">
              <h2>House Rules</h2>
              <p className="ps-hint">Rules are <em>guarantees, not preferences</em>. The Guidebook says: write each rule as a non-negotiable constraint — one sentence, binding language ("must", "always", "never"), ordered by criticality.</p>

              <div className="ps-field">
                <label>Rules <span className="ps-guidebook-tag">③ Rules — Non-Negotiable Constraints</span></label>
                <p className="ps-field-hint">
                  Write each rule with <strong>binding modals</strong> (must, shall, always, never). Think of them as contractual clauses — the AI treats "should" as optional but "must" as mandatory. Order by criticality: most important first. Aim for 3–6 rules.
                </p>
                <div className="ps-rules-list">
                  {safeRules(form.guidance?.rules).map((rule, idx) => (
                    <div key={idx} className="ps-rule-row">
                      <span className="ps-rule-num">{idx + 1}</span>
                      <input value={rule} onChange={(e) => updateRule(idx, e.target.value)} placeholder={RULE_PLACEHOLDERS[idx] || RULE_PLACEHOLDERS[RULE_PLACEHOLDERS.length - 1]} />
                      <button type="button" onClick={() => removeRule(idx)} className="ps-remove-btn" title="Remove">×</button>
                    </div>
                  ))}
                </div>
                <button type="button" onClick={addRule} className="ps-add-btn">+ Add Rule</button>
                <ExamplesDrawer title="See rules from our built-in templates (click to add)">
                  <div className="ps-example-list">
                    {RULE_EXAMPLES.map((ex, i) => (
                      <div key={i} className="ps-example-item clickable" onClick={() => setForm((f) => ({ ...f, guidance: { ...f.guidance, rules: [...safeRules(f.guidance?.rules), ex.value] } }))}>
                        <span className="ps-example-source">{ex.template}</span>
                        <span className="ps-example-value">{ex.value}</span>
                      </div>
                    ))}
                  </div>
                </ExamplesDrawer>
              </div>

              <WalkthroughBox title="Guidebook rule-writing formula" visible={true}>
                <p className="ps-wt-note"><strong>Weak (preference):</strong> "Try to use accurate data."</p>
                <p className="ps-wt-note"><strong>Strong (guarantee):</strong> "Every claim must cite a specific data point from the input."</p>
                <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>Binding modals:</strong> must | shall | always | never | exactly | only</div>
                <div className="ps-wt-row" style={{marginTop:"0.3rem"}}><strong>Ordering:</strong> Most critical rule first — if the AI truncates, the top rule survives.</div>
                <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>Sentiment Analyzer example:</strong></div>
                <ol className="ps-wt-rules">
                  <li>Every review must be classified into exactly one of: positive, negative, neutral, mixed, sarcastic.</li>
                  <li>Always consider tone, intensity, hedging, sarcasm, and mixed signals before classifying.</li>
                  <li>Every response must include reasoning, what_is_good, what_is_bad, and recommendations fields.</li>
                  <li>Output must be valid JSON — never include text outside the JSON object.</li>
                </ol>
              </WalkthroughBox>

              <Tip>The Guidebook's key insight: the difference between "should" and "must" is the difference between a suggestion and a contract. Use "must" for every rule.</Tip>
            </div>
          )}

          {/* ── Step 4: Reasoning + Examples (⑧.5 Reasoning, ⑤ Examples from Guidebook) ── */}
          {step === 4 && (
            <div className="ps-panel fade-in">
              <h2>Teach It to Think</h2>
              <p className="ps-hint">The Guidebook defines <strong>five reasoning strategies</strong> — each controls <em>how</em> the AI approaches your task. Pick the one that fits, then optionally show examples of what "good" looks like.</p>

              <div className="ps-field ps-think-question">
                <label className="ps-think-ask">How do you want the AI to think? <span className="ps-guidebook-tag">⑧.5 Reasoning Strategy</span></label>
                <p className="ps-field-hint">Each strategy fundamentally changes the AI's reasoning path. The Guidebook says: pick the strategy that matches your task's complexity — and stick to one per prompt.</p>

                <div className="ps-strategy-cards">
                  {THINKING_STRATEGIES.map((strategy) => (
                    <label
                      key={strategy.id}
                      className={`ps-strategy-card ${form.thinking_strategy === strategy.id ? "selected" : ""}`}
                    >
                      <input
                        type="radio"
                        name="thinking_strategy"
                        value={strategy.id}
                        checked={form.thinking_strategy === strategy.id}
                        onChange={() => setForm(f => ({ ...f, thinking_strategy: strategy.id }))}
                      />
                      <div className="ps-strategy-content">
                        <span className="ps-strategy-icon">{strategy.icon}</span>
                        <span className="ps-strategy-label">{strategy.label}</span>
                        <span className="ps-strategy-question">{strategy.question}</span>
                        <span className="ps-strategy-desc">{strategy.whatItMeans}</span>
                        <span className="ps-strategy-when"><strong>Best for:</strong> {strategy.whenToUse}</span>
                        <span className="ps-strategy-badge">{strategy.technique}</span>
                      </div>
                    </label>
                  ))}
                </div>

                {selectedStrategy.injection && (
                  <div className="ps-strategy-injection">
                    <span className="ps-strategy-injection-label">What gets added to your prompt:</span>
                    <p className="ps-strategy-injection-text">"{selectedStrategy.injection}"</p>
                  </div>
                )}
              </div>

              <div className="ps-field ps-examples-section">
                <label className="ps-think-ask">Show it what "good" looks like <span className="ps-guidebook-tag">⑤ Examples — Few-Shot Anchors</span></label>
                <p className="ps-field-hint">The Guidebook says: <strong>2–5 examples, representative of edge cases, matching the exact output format.</strong> Few-shot examples are the single strongest accuracy lever — they teach by demonstration, not instruction.</p>

                {safeArray(form.examples).map((ex, idx) => (
                  <div key={idx} className="ps-example-pair">
                    <div className="ps-example-input">
                      <span className="ps-example-pair-label">When the AI sees this...</span>
                      <textarea
                        value={ex.input || ""}
                        onChange={(e) => updateExample(idx, "input", e.target.value)}
                        rows={2}
                        placeholder='e.g. "This product is amazing, best purchase this year!"'
                      />
                    </div>
                    <div className="ps-example-arrow-col">
                      <span className="ps-example-arrow-icon">→</span>
                    </div>
                    <div className="ps-example-output">
                      <span className="ps-example-pair-label">...it should respond like this</span>
                      <textarea
                        value={ex.output || ""}
                        onChange={(e) => updateExample(idx, "output", e.target.value)}
                        rows={2}
                        placeholder='e.g. "Positive — strong enthusiasm, superlative language"'
                      />
                    </div>
                    <button type="button" onClick={() => removeExample(idx)} className="ps-remove-btn" title="Remove example">×</button>
                  </div>
                ))}

                <button type="button" onClick={addExample} className="ps-add-btn">+ Add Example</button>
              </div>

              <WalkthroughBox title="Guidebook: Reasoning + Examples are the strongest accuracy combo" visible={true}>
                <div className="ps-wt-row"><strong>Reasoning strategy</strong> controls <em>how</em> the AI thinks.</div>
                <div className="ps-wt-row"><strong>Examples</strong> show <em>what good looks like</em>.</div>
                <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>Guidebook example guidelines:</strong></div>
                <ul className="ps-wt-list">
                  <li>Include <strong>2–5 examples</strong> (diminishing returns beyond 5)</li>
                  <li>Make them <strong>representative of edge cases</strong> — not just easy ones</li>
                  <li>Match the <strong>exact output format</strong> you defined in step 5</li>
                </ul>
                <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>Sentiment Analyzer examples:</strong></div>
                <div className="ps-wt-example">"This product is amazing!" → Positive — strong enthusiasm, superlative language</div>
                <div className="ps-wt-example">"Terrible experience, would not recommend" → Negative — strong negative language</div>
                <div className="ps-wt-example">"Delivery was fast but product broke" → Mixed — positive + negative in same review</div>
              </WalkthroughBox>

              <Tip>The Guidebook's golden rule for examples: <strong>include at least one edge case</strong> (mixed sentiment, ambiguous input, sarcasm). Edge-case examples prevent the most common AI mistakes.</Tip>
            </div>
          )}

          {/* ── Step 5: Output Contract (⑦ Output Contract from Guidebook) ── */}
          {step === 5 && (
            <div className="ps-panel fade-in">
              <div className="ps-split">
                <div className="ps-form-side">
                  <h2>Shape the Answer</h2>
                  <p className="ps-hint">The Guidebook says: <strong>"Return ONLY [form] structured as [structure]. Exclude [X]."</strong> This is your output contract — it locks the AI into a specific response shape.</p>

                  <div className="ps-field">
                    <label>Output Fields <span className="ps-guidebook-tag">⑦ Output Contract — The "Return ONLY" Clause</span></label>
                    <p className="ps-field-hint">Define <strong>form</strong> (field names), <strong>structure</strong> (types), and <strong>what to exclude</strong>. Every field you add becomes a non-negotiable part of the response. The AI will return exactly these fields, nothing more.</p>
                    <div className="ps-schema-list">
                      {safeArray(form.outputSchema).map((field, idx) => (
                        <div key={idx} className="ps-schema-row">
                          <input
                            value={field.name}
                            onChange={(e) => updateOutputField(idx, { name: e.target.value })}
                            placeholder="e.g. sentiment, confidence, reasoning"
                            className="ps-schema-name"
                          />
                          <select
                            value={field.type}
                            onChange={(e) => updateOutputField(idx, { type: e.target.value })}
                            className="ps-schema-type"
                          >
                            {OUTPUT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
                          </select>
                          <button type="button" onClick={() => removeOutputField(idx)} className="ps-remove-btn">×</button>
                        </div>
                      ))}
                    </div>
                    <button type="button" onClick={addOutputField} className="ps-add-btn">+ Add Field</button>
                  </div>

                  <WalkthroughBox title="The Guidebook's 'Return ONLY' formula" visible={true}>
                    <p className="ps-wt-note"><strong>Formula:</strong> "Return ONLY [form] structured as [structure]. Exclude [X]."</p>
                    <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>Sentiment Analyzer output contract:</strong></div>
                    <table className="ps-wt-schema">
                      <tbody>
                        <tr><td>sentiment</td><td className="ps-type">str</td><td className="ps-explain">"Return ONLY a JSON object"</td></tr>
                        <tr><td>confidence</td><td className="ps-type">float</td><td className="ps-explain">"structured as {'{'}sentiment, confidence, ...{'}'}"</td></tr>
                        <tr><td>reasoning</td><td className="ps-type">str</td><td className="ps-explain">"Exclude any preamble or explanation"</td></tr>
                        <tr><td>needs_human_review</td><td className="ps-type">bool</td><td className="ps-explain">true/false flag</td></tr>
                        <tr><td>recommendations</td><td className="ps-type">str</td><td className="ps-explain">actionable next steps</td></tr>
                      </tbody>
                    </table>
                    <p className="ps-wt-note">Each field you define here becomes enforceable in the Guard Rails step. The AI treats this as a binding contract — it will return exactly these fields in the exact types specified.</p>
                  </WalkthroughBox>
                </div>

                <PreviewPanel builderBuilt={builderBuilt} building={building} onRefresh={handleBuildPreview} />
              </div>
            </div>
          )}

          {/* ── Step 6: Guard Rails (⑧ Guard Rails from Guidebook) ── */}
          {step === 6 && (
            <div className="ps-panel fade-in">
              <div className="ps-split">
                <div className="ps-form-side">
                  <h2>Guard Rails</h2>
                  <p className="ps-hint">The Guidebook says: <strong>use positive redirects over bare negation.</strong> Instead of "Don't speculate," say "Omit any claim not supported by the input data." Positive phrasing tells the AI what to do <em>instead</em>, which is more effective.</p>

                  <div className="ps-field">
                    <label>Must NOT Include <span className="ps-guidebook-tag">⑧ Guard Rails — Boundary Fences</span></label>
                    <p className="ps-field-hint">Use the <strong>"Omit [X]"</strong> pattern from the Guidebook. "Omit personal opinions" is clearer than "Don't give opinions." Add a <strong>fallback phrase</strong> where possible: "If uncertain, respond with 'Insufficient data' rather than guessing."</p>
                    <div className="ps-constraint-list">
                      {safeArray(form.constraints?.must_not_include).map((item, idx) => (
                        <div key={idx} className="ps-constraint-row">
                          <input value={item} onChange={(e) => updateConstraintItem("must_not_include", idx, e.target.value)} placeholder="e.g. personal opinions, speculation" />
                          <button type="button" onClick={() => removeConstraintItem("must_not_include", idx)} className="ps-remove-btn">×</button>
                        </div>
                      ))}
                    </div>
                    <button type="button" onClick={() => addConstraintItem("must_not_include")} className="ps-add-btn">+ Add</button>
                  </div>

                  <div className="ps-field">
                    <label>Must Include</label>
                    <p className="ps-field-hint">What must <em>always</em> appear in the response? These are your inclusion guarantees — the AI treats each as a mandatory checklist item.</p>
                    <div className="ps-constraint-list">
                      {safeArray(form.constraints?.must_include).map((item, idx) => (
                        <div key={idx} className="ps-constraint-row">
                          <input value={item} onChange={(e) => updateConstraintItem("must_include", idx, e.target.value)} placeholder="e.g. reasoning, confidence score" />
                          <button type="button" onClick={() => removeConstraintItem("must_include", idx)} className="ps-remove-btn">×</button>
                        </div>
                      ))}
                    </div>
                    <button type="button" onClick={() => addConstraintItem("must_include")} className="ps-add-btn">+ Add</button>
                  </div>

                  <div className="ps-field">
                    <label>Format Rules</label>
                    <p className="ps-field-hint">Structural enforcement: "Output valid JSON only", "Confidence must be 0.0–1.0", "Maximum 500 words". These control the <em>shape</em> of the response.</p>
                    <div className="ps-constraint-list">
                      {safeArray(form.constraints?.format_rules).map((item, idx) => (
                        <div key={idx} className="ps-constraint-row">
                          <input value={item} onChange={(e) => updateConstraintItem("format_rules", idx, e.target.value)} placeholder="e.g. Output valid JSON only" />
                          <button type="button" onClick={() => removeConstraintItem("format_rules", idx)} className="ps-remove-btn">×</button>
                        </div>
                      ))}
                    </div>
                    <button type="button" onClick={() => addConstraintItem("format_rules")} className="ps-add-btn">+ Add</button>
                  </div>

                  <WalkthroughBox title="Guidebook: Positive redirect over bare negation" visible={true}>
                    <p className="ps-wt-note"><strong>Bare negation (weak):</strong> "Don't speculate."</p>
                    <p className="ps-wt-note"><strong>Positive redirect (strong):</strong> "Omit any claim not directly supported by the input data."</p>
                    <p className="ps-wt-note"><strong>With fallback (strongest):</strong> "If the input lacks sufficient evidence, respond with 'Insufficient data to determine' rather than guessing."</p>
                    <div className="ps-wt-row" style={{ marginTop: "0.5rem" }}><strong>Sentiment Analyzer guard rails:</strong></div>
                    <ul className="ps-wt-list">
                      <li><strong>Omit:</strong> personal opinions, speculation, text outside the JSON object</li>
                      <li><strong>Always include:</strong> sentiment, confidence, reasoning for every classification</li>
                      <li><strong>Format:</strong> Output valid JSON only, confidence 0.0–1.0</li>
                      <li><strong>Fallback:</strong> If sentiment is unclear, classify as "mixed" with confidence &lt; 0.5</li>
                    </ul>
                  </WalkthroughBox>
                </div>

                <PreviewPanel builderBuilt={builderBuilt} building={building} onRefresh={handleBuildPreview} />
              </div>
            </div>
          )}

          {/* ── Step 7: Task (⑨ Task from Guidebook) ── */}
          {step === 7 && (
            <div className="ps-panel fade-in">
              <div className="ps-split">
                <div className="ps-form-side">
                  <h2>The Big Ask</h2>
                  <p className="ps-hint">The Guidebook says: <strong>Task always comes last.</strong> By the time the AI reads the task, it already knows who it is, how to think, what rules to follow, and what format to return. The task is the trigger that fires everything.</p>

                  <div className="ps-field">
                    <label>What should the AI do? <span className="ps-required">*</span> <span className="ps-guidebook-tag">⑨ Task — The Trigger</span></label>
                    <p className="ps-field-hint">Write the core instruction in plain language. Reference your input <strong>specifically</strong> — use <code>[variable_name]</code> for parts that change each time. Use <code>---</code> separators to clearly mark where input data begins.</p>
                    <textarea
                      ref={directiveRef}
                      value={directiveDisplay}
                      onChange={(e) => handleDirectiveDisplayChange(e.target.value)}
                      rows={5}
                      placeholder={"e.g. Analyze the following text for sentiment.\nProvide reasoning and recommendations.\n\n[user_text]"}
                    />
                  </div>

                  {/* Variables — supporting cast */}
                  <div className="ps-field">
                    <label>Changeable Parts (Variables)</label>
                    <p className="ps-field-hint">
                      These are the blanks that get filled in each time. Click <strong>Insert</strong> to place one in your instructions above.
                    </p>
                    {(form.input_schema || []).map((field, idx) => {
                      const paramKey = field?.name ?? `param_${idx}`;
                      return (
                        <div key={`${paramKey}-${idx}`} className="ps-var-row">
                          <div className="ps-var-name-col">
                            <span className="ps-var-label">Variable name</span>
                            <input placeholder="e.g. user_text" value={field?.name ?? ""} onChange={(e) => updateSchemaField(idx, { name: e.target.value })} />
                          </div>
                          <div className="ps-var-test-col">
                            <span className="ps-var-label">Try it with this value</span>
                            <input placeholder="e.g. I love this product!" value={params[paramKey] ?? field?.default ?? ""} onChange={(e) => setParams((p) => ({ ...p, [paramKey]: e.target.value }))} />
                          </div>
                          <button type="button" onClick={() => insertVariable(field?.name || paramKey)} className="ps-insert-btn" title="Insert into instructions">Insert</button>
                          <button type="button" onClick={() => removeSchemaField(idx)} className="ps-remove-btn" title="Remove">×</button>
                        </div>
                      );
                    })}
                    <button type="button" onClick={addSchemaField} className="ps-add-btn">+ Add Variable</button>
                  </div>

                  {form.directive_template && (
                    <div className="ps-field">
                      <label>What the AI will actually see</label>
                      <p className="ps-field-hint">Variables are replaced with real values. This is exactly what gets sent to the AI.</p>
                      <DirectivePreview template={form.directive_template} params={params} />
                    </div>
                  )}

                  <WalkthroughBox title="Guidebook: Task always last, specific input reference" visible={true}>
                    <p className="ps-wt-note"><strong>Why last?</strong> The AI reads instructions before data. By placing the task at the end, the AI has full context (role, rules, reasoning, output format) before it processes your input.</p>
                    <div className="ps-wt-row" style={{marginTop:"0.5rem"}}><strong>Use separators for clarity:</strong></div>
                    <div className="ps-wt-code">Analyze the following product review for sentiment. Provide reasoning and recommendations.<br/><br/>---<br/><span className="ps-var-chip filled">I love this product! Best purchase this year, but shipping was really slow.</span><br/>---</div>
                    <p className="ps-wt-note">The <code>---</code> separators clearly mark where user input begins and ends — this prevents prompt injection and keeps the AI focused on the right data.</p>
                    <p className="ps-wt-note"><strong>Specific input reference:</strong> Say "Analyze the following product review" not just "Analyze this." The AI needs to know <em>what</em> it's looking at.</p>
                  </WalkthroughBox>
                </div>

                <PreviewPanel builderBuilt={builderBuilt} building={building} onRefresh={handleBuildPreview} />
              </div>
            </div>
          )}

          {/* ── Step 8: Ship It! ─────────────── */}
          {step === 8 && (() => {
            const filledRules = safeRules(form.guidance?.rules).filter(Boolean);
            const filledExamples = safeArray(form.examples).filter(ex => ex.input?.trim() && ex.output?.trim());
            const filledSchema = safeArray(form.outputSchema).filter(f => f.name);
            const hasConstraints = form.constraints && (
              safeArray(form.constraints.must_include).filter(Boolean).length > 0 ||
              safeArray(form.constraints.must_not_include).filter(Boolean).length > 0 ||
              safeArray(form.constraints.format_rules).filter(Boolean).length > 0
            );
            return (
            <div className="ps-panel fade-in">
              <h2>Ship It!</h2>
              <p className="ps-hint">Here's everything you've built, step by step. Click any section header to jump back and edit. When you're happy, hit <strong>Finalize & Save</strong>.</p>

              <div className="ps-review ps-review-steps">

                {/* ── Section 1: Give It a Name ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(1)} title="Click to edit">
                    <span className="ps-review-step-num">1</span>
                    <span className="ps-review-step-title">Give It a Name</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    <div className="ps-review-row"><strong>Name:</strong> {form.name || <span className="ps-review-empty-hint">Not set</span>}</div>
                    <div className="ps-review-row"><strong>Description:</strong> {form.description || <span className="ps-review-empty-hint">Not set</span>}</div>
                    <div className="ps-review-row"><strong>Goal:</strong> {form.guidance?.goal || <span className="ps-review-empty-hint">Not set</span>}</div>
                  </div>
                </div>

                {/* ── Section 2: Who Should It Be? ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(2)} title="Click to edit">
                    <span className="ps-review-step-num">2</span>
                    <span className="ps-review-step-title">Who Should It Be?</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    <div className="ps-review-row"><strong>Role:</strong> {form.guidance?.role || <span className="ps-review-empty-hint">Not set</span>}</div>
                    <div className="ps-review-row"><strong>Style:</strong> {form.guidance?.style || <span className="ps-review-empty-hint">Not set</span>}</div>
                  </div>
                </div>

                {/* ── Section 3: House Rules ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(3)} title="Click to edit">
                    <span className="ps-review-step-num">3</span>
                    <span className="ps-review-step-title">House Rules</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    {filledRules.length > 0 ? (
                      <ol className="ps-review-rules">{filledRules.map((r, i) => <li key={i}>{r}</li>)}</ol>
                    ) : (
                      <p className="ps-review-empty-hint">No rules set — the AI will use its own judgment.</p>
                    )}
                  </div>
                </div>

                {/* ── Section 4: Teach It to Think ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(4)} title="Click to edit">
                    <span className="ps-review-step-num">4</span>
                    <span className="ps-review-step-title">Teach It to Think</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    <div className="ps-review-strategy-card">
                      <span className="ps-review-strategy-label">{selectedStrategy.icon} {selectedStrategy.label}</span>
                      <span className="ps-review-strategy-what">{selectedStrategy.whatItMeans}</span>
                      <span className="ps-review-strategy-tech">{selectedStrategy.technique}</span>
                      {selectedStrategy.injection && (
                        <p className="ps-review-strategy-inject">Adds: "{selectedStrategy.injection.length > 80 ? selectedStrategy.injection.slice(0, 80) + "..." : selectedStrategy.injection}"</p>
                      )}
                    </div>
                    {filledExamples.length > 0 ? (
                      <>
                        <div className="ps-review-sub-label">Examples ({filledExamples.length})</div>
                        <div className="ps-review-examples">
                          {filledExamples.map((ex, i) => (
                            <div key={i} className="ps-review-example-row">
                              <span className="ps-review-example-in">{ex.input}</span>
                              <span className="ps-review-example-arrow">→</span>
                              <span className="ps-review-example-out">{ex.output}</span>
                            </div>
                          ))}
                        </div>
                      </>
                    ) : (
                      <p className="ps-review-empty-hint">No examples added — the AI won't have reference outputs to learn from.</p>
                    )}
                  </div>
                </div>

                {/* ── Section 5: Shape the Answer ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(5)} title="Click to edit">
                    <span className="ps-review-step-num">5</span>
                    <span className="ps-review-step-title">Shape the Answer</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    {filledSchema.length > 0 ? (
                      <>
                        <div className="ps-review-sub-label">Output Schema ({filledSchema.length} fields)</div>
                        <table className="ps-schema-table">
                          <thead><tr><th>Field</th><th>Type</th></tr></thead>
                          <tbody>
                            {filledSchema.map((f, i) => (
                              <tr key={i}><td>{f.name}</td><td className="ps-schema-type-cell">{f.type}</td></tr>
                            ))}
                          </tbody>
                        </table>
                      </>
                    ) : (
                      <p className="ps-review-empty-hint">No output schema — the AI will choose its own response format.</p>
                    )}
                  </div>
                </div>

                {/* ── Section 6: Guard Rails ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(6)} title="Click to edit">
                    <span className="ps-review-step-num">6</span>
                    <span className="ps-review-step-title">Guard Rails</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    {hasConstraints ? (
                      <div className="ps-review-constraints">
                        {safeArray(form.constraints.must_not_include).filter(Boolean).length > 0 && <div><strong>Must NOT include:</strong> {form.constraints.must_not_include.filter(Boolean).join(", ")}</div>}
                        {safeArray(form.constraints.must_include).filter(Boolean).length > 0 && <div><strong>Must include:</strong> {form.constraints.must_include.filter(Boolean).join(", ")}</div>}
                        {safeArray(form.constraints.format_rules).filter(Boolean).length > 0 && <div><strong>Format rules:</strong> {form.constraints.format_rules.filter(Boolean).join("; ")}</div>}
                      </div>
                    ) : (
                      <p className="ps-review-empty-hint">No guard rails set — no constraints on the AI's output.</p>
                    )}
                  </div>
                </div>

                {/* ── Section 7: The Big Ask ──── */}
                <div className="ps-review-step">
                  <div className="ps-review-step-header" onClick={() => setStep(7)} title="Click to edit">
                    <span className="ps-review-step-num">7</span>
                    <span className="ps-review-step-title">The Big Ask</span>
                    <span className="ps-review-edit-hint">Edit</span>
                  </div>
                  <div className="ps-review-step-body">
                    {varNames.length > 0 ? (
                      <>
                        <div className="ps-review-sub-label">Changeable Parts ({varNames.length})</div>
                        <div className="ps-review-vars-table">
                          {(form.input_schema || []).filter(f => f?.name).map((f, i) => (
                            <div key={i} className="ps-review-var-row">
                              <code className="ps-review-var">[{f.name}]</code>
                              <span className="ps-review-var-arrow">→</span>
                              <span className="ps-review-var-value">{params[f.name] || f.default || <em className="ps-review-empty-hint">no sample value</em>}</span>
                            </div>
                          ))}
                        </div>
                      </>
                    ) : (
                      <div className="ps-review-row"><strong>Variables:</strong> <span className="ps-review-empty-hint">None — the same text is used every time.</span></div>
                    )}
                    {form.directive_template ? (
                      <>
                        <div className="ps-review-sub-label" style={{ marginTop: "0.65rem" }}>The Task (template)</div>
                        <div className="ps-review-template-raw">{toDisplay(form.directive_template)}</div>
                        {varNames.length > 0 && (
                          <>
                            <div className="ps-review-sub-label" style={{ marginTop: "0.5rem" }}>What the AI actually sees</div>
                            <DirectivePreview template={form.directive_template} params={params} />
                          </>
                        )}
                      </>
                    ) : (
                      <p className="ps-review-empty-hint">No instructions written yet.</p>
                    )}
                  </div>
                </div>

                {/* ── Quality Score ──── */}
                {builderBuilt && <div className="ps-review-score"><QualityScore assembled={builderBuilt.assembled} hasKey={hasKey} onError={setError} /></div>}
                {!builderBuilt && (
                  <button type="button" onClick={handleBuildPreview} disabled={building} className="ps-btn secondary" style={{ marginTop: "1rem" }}>
                    {building ? "Building..." : "See It Live to get quality score"}
                  </button>
                )}
              </div>

              <div className="ps-finalize-actions">
                <button type="button" onClick={handleFinalize} disabled={!form.name?.trim() || building} className="ps-btn primary large">
                  {building ? "Saving..." : "Finalize & Save"}
                </button>
              </div>

              {finalized && builderBuilt && (
                <div ref={downloadRef} className="ps-download fade-in">
                  <h3>Your prompt is ready!</h3>
                  <p className="ps-download-subtitle">Copy this prompt and paste it into any AI tool — ChatGPT, Claude, Gemini, or your own app.</p>
                  <div className="ps-download-content ps-prompt-output">
                    <pre className="ps-prompt-text">{builderBuilt.assembled || ""}</pre>
                  </div>
                  <div className="ps-download-actions">
                    <button type="button" onClick={() => copyBuilderFormat("markdown")} className="ps-btn primary">Copy to Clipboard</button>
                    <button type="button" onClick={() => downloadBuilderFormat("markdown")} className="ps-btn secondary">Download as Text</button>
                  </div>
                </div>
              )}
            </div>
            );
          })()}

          {/* ── Navigation ─────────────────────── */}
          <div className="ps-nav ps-nav-fullscreen">
            <button type="button" onClick={() => setStep(step - 1)} className="ps-btn secondary large">
              {"\u2190"} Back
            </button>
            <div className="ps-nav-center-hint">
              {step < 8 ? (
                <span className="ps-nav-skip" onClick={() => setStep(step + 1)}>Skip this step →</span>
              ) : null}
            </div>
            {step < 8 && (
              <button type="button" onClick={() => setStep(step + 1)} disabled={!canProceed()} className="ps-btn primary large">
                Next: {WIZARD_STEPS[step + 1]?.short || "Continue"} {"\u2192"}
              </button>
            )}
          </div>
        </div>

        {/* ── Copilot: fixed right panel (always-open for AI Drive, toggle FAB for manual) ── */}
        {copilotMode ? (
          <div className="ps-copilot-fixed-right">
            <CopilotPanel
              form={form}
              onApplySuggestion={(s) => { handleCopilotSuggestion(s); }}
              onError={setError}
              onBuildPreview={handleBuildPreview}
              onGoToReview={() => setStep(8)}
              previewReady={!!builderBuilt}
              builderBuilt={builderBuilt}
            />
          </div>
        ) : (
          <div className={`ps-copilot-fab-wrapper ${copilotOpen ? "open" : ""}`}>
            <button
              type="button"
              className="ps-copilot-fab"
              onClick={() => setCopilotOpen(!copilotOpen)}
              title="Open AI Copilot"
            >
              {copilotOpen ? "✕" : "🤖"} {copilotOpen ? "Close" : "Copilot"}
            </button>
            {copilotOpen && (
              <div className="ps-copilot-fab-panel">
                <CopilotPanel
                  form={form}
                  onApplySuggestion={(s) => { handleCopilotSuggestion(s); }}
                  onError={setError}
                  onBuildPreview={handleBuildPreview}
                  onGoToReview={() => { setStep(8); setCopilotOpen(false); }}
                  previewReady={!!builderBuilt}
                  builderBuilt={builderBuilt}
                />
              </div>
            )}
          </div>
        )}
        </div>
      )}

      {/* ── Saved templates ─────────────────────── */}
      {!wizardActive && (
        <>
          {loading ? (
            <p className="ps-loading">Loading...</p>
          ) : templates.length > 0 ? (
            <div className="ps-saved">
              <h2>Your Prompts</h2>
              <div className="ps-saved-grid">
                {templates.map((t) => (
                  <div key={t.id} className="ps-saved-card">
                    <h3>{t.name}</h3>
                    <p>{t.description || "Custom template"}</p>
                    <div className="ps-saved-actions">
                      <button type="button" onClick={() => startEdit(t)} className="ps-btn primary small">Edit</button>
                      <button type="button" onClick={() => handleDelete(t.id)} className="ps-btn small danger">Delete</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="ps-empty">
              <div className="ps-empty-icon">✨</div>
              <h2>No prompts yet</h2>
              <p>Create your first AI prompt — we'll guide you through every step.</p>
              <button type="button" onClick={() => { resetWizard(); setWizardActive(true); }} className="ps-btn primary large">Create Your First Prompt</button>
            </div>
          )}
        </>
      )}

      {/* ── Prompt Improver Overlay ─────────────────────── */}
      {improverOpen && (
        <>
          <div className="ps-improver-overlay" onClick={() => setImproverOpen(false)} />
          <div className="ps-improver-panel">
            <div className="ps-improver-header">
              <h2>{"\uD83D\uDD27"} Pit Stop</h2>
              <p>Paste any existing prompt. We'll X-ray it against the 9 sections, then upgrade it using the Guidebook's architecture.</p>
              <button type="button" className="ps-improver-close" onClick={() => setImproverOpen(false)}>&times;</button>
            </div>

            <div className="ps-improver-body">
              <div className="ps-improver-llm-bar">
                <label>Provider</label>
                <select value={improveProvider} onChange={(e) => { setImproveProvider(e.target.value); setImproveModel(""); }}>
                  {IMPROVE_PROVIDERS.map((p) => (<option key={p} value={p}>{p}</option>))}
                </select>
                <label>Model</label>
                <select value={improveModel} onChange={(e) => setImproveModel(e.target.value)} className="ps-improver-model-input">
                  <option value="">Auto (recommended)</option>
                  {modelsForProvider(improveProvider).map((m) => (
                    <option key={m.id} value={m.id}>{m.label}</option>
                  ))}
                </select>
              </div>

              <textarea
                className="ps-improver-input"
                rows={8}
                placeholder="Paste your existing prompt here..."
                value={improveInput}
                onChange={(e) => { setImproveInput(e.target.value); setParseResult(null); setImproveResult(null); setImproveError(""); }}
              />

              <div className="ps-improver-actions">
                <button type="button" onClick={handleParsePrompt} disabled={parseLoading || !improveInput.trim()} className="ps-btn secondary">
                  {parseLoading ? "Analyzing..." : "Analyze (Free)"}
                </button>
                <button type="button" onClick={handleImprovePrompt} disabled={improveLoading || !improveInput.trim() || !hasKey} className="ps-btn primary" title={!hasKey ? "Add an API key in Settings first" : ""}>
                  {improveLoading ? "Improving..." : "\u2728 Improve with AI (API key)"}
                </button>
              </div>

              {improveError && <p className="ps-improver-error">{improveError}</p>}

              {parseResult && (
                <div className="ps-improver-result fade-in">
                  <h4>9-Section Analysis</h4>
                  <div className="ps-improver-chips">
                    {Object.entries(SECTION_LABELS).map(([key, label]) => {
                      const present = parseResult.present?.includes(key);
                      return (
                        <span key={key} className={`ps-improver-chip ${present ? "present" : "missing"}`}>
                          {present ? "\u2713" : "\u2717"} {label}
                        </span>
                      );
                    })}
                  </div>
                  {parseResult.missing?.length > 0 && (
                    <p className="ps-improver-hint">
                      <strong>{parseResult.missing.length} section{parseResult.missing.length !== 1 ? "s" : ""} missing.</strong> Click <strong>Improve with AI</strong> to fill them in.
                    </p>
                  )}
                  {parseResult.present?.length === 9 && (
                    <p className="ps-improver-hint ps-improver-hint--good">All 9 sections detected. Click Improve to strengthen weak ones.</p>
                  )}
                </div>
              )}

              {improveResult && (
                <div className="ps-improver-result fade-in">
                  <div className="ps-improver-score-bar">
                    <span className="ps-improver-score-label">Quality</span>
                    <span className="ps-improver-score before">{Math.round((improveResult.before_score || 0) * 100)}%</span>
                    <span className="ps-improver-arrow">{"\u2192"}</span>
                    <span className="ps-improver-score after">{Math.round((improveResult.after_score || 0) * 100)}%</span>
                    <span className="ps-improver-delta">+{Math.round((improveResult.score_delta || 0) * 100)}%</span>
                  </div>

                  {improveResult.resolved_issues?.length > 0 && (
                    <div className="ps-improver-resolved">
                      <strong>✓ {improveResult.resolved_issues.length} issue{improveResult.resolved_issues.length !== 1 ? "s" : ""} resolved</strong>
                      <ul>{improveResult.resolved_issues.map((iss, i) => <li key={i}>{iss}</li>)}</ul>
                    </div>
                  )}
                  {improveResult.after_issues?.length > 0 && (
                    <p className="ps-improver-hint">
                      {improveResult.after_issues.length} issue{improveResult.after_issues.length !== 1 ? "s" : ""} remaining — see section diffs for details.
                    </p>
                  )}

                  {improveResult.diffs?.length > 0 && (
                    <details className="ps-improver-diffs">
                      <summary>Section-by-section changes ({improveResult.diffs.filter((d) => d.action !== "unchanged").length} changed)</summary>
                      <div className="ps-improver-diff-list">
                        {improveResult.diffs.filter((d) => d.action !== "unchanged").map((d, i) => (
                          <div key={i} className={`ps-improver-diff ps-improver-diff--${d.action}`}>
                            <span className="ps-improver-diff-badge">{d.action.toUpperCase()}</span>
                            <span className="ps-improver-diff-section">{SECTION_LABELS[d.section] || d.section}</span>
                            {d.before && d.action !== "unchanged" && (
                              <p className="ps-improver-diff-before">{d.before}</p>
                            )}
                            {d.after && <p className="ps-improver-diff-after">{d.after}</p>}
                            <p className="ps-improver-diff-rationale">{d.rationale}</p>
                          </div>
                        ))}
                      </div>
                    </details>
                  )}

                  <div className="ps-improver-output-header">
                    <h4>Improved Prompt</h4>
                    <div className="ps-improver-output-actions">
                      <button type="button" className="ps-btn secondary" onClick={async () => { try { await navigator.clipboard.writeText(improveResult.improved_prompt); setToast("Copied!"); } catch { setToast("Copy failed"); } }}>Copy</button>
                      <button type="button" className="ps-btn secondary" onClick={() => { const blob = new Blob([improveResult.improved_prompt], { type: "text/plain" }); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "improved_prompt.txt"; a.click(); URL.revokeObjectURL(url); setToast("Downloaded"); }}>Download</button>
                    </div>
                  </div>
                  <pre className="ps-improver-output">{improveResult.improved_prompt}</pre>
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {toast && <Toast message={toast} onClose={() => setToast("")} />}

    </div>
  );
}
