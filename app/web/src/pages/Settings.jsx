import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import * as api from "../api/client";
import { useTour, TOUR_KEY } from "../context/TourContext";
import { modelsForProvider, PROVIDERS } from "../config/models";
import ThemeToggle from "../components/ThemeToggle";
import Toast from "../components/Toast";
import "./Settings.css";

const TABS = ["API Keys", "Preferences", "Legal"];

export default function Settings() {
  useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { startTour } = useTour();

  const initialTab = location.state?.tab && TABS.includes(location.state.tab) ? location.state.tab : "API Keys";
  const [tab, setTab] = useState(initialTab);

  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [toast, setToast] = useState("");

  const fetchKeys = () =>
    api
      .listKeys()
      .then(setKeys)
      .catch(() => setKeys([]));

  useEffect(() => {
    fetchKeys().finally(() => setLoading(false));
  }, []);

  async function handleAdd(e) {
    e.preventDefault();
    if (!apiKey.trim()) return;
    setSubmitting(true);
    setError("");
    setSuccess("");
    try {
      await api.addKey(provider, apiKey.trim());
      await fetchKeys();
      setApiKey("");
      setToast("API key saved");
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(p) {
    try {
      await api.deleteKey(p);
      await fetchKeys();
      setToast("Key removed");
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleActivate(p) {
    setError("");
    try {
      await api.setActiveProvider(p);
      await fetchKeys();
      setToast(`${p} is now your active provider.`);
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleSetDefault(p, modelId) {
    setError("");
    try {
      await api.updatePreferredModel(p, modelId);
      await fetchKeys();
    } catch (e) {
      setError(e.message);
    }
  }

  const hasKey = (p) => keys.some((k) => k.provider === p);

  const tierBadge = (tier) => {
    const cls = tier === "best" ? "tier-best" : tier === "mid" ? "tier-mid" : "tier-fast";
    return <span className={`settings-tier-badge ${cls}`}>{tier}</span>;
  };

  return (
    <div className="settings-page">
      <div className="page-header-styled">
        <span className="page-header-icon">{"\u2699\uFE0F"}</span>
        <div>
          <h1>Settings</h1>
          <p className="page-header-sub">API keys and app preferences.</p>
        </div>
      </div>

      <div className="settings-tabs">
        {TABS.map((t) => (
          <button key={t} type="button" className={`settings-tab ${tab === t ? "active" : ""}`} onClick={() => { setTab(t); setError(""); setSuccess(""); }}>
            {t}
          </button>
        ))}
      </div>

      {error && <p className="settings-error">{error}</p>}
      {success && <p className="settings-success">{success}</p>}

      {/* ── API Keys ─────────────────────────────────────────── */}
      {tab === "API Keys" && (
        <div className="settings-panel fade-in">
          <p className="settings-intro">
            Add LLM API keys (stored encrypted). Keys are never shown after saving.
          </p>
          <p className="settings-intro-hint">
            The <strong>active</strong> provider is the global default for all
            features. Click any model chip to set it as the default for that
            provider. Each feature can still override locally.
          </p>

          <div className="settings-section">
            <h3>Your Providers</h3>
            {loading ? (
              <p className="settings-loading">Loading...</p>
            ) : keys.length === 0 ? (
              <p className="settings-loading">No API keys stored yet. Add one below.</p>
            ) : (
              <div className="settings-keys">
                {keys.map((k) => {
                  const providerModels = modelsForProvider(k.provider);
                  return (
                    <div
                      key={k.provider}
                      className={`settings-provider-card ${k.is_active ? "settings-provider-active" : ""}`}
                    >
                      <div className="settings-provider-header">
                        <div className="settings-provider-left">
                          <span className="settings-key-name">{k.provider}</span>
                          {k.is_active && (
                            <span className="settings-active-badge">Active</span>
                          )}
                        </div>
                        <div className="settings-provider-actions">
                          {!k.is_active && (
                            <button
                              type="button"
                              className="settings-activate"
                              onClick={() => handleActivate(k.provider)}
                            >
                              Activate
                            </button>
                          )}
                          <button
                            type="button"
                            onClick={() => handleDelete(k.provider)}
                            className="settings-delete"
                          >
                            Remove
                          </button>
                        </div>
                      </div>
                      <div className="settings-models-row">
                        {providerModels.map((m) => {
                          const isDefault = k.preferred_model === m.id;
                          return (
                            <button
                              key={m.id}
                              type="button"
                              className={`settings-model-chip ${isDefault ? "settings-model-default" : ""}`}
                              onClick={() => handleSetDefault(k.provider, m.id)}
                              title={isDefault ? "Current default" : `Set ${m.label} as default`}
                            >
                              <span className="settings-model-label">{m.label}</span>
                              {tierBadge(m.tier)}
                              {isDefault && <span className="settings-default-tag">default</span>}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="settings-section">
            <h3>Add key</h3>
            <form onSubmit={handleAdd} className="settings-form">
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
              >
                {PROVIDERS.map((p) => (
                  <option key={p} value={p}>
                    {p} {hasKey(p) ? "(replaces existing)" : ""}
                  </option>
                ))}
              </select>
              <input
                type="password"
                placeholder="API key"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                required
              />
              <button type="submit" disabled={submitting}>
                {submitting ? "Saving..." : "Save"}
              </button>
            </form>
          </div>

          <div className="settings-disclaimer">
            <span className="settings-disclaimer-icon">&#x1F512;</span>
            <div>
              <strong>Security &amp; Privacy</strong>
              <p>Your API keys are encrypted at rest using AES-256 (Fernet) encryption and are never logged, displayed after saving, or shared with third parties. Keys are decrypted only at the moment of an API call to your chosen LLM provider. <strong>You are responsible for any costs</strong> incurred through your provider (e.g., OpenAI, Anthropic) when using Smart, Hybrid, or Execute features. You can remove your keys at any time. See the <button type="button" className="settings-disclaimer-link" onClick={() => { setTab("Legal"); setError(""); setSuccess(""); }}>Legal</button> tab for our full privacy notice.</p>
            </div>
          </div>
        </div>
      )}

      {/* ── Preferences ──────────────────────────────────────── */}
      {tab === "Preferences" && (
        <div className="settings-panel fade-in">
          <div className="settings-section">
            <div className="settings-pref-row">
              <div>
                <strong>Theme</strong>
                <p>Switch between light and dark mode.</p>
              </div>
              <ThemeToggle />
            </div>
          </div>

          <div className="settings-section">
            <h3>Guided Tour</h3>
            <p className="settings-tour-desc">
              Restart the guided tour to see Templates, Chain Builder, Custom, and Settings.
            </p>
            <button
              type="button"
              className="settings-tour-btn"
              onClick={() => {
                try {
                  localStorage.removeItem(TOUR_KEY);
                } catch {}
                startTour();
                navigate("/");
              }}
            >
              Start tour again
            </button>
          </div>
        </div>
      )}

      {/* ── Legal / Privacy ─────────────────────────────────── */}
      {tab === "Legal" && (
        <div className="settings-panel fade-in">
          <div className="settings-section">
            <h3>Privacy Notice</h3>
            <p className="settings-legal-updated">Last updated: February 2026</p>
            <div className="settings-legal-text">
              <p>
                <strong>mycontext AI</strong>, operated by Sadhira AI, is committed to protecting your privacy.
                This notice explains what data we collect, how we use it, and your rights.
              </p>

              <h4>Data We Collect</h4>
              <ul>
                <li><strong>Account information:</strong> Email address and a securely hashed password (bcrypt). We never store or have access to your plaintext password.</li>
                <li><strong>API keys:</strong> Your LLM provider API keys (OpenAI, Anthropic, Google, etc.) are encrypted at rest using AES-256 Fernet symmetric encryption. They are decrypted only at the moment of an API call and are never logged, displayed after initial entry, or shared with any third party.</li>
                <li><strong>Feedback:</strong> If you submit feedback, we store the message, feedback type, and page URL to improve the product.</li>
                <li><strong>Custom templates:</strong> Templates you create are stored in our database and tied to your account.</li>
              </ul>

              <h4>Data We Do Not Collect</h4>
              <ul>
                <li><strong>Prompts and outputs:</strong> The cognitive templates and chain compositions you build are processed in real-time and are <strong>not stored</strong> on our servers. When using Smart/Hybrid modes, your question is sent directly to your chosen LLM provider using your own API key.</li>
                <li><strong>Cookies:</strong> We do not use tracking cookies. Cloudflare Web Analytics is cookie-free and privacy-first.</li>
                <li><strong>Personal profiles:</strong> We do not build behavioral profiles or track browsing activity.</li>
              </ul>

              <h4>Third-Party Services</h4>
              <ul>
                <li><strong>LLM providers:</strong> When you use features that call an LLM (Smart Compose, Execute, Chat), your input is sent to the provider you selected (e.g., OpenAI, Anthropic) under their terms of service and privacy policy. We act only as a conduit.</li>
                <li><strong>Analytics:</strong> We use privacy-first, cookie-free web analytics. No personal data is collected.</li>
                <li><strong>Infrastructure:</strong> Our backend and database infrastructure is hosted on enterprise-grade cloud providers with encryption at rest and in transit for all data.</li>
              </ul>

              <h4>Your Rights</h4>
              <ul>
                <li>You can <strong>delete your API keys</strong> at any time from Settings.</li>
                <li>You can request <strong>account deletion</strong> by contacting us. We will permanently remove your account, API keys, custom templates, and all associated data.</li>
                <li>You can request a <strong>copy of your data</strong> by contacting us.</li>
              </ul>
            </div>
          </div>

          <div className="settings-section">
            <h3>Terms of Use</h3>
            <div className="settings-legal-text">
              <h4>Service Description</h4>
              <p>mycontext AI provides cognitive prompt engineering tools including pattern-based context assembly, chain composition, quality scoring, and LLM execution. Output quality depends on the LLM provider, model, and prompt you use.</p>

              <h4>Your Responsibilities</h4>
              <ul>
                <li>You are responsible for your own LLM provider API keys, their security, and any costs incurred through their use on this platform.</li>
                <li>You must not share your account credentials with others.</li>
                <li>You must comply with the terms of service of any LLM provider you use through this platform.</li>
                <li>You must not use the service for any unlawful purpose or to generate harmful content.</li>
              </ul>

              <h4>Open-Source SDK</h4>
              <ul>
                <li>All cognitive patterns are open source and available to every user at no cost.</li>
                <li>The mycontext SDK is distributed under the MIT license.</li>
                <li>You may use, modify, and redistribute the SDK in accordance with the MIT license terms.</li>
              </ul>

              <h4>Intellectual Property</h4>
              <ul>
                <li>mycontext AI, its cognitive patterns, templates, and SDK are the intellectual property of Sadhira AI.</li>
                <li>Content you generate using the service belongs to you, subject to the terms of your LLM provider.</li>
                <li>Custom templates you create belong to you.</li>
              </ul>

              <h4>Disclaimers</h4>
              <ul>
                <li>The service is provided <strong>&ldquo;as is&rdquo;</strong> and <strong>&ldquo;as available&rdquo;</strong> without warranties of any kind, express or implied.</li>
                <li>We do not guarantee the accuracy, completeness, reliability, or usefulness of any LLM-generated output.</li>
                <li>We do not guarantee uninterrupted or error-free service availability.</li>
                <li>AI-generated outputs should not be relied upon as professional, legal, medical, or financial advice.</li>
              </ul>

              <h4>Limitation of Liability</h4>
              <p>To the maximum extent permitted by law, Sadhira AI shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including loss of profits, data, or business opportunities, arising from the use of or inability to use this service. Total liability shall not exceed the amount paid for the service in the 12 months preceding the claim.</p>

              <h4>Account Termination</h4>
              <p>We reserve the right to suspend or terminate accounts that violate these terms, engage in abusive behavior, or attempt to compromise system security. You may delete your account at any time by contacting us.</p>
            </div>
          </div>

          <div className="settings-section">
            <h3>Contact</h3>
            <div className="settings-legal-text">
              <p>For privacy inquiries, data deletion requests, or legal questions:</p>
              <p><strong>Contact:</strong> <a href="https://contact.sadhiraai.com" target="_blank" rel="noopener noreferrer">contact.sadhiraai.com</a></p>
              <p><strong>Website:</strong> <a href="https://mycontext.sadhiraai.com" target="_blank" rel="noopener noreferrer">mycontext.sadhiraai.com</a></p>
              <p className="settings-legal-muted">Sadhira AI reserves the right to update these terms. Material changes will be communicated via the application.</p>
            </div>
          </div>
        </div>
      )}

      {toast && <Toast message={toast} onClose={() => setToast("")} />}
    </div>
  );
}
