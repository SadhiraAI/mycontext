import React, { createContext, useContext, useState, useEffect, useLayoutEffect } from "react";

const STORAGE_KEY = "mycontext-theme";

const ThemeContext = createContext(null);

function getSystemTheme() {
  if (typeof window === "undefined") return "dark";
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

function getStoredTheme() {
  try {
    return localStorage.getItem(STORAGE_KEY) || "system";
  } catch {
    return "system";
  }
}

function getEffectiveTheme() {
  const stored = getStoredTheme();
  if (stored === "system") return getSystemTheme();
  return stored;
}

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState(getStoredTheme);
  const [effective, setEffective] = useState(getEffectiveTheme);

  useLayoutEffect(() => {
    document.documentElement.setAttribute("data-theme", getEffectiveTheme());
  }, []);

  useEffect(() => {
    const effectiveTheme = getEffectiveTheme();
    setEffective(effectiveTheme);
    document.documentElement.setAttribute("data-theme", effectiveTheme);
  }, [theme]);

  useEffect(() => {
    if (theme !== "system") return;
    const mq = window.matchMedia("(prefers-color-scheme: light)");
    const handler = () => {
      setEffective(getSystemTheme());
      document.documentElement.setAttribute("data-theme", getSystemTheme());
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [theme]);

  const setTheme = (value) => {
    setThemeState(value);
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch {}
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, effective }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}
