import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./OnboardingWizard.css";

const INTENTS = [
  { id: "prompts", label: "I want better AI prompts", path: "/templates", desc: "Browse 85 templates and build structured contexts" },
  { id: "product", label: "I'm building an AI product", path: "/custom", desc: "Create custom templates for your use case" },
  { id: "explore", label: "I'm exploring context engineering", path: "/templates", desc: "See how structured contexts improve AI output" },
];

export default function OnboardingWizard({ onComplete }) {
  const [step, setStep] = useState(0);
  const [intent, setIntent] = useState(null);
  const navigate = useNavigate();

  function handleFinish() {
    localStorage.setItem("mc_onboarding_done", "true");
    if (onComplete) onComplete();
    if (intent) navigate(intent.path);
  }

  function handleSkip() {
    localStorage.setItem("mc_onboarding_done", "true");
    if (onComplete) onComplete();
  }

  return (
    <div className="onboard-overlay">
      <div className="onboard-card">
        {step === 0 && (
          <div className="onboard-step fade-in">
            <h1>Welcome to mycontext</h1>
            <p className="onboard-sub">The context engineering platform. Transform any question into a structured, measurable AI context.</p>
            <button type="button" className="onboard-btn primary" onClick={() => setStep(1)}>Get started</button>
            <button type="button" className="onboard-skip" onClick={handleSkip}>Skip intro</button>
          </div>
        )}

        {step === 1 && (
          <div className="onboard-step fade-in">
            <h2>What brings you here?</h2>
            <p className="onboard-sub">This helps us personalize your experience.</p>
            <div className="onboard-intents">
              {INTENTS.map((i) => (
                <button
                  key={i.id}
                  type="button"
                  className={`onboard-intent ${intent?.id === i.id ? "active" : ""}`}
                  onClick={() => setIntent(i)}
                >
                  <strong>{i.label}</strong>
                  <span>{i.desc}</span>
                </button>
              ))}
            </div>
            <div className="onboard-actions">
              <button type="button" className="onboard-btn secondary" onClick={() => setStep(0)}>Back</button>
              <button type="button" className="onboard-btn primary" onClick={() => setStep(2)} disabled={!intent}>Next</button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="onboard-step fade-in">
            <h2>How it works</h2>
            <div className="onboard-flow">
              <div className="onboard-flow-step">
                <span className="onboard-flow-num">1</span>
                <div><strong>Pick a pattern</strong><p>85 research-backed templates for analysis, reasoning, decisions, and more.</p></div>
              </div>
              <div className="onboard-flow-step">
                <span className="onboard-flow-num">2</span>
                <div><strong>Fill parameters</strong><p>Each template has clear inputs. Fill them in, we handle the structure.</p></div>
              </div>
              <div className="onboard-flow-step">
                <span className="onboard-flow-num">3</span>
                <div><strong>Export anywhere</strong><p>Download for OpenAI, Anthropic, Google, LangChain, and 9 more formats.</p></div>
              </div>
            </div>
            <div className="onboard-actions">
              <button type="button" className="onboard-btn secondary" onClick={() => setStep(1)}>Back</button>
              <button type="button" className="onboard-btn primary" onClick={handleFinish}>
                {intent ? `Go to ${intent.id === "product" ? "Custom Builder" : "Templates"}` : "Get started"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
