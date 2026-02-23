const API_BASE = import.meta.env.VITE_API_URL || "/api";

function getToken() {
  return localStorage.getItem("token");
}

function getHeaders() {
  const token = getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  return headers;
}

function userFriendlyMessage(data, status) {
  const raw = data?.detail ?? data?.message ?? "";
  if (typeof raw === "string" && raw) return raw;
  if (Array.isArray(raw) && raw[0]?.msg) return raw[0].msg;
  if (status === 401) return "Please log in again.";
  if (status >= 500) return "Server error. Please try again.";
  if (status >= 400) return "Request failed. Please check your input.";
  return "Something went wrong. Please try again.";
}

async function handleResponse(res) {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = userFriendlyMessage(data, res.status);
    const err = new Error(msg);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export async function signup(email, password) {
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}

export async function login(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}

export async function getMe() {
  const res = await fetch(`${API_BASE}/auth/me`, { headers: getHeaders() });
  return handleResponse(res);
}

export async function listKeys() {
  const res = await fetch(`${API_BASE}/keys`, { headers: getHeaders() });
  return handleResponse(res);
}

export async function addKey(provider, apiKey) {
  const res = await fetch(`${API_BASE}/keys`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ provider, api_key: apiKey }),
  });
  return handleResponse(res);
}

export async function deleteKey(provider) {
  const res = await fetch(`${API_BASE}/keys/${provider}`, {
    method: "DELETE",
    headers: getHeaders(),
  });
  return handleResponse(res);
}

export async function listTemplates() {
  const res = await fetch(`${API_BASE}/templates`, { headers: getHeaders() });
  return handleResponse(res);
}

export async function getTemplateParams(name) {
  const res = await fetch(`${API_BASE}/templates/${encodeURIComponent(name)}/params`, {
    headers: getHeaders(),
  });
  return handleResponse(res);
}

export async function listCustomTemplates() {
  const res = await fetch(`${API_BASE}/templates/custom`, { headers: getHeaders() });
  return handleResponse(res);
}

export async function createCustomTemplate(data) {
  const res = await fetch(`${API_BASE}/templates/custom`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function getCustomTemplate(id) {
  const res = await fetch(`${API_BASE}/templates/custom/${id}`, { headers: getHeaders() });
  return handleResponse(res);
}

export async function updateCustomTemplate(id, data) {
  const res = await fetch(`${API_BASE}/templates/custom/${id}`, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function deleteCustomTemplate(id) {
  const res = await fetch(`${API_BASE}/templates/custom/${id}`, {
    method: "DELETE",
    headers: getHeaders(),
  });
  return handleResponse(res);
}

export async function buildCustomTemplate(id, params, outputFormat = null) {
  const body = { params };
  if (outputFormat) body.output_format = outputFormat;
  const res = await fetch(`${API_BASE}/templates/custom/${id}/build`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

/** Build from template definition without saving. For example panel. */
export async function buildCustomPreview(definition, params = {}, outputFormat = null) {
  const body = {
    guidance: definition.guidance,
    directive_template: definition.directive_template,
    input_schema: definition.input_schema || [],
    params,
    output_format: outputFormat || null,
    constraints: definition.constraints || null,
    thinking_strategy: definition.thinking_strategy || "direct",
    examples: definition.examples || null,
    output_schema: definition.output_schema || null,
  };
  const res = await fetch(`${API_BASE}/templates/custom/build-preview`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function buildTemplate(name, params, options = {}) {
  const { exportFormat = "markdown", outputFormat = null } =
    typeof options === "string" ? { exportFormat: options } : options;
  const body = { params, export_format: exportFormat };
  if (outputFormat) body.output_format = outputFormat;
  const res = await fetch(`${API_BASE}/templates/${encodeURIComponent(name)}/build`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function suggestChain(question, options = {}) {
  const res = await fetch(`${API_BASE}/chains/suggest`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ question, ...options }),
  });
  return handleResponse(res);
}

export async function evaluateQuality(assembledContent, mode = "fast", provider = "openai") {
  const res = await fetch(`${API_BASE}/quality/evaluate`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      assembled_content: assembledContent,
      mode,
      provider,
    }),
  });
  return handleResponse(res);
}

export async function transformQuestion(question) {
  const res = await fetch(`${API_BASE}/transform`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ question }),
  });
  return handleResponse(res);
}

export async function executeChain(chain, chainParams, initialInput, topic, maxCharsPerStep) {
  const res = await fetch(`${API_BASE}/chains/execute`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      chain,
      chain_params: chainParams,
      initial_input: initialInput,
      topic: topic || "Task",
      max_chars_per_step: maxCharsPerStep ?? 4000,
    }),
  });
  return handleResponse(res);
}

export async function evaluateOutput(assembledContent, llmOutput, mode = "fast", provider = "openai") {
  const res = await fetch(`${API_BASE}/evaluate/output`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      assembled_content: assembledContent,
      llm_output: llmOutput,
      mode,
      provider,
    }),
  });
  return handleResponse(res);
}

export async function measureCAI(question, templateName, provider = "openai", evalMode = "fast") {
  const res = await fetch(`${API_BASE}/evaluate/cai`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      question,
      template_name: templateName,
      provider,
      eval_mode: evalMode,
    }),
  });
  return handleResponse(res);
}

export async function runBenchmark(templateName, provider = "openai", evalMode = "fast") {
  const res = await fetch(`${API_BASE}/evaluate/benchmark`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      template_name: templateName,
      provider,
      eval_mode: evalMode,
    }),
  });
  return handleResponse(res);
}

export async function executeContext(assembledContent, provider = "openai", userMessage = "", outputFormat = null) {
  const body = {
    assembled_content: assembledContent,
    provider,
    user_message: userMessage,
  };
  if (outputFormat) body.output_format = outputFormat;
  const res = await fetch(`${API_BASE}/execute`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function getActiveProvider() {
  const res = await fetch(`${API_BASE}/keys/active`, { headers: getHeaders() });
  return handleResponse(res);
}

export async function setActiveProvider(provider) {
  const res = await fetch(`${API_BASE}/keys/${provider}/activate`, {
    method: "PUT",
    headers: getHeaders(),
  });
  return handleResponse(res);
}

export async function updatePreferredModel(provider, model) {
  const res = await fetch(`${API_BASE}/keys/${provider}/model`, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify({ model }),
  });
  return handleResponse(res);
}

/** Copilot streaming chat. Calls onChunk(chunk, fullSoFar) for each chunk. */
export async function copilotChatStream(messages, options, onChunk) {
  const { mode = "guide", provider, model, currentContext, qualityScore } = options || {};
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      messages,
      mode,
      provider: provider || "openai",
      model: model || null,
      current_context: currentContext || null,
      quality_score: qualityScore || null,
      stream: true,
    }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(userFriendlyMessage(data, res.status));
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let fullSoFar = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value, { stream: true });
    const lines = text.split(/\n/);
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const json = line.slice(6);
        if (json === "[DONE]" || json.trim() === "") continue;
        try {
          const data = JSON.parse(json);
          if (data.error) throw new Error(data.error);
          if (data.done) return;
          if (data.chunk) {
            fullSoFar += data.chunk;
            onChunk(data.chunk, fullSoFar);
          }
        } catch (e) {
          if (e instanceof SyntaxError) continue;
          throw e;
        }
      }
    }
  }
}

/** Copilot quality-gated refinement. */
export async function copilotRefine(assembledContent, provider = "openai", model = null) {
  const res = await fetch(`${API_BASE}/chat/refine`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      assembled_content: assembledContent,
      provider,
      model,
    }),
  });
  return handleResponse(res);
}

/** Get the filled generic prompt for a template. */
export async function getGenericPrompt(name, question) {
  const res = await fetch(`${API_BASE}/templates/${encodeURIComponent(name)}/generic-prompt`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ question }),
  });
  return handleResponse(res);
}

/** Compile templates into a single prompt (dynamic, LLM-refined). */
export async function compilePrompt(question, templateNames, provider = "openai", refine = true) {
  const res = await fetch(`${API_BASE}/chains/compile-prompt`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ question, template_names: templateNames, provider, refine }),
  });
  return handleResponse(res);
}

/** Compile generic prompts statically — zero LLM calls. */
export async function compileGeneric(question, templateNames) {
  const res = await fetch(`${API_BASE}/chains/compile-generic`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ question, template_names: templateNames }),
  });
  return handleResponse(res);
}

/** Smart three-tier execution via complexity router. */
export async function smartExecute(question, provider = "openai") {
  const res = await fetch(`${API_BASE}/execute/smart`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ question, provider }),
  });
  return handleResponse(res);
}

/** Generate integrated template from selected patterns. */
export async function integrateTemplates(question, selectedTemplates, selectionReasoning = {}, provider = "openai") {
  const res = await fetch(`${API_BASE}/chains/integrate`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      question,
      selected_templates: selectedTemplates,
      selection_reasoning: selectionReasoning,
      provider,
    }),
  });
  return handleResponse(res);
}

export async function updateProfile(data) {
  const res = await fetch(`${API_BASE}/auth/profile`, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function changePassword(currentPassword, newPassword) {
  const res = await fetch(`${API_BASE}/auth/password`, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
  });
  return handleResponse(res);
}

export async function activateLicense(key) {
  const res = await fetch(`${API_BASE}/license/activate`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ key }),
  });
  return handleResponse(res);
}

export async function verifyEmail(token) {
  const res = await fetch(`${API_BASE}/auth/verify-email?token=${encodeURIComponent(token)}`, {
    headers: getHeaders(),
  });
  return handleResponse(res);
}

export async function resendVerification() {
  const res = await fetch(`${API_BASE}/auth/resend-verification`, {
    method: "POST",
    headers: getHeaders(),
  });
  return handleResponse(res);
}

export async function submitFeedback(feedbackType, message, pageUrl = null) {
  const res = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({ feedback_type: feedbackType, message, page_url: pageUrl }),
  });
  return handleResponse(res);
}
