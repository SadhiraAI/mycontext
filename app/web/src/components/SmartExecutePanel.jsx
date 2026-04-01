import { useState } from "react";
import * as api from "../api/client";
import "./SmartExecutePanel.css";

const MODE_LABELS = {
  raw: "Raw (no template)",
  single_template: "Single Template",
  integrated: "Integrated Templates",
};

const MODE_TIERS = {
  raw: "Direct",
  single_template: "Dynamic",
  integrated: "Full Response",
};

const VERBOSITY_OPTIONS = [
  { value: "", label: "Auto" },
  { value: "minimal", label: "Concise" },
  { value: "standard", label: "Standard" },
  { value: "detailed", label: "Detailed" },
];

export default function SmartExecutePanel({ provider = "openai", hasKey = false, compact = false }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [showQuality, setShowQuality] = useState(false);
  const [verbosity, setVerbosity] = useState("");
  const [answerFirst, setAnswerFirst] = useState(true);
  const [selfVerify, setSelfVerify] = useState(true);

  async function handleExecute() {
    if (!question.trim() || !hasKey) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const quality = {};
      if (verbosity) quality.verbosity = verbosity;
      if (!answerFirst) quality.answer_first = false;
      if (!selfVerify) quality.self_check = [];
      const hasOverrides = Object.keys(quality).length > 0;
      const res = await api.smartExecute(
        question.trim(),
        provider,
        hasOverrides ? quality : undefined
      );
      setResult(res);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={`smart-exec ${compact ? "smart-exec--compact" : ""}`}>
      <div className="smart-exec-header">
        <h4>Smart Execute</h4>
        <span className="smart-exec-badge">Three-Tier</span>
      </div>
      <p className="smart-exec-desc">
        Ask a question and let the complexity router decide the optimal execution tier automatically.
      </p>
      <div className="smart-exec-form">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={compact ? 2 : 3}
          placeholder="Ask any question — the system routes it to the best approach..."
          className="smart-exec-input"
        />
        <div className="smart-exec-quality-toggle">
          <button
            type="button"
            className="smart-exec-quality-btn"
            onClick={() => setShowQuality(!showQuality)}
          >
            {showQuality ? "▾ Output Style" : "▸ Output Style"}
          </button>
        </div>
        {showQuality && (
          <div className="smart-exec-quality">
            <label className="smart-exec-quality-field">
              <span>Verbosity</span>
              <select value={verbosity} onChange={(e) => setVerbosity(e.target.value)}>
                {VERBOSITY_OPTIONS.map((o) => (
                  <option key={o.value} value={o.value}>{o.label}</option>
                ))}
              </select>
            </label>
            <label className="smart-exec-quality-field smart-exec-quality-check">
              <input
                type="checkbox"
                checked={answerFirst}
                onChange={(e) => setAnswerFirst(e.target.checked)}
              />
              <span>Answer first</span>
            </label>
            <label className="smart-exec-quality-field smart-exec-quality-check">
              <input
                type="checkbox"
                checked={selfVerify}
                onChange={(e) => setSelfVerify(e.target.checked)}
              />
              <span>Self-verify</span>
            </label>
          </div>
        )}
        <button
          type="button"
          onClick={handleExecute}
          disabled={loading || !question.trim() || !hasKey}
          className="smart-exec-btn"
        >
          {loading ? "Executing..." : hasKey ? "Smart Execute" : "Add API key first"}
        </button>
      </div>
      {error && <p className="smart-exec-error">{error}</p>}
      {result && (
        <div className="smart-exec-result">
          <div className="smart-exec-meta">
            <span className="smart-exec-tier" data-mode={result.mode}>
              {MODE_TIERS[result.mode] || result.mode}
            </span>
            <span className="smart-exec-mode-label">{MODE_LABELS[result.mode] || result.mode}</span>
            {result.templates_used?.length > 0 && (
              <span className="smart-exec-templates">
                {result.templates_used.map((t) => t.replace(/_/g, " ")).join(", ")}
              </span>
            )}
          </div>
          <pre className="smart-exec-response">{result.response}</pre>
          <div className="smart-exec-actions">
            <button
              type="button"
              className="smart-exec-copy"
              onClick={() => navigator.clipboard.writeText(result.response)}
            >
              Copy
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
