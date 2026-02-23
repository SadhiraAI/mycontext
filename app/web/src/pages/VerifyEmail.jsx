import { useState, useEffect } from "react";
import { Link, useSearchParams } from "react-router-dom";
import * as api from "../api/client";
import "./Auth.css";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState("verifying");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("No verification token found. Please check the link in your email.");
      return;
    }

    api.verifyEmail(token)
      .then((res) => {
        setStatus("success");
        setMessage(res.message || "Email verified successfully!");
      })
      .catch((err) => {
        setStatus("error");
        setMessage(err.message || "Verification failed. The link may be expired or invalid.");
      });
  }, [token]);

  return (
    <div className="auth-page">
      <div className="auth-card" style={{ textAlign: "center" }}>
        <h1>mycontext</h1>
        {status === "verifying" && (
          <>
            <p className="auth-sub">Verifying your email...</p>
            <div className="auth-spinner" />
          </>
        )}
        {status === "success" && (
          <>
            <p className="auth-verify-icon">&#x2705;</p>
            <p className="auth-sub">{message}</p>
            <Link to="/login" className="auth-verify-link">Sign in to your account</Link>
          </>
        )}
        {status === "error" && (
          <>
            <p className="auth-verify-icon">&#x274C;</p>
            <p className="auth-error">{message}</p>
            <Link to="/signup" className="auth-verify-link">Back to sign up</Link>
          </>
        )}
      </div>
    </div>
  );
}
