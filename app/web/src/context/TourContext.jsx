import { createContext, useContext, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

export const TOUR_KEY = "mycontext-tour-done";
const TOUR_DONE_VALUE = "1";

export const TOUR_STEPS = [
  { path: "/", title: "Welcome", body: "mycontext turns your questions into structured AI prompts. This quick tour will show you the main areas." },
  { path: "/templates", title: "Templates", body: "Browse 85 research-backed patterns. Pick one, fill in your content, build context, and export to any format or run with your LLM." },
  { path: "/chains", title: "Chain Builder", body: "Describe your task in plain language. We suggest a workflow chain of patterns, run them, and optionally execute the final output through your LLM." },
  { path: "/custom", title: "Custom Templates", body: "Create your own templates with role, rules, and placeholders. Build reusable prompts for your team." },
  { path: "/settings", title: "Settings", body: "Add API keys for OpenAI, Anthropic, or Google. Required for LLM execution and quality scoring." },
];

const TourContext = createContext(null);

export function TourProvider({ children }) {
  const navigate = useNavigate();
  const [active, setActive] = useState(false);
  const [step, setStep] = useState(0);
  const [dontShowAgain, setDontShowAgain] = useState(false);

  const isTourDone = useCallback(() => {
    try {
      return localStorage.getItem(TOUR_KEY) === TOUR_DONE_VALUE;
    } catch {
      return false;
    }
  }, []);

  const startTour = useCallback(() => {
    setActive(true);
    setStep(0);
    navigate("/");
  }, [navigate]);

  const nextStep = useCallback(() => {
    if (step >= TOUR_STEPS.length - 1) {
      setActive(false);
      try {
        localStorage.setItem(TOUR_KEY, TOUR_DONE_VALUE);
      } catch {}
      return;
    }
    const next = step + 1;
    setStep(next);
    navigate(TOUR_STEPS[next].path);
  }, [step, navigate]);

  const prevStep = useCallback(() => {
    if (step <= 0) return;
    const prev = step - 1;
    setStep(prev);
    navigate(TOUR_STEPS[prev].path);
  }, [step, navigate]);

  const skipTour = useCallback(() => {
    setActive(false);
    if (dontShowAgain) {
      try {
        localStorage.setItem(TOUR_KEY, TOUR_DONE_VALUE);
      } catch {}
    }
  }, [dontShowAgain]);

  const completeTour = useCallback(() => {
    setActive(false);
    try {
      localStorage.setItem(TOUR_KEY, TOUR_DONE_VALUE);
    } catch {}
  }, []);

  const value = {
    active,
    step,
    totalSteps: TOUR_STEPS.length,
    currentStep: TOUR_STEPS[step],
    dontShowAgain,
    setDontShowAgain,
    startTour,
    nextStep,
    prevStep,
    skipTour,
    completeTour,
    isTourDone,
  };

  return (
    <TourContext.Provider value={value}>
      {children}
    </TourContext.Provider>
  );
}

export function useTour() {
  const ctx = useContext(TourContext);
  if (!ctx) throw new Error("useTour must be used within TourProvider");
  return ctx;
}
