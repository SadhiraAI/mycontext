import { useState } from "react";
import * as api from "../api/client";
import "./QualityScore.css";

function scoreColor(val) {
  if (val >= 0.80) return "score-excellent";
  if (val >= 0.65) return "score-good";
  if (val >= 0.45) return "score-adequate";
  return "score-poor";
}

function scoreEmoji(val) {
  if (val >= 0.80) return "\u2705";
  if (val >= 0.65) return "\u2714\uFE0F";
  if (val >= 0.45) return "\u26A0\uFE0F";
  return "\u274C";
}

export default function QualityScore({ assembled, provider = "openai", hasKey = false, onError, heading = true }) {
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("fast");
  const [result, setResult] = useState(null);

  async function handleScore() {
    if (!assembled?.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await api.evaluateQuality(assembled, mode, provider);
      setResult(res);
    } catch (e) {
      if (onError) onError(e.message);
    } finally {
      setLoading(false);
    }
  }

  if (!assembled?.trim()) return null;

  return (
    <div className="quality-score">
      {heading && <h4>Quality Score</h4>}
      <div className="quality-score-actions">
        <select value={mode} onChange={(e) => setMode(e.target.value)} title="Quick Scan: free instant analysis. AI Judge: deeper evaluation using your LLM.">
          <option value="fast">Quick Scan (free)</option>
          <option value="accurate" disabled={!hasKey}>AI Judge</option>
        </select>
        <button type="button" onClick={handleScore} disabled={loading} className="quality-score-btn">
          {loading ? "Scoring\u2026" : "Score"}
        </button>
      </div>
      {result && (
        <div className="quality-result fade-in">
          <div className={`quality-overall ${scoreColor(result.overall)}`}>
            <span className="quality-value">{(result.overall * 100).toFixed(0)}%</span>
            <span className="quality-label">Overall</span>
          </div>
          {result.dimensions && Object.keys(result.dimensions).length > 0 && (
            <div className="quality-dimensions">
              {Object.entries(result.dimensions).map(([k, v]) => (
                <div key={k} className={`quality-dim ${scoreColor(v)}`}>
                  <span className="quality-dim-name">{k}</span>
                  <div className="quality-dim-bar-track">
                    <div className="quality-dim-bar-fill" style={{ width: `${(v * 100).toFixed(0)}%` }} />
                  </div>
                  <span className="quality-dim-value">{(v * 100).toFixed(0)}%</span>
                </div>
              ))}
            </div>
          )}
          {result.issues?.length > 0 && (
            <div className="quality-section quality-issues">
              <h5>Issues</h5>
              <ul>
                {result.issues.map((i, idx) => (
                  <li key={idx}>{i}</li>
                ))}
              </ul>
            </div>
          )}
          {result.strengths?.length > 0 && (
            <div className="quality-section quality-strengths">
              <h5>Strengths</h5>
              <ul>
                {result.strengths.map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>
          )}
          {result.suggestions?.length > 0 && (
            <div className="quality-section quality-suggestions">
              <h5>Suggestions</h5>
              <ul>
                {result.suggestions.map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
