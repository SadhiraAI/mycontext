/**
 * Curated examples by use case for Phase 7.2 Examples Library.
 * Each example can pre-fill Templates or Chain Builder.
 */
export const EXAMPLES = [
  {
    id: "sentiment",
    useCase: "Sentiment",
    question: "This product exceeded expectations! Best purchase ever. Would recommend to everyone.",
    templates: ["pattern_recognition_engine"],
    description: "Find sentiment and tone patterns in text.",
    targetPage: "templates",
    templateName: "pattern_recognition_engine",
    params: {
      data: "This product exceeded expectations! Best purchase ever. Would recommend to everyone.",
      pattern_focus: "Sentiment and tone",
    },
  },
  {
    id: "root-cause",
    useCase: "Root Cause",
    question: "Support tickets doubled in Q2. Complaints up 40%. What's driving this?",
    templates: ["root_cause_analyzer"],
    description: "Find root causes behind symptoms or metrics.",
    targetPage: "chains",
    chainQuestion: "Support tickets doubled in Q2. Complaints up 40%. What's driving this?",
  },
  {
    id: "decision",
    useCase: "Decision",
    question: "Choose database for new service: Postgres vs MongoDB vs DynamoDB.",
    templates: ["decision_framework"],
    description: "Structured decision-making across options.",
    targetPage: "templates",
    templateName: "decision_framework",
    params: {
      decision: "Choose database for new service",
      options: ["Postgres", "MongoDB", "DynamoDB"],
      depth: "comprehensive",
    },
  },
  {
    id: "comparison",
    useCase: "Comparison",
    question: "Compare microservices vs monolith for our team of 8 engineers.",
    templates: ["comparative_analyzer"],
    description: "Side-by-side comparison with criteria.",
    targetPage: "chains",
    chainQuestion: "Compare microservices vs monolith for our team of 8 engineers.",
  },
  {
    id: "churn",
    useCase: "Churn Analysis",
    question: "Why did churn spike last quarter? Timeline, root cause, and next steps.",
    templates: ["temporal_sequence_analyzer", "root_cause_analyzer"],
    description: "Multi-step analysis: timeline then root cause.",
    targetPage: "chains",
    chainQuestion: "Why did churn spike last quarter? Timeline, root cause, and next steps.",
  },
  {
    id: "intent",
    useCase: "Intent",
    question: "I want to cancel my subscription and get a refund.",
    templates: ["intent_recognizer"],
    description: "Recognize user intent from a message.",
    targetPage: "templates",
    templateName: "intent_recognizer",
    params: {
      input: "I want to cancel my subscription and get a refund.",
      context: "Customer support",
      depth: "comprehensive",
    },
  },
];
