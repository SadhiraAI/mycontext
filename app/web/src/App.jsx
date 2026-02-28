import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import Layout from "./components/Layout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import VerifyEmail from "./pages/VerifyEmail";
import Dashboard from "./pages/Dashboard";
import Templates from "./pages/Templates";
import ChainBuilder from "./pages/ChainBuilder";
import CustomTemplates from "./pages/CustomTemplates";
import Account from "./pages/Account";
import Settings from "./pages/Settings";
import Academy from "./pages/Academy";

import Changelog from "./pages/Changelog";
import NotFound from "./pages/NotFound";
import ErrorBoundary from "./components/ErrorBoundary";

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading-screen">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function HomeOrApp() {
  const { user, loading } = useAuth();
  const { pathname } = useLocation();
  if (loading) return <div className="loading-screen">Loading...</div>;
  if (!user) {
    if (pathname !== "/") return <Navigate to="/" replace />;
    return <Landing />;
  }
  return <Layout />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/verify-email" element={<VerifyEmail />} />
      <Route path="/" element={<HomeOrApp />}>
        <Route index element={<Dashboard />} />
        <Route path="templates" element={<Templates />} />
        <Route path="chains" element={<ChainBuilder />} />
        <Route path="custom" element={<ErrorBoundary><CustomTemplates /></ErrorBoundary>} />
        <Route path="academy" element={<Academy />} />
        {/* Tutorial route removed — will be rebuilt */}
        <Route path="account" element={<Account />} />
        <Route path="settings" element={<Settings />} />
        <Route path="help" element={<Navigate to="/academy" replace />} />
        <Route path="changelog" element={<Changelog />} />
        <Route path="*" element={<NotFound />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
