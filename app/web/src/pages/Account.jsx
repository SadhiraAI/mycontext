import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import * as api from "../api/client";
import Toast from "../components/Toast";
import "./Account.css";

export default function Account() {
  const { user, refreshUser } = useAuth();
  const [toast, setToast] = useState("");
  const [error, setError] = useState("");

  const [displayName, setDisplayName] = useState(() => user?.display_name || user?.email?.split("@")[0] || "");
  const [savingName, setSavingName] = useState(false);
  const [currentPwd, setCurrentPwd] = useState("");
  const [newPwd, setNewPwd] = useState("");
  const [confirmPwd, setConfirmPwd] = useState("");
  const [changingPwd, setChangingPwd] = useState(false);

  async function handleSaveName(e) {
    e.preventDefault();
    if (!displayName.trim()) return;
    setSavingName(true);
    setError("");
    try {
      await api.updateProfile({ display_name: displayName.trim() });
      setToast("Display name updated");
      if (refreshUser) await refreshUser();
    } catch (err) {
      setError(err.message);
    } finally {
      setSavingName(false);
    }
  }

  async function handleChangePassword(e) {
    e.preventDefault();
    setError("");
    if (!currentPwd || !newPwd) return;
    if (newPwd !== confirmPwd) {
      setError("New passwords do not match.");
      return;
    }
    if (newPwd.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    setChangingPwd(true);
    try {
      await api.changePassword(currentPwd, newPwd);
      setToast("Password changed successfully");
      setCurrentPwd("");
      setNewPwd("");
      setConfirmPwd("");
    } catch (err) {
      setError(err.message);
    } finally {
      setChangingPwd(false);
    }
  }

  return (
    <div className="account-page">
      <div className="page-header-styled">
        <span className="page-header-icon">{"\uD83D\uDC64"}</span>
        <div>
          <h1>Profile</h1>
          <p className="page-header-sub">Manage your identity and credentials.</p>
        </div>
      </div>

      {error && <p className="account-error">{error}</p>}

      <div className="account-panel">
        <div className="account-profile-card">
          <div className="account-profile-avatar">
            {(displayName || "U").charAt(0).toUpperCase()}
          </div>
          <div className="account-profile-info">
            <strong>{displayName || user?.email?.split("@")[0]}</strong>
            <span>{user?.email}</span>
            <span className={`account-plan-badge ${user?.enterprise_license ? "enterprise" : ""}`}>
              {user?.enterprise_license ? "Enterprise" : "Free"}
            </span>
          </div>
        </div>

        <form onSubmit={handleSaveName} className="account-profile-form">
          <div className="account-field">
            <label>Display Name</label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="Your name"
            />
          </div>
          <div className="account-field">
            <label>Email</label>
            <input type="email" value={user?.email || ""} disabled />
            <p className="account-field-hint">Contact support to change your email.</p>
          </div>
          <button type="submit" className="account-btn primary" disabled={savingName}>
            {savingName ? "Saving..." : "Save Profile"}
          </button>
        </form>

        <div className="account-divider" />

        <h3 className="account-subsection-title">Change Password</h3>
        <form onSubmit={handleChangePassword} className="account-pwd-form">
          <div className="account-field">
            <label>Current Password</label>
            <input
              type="password"
              value={currentPwd}
              onChange={(e) => setCurrentPwd(e.target.value)}
              placeholder="Enter current password"
            />
          </div>
          <div className="account-field">
            <label>New Password</label>
            <input
              type="password"
              value={newPwd}
              onChange={(e) => setNewPwd(e.target.value)}
              placeholder="At least 8 characters"
            />
          </div>
          <div className="account-field">
            <label>Confirm New Password</label>
            <input
              type="password"
              value={confirmPwd}
              onChange={(e) => setConfirmPwd(e.target.value)}
              placeholder="Re-enter new password"
            />
          </div>
          <button type="submit" className="account-btn primary" disabled={changingPwd || !currentPwd || !newPwd || !confirmPwd}>
            {changingPwd ? "Changing..." : "Change Password"}
          </button>
        </form>
      </div>

      {toast && <Toast message={toast} onClose={() => setToast("")} />}
    </div>
  );
}
