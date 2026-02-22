import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import ThemeToggle from "../components/ThemeToggle";
import "./Auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-theme">
        <Link to="/" className="auth-back">← Back</Link>
        <ThemeToggle />
      </div>
      <div className="auth-card">
        <h1>mycontext</h1>
        <p className="auth-sub">Sign in to continue</p>
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="current-password" />
          {error && <p className="auth-error">{error}</p>}
          <button type="submit" disabled={loading}>{loading ? "Signing in…" : "Sign in"}</button>
        </form>
        <p className="auth-switch">No account? <Link to="/signup">Sign up</Link></p>
      </div>
    </div>
  );
}
