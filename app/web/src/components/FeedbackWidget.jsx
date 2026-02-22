import { useState } from "react";
import { submitFeedback } from "../api/client";
import "./FeedbackWidget.css";

const TYPES = [
  { id: "bug", label: "Bug Report" },
  { id: "feature", label: "Feature Request" },
  { id: "general", label: "General Feedback" },
];

export default function FeedbackWidget() {
  const [open, setOpen] = useState(false);
  const [type, setType] = useState("general");
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!message.trim()) return;
    setError("");
    try {
      await submitFeedback(type, message, window.location.href);
      setSent(true);
      setTimeout(() => { setOpen(false); setSent(false); setMessage(""); }, 2000);
    } catch {
      setError("Could not send feedback. Please try again.");
    }
  }

  return (
    <>
      <button type="button" className="feedback-trigger" onClick={() => setOpen(!open)} aria-label="Send feedback">
        ?
      </button>
      {open && (
        <div className="feedback-panel fade-in">
          {sent ? (
            <div className="feedback-thanks">
              <p>Thanks for your feedback!</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <h3>Send Feedback</h3>
              <div className="feedback-types">
                {TYPES.map((t) => (
                  <button
                    key={t.id}
                    type="button"
                    className={`feedback-type ${type === t.id ? "active" : ""}`}
                    onClick={() => setType(t.id)}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Tell us what you think..."
                rows={4}
              />
              {error && <p className="feedback-error">{error}</p>}
              <button type="submit" className="feedback-submit" disabled={!message.trim()}>
                Send
              </button>
            </form>
          )}
        </div>
      )}
    </>
  );
}
