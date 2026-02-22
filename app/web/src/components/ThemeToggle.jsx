import { useState, useRef, useEffect } from "react";
import { useTheme } from "../context/ThemeContext";
import "./ThemeToggle.css";

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="theme-toggle" ref={ref}>
      <button
        type="button"
        className="theme-toggle-btn"
        onClick={() => setOpen((o) => !o)}
        title="Theme"
        aria-label="Choose theme"
      >
        <span className="theme-icon" aria-hidden="true">
          {theme === "light" ? "☀" : theme === "dark" ? "🌙" : "◐"}
        </span>
      </button>
      {open && (
        <div className="theme-dropdown">
          <button
            type="button"
            className={theme === "light" ? "active" : ""}
            onClick={() => { setTheme("light"); setOpen(false); }}
          >
            Light
          </button>
          <button
            type="button"
            className={theme === "dark" ? "active" : ""}
            onClick={() => { setTheme("dark"); setOpen(false); }}
          >
            Dark
          </button>
          <button
            type="button"
            className={theme === "system" ? "active" : ""}
            onClick={() => { setTheme("system"); setOpen(false); }}
          >
            System
          </button>
        </div>
      )}
    </div>
  );
}
