import React, { createContext, useContext, useState, useEffect } from "react";
import * as api from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    api
      .getMe()
      .then((u) => setUser(u))
      .catch(() => {
        localStorage.removeItem("token");
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    const data = await api.login(email, password);
    localStorage.setItem("token", data.access_token);
    const u = await api.getMe();
    setUser(u);
    return data;
  };

  const signup = async (email, password) => {
    const data = await api.signup(email, password);
    localStorage.setItem("token", data.access_token);
    const u = await api.getMe();
    setUser(u);
    return data;
  };

  const refreshUser = async () => {
    try {
      const u = await api.getMe();
      setUser(u);
    } catch { /* token may be expired */ }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
