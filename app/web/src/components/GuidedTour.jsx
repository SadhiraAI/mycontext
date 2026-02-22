import { useEffect, useRef } from "react";
import { useTour } from "../context/TourContext";
import "./GuidedTour.css";

export default function GuidedTour() {
  const { active, step, totalSteps, currentStep, dontShowAgain, setDontShowAgain, nextStep, prevStep, skipTour } = useTour();
  const nextRef = useRef(null);

  useEffect(() => {
    if (active && nextRef.current) nextRef.current.focus();
  }, [active, step]);

  if (!active || !currentStep) return null;

  const isLast = step === totalSteps - 1;

  return (
    <div
      className="guided-tour-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="tour-title"
      aria-describedby="tour-body"
    >
      <div className="guided-tour-backdrop" aria-hidden="true" />
      <div className="guided-tour-modal">
        <div className="guided-tour-progress">
          Step {step + 1} of {totalSteps}
        </div>
        <h2 id="tour-title" className="guided-tour-title">
          {currentStep.title}
        </h2>
        <p id="tour-body" className="guided-tour-body">
          {currentStep.body}
        </p>
        <div className="guided-tour-actions">
          <button type="button" onClick={prevStep} disabled={step === 0} className="guided-tour-btn secondary">
            Previous
          </button>
          <button type="button" ref={nextRef} onClick={nextStep} className="guided-tour-btn primary">
            {isLast ? "Finish" : "Next"}
          </button>
        </div>
        <div className="guided-tour-skip-row">
          <label className="guided-tour-dont-show">
            <input
              type="checkbox"
              checked={dontShowAgain}
              onChange={(e) => setDontShowAgain(e.target.checked)}
              aria-label="Don't show this tour again"
            />
            Don't show again
          </label>
          <button type="button" onClick={skipTour} className="guided-tour-skip">
            Skip tour
          </button>
        </div>
      </div>
    </div>
  );
}
