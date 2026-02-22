/**
 * Shared model catalog used by CopilotPanel, Settings, and other components.
 * Each entry: { id, provider, label, tier }
 *   - id:       LiteLLM-compatible model name
 *   - provider: openai | anthropic | google
 *   - label:    Human-friendly name
 *   - tier:     best | mid | fast
 */

export const MODEL_CATALOG = [
  { id: "gpt-5.2",                     provider: "openai",    label: "GPT-5.2",              tier: "best" },
  { id: "gpt-4.1",                     provider: "openai",    label: "GPT-4.1",              tier: "mid" },
  { id: "gpt-4.1-mini",               provider: "openai",    label: "GPT-4.1 Mini",         tier: "fast" },
  { id: "claude-sonnet-4-6",          provider: "anthropic", label: "Claude Sonnet 4.6",    tier: "best" },
  { id: "claude-3-7-sonnet-20250219", provider: "anthropic", label: "Claude 3.7 Sonnet",    tier: "mid" },
  { id: "claude-haiku-4-5",           provider: "anthropic", label: "Claude Haiku 4.5",     tier: "fast" },
  { id: "gemini-2.5-pro",             provider: "google",    label: "Gemini 2.5 Pro",       tier: "best" },
  { id: "gemini-2.5-flash",           provider: "google",    label: "Gemini 2.5 Flash",     tier: "mid" },
  { id: "gemini-2.0-flash",           provider: "google",    label: "Gemini 2.0 Flash",     tier: "fast" },
];

/** Get models for a specific provider */
export function modelsForProvider(provider) {
  return MODEL_CATALOG.filter((m) => m.provider === provider);
}

/** Get the default (fast-tier) model for a provider */
export function defaultModelForProvider(provider) {
  const fast = MODEL_CATALOG.find((m) => m.provider === provider && m.tier === "fast");
  return fast || MODEL_CATALOG.find((m) => m.provider === provider) || MODEL_CATALOG[2];
}

/** All unique provider names */
export const PROVIDERS = [...new Set(MODEL_CATALOG.map((m) => m.provider))];
