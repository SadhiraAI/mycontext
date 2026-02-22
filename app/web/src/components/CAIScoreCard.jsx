import { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as api from "../api/client";
import { modelsForProvider, PROVIDERS } from "../config/models";
import "./CAIScoreCard.css";

function scoreColor(val) {
  if (val >= 0.80) return "cai-excellent";
  if (val >= 0.65) return "cai-good";
  if (val >= 0.45) return "cai-adequate";
  return "cai-poor";
}

function verdictColor(verdict) {
  if (verdict === "significant lift") return "cai-verdict--significant";
  if (verdict === "moderate lift") return "cai-verdict--moderate";
  if (verdict === "slight lift") return "cai-verdict--slight";
  if (verdict === "neutral") return "cai-verdict--neutral";
  return "cai-verdict--negative";
}

const DIM_LABELS = {
  instruction_following: "Instruction Following",
  reasoning_depth: "Reasoning Depth",
  actionability: "Actionability",
  structure_compliance: "Structure Compliance",
  cognitive_scaffolding: "Cognitive Scaffolding",
};

export default function CAIScoreCard({
  templateName,
  hasKey = false,
  provider = "openai",
  onError,
  compact = false,
}) {
  const navigate = useNavigate();
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [inlineError, setInlineError] = useState("");
  const [elapsed, setElapsed] = useState(0);
  const [showInfo, setShowInfo] = useState(false);
  const [localProvider, setLocalProvider] = useState(provider);
  const [localModel, setLocalModel] = useState("");

  async function handleMeasure() {
    if (!question.trim() || !templateName) return;
    if (!hasKey) {
      setInlineError("You need an API key to measure CAI. Add one in Settings.");
      return;
    }
    setLoading(true);
    setResult(null);
    setInlineError("");
    setElapsed(0);

    const timer = setInterval(() => setElapsed((s) => s + 1), 1000);

    try {
      const res = await api.measureCAI(question, templateName, localProvider, "fast");
      setResult(res);
    } catch (e) {
      const msg = e.message || "Measurement failed. Check your API key and try again.";
      setInlineError(msg);
      if (onError) onError(msg);
    } finally {
      clearInterval(timer);
      setLoading(false);
    }
  }

  return (
    <div className={`cai-scorecard ${compact ? "cai-scorecard--compact" : ""}`}>
      <div className="cai-header">
        <h4 className="cai-title">Context Amplification Index (CAI)</h4>
        <button
          className="cai-info-toggle"
          onClick={() => setShowInfo((v) => !v)}
          title="What is CAI?"
        >
          {showInfo ? "\u2715" : "\u2139"}
        </button>
      </div>

      {showInfo && (
        <div className="cai-info-panel fade-in">
          <p><strong>What is CAI?</strong></p>
          <p>
            The Context Amplification Index measures how much a cognitive template
            improves LLM output quality compared to a plain prompt. It is one of
            three evaluation pillars in mycontext:
          </p>
          <ul>
            <li><strong>Intrinsic Quality</strong> &mdash; scores the prompt/context
              structure itself (role clarity, specificity, cognitive scaffolding)</li>
            <li><strong>Extrinsic Quality</strong> &mdash; scores the LLM&rsquo;s actual
              response on 5 dimensions (instruction following, reasoning depth,
              actionability, structure compliance, cognitive scaffolding)</li>
            <li><strong>CAI (A/B Lift)</strong> &mdash; runs the LLM twice with
              the same question &mdash; once raw, once with the template &mdash; and
              compares the two responses. CAI &gt; 1.0 means the template amplified quality.</li>
          </ul>
          <p className="cai-info-note">
            CAI provides empirical, reproducible evidence that structured context
            engineering outperforms raw prompting.
          </p>
        </div>
      )}

      <p className="cai-subtitle">
        Sends your question to the LLM twice &mdash; once as a plain prompt, once
        using this template &mdash; then compares the two responses.
      </p>

      <div className="cai-input-row">
        <div className="cai-provider-row">
          <div className="cai-provider-option">
            <label>Provider</label>
            <select value={localProvider} onChange={(e) => { setLocalProvider(e.target.value); setLocalModel(""); }}>
              {PROVIDERS.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
          <div className="cai-provider-option">
            <label>Model</label>
            <select value={localModel} onChange={(e) => setLocalModel(e.target.value)}>
              <option value="">Auto (default)</option>
              {modelsForProvider(localProvider).map((m) => (
                <option key={m.id} value={m.id}>{m.label} ({m.tier})</option>
              ))}
            </select>
          </div>
        </div>

        <textarea
          className="cai-question"
          placeholder="Enter a question relevant to this template..."
          value={question}
          onChange={(e) => { setQuestion(e.target.value); setInlineError(""); }}
          rows={2}
        />

        <div className="cai-prompt-tip">
          <strong>Tip:</strong> Write your question the way you would naturally ask the
          LLM <em>without</em> any template. Include domain context so the raw
          prompt is a fair baseline. For example, for a data analysis template:{" "}
          <em>&ldquo;How should I analyze our sales data to find what caused the spike in
          customer churn last quarter?&rdquo;</em> &mdash; not just{" "}
          <em>&ldquo;Why did churn spike?&rdquo;</em>
        </div>

        <div className="cai-actions">
          <button
            className="cai-measure-btn"
            onClick={handleMeasure}
            disabled={loading || !question.trim()}
          >
            {loading ? (
              <span className="cai-btn-loading">
                <span className="cai-spinner" />
                {"Measuring\u2026"} {elapsed > 0 && `(${elapsed}s)`}
              </span>
            ) : (
              "Measure CAI"
            )}
          </button>
        </div>

        {!hasKey && (
          <div className="cai-key-banner">
            <span className="cai-key-banner-icon">&#x1F511;</span>
            <div>
              <strong>API key required</strong>
              <p>CAI executes the LLM to compare responses. Add a key in{" "}
                <span className="cai-link" onClick={() => navigate("/account")} role="button" tabIndex={0}>Settings</span>.
              </p>
            </div>
          </div>
        )}
      </div>

      {loading && (
        <div className="cai-loading-box fade-in">
          <div className="cai-loading-spinner" />
          <div className="cai-loading-text">
            <strong>Running CAI measurement</strong>
            <p>Executing LLM with raw prompt, then with template context. This typically takes 10&ndash;30 seconds.</p>
            <div className="cai-loading-steps">
              <span className={elapsed >= 0 ? "cai-step-active" : ""}>1. Raw prompt &rarr; LLM response</span>
              <span className={elapsed >= 5 ? "cai-step-active" : ""}>2. Template context &rarr; LLM response</span>
              <span className={elapsed >= 12 ? "cai-step-active" : ""}>3. Scoring &amp; comparing</span>
            </div>
          </div>
        </div>
      )}

      {inlineError && !loading && (
        <div className="cai-error-box fade-in">
          <span className="cai-error-icon">&#x26A0;</span>
          <div>
            <strong>Measurement failed</strong>
            <p>{inlineError}</p>
          </div>
          <button className="cai-error-dismiss" onClick={() => setInlineError("")}>&times;</button>
        </div>
      )}

      {result && (
        <div className="cai-result fade-in">
          <div className="cai-hero">
            <div className={`cai-overall-badge ${verdictColor(result.verdict)}`}>
              <span className="cai-overall-value">{result.cai_overall}x</span>
              <span className="cai-overall-label">{result.verdict}</span>
            </div>
            <div className="cai-hero-scores">
              <div className={`cai-hero-score ${scoreColor(result.raw_score?.overall || 0)}`}>
                <span className="cai-hero-value">{((result.raw_score?.overall || 0) * 100).toFixed(0)}%</span>
                <span className="cai-hero-label">Raw Prompt</span>
              </div>
              <span className="cai-hero-arrow">&rarr;</span>
              <div className={`cai-hero-score ${scoreColor(result.templated_score?.overall || 0)}`}>
                <span className="cai-hero-value">{((result.templated_score?.overall || 0) * 100).toFixed(0)}%</span>
                <span className="cai-hero-label">Templated</span>
              </div>
            </div>
          </div>

          {result.cai_dimensions && (
            <div className="cai-dimensions">
              <h5>Per-Dimension Amplification</h5>
              {Object.entries(result.cai_dimensions).map(([key, val]) => {
                const rawDim = result.raw_score?.dimensions?.[key] || 0;
                const tmplDim = result.templated_score?.dimensions?.[key] || 0;
                return (
                  <div key={key} className="cai-dim-row">
                    <span className="cai-dim-name">{DIM_LABELS[key] || key}</span>
                    <div className="cai-dim-bars">
                      <div className="cai-dim-bar-pair">
                        <div className="cai-dim-bar cai-dim-bar--raw">
                          <div
                            className="cai-dim-bar-fill cai-dim-bar-fill--raw"
                            style={{ width: (rawDim * 100).toFixed(0) + "%" }}
                          />
                        </div>
                        <div className="cai-dim-bar cai-dim-bar--tmpl">
                          <div
                            className="cai-dim-bar-fill cai-dim-bar-fill--tmpl"
                            style={{ width: (tmplDim * 100).toFixed(0) + "%" }}
                          />
                        </div>
                      </div>
                    </div>
                    <span className="cai-dim-cai">{val.toFixed(2)}x</span>
                  </div>
                );
              })}
              <div className="cai-dim-legend">
                <span className="cai-legend-raw">Raw</span>
                <span className="cai-legend-tmpl">Templated</span>
              </div>
            </div>
          )}

          {!compact && result.raw_output && (
            <details className="cai-output-details">
              <summary>Compare LLM responses</summary>
              <div className="cai-output-pair">
                <div className="cai-output-box">
                  <h6>LLM Response (raw prompt)</h6>
                  <pre>{result.raw_output}</pre>
                </div>
                <div className="cai-output-box">
                  <h6>LLM Response (with template)</h6>
                  <pre>{result.templated_output}</pre>
                </div>
              </div>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
