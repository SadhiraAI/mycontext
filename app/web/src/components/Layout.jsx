import { useState, useEffect, useRef } from "react";
import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import GuidedTour from "./GuidedTour";
import OnboardingWizard from "./OnboardingWizard";
import FeedbackWidget from "./FeedbackWidget";
import "./Layout.css";

export default function Layout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [showOnboarding, setShowOnboarding] = useState(() => {
    return !localStorage.getItem("mc_onboarding_done");
  });
  const [cockpitOpen, setCockpitOpen] = useState(false);
  const cockpitRef = useRef(null);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const isActive = (path) => location.pathname === path || (path !== "/" && location.pathname.startsWith(path));

  const displayName = user?.email?.split("@")[0] || "user";
  const initial = displayName.charAt(0).toUpperCase();

  useEffect(() => {
    function handleClickOutside(e) {
      if (cockpitRef.current && !cockpitRef.current.contains(e.target)) {
        setCockpitOpen(false);
      }
    }
    if (cockpitOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [cockpitOpen]);

  useEffect(() => {
    setCockpitOpen(false);
  }, [location.pathname]);

  return (
    <div className="layout">
      <header className="layout-header" role="banner">
        <Link to="/" className="layout-brand" aria-label="mycontext-ai home">
          <svg className="brand-icon-svg" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="url(#brandGrad)" strokeWidth="2.2" strokeLinecap="round"><defs><linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stopColor="#5ba8a0"/><stop offset="100%" stopColor="#8b5cf6"/></linearGradient></defs><path d="M4 6c4-2 12-2 16 0"/><path d="M4 12c4-2 12-2 16 0"/><path d="M4 18c4-2 12-2 16 0"/></svg>
          <span className="brand-my">my</span>
          <span className="brand-context">context</span>
          <span className="brand-dash">-</span>
          <span className="brand-ai">ai</span>
        </Link>
        <nav className="layout-nav" aria-label="Main navigation">
          <Link to="/" className={location.pathname === "/" ? "active" : ""}>
            <span className="nav-icon">{"\uD83C\uDFAF"}</span>
            <span className="nav-label">Launchpad</span>
            <span className="nav-tier">Mission Control</span>
          </Link>
          <Link to="/custom" className={isActive("/custom") ? "active" : ""}>
            <span className="nav-icon">{"\uD83D\uDCBB"}</span>
            <span className="nav-label">Context Studio</span>
            <span className="nav-tier">Novice</span>
          </Link>
          <Link to="/templates" className={isActive("/templates") ? "active" : ""}>
            <span className="nav-icon">{"\uD83E\uDDE0"}</span>
            <span className="nav-label">Cognitive Studio</span>
            <span className="nav-tier">Adept</span>
          </Link>
          <Link to="/chains" className={isActive("/chains") ? "active" : ""}>
            <span className="nav-icon">{"\uD83E\uDDEC"}</span>
            <span className="nav-label">Chain Composer</span>
            <span className="nav-tier">Architect</span>
          </Link>
        </nav>
        <div className="layout-user">
          <Link to="/academy" className={`layout-academy-link${isActive("/academy") ? " active" : ""}`} title="Sadhira Academy">
            <span className="layout-academy-icon">{"\uD83C\uDF93"}</span>
            <span className="layout-academy-text">Academy</span>
          </Link>

          <div className="layout-cockpit" ref={cockpitRef}>
            <button
              type="button"
              className={`layout-cockpit-trigger${cockpitOpen ? " open" : ""}`}
              onClick={() => setCockpitOpen(!cockpitOpen)}
              aria-expanded={cockpitOpen}
              aria-haspopup="true"
            >
              <span className="layout-cockpit-avatar">{initial}</span>
              <span className="layout-cockpit-name">{displayName}</span>
              <span className="layout-cockpit-chevron">{cockpitOpen ? "\u25B2" : "\u25BC"}</span>
            </button>

            {cockpitOpen && (
              <div className="layout-cockpit-dropdown">
                <div className="layout-cockpit-header">
                  <span className="layout-cockpit-header-name">{displayName}</span>
                  <span className="layout-cockpit-header-email">{user?.email}</span>
                </div>
                <div className="layout-cockpit-divider" />
                <Link to="/account" className="layout-cockpit-item">
                  <span className="layout-cockpit-item-icon">{"\uD83D\uDC64"}</span>
                  Profile
                </Link>
                <Link to="/settings" className="layout-cockpit-item">
                  <span className="layout-cockpit-item-icon">{"\u2699\uFE0F"}</span>
                  Settings
                </Link>
                <div className="layout-cockpit-divider" />
                <button type="button" className="layout-cockpit-item layout-cockpit-logout" onClick={handleLogout}>
                  <span className="layout-cockpit-item-icon">{"\uD83D\uDEAA"}</span>
                  Log out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>
      <main className="layout-main" role="main">
        <Outlet />
      </main>

      <footer className="layout-footer">
        <div className="layout-footer-info">
          <strong>Sadhira AI &amp; Analytics</strong>
          <span className="layout-footer-sep">&middot;</span>
          <span>6912 Hapsburg Lane, Henrico, VA 23231</span>
          <span className="layout-footer-sep">&middot;</span>
          <span>(804) 418-2759</span>
          <span className="layout-footer-sep">&middot;</span>
          <a href="mailto:dhirajp@sadhiraai.com">dhirajp@sadhiraai.com</a>
        </div>
        <div className="layout-footer-social">
          <a href="#" title="Facebook" className="layout-social-badge" aria-label="Facebook">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="#" title="X / Twitter" className="layout-social-badge" aria-label="X">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
          </a>
          <a href="#" title="LinkedIn" className="layout-social-badge" aria-label="LinkedIn">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
          <a href="#" title="GitHub" className="layout-social-badge" aria-label="GitHub">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
          </a>
        </div>
      </footer>

      <GuidedTour />
      {showOnboarding && <OnboardingWizard onComplete={() => setShowOnboarding(false)} />}
      <FeedbackWidget />
    </div>
  );
}
