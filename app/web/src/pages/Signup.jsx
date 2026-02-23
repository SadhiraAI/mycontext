import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import ThemeToggle from "../components/ThemeToggle";
import "./Auth.css";

const PW_RULES = [
  { test: (p) => p.length >= 8, label: "At least 8 characters" },
  { test: (p) => /[A-Z]/.test(p), label: "One uppercase letter" },
  { test: (p) => /[a-z]/.test(p), label: "One lowercase letter" },
  { test: (p) => /\d/.test(p), label: "One digit" },
];

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [verificationSent, setVerificationSent] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const allRulesPass = PW_RULES.every((r) => r.test(password));

  async function handleSubmit(e) {
    e.preventDefault();
    if (!allRulesPass) {
      setError("Please meet all password requirements.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const res = await signup(email, password);
      if (res?.verification_sent) {
        setVerificationSent(true);
      } else {
        navigate("/");
      }
    } catch (err) {
      setError(err.message || "Signup failed");
    } finally {
      setLoading(false);
    }
  }

  if (verificationSent) {
    return (
      <div className="auth-page">
        <div className="auth-card" style={{ textAlign: "center" }}>
          <h1>mycontext</h1>
          <p className="auth-verify-icon">&#x2709;&#xFE0F;</p>
          <p className="auth-sub">Check your email</p>
          <p className="auth-verify-msg">
            We sent a verification link to <strong>{email}</strong>.
            Click the link to activate your account, then sign in.
          </p>
          <Link to="/login" className="auth-verify-link">Go to sign in</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-page">
      <div className="auth-theme">
        <Link to="/" className="auth-back">&larr; Back</Link>
        <ThemeToggle />
      </div>
      <div className="auth-card">
        <h1>mycontext</h1>
        <p className="auth-sub">Create an account</p>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email (no disposable emails)"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoComplete="email"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="new-password"
            minLength={8}
          />
          {password.length > 0 && (
            <ul className="auth-pw-rules">
              {PW_RULES.map((r) => (
                <li key={r.label} className={r.test(password) ? "pass" : "fail"}>
                  <span className="auth-pw-check">{r.test(password) ? "\u2713" : "\u2717"}</span>
                  {r.label}
                </li>
              ))}
            </ul>
          )}
          {error && <p className="auth-error">{error}</p>}
          <button type="submit" disabled={loading || !allRulesPass}>
            {loading ? "Creating\u2026" : "Create account"}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
