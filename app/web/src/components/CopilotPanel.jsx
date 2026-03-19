import { useState, useRef, useEffect, useCallback } from "react";
import { copilotChatStream } from "../api/client";
import { MODEL_CATALOG } from "../config/models";
import useActiveProvider from "../hooks/useActiveProvider";
import MarkdownContent from "./MarkdownContent";
import "./CopilotPanel.css";

/* ── Step definitions (mirror the 8 active wizard steps 1-8) ── */

const GUIDED_STEPS = [
  { key: "name",    label: "Name" },
  { key: "who",     label: "Who" },
  { key: "rules",   label: "Rules" },
  { key: "think",   label: "Think" },
  { key: "answer",  label: "Answer" },
  { key: "guards",  label: "Guards" },
  { key: "ask",     label: "Ask" },
  { key: "ship",    label: "Ship!" },
];

/* ── Suggestion parsing ──────────────────────────── */

function parseSuggestions(text) {
  const xmlSugs = parseXmlSuggestions(text);
  if (xmlSugs.length > 0) return xmlSugs;
  return parseFallbackSuggestions(text);
}

function parseXmlSuggestions(text) {
  const suggestions = [];
  const re = /<suggest\s+field="([^"]+)"(?:\s+action="([^"]+)")?>([^<]*(?:<(?!\/suggest>)[^<]*)*)<\/suggest>/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    let value = m[3].trim();
    if (value.startsWith("[") && value.endsWith("]")) {
      try { value = JSON.parse(value); } catch (_) {}
    }
    suggestions.push({ field: m[1], action: m[2] || "replace", value });
  }
  return suggestions;
}

function parseFallbackSuggestions(text) {
  const suggestions = [];
  const seen = new Set();
  const lines = text.split("\n");

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const cleaned = line.replace(/\*+/g, "").replace(/`+/g, "").replace(/^>\s*/, "").trim();

    const singleFields = [
      { field: "name", re: /^(?:name|template.name)\s*[:–—-]\s*(.+)/i },
      { field: "description", re: /^(?:description|desc|summary)\s*[:–—-]\s*(.+)/i },
      { field: "goal", re: /^(?:goal|objective|purpose)\s*[:–—-]\s*(.+)/i },
      { field: "role", re: /^role\s*[:–—-]\s*(.+)/i },
      { field: "style", re: /^(?:style|tone|voice)\s*[:–—-]\s*(.+)/i },
      { field: "directive", re: /^(?:directive|instruction|task)\s*[:–—-]\s*(.+)/i },
      { field: "thinking_strategy", re: /^(?:thinking.?strategy|strategy)\s*[:–—-]\s*(.+)/i },
    ];

    for (const { field, re: rx } of singleFields) {
      const match = cleaned.match(rx);
      if (match && !seen.has(field)) {
        let val = match[1].replace(/\*+/g, "").replace(/`+/g, "").replace(/^["']|["']$/g, "").trim();
        if (val.length > 3 && val.length < 400) {
          suggestions.push({ field, action: "replace", value: val });
          seen.add(field);
        }
      }
    }

    if (/^(?:rules?|guidelines?)\s*[:–—-]/i.test(cleaned) && !seen.has("rules")) {
      const items = [];
      for (let j = i + 1; j < lines.length && j < i + 15; j++) {
        const rl = lines[j].replace(/\*+/g, "").replace(/`+/g, "").trim();
        if (/^[-*\d.)]+\s+/.test(rl)) {
          items.push(rl.replace(/^[-*\d.)\s]+/, "").trim());
        } else if (rl === "" && items.length > 0) {
          break;
        } else if (items.length > 0) {
          break;
        }
      }
      if (items.length > 0) {
        suggestions.push({ field: "rules", action: "replace", value: items });
        seen.add("rules");
      }
    }

    if (/^(?:constraints?|must.include|format.rules?)\s*[:–—-]/i.test(cleaned) && !seen.has("constraints_must_include")) {
      const items = [];
      for (let j = i + 1; j < lines.length && j < i + 10; j++) {
        const cl = lines[j].replace(/\*+/g, "").replace(/`+/g, "").trim();
        if (/^[-*\d.)]+\s+/.test(cl)) {
          items.push(cl.replace(/^[-*\d.)\s]+/, "").trim());
        } else if (cl === "" && items.length > 0) {
          break;
        }
      }
      if (items.length > 0) {
        suggestions.push({ field: "constraints_must_include", action: "replace", value: items });
        seen.add("constraints_must_include");
      }
    }
  }

  return suggestions;
}

function stripSuggestTags(text) {
  return text.replace(/<suggest\s+field="[^"]*"(?:\s+action="[^"]*")?>[^<]*(?:<(?!\/suggest>)[^<]*)*<\/suggest>/g, "").trim();
}

/* ── Chip component ──────────────────────────── */

const FIELD_LABELS = {
  name: "Name", description: "Desc", goal: "Goal", role: "Role",
  rules: "Rules", style: "Style", variables: "Vars",
  directive: "Directive", output_schema: "Schema",
  thinking_strategy: "Strategy", examples: "Examples",
  constraints_must_include: "Must Have", constraints_must_not_include: "Exclude",
  constraints_format_rules: "Format",
};

function SuggestionChip({ suggestion, onApply }) {
  const { field, value } = suggestion;
  let display;
  if (field === "output_schema" && Array.isArray(value)) {
    display = value.map(f => typeof f === "object" ? f.name + " (" + f.type + ")" : String(f)).join(", ");
  } else if (Array.isArray(value)) {
    display = value.join(", ");
  } else {
    display = String(value);
  }
  const label = FIELD_LABELS[field] || field.replace(/_/g, " ");
  return (
    <button type="button" className="copilot-suggest-chip" onClick={() => onApply(suggestion)}>
      <span className="copilot-chip-field">{label}</span>
      <span className="copilot-chip-value">{display.length > 120 ? display.slice(0, 120) + "\u2026" : display}</span>
      <span className="copilot-chip-action">Apply &rarr;</span>
    </button>
  );
}

/* ── Main panel ──────────────────────────── */

export default function CopilotPanel({ form, onApplySuggestion, provider, onError, onBuildPreview, onGoToReview, previewReady, builderBuilt, onSaveFinalize, docked = false }) {
  const active = useActiveProvider();
  const [panelState, setPanelState] = useState("open");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [selectedModel, setSelectedModel] = useState("gpt-4.1-mini");
  const messagesEnd = useRef(null);
  const inputRef = useRef(null);
  const activeModel = MODEL_CATALOG.find(m => m.id === selectedModel) || MODEL_CATALOG[2];
  const prov = activeModel.provider;

  const scrollToBottom = useCallback(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages, scrollToBottom]);
  useEffect(() => { if (panelState === "open" && inputRef.current) inputRef.current.focus(); }, [panelState]);

  useEffect(() => {
    if (active.model && !active.loading) {
      const found = MODEL_CATALOG.find(m => m.id === active.model);
      if (found) setSelectedModel(active.model);
    }
  }, [active.model, active.loading]);

  const stepStatus = GUIDED_STEPS.map(s => {
    if (s.key === "name") return { ...s, filled: !!form?.name && !!form?.guidance?.goal };
    if (s.key === "who") return { ...s, filled: !!form?.guidance?.role && !!form?.guidance?.style };
    if (s.key === "rules") return { ...s, filled: (form?.guidance?.rules || []).filter(Boolean).length > 0 };
    if (s.key === "think") return { ...s, filled: !!(form?.thinking_strategy && form.thinking_strategy !== "direct") || (form?.examples || []).filter(ex => ex.input?.trim() && ex.output?.trim()).length > 0 };
    if (s.key === "answer") return { ...s, filled: !!(form?.outputSchema?.filter(f => f.name).length) };
    if (s.key === "guards") return { ...s, filled: !!(form?.constraints?.must_include?.length || form?.constraints?.must_not_include?.length || form?.constraints?.format_rules?.length) };
    if (s.key === "ask") return { ...s, filled: !!form?.directive_template };
    if (s.key === "ship") return { ...s, filled: false };
    return { ...s, filled: false };
  });
  const completedCount = stepStatus.filter(s => s.filled).length;
  const currentStepIdx = stepStatus.findIndex(s => !s.filled);
  const allDone = completedCount >= 7;
  const formReady = !!form?.guidance?.role && !!form?.directive_template;

  function getContextSnapshot() {
    return {
      name: form?.name || "",
      description: form?.description || "",
      guidance: form?.guidance || {},
      directive_template: form?.directive_template || "",
      input_schema: form?.input_schema || [],
      outputSchema: form?.outputSchema || [],
      constraints: form?.constraints || null,
      thinking_strategy: form?.thinking_strategy || "direct",
      examples: form?.examples || [],
    };
  }

  async function sendMessage(overrideText) {
    const text = (overrideText || input).trim();
    if (!text || streaming) return;
    if (!overrideText) setInput("");
    const userMsg = { role: "user", content: text };
    const withoutQuickReplies = messages.filter(m => !m._quickReplies);
    const newMessages = [...withoutQuickReplies, userMsg];
    setMessages([...newMessages, { role: "assistant", content: "", _streaming: true }]);
    setStreaming(true);
    try {
      const apiMessages = newMessages.filter(m => m.role !== "system").map(({ role, content }) => ({ role, content }));
      await copilotChatStream(
        apiMessages,
        { mode: "guide", provider: prov, model: selectedModel, currentContext: getContextSnapshot() },
        (_chunk, fullSoFar) => {
          setMessages(prev => {
            const updated = [...prev];
            updated[updated.length - 1] = { role: "assistant", content: fullSoFar, _streaming: true };
            return updated;
          });
        }
      );
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = { ...updated[updated.length - 1], _streaming: false };
        return updated;
      });
    } catch (err) {
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: "assistant", content: "Error: " + err.message, _streaming: false };
        return updated;
      });
      if (onError) onError(err.message);
    } finally {
      setStreaming(false);
    }
  }

  function handleApply(suggestion) {
    if (onApplySuggestion) onApplySuggestion(suggestion);
    const desc = Array.isArray(suggestion.value) ? suggestion.value.join(", ") : suggestion.value;
    const fieldLabel = (FIELD_LABELS[suggestion.field] || suggestion.field).replace(/_/g, " ");
    setMessages(prev => {
      const cleaned = prev.filter(m => !m._quickReplies);
      return [...cleaned,
        {
          role: "system",
          content: "\u2705 Applied " + fieldLabel + ": " + (desc.length > 60 ? desc.slice(0, 60) + "\u2026" : desc),
        },
        {
          role: "system",
          _quickReplies: true,
          content: "",
          replies: [
            { label: "\uD83D\uDD04 Refine " + fieldLabel, text: "Can you rewrite the " + fieldLabel + "? Give me a different version." },
            { label: "Next step \u2192", text: "Looks good, let's move to the next step." },
          ],
        },
      ];
    });
  }

  function handleQuickReply(text) {
    setMessages(prev => prev.filter(m => !m._quickReplies));
    if (text === "__finalize__") {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Great work! Here's what to do next:\n\n1. **Switch to the main panel** (the wizard on the left)\n2. **Review your prompt** on the Ship It! step\n3. **Check the quality score** — hit \"See It Live\" to preview and score\n4. **Tweak anything** that needs work\n5. **Save & finalize** when you're happy\n\nI'll take you to the review now!",
      }]);
      setTimeout(() => { if (onGoToReview) onGoToReview(); }, 1500);
      return;
    }
    sendMessage(text);
  }

  function assembleContent() {
    const parts = [];
    if (form?.name) parts.push("Name: " + form.name);
    if (form?.description) parts.push("Description: " + form.description);
    const g = form?.guidance || {};
    if (g.goal) parts.push("Goal: " + g.goal);
    if (g.role) parts.push("Role: " + g.role);
    if (g.style) parts.push("Style: " + g.style);
    if (g.rules?.length) parts.push("Rules:\n" + g.rules.filter(Boolean).map(r => "- " + r).join("\n"));
    if (form?.thinking_strategy && form.thinking_strategy !== "direct") {
      parts.push("Thinking Strategy: " + form.thinking_strategy);
    }
    const exs = (form?.examples || []).filter(ex => ex.input?.trim() && ex.output?.trim());
    if (exs.length) parts.push("Examples:\n" + exs.map((ex, i) => `${i + 1}. "${ex.input}" → "${ex.output}"`).join("\n"));
    const vars = (form?.input_schema || []).map(v => v.name).filter(Boolean);
    if (vars.length) parts.push("Variables: " + vars.join(", "));
    if (form?.directive_template) parts.push("Directive: " + form.directive_template);
    const schema = (form?.outputSchema || []).filter(f => f.name);
    if (schema.length) parts.push("Output Schema:\n" + schema.map(f => "- " + f.name + " (" + f.type + ")").join("\n"));
    const c = form?.constraints;
    if (c?.must_include?.length) parts.push("Must include: " + c.must_include.join(", "));
    if (c?.must_not_include?.length) parts.push("Must not include: " + c.must_not_include.join(", "));
    if (c?.format_rules?.length) parts.push("Format rules: " + c.format_rules.join(", "));
    return parts.join("\n\n");
  }

  function handleRefineExisting() {
    sendMessage("Help me refine what I have so far. Review my current context and suggest improvements to any field — role, rules, style, examples, constraints, or directive.");
  }

  function handleAddMore() {
    sendMessage("What fields am I still missing? Help me fill in the gaps — suggest what I should add next.");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  }

  if (panelState === "closed") {
    if (docked) {
      return (
        <div className="copilot-docked-closed" onClick={() => setPanelState("open")} title="Open AI Copilot">
          <span className="copilot-logo">AI</span>
          <span>Copilot</span>
        </div>
      );
    }
    return (
      <button type="button" className="copilot-fab" onClick={() => setPanelState("open")} title="Open AI Copilot">
        <span className="copilot-fab-icon">AI</span>
        <span className="copilot-fab-label">Copilot</span>
        {completedCount > 0 && completedCount < 7 && <span className="copilot-fab-badge">{completedCount}/7</span>}
      </button>
    );
  }

  if (panelState === "minimized") {
    return (
      <div className={`copilot-minimized${docked ? " copilot-docked-mini" : ""}`} onClick={() => setPanelState("open")}>
        <span className="copilot-logo">AI</span>
        <span className="copilot-mini-title">Context Copilot</span>
        {completedCount > 0 && <span className="copilot-mini-badge">{completedCount}/7</span>}
        {streaming && <span className="copilot-mini-typing">typing...</span>}
        <button type="button" className="copilot-mini-expand" onClick={e => { e.stopPropagation(); setPanelState("open"); }} title="Expand">&uarr;</button>
        <button type="button" className="copilot-mini-close" onClick={e => { e.stopPropagation(); setPanelState("closed"); }} title="Close">&times;</button>
      </div>
    );
  }

  return (
    <div className={`copilot-panel${docked ? " copilot-docked" : ""}`}>
      <div className="copilot-header">
        <div className="copilot-header-left">
          <span className="copilot-logo">AI</span>
          <span className="copilot-title">Context Copilot</span>
        </div>
        <div className="copilot-header-actions">
          <button type="button" onClick={() => setMessages([])} className="copilot-clear">Clear</button>
          <button type="button" onClick={() => setPanelState("minimized")} className="copilot-minimize" title="Minimize">&darr;</button>
          <button type="button" onClick={() => setPanelState("closed")} className="copilot-close" title="Close">&times;</button>
        </div>
      </div>

      <div className="copilot-model-bar">
        <label className="copilot-model-label">Model</label>
        <select
          className="copilot-model-select"
          value={selectedModel}
          onChange={e => setSelectedModel(e.target.value)}
          disabled={streaming}
        >
          <optgroup label="OpenAI">
            {MODEL_CATALOG.filter(m => m.provider === "openai").map(m => (
              <option key={m.id} value={m.id}>{m.label} ({m.tier})</option>
            ))}
          </optgroup>
          <optgroup label="Anthropic">
            {MODEL_CATALOG.filter(m => m.provider === "anthropic").map(m => (
              <option key={m.id} value={m.id}>{m.label} ({m.tier})</option>
            ))}
          </optgroup>
          <optgroup label="Google">
            {MODEL_CATALOG.filter(m => m.provider === "google").map(m => (
              <option key={m.id} value={m.id}>{m.label} ({m.tier})</option>
            ))}
          </optgroup>
        </select>
        <span className={"copilot-provider-badge " + activeModel.provider}>{activeModel.provider}</span>
        <span className={"copilot-tier-badge " + activeModel.tier}>{activeModel.tier}</span>
      </div>

      {/* Step progress bar */}
      <div className="copilot-steps copilot-steps-8">
        {stepStatus.map((s, i) => (
          <div key={s.key} className={"copilot-step " + (s.filled ? "done" : i === currentStepIdx ? "active" : "")}>
            <span className="copilot-step-num">{s.filled ? "\u2713" : i + 1}</span>
            <span className="copilot-step-label">{s.label}</span>
          </div>
        ))}
      </div>

      <div className="copilot-messages">
        {messages.length === 0 && (
          <div className="copilot-welcome">
            <h3>Let's build your AI context — following the 9-Section Architecture.</h3>
            <p>Tell me what you want to build. I'll guide you through each section from the Prompt Guidebook: Role, Goal, Rules, Style, Reasoning, Examples, Output Contract, Guard Rails, and Task.</p>
            <div className="copilot-starters">
              {[
                "I want to build a data analysis assistant",
                "Help me create a code reviewer",
                "Build me a document summarizer",
                "I need a customer support classifier",
              ].map(s => (
                <button key={s} type="button" onClick={() => sendMessage(s)} className="copilot-starter">{s}</button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, idx) => {
          if (msg._quickReplies) {
            return (
              <div key={idx} className="copilot-msg copilot-quick-replies">
                {msg.replies.map((r, ri) => (
                  <button key={ri} type="button" onClick={() => handleQuickReply(r.text)} className="copilot-quick-btn" disabled={streaming}>
                    {r.label}
                  </button>
                ))}
              </div>
            );
          }
          if (msg.role === "system") {
            return (<div key={idx} className="copilot-msg copilot-msg-system"><span>{msg.content}</span></div>);
          }
          if (msg.role === "user") {
            return (<div key={idx} className="copilot-msg copilot-msg-user"><div className="copilot-bubble user">{msg.content}</div></div>);
          }
          const suggestions = msg._streaming ? [] : parseSuggestions(msg.content);
          const cleanText = stripSuggestTags(msg.content);
          return (
            <div key={idx} className="copilot-msg copilot-msg-assistant">
              <div className="copilot-bubble assistant">
                {cleanText && (
                  <div className="copilot-text">
                    <MarkdownContent content={cleanText} />
                  </div>
                )}
                {msg._streaming && <span className="copilot-cursor" />}
                {suggestions.length > 0 && (
                  <div className="copilot-suggestions">
                    {suggestions.map((s, si) => (<SuggestionChip key={si} suggestion={s} onApply={handleApply} />))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        <div ref={messagesEnd} />
      </div>

      <div className="copilot-footer">
        {formReady && (
          <div className="copilot-done-row">
            <button type="button" className="copilot-refine-btn" onClick={handleRefineExisting} disabled={streaming}>
              {"\uD83D\uDD04"} Refine What I Have
            </button>
            <button type="button" className="copilot-add-btn" onClick={handleAddMore} disabled={streaming}>
              + Add More
            </button>
            {allDone && (
              <button type="button" className="copilot-save-btn" onClick={onGoToReview}>
                Ship It! {"\u2192"}
              </button>
            )}
          </div>
        )}
        <div className="copilot-input-row">
          <textarea ref={inputRef} value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder={messages.length === 0 ? "What do you want to build?" : "Type your response..."} rows={1} disabled={streaming} />
          <button type="button" onClick={() => sendMessage()} disabled={!input.trim() || streaming} className="copilot-send">
            {streaming ? "..." : "\u2191"}
          </button>
        </div>
      </div>
    </div>
  );
}
