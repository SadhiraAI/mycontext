import { useState, useEffect, useCallback, useRef } from "react";
import { Link } from "react-router-dom";
import * as api from "../api/client";
import Toast from "../components/Toast";
import QualityScore from "../components/QualityScore";
import MarkdownContent from "../components/MarkdownContent";
import CopilotPanel from "../components/CopilotPanel";
import { STARTER_TEMPLATES, THINKING_STRATEGIES } from "../data/starterTemplates";
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
            <div className="ps-research-zone"><span className="ps-rz-label middle">Middle</span> <span className="ps-rz-sections">Reasoning → Examples</span> <span className="ps-rz-why">Demos stable here (+6 pts)</span></div>
            <div className="ps-research-zone"><span className="ps-rz-label late">Late</span> <span className="ps-rz-sections">Output Format → Guard Rails</span> <span className="ps-rz-why">Fresh before generating</span></div>
            <div className="ps-research-zone"><span className="ps-rz-label recency">Recency Zone</span> <span className="ps-rz-sections">Task (always last)</span> <span className="ps-rz-why">+9.7 BLEU improvement</span></div>
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

const WIZARD_STEPS = [
  { title: "Pick Your Adventure", short: "Adventure" },  // 0
  { title: "Give It a Name", short: "Name" },             // 1
  { title: "Who Should It Be?", short: "Who" },           // 2
  { title: "House Rules", short: "Rules" },                // 3
  { title: "Teach It to Think", short: "Think" },          // 4
  { title: "Shape the Answer", short: "Answer" },          // 5 — output schema only
  { title: "Guard Rails", short: "Guards" },               // 6 — constraints
  { title: "The Big Ask", short: "Ask" },                  // 7
  { title: "Ship It!", short: "Ship!" },                   // 8
];

const DEFAULT_GUIDANCE = { goal: "", role: "", rules: [], style: "" };
const DEFAULT_SCHEMA = [{ name: "topic", type: "text", default: "" }];
const OUTPUT_TYPES = ["str", "float", "int", "bool", "list"];

const ROLE_EXAMPLES = [
  { template: "SWOT Analyzer", value: "Expert Strategic Analyst and Business Consultant" },
  { template: "Root Cause Analyzer", value: "Root Cause Analysis Specialist and Systems Thinker" },
  { template: "Technical Translator", value: "Expert Technical Communicator and Plain Language Specialist" },
  { template: "Sentiment Analyzer", value: "Sentiment analysis expert" },
  { template: "Code Reviewer", value: "Senior software engineer and code reviewer" },
];

const RULE_EXAMPLES = [
  { template: "SWOT", value: "Be honest about weaknesses — don't sugarcoat" },
  { template: "Root Cause", value: "Distinguish symptoms from causes" },
  { template: "Root Cause", value: "Use evidence, not speculation" },
  { template: "Translator", value: "Replace jargon with common words" },
  { template: "Sentiment", value: "Consider tone, intensity, hedging, sarcasm, and mixed signals" },
  { template: "Sentiment", value: "Respond only with valid JSON matching the required schema" },
  { template: "Code Review", value: "Categorize issues by severity: critical, warning, suggestion" },
  { template: "Code Review", value: "Suggest concrete fixes for each issue" },
];

const STYLE_EXAMPLES = [
  { template: "SWOT", value: "analytical, balanced, strategic" },
  { template: "Root Cause", value: "investigative, thorough, evidence-based" },
  { template: "Translator", value: "clear, accessible, respectful" },
  { template: "Sentiment", value: "consistent, concise, structured" },
  { template: "Code Review", value: "professional, constructive, specific" },
];

const RULE_PLACEHOLDERS = [
  "What's the #1 thing the AI must do? e.g., Always cite sources",
  "How should the output look? e.g., Use bullet points with headers",
  "What should the AI avoid? e.g., Never make up information",
  "Any quality standards? e.g., Rate confidence from 0.0 to 1.0",
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

  // ── Render ──────────────────────────────────────────────
  return (
    <div className={`ps-page ${wizardActive && step > 0 ? "ps-page--copilot-active" : ""}`}>
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

          <div className="ps-two-paths">
            {/* ── Manual Path ── */}
            <button
              type="button"
              className="ps-path-card ps-path-manual"
              onClick={() => startFromStarter(STARTER_TEMPLATES.find(s => s.id === "blank"))}
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
              onClick={() => startFromStarter(STARTER_TEMPLATES.find(s => s.id === "blank"))}
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
          </div>

          <div className="ps-splash-pick-label">Pick a starting point</div>

          <div className="ps-starters ps-starters-splash">
            {STARTER_TEMPLATES.map((s) => (
              <button key={s.id} type="button" className="ps-starter-card" onClick={() => startFromStarter(s)}>
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
          <div className="ps-progress ps-progress-9">
            {WIZARD_STEPS.map((ws, i) => (
              <div key={i} className={`ps-progress-step ${i === step ? "active" : ""} ${i < step ? "done" : ""}`} onClick={() => { if (i < step) setStep(i); }}>
                <span className="ps-step-num">{i < step ? "✓" : i + 1}</span>
                <span className="ps-step-label">{ws.short}</span>
              </div>
            ))}
          </div>

          {/* ── Step 1: Give It a Name ──────────── */}
          {step === 1 && (
            <div className="ps-panel fade-in">
              <h2>Give It a Name</h2>
              <p className="ps-hint">Think of it like naming a tool. What does this prompt do? Who is it for?</p>

              <div className="ps-field">
                <label>Template Name <span className="ps-required">*</span></label>
                <p className="ps-field-hint">A short name — like naming a file. Use underscores instead of spaces.</p>
                <input value={form.name} onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))} placeholder="e.g. sentiment_analyzer" />
              </div>

              <div className="ps-field">
                <label>Description</label>
                <p className="ps-field-hint">One sentence so you remember what this does later.</p>
                <input value={form.description} onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))} placeholder="e.g. Classify product reviews into sentiment categories" />
              </div>

              <div className="ps-field">
                <label>Goal</label>
                <p className="ps-field-hint">What exactly do you want the AI to accomplish? Be as specific as you can.</p>
                <textarea value={form.guidance?.goal || ""} onChange={(e) => setForm((f) => ({ ...f, guidance: { ...f.guidance, goal: e.target.value } }))} rows={2} placeholder="e.g. Classify reviews into 10 sentiment types with confidence scores and recommendations" />
              </div>

              <WalkthroughBox title="Here's a complete example to follow" visible={showWalkthrough}>
                <div className="ps-wt-row"><strong>Name:</strong> sentiment_analyzer</div>
                <div className="ps-wt-row"><strong>Description:</strong> Classify product reviews into sentiment categories with confidence scores</div>
                <div className="ps-wt-row"><strong>Goal:</strong> Classify product/review text into one of 10 sentiment types with reasoning and actionable fields</div>
                <p className="ps-wt-note">Notice how the goal is very specific — it says <em>exactly</em> how many types (10), and what extra info to include (reasoning, actionable fields). The more detail here, the better your AI output will be.</p>
              </WalkthroughBox>

              {!showWalkthrough && (
                <Tip>A specific goal like "Classify reviews into 10 categories with confidence scores" works much better than a vague one like "Analyze text".</Tip>
              )}
            </div>
          )}

          {/* ── Step 2: Who Should It Be? ──────── */}
          {step === 2 && (
            <div className="ps-panel fade-in">
              <h2>Who Should It Be?</h2>
              <p className="ps-hint">Imagine you're hiring an expert for this task. What's their job title? How should they write?</p>

              <div className="ps-field">
                <label>Role <span className="ps-required">*</span></label>
                <p className="ps-field-hint">Give the AI a job title. Be specific — "Senior data analyst with 10 years experience" works way better than just "analyst".</p>
                <input value={form.guidance?.role || ""} onChange={(e) => setForm((f) => ({ ...f, guidance: { ...f.guidance, role: e.target.value } }))} placeholder="e.g. Senior software engineer and code reviewer" />
                <ExamplesDrawer title="See roles from our 85 built-in templates (click to use)">
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

              <div className="ps-field">
                <label>Writing Style</label>
                <p className="ps-field-hint">Pick 2–4 words that describe how the AI should write. Think about tone and format.</p>
                <input value={form.guidance?.style || ""} onChange={(e) => setForm((f) => ({ ...f, guidance: { ...f.guidance, style: e.target.value } }))} placeholder="e.g. professional, concise, actionable" />
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

              <WalkthroughBox title="Here's how the Sentiment Analyzer does it" visible={showWalkthrough}>
                <div className="ps-wt-row"><strong>Role:</strong> Sentiment analysis expert</div>
                <div className="ps-wt-row"><strong>Style:</strong> consistent, concise, structured</div>
                <p className="ps-wt-note">A clear role + style combo like this helps the AI produce focused, consistently-formatted output from the very first response.</p>
              </WalkthroughBox>

              {!showWalkthrough && (
                <Tip>The more specific the role, the better. "Expert data scientist specializing in NLP" beats "data scientist" every time.</Tip>
              )}
            </div>
          )}

          {/* ── Step 3: House Rules ──────────────── */}
          {step === 3 && (
            <div className="ps-panel fade-in">
              <h2>House Rules</h2>
              <p className="ps-hint">These are the instructions that control how the AI behaves. Think of them like rules for an employee — add one at a time and aim for 3 to 6 rules.</p>

              <div className="ps-field">
                <label>Rules</label>
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

              <WalkthroughBox title="Here's how the Sentiment Analyzer does it" visible={showWalkthrough}>
                <div className="ps-wt-row"><strong>Rules:</strong></div>
                <ol className="ps-wt-rules">
                  <li>Classify sentiment as one of: positive, negative, neutral, mixed, sarcastic</li>
                  <li>Consider tone, intensity, hedging, sarcasm, and mixed signals</li>
                  <li>Include reasoning, what_is_good, what_is_bad, recommendations</li>
                  <li>Respond only with valid JSON</li>
                </ol>
                <p className="ps-wt-note">See the pattern? Rule 1 says <em>what to do</em>, Rules 2–3 say <em>what to include</em>, Rule 4 says <em>what format</em>. That's a great formula for any prompt!</p>
              </WalkthroughBox>

              {!showWalkthrough && (
                <Tip>A good recipe: Rule 1 = what to do, Rule 2 = what to include, Rule 3 = what format to use, Rule 4 = what to avoid.</Tip>
              )}
            </div>
          )}

          {/* ── Step 4: Teach It to Think ─────── */}
          {step === 4 && (
            <div className="ps-panel fade-in">
              <h2>Teach It to Think</h2>
              <p className="ps-hint">Now let's teach the AI <em>how</em> to approach your task. Pick the thinking style that fits, and optionally show it examples of what you expect.</p>

              <div className="ps-field ps-think-question">
                <label className="ps-think-ask">How do you want the AI to think?</label>
                <p className="ps-field-hint">Each option changes how the AI reasons through your task. Pick one and we'll inject the right instructions behind the scenes.</p>

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
                <label className="ps-think-ask">Want to show it some examples?  <span className="ps-optional">(optional but powerful)</span></label>
                <p className="ps-field-hint">Give the AI a few input → output pairs so it knows exactly what "good" looks like. Even 2–3 examples dramatically improve accuracy.</p>

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

              <WalkthroughBox title="Here's how the Sentiment Analyzer does it" visible={showWalkthrough}>
                <div className="ps-wt-row"><strong>Strategy:</strong> Walk me through it (Chain of Thought)</div>
                <div className="ps-wt-row"><strong>Examples:</strong></div>
                <div className="ps-wt-example">"This product is amazing!" → Positive — strong enthusiasm, superlative language</div>
                <div className="ps-wt-example">"Terrible experience, would not recommend" → Negative — strong negative language</div>
                <div className="ps-wt-example">"Delivery was fast but product broke" → Mixed — positive on delivery, negative on durability</div>
                <p className="ps-wt-note">The thinking strategy tells the AI <em>how</em> to approach the problem, and the examples show it <em>exactly</em> what you expect. Together, they're the most powerful combo in prompt engineering.</p>
              </WalkthroughBox>

              {!showWalkthrough && (
                <Tip>"Walk me through it" is the most popular choice — it works great for analysis, math, and anything with multiple parts. When in doubt, start there!</Tip>
              )}
            </div>
          )}

          {/* ── Step 5: Shape the Answer (output schema only) ── */}
          {step === 5 && (
            <div className="ps-panel fade-in">
              <div className="ps-split">
                <div className="ps-form-side">
                  <h2>Shape the Answer</h2>
                  <p className="ps-hint">Define what fields the AI should return. This tells the AI exactly what structure you expect in its response.</p>

                  <div className="ps-field">
                    <label>Output Fields</label>
                    <p className="ps-field-hint">Add each field the AI must return. Pick a type for each one (str = text, float = decimal number, int = whole number, bool = true/false, list = multiple items).</p>
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

                  <WalkthroughBox title="Here's how the Sentiment Analyzer does it" visible={showWalkthrough}>
                    <div className="ps-wt-row"><strong>Output Schema</strong> — these are the fields the AI must return:</div>
                    <table className="ps-wt-schema">
                      <tbody>
                        <tr><td>sentiment</td><td className="ps-type">str</td><td className="ps-explain">positive, negative, neutral...</td></tr>
                        <tr><td>confidence</td><td className="ps-type">float</td><td className="ps-explain">0.0 to 1.0</td></tr>
                        <tr><td>reasoning</td><td className="ps-type">str</td><td className="ps-explain">why the AI chose that label</td></tr>
                        <tr><td>needs_human_review</td><td className="ps-type">bool</td><td className="ps-explain">true/false flag</td></tr>
                        <tr><td>recommendations</td><td className="ps-type">str</td><td className="ps-explain">actionable next steps</td></tr>
                      </tbody>
                    </table>
                    <p className="ps-wt-note">The output schema tells the AI <em>exactly</em> what to return and the types to use. You'll add quality checks in the next step.</p>
                  </WalkthroughBox>
                </div>

                <PreviewPanel builderBuilt={builderBuilt} building={building} onRefresh={handleBuildPreview} />
              </div>
            </div>
          )}

          {/* ── Step 6: Guard Rails (constraints) ── */}
          {step === 6 && (
            <div className="ps-panel fade-in">
              <div className="ps-split">
                <div className="ps-form-side">
                  <h2>Guard Rails</h2>
                  <p className="ps-hint">Set boundaries for the AI. What must always be in its response? What should it never say? Any formatting rules?</p>

                  <div className="ps-field">
                    <label>Must NOT Include</label>
                    <p className="ps-field-hint">What should the AI never put in its response? These are the strongest constraints — listed first so the AI pays extra attention.</p>
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
                    <p className="ps-field-hint">What should always be in the AI's response?</p>
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
                    <p className="ps-field-hint">Any rules about how the output should look?</p>
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

                  <WalkthroughBox title="Why Guard Rails matter" visible={showWalkthrough}>
                    <p className="ps-wt-note"><strong>"Must NOT"</strong> constraints are listed first because research shows LLMs pay strongest attention to information at the <strong>beginning</strong> (primacy effect) and <strong>end</strong> (recency effect). Placing hard restrictions early prevents violations.</p>
                    <div className="ps-wt-row" style={{ marginTop: "0.5rem" }}><strong>Example Guard Rails</strong>:</div>
                    <ul className="ps-wt-list">
                      <li>Must NOT include: personal opinions, speculation</li>
                      <li>Must include: sentiment, confidence, reasoning</li>
                      <li>Format rules: Output valid JSON only, Confidence 0.0–1.0</li>
                    </ul>
                  </WalkthroughBox>
                </div>

                <PreviewPanel builderBuilt={builderBuilt} building={building} onRefresh={handleBuildPreview} />
              </div>
            </div>
          )}

          {/* ── Step 7: The Big Ask ────────────── */}
          {step === 7 && (
            <div className="ps-panel fade-in">
              <div className="ps-split">
                <div className="ps-form-side">
                  <h2>The Big Ask</h2>
                  <p className="ps-hint">Everything above tells the AI <em>who it is</em> and <em>how to think</em>. Now tell it <strong>what to do</strong>.</p>

                  {/* Instructions first — the main event */}
                  <div className="ps-field">
                    <label>What should the AI do? <span className="ps-required">*</span></label>
                    <p className="ps-field-hint">Write the task in plain language. Use <code>[variable_name]</code> for parts that change each time.</p>
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

                  <WalkthroughBox title="Here's how the Sentiment Analyzer does it" visible={showWalkthrough}>
                    <div className="ps-wt-row"><strong>Task:</strong> "Analyze the user's text for sentiment. Provide reasoning and recommendations."</div>
                    <div className="ps-wt-row"><strong>Variable:</strong> <code>[user_text]</code> gets replaced with the actual review text each time</div>
                    <div className="ps-wt-row"><strong>What the AI sees:</strong></div>
                    <div className="ps-wt-code">Analyze the user's text for sentiment. Provide reasoning and recommendations.<br/><br/><span className="ps-var-chip filled">I love this product! Best purchase this year, but shipping was really slow.</span></div>
                    <p className="ps-wt-note">The task comes first, then the actual text at the bottom. The AI reads the instructions before seeing the input — like briefing someone before handing them a document.</p>
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
          <div className="ps-nav">
            <button type="button" onClick={() => setStep(step - 1)} className="ps-btn secondary">
              {"\u2190"} Back
            </button>
            {step < 8 && (
              <button type="button" onClick={() => setStep(step + 1)} disabled={!canProceed()} className="ps-btn primary">Next {"\u2192"}</button>
            )}
          </div>
        </div>

        <CopilotPanel
          form={form}
          onApplySuggestion={handleCopilotSuggestion}
          onError={setError}
          onBuildPreview={handleBuildPreview}
          onGoToReview={() => setStep(8)}
          previewReady={!!builderBuilt}
          builderBuilt={builderBuilt}
          docked
        />
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

      {toast && <Toast message={toast} onClose={() => setToast("")} />}

    </div>
  );
}
