import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import * as api from "../api/client";
import { useTour, TOUR_KEY } from "../context/TourContext";
import { modelsForProvider, PROVIDERS } from "../config/models";
import ThemeToggle from "../components/ThemeToggle";
import Toast from "../components/Toast";
import "./Settings.css";

const TABS = ["API Keys", "License", "Preferences"];

export default function Settings() {
  const { user, refreshUser } = useAuth();
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

  const [licenseKey, setLicenseKey] = useState("");
  const [activating, setActivating] = useState(false);

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

  async function handleActivateLicense(e) {
    e.preventDefault();
    if (!licenseKey.trim()) return;
    setActivating(true);
    setError("");
    setSuccess("");
    try {
      const res = await api.activateLicense(licenseKey.trim());
      setSuccess(res.message || "Enterprise license activated!");
      setLicenseKey("");
      setToast("Enterprise license activated!");
      if (refreshUser) await refreshUser();
    } catch (err) {
      setError(err.message);
    } finally {
      setActivating(false);
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
          <p className="page-header-sub">API keys, license management, and app preferences.</p>
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
        </div>
      )}

      {/* ── License ──────────────────────────────────────────── */}
      {tab === "License" && (
        <div className="settings-panel fade-in">
          <div className="settings-section">
            <div className="settings-license-current">
              <span className={`settings-plan-badge ${user?.enterprise_license ? "enterprise" : ""}`}>
                {user?.enterprise_license ? "Enterprise" : "Free Edition"}
              </span>
              <p className="settings-license-desc">
                {user?.enterprise_license
                  ? "Full access to all 85 patterns."
                  : "Access to 16 free patterns. Upgrade to Enterprise for 69 advanced patterns."}
              </p>
            </div>

            {!user?.enterprise_license && (
              <div className="settings-license-activate">
                <h3>Activate Enterprise License</h3>
                <p className="settings-intro-hint">Enter your license key to unlock all 85 cognitive patterns, advanced decision-making, systems thinking, and ethical reasoning frameworks.</p>
                <form onSubmit={handleActivateLicense} className="settings-form">
                  <input
                    type="text"
                    placeholder="MC-ENT-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                    value={licenseKey}
                    onChange={(e) => setLicenseKey(e.target.value)}
                    disabled={activating}
                    style={{ fontFamily: "var(--font-mono, monospace)", letterSpacing: "0.04em" }}
                  />
                  <button type="submit" disabled={activating || !licenseKey.trim()}>
                    {activating ? "Activating..." : "Activate"}
                  </button>
                </form>
                <p className="settings-license-help">
                  Need a license key? Contact <strong>dhirajp@sadhiraai.com</strong> or visit our website.
                </p>
              </div>
            )}

            {user?.enterprise_license && (
              <div className="settings-license-active-banner">
                <span className="settings-license-check">&#x2705;</span>
                <div>
                  <strong>Enterprise license is active</strong>
                  <p>You have full access to all 85 cognitive patterns and advanced features.</p>
                </div>
              </div>
            )}
          </div>

          <div className="settings-section">
            <h3>Feature Comparison</h3>
            <table className="settings-compare-table">
              <thead><tr><th>Feature</th><th>Free</th><th>Enterprise</th></tr></thead>
              <tbody>
                <tr><td>Cognitive patterns</td><td>16</td><td>85</td></tr>
                <tr><td>Export formats</td><td>13</td><td>13</td></tr>
                <tr><td>Custom templates</td><td>Yes</td><td>Yes</td></tr>
                <tr><td>Quality scoring</td><td>Heuristic</td><td>Heuristic + LLM</td></tr>
                <tr><td>Decision patterns</td><td>-</td><td>Yes</td></tr>
                <tr><td>Systems thinking</td><td>-</td><td>Yes</td></tr>
                <tr><td>Ethical reasoning</td><td>-</td><td>Yes</td></tr>
              </tbody>
            </table>
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

      {toast && <Toast message={toast} onClose={() => setToast("")} />}
    </div>
  );
}
