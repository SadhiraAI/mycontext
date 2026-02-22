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

export default function SmartExecutePanel({ provider = "openai", hasKey = false, compact = false }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleExecute() {
    if (!question.trim() || !hasKey) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await api.smartExecute(question.trim(), provider);
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
