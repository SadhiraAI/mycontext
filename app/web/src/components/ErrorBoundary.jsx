import { Component } from "react";

export default class ErrorBoundary extends Component {
  state = { error: null };

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error("ErrorBoundary caught:", error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="error-boundary" style={{ padding: "1.5rem", maxWidth: "600px" }}>
          <h2 style={{ marginBottom: "0.5rem" }}>Something went wrong</h2>
          <p style={{ color: "var(--text-muted)", marginBottom: "1rem" }}>{String(this.state.error?.message || this.state.error)}</p>
          <button type="button" onClick={() => this.setState({ error: null })} className="error-boundary-retry">
            Dismiss
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
