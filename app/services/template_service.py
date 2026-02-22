"""Template service: wrap get_pattern_class, build_context, and rich metadata for all 85 templates."""

from typing import Any

try:
    from mycontext.intelligence import get_pattern_class
    from mycontext.intelligence.chain_orchestration_agent import PATTERN_BUILD_CONTEXT_REGISTRY
    from mycontext.intelligence.pattern_catalog import FULL_PATTERN_CATALOG
    from mycontext.intelligence.prompt_composer import get_generic_prompt_for
except ImportError:
    get_pattern_class = None
    PATTERN_BUILD_CONTEXT_REGISTRY = {}
    FULL_PATTERN_CATALOG = []
    get_generic_prompt_for = None


# ---------------------------------------------------------------------------
# Cross-cutting themes (independent of license category)
# ---------------------------------------------------------------------------
THEMES = [
    "Strategic Thinking",
    "Problem Investigation",
    "Data & Analytics",
    "Communication & Clarity",
    "Innovation & Creativity",
    "Risk & Compliance",
    "Learning & Development",
    "Systems & Complexity",
    "Evaluation & Quality",
    "Self-Improvement",
    "Project Management",
    "Ethics & Governance",
]


# ---------------------------------------------------------------------------
# TEMPLATE_METADATA  –  all 85 templates
# Keys: description, use_cases, parameter_descriptions, research_basis, theme
# ---------------------------------------------------------------------------
TEMPLATE_METADATA: dict[str, dict[str, Any]] = {
    # ── FREE — Analysis (6) ──────────────────────────────────────────────
    "question_analyzer": {
        "description": "Systematic decomposition of questions into type, scope, assumptions, and requirements.",
        "use_cases": ["Unclear requirements", "Multi-part questions", "Pre-analysis triage", "Customer support intake"],
        "parameter_descriptions": {
            "question": "The question or problem statement to analyze",
            "context": "Domain or background (e.g. 'customer success', 'engineering')",
            "depth": "Analysis depth: quick, standard, or comprehensive",
        },
        "research_basis": "Graesser & Person (1994) question taxonomy; Bloom's Taxonomy (Anderson & Krathwohl, 2001); IBM Watson DeepQA question analysis pipeline (Ferrucci et al., 2010).",
        "theme": "Data & Analytics",
    },
    "data_analyzer": {
        "description": "Structured framework for identifying trends, anomalies, and patterns in data.",
        "use_cases": ["Sales analysis", "Metrics review", "Dashboard insights", "Quarterly business reports"],
        "parameter_descriptions": {
            "data_description": "Description of the dataset or key data points",
            "goal": "What to find — trends, anomalies, correlations",
            "context": "Business context or domain (e.g. 'e-commerce', 'SaaS metrics')",
        },
        "research_basis": "Tukey (1977) Exploratory Data Analysis; CRISP-DM process model (Chapman et al., 2000); Wild & Pfannkuch (1999) statistical thinking.",
        "theme": "Data & Analytics",
    },
    "trend_identifier": {
        "description": "Systematic detection and characterization of trends over time.",
        "use_cases": ["Market trend analysis", "KPI tracking", "Technology adoption curves", "Social media monitoring"],
        "parameter_descriptions": {
            "data_description": "Time-series data or observations to analyze",
            "domain": "Domain context (e.g. 'fintech', 'healthcare')",
        },
        "research_basis": "Box & Jenkins (1976) Time Series Analysis; Gigerenzer & Brighton (2009) on heuristic-based trend detection; Cleveland & Devlin (1988) LOESS regression.",
        "theme": "Data & Analytics",
    },
    "gap_analyzer": {
        "description": "Identification of missing elements, incomplete information, and logical gaps.",
        "use_cases": ["Requirements gap analysis", "Competitive gaps", "Skills assessment", "Process audit"],
        "parameter_descriptions": {
            "current_state": "Description of the current situation",
            "desired_state": "The target or ideal state",
        },
        "research_basis": "Polya (1945) How to Solve It; Newell & Simon (1972) problem space theory; Belkin et al. (1982) ASK model for information-seeking.",
        "theme": "Strategic Thinking",
    },
    "swot_analyzer": {
        "description": "Strengths, Weaknesses, Opportunities, Threats strategic analysis.",
        "use_cases": ["Business strategy", "Product launches", "Market positioning", "Team capability assessment"],
        "parameter_descriptions": {
            "subject": "Subject of the SWOT analysis (company, product, team)",
            "context": "Industry or market context",
        },
        "research_basis": "Learned et al. (1965) Business Policy; Porter (1980) Competitive Strategy; Weihrich (1982) TOWS matrix.",
        "theme": "Strategic Thinking",
    },
    "anomaly_detector": {
        "description": "Systematic identification of outliers, anomalies, and unexpected patterns.",
        "use_cases": ["Fraud detection", "Quality control", "System monitoring", "Financial auditing"],
        "parameter_descriptions": {
            "data": "Data or observations to scan for anomalies",
            "baseline": "Expected baseline or normal behavior",
        },
        "research_basis": "Hawkins (1980) Identification of Outliers; Chandola et al. (2009) anomaly detection survey; Barnett & Lewis (1994) statistical outlier methods.",
        "theme": "Data & Analytics",
    },

    # ── FREE — Reasoning (5) ─────────────────────────────────────────────
    "root_cause_analyzer": {
        "description": "Root cause investigation using Five Whys and Ishikawa-style analysis.",
        "use_cases": ["Production outages", "Support ticket spikes", "Performance degradation", "Incident postmortems"],
        "parameter_descriptions": {
            "problem": "The issue or situation to investigate",
            "context": "Domain or operational background",
        },
        "research_basis": "Ishikawa (1986) fishbone diagrams; Ohno (1988) Five Whys from Toyota Production System; Senge (1990) systems thinking.",
        "theme": "Problem Investigation",
    },
    "step_by_step_reasoner": {
        "description": "Break down reasoning into clear, sequential, verifiable steps.",
        "use_cases": ["Logic walkthroughs", "Troubleshooting guides", "Teaching explanations", "Process documentation"],
        "parameter_descriptions": {
            "problem": "The problem or question to reason through",
            "context": "Domain context or constraints",
        },
        "research_basis": "Polya (1945) How to Solve It; Wei et al. (2022) Chain-of-Thought prompting (NeurIPS); Sweller (1988) cognitive load theory.",
        "theme": "Problem Investigation",
    },
    "causal_reasoner": {
        "description": "Systematic identification and analysis of cause-effect relationships.",
        "use_cases": ["Root cause chains", "Policy impact analysis", "Scientific reasoning", "Debugging complex systems"],
        "parameter_descriptions": {
            "phenomenon": "The effect or outcome to explain",
            "context": "Domain or situational background",
        },
        "research_basis": "Pearl (2009) Causality; Sloman (2005) causal mental models; Kahneman & Miller (1986) counterfactual reasoning.",
        "theme": "Problem Investigation",
    },
    "analogical_reasoner": {
        "description": "Use analogies to transfer knowledge from familiar to unfamiliar domains.",
        "use_cases": ["Explaining technical concepts", "Cross-industry learning", "Creative problem solving", "Teaching"],
        "parameter_descriptions": {
            "concept": "The concept or problem to explain by analogy",
            "domain": "Source domain for analogies (e.g. 'sports', 'cooking')",
        },
        "research_basis": "Gentner (1983) structure-mapping theory; Holyoak & Thagard (1995) Mental Leaps; Lakoff & Johnson (1980) conceptual metaphor.",
        "theme": "Innovation & Creativity",
    },
    "hypothesis_generator": {
        "description": "Systematic generation of testable, falsifiable hypotheses.",
        "use_cases": ["Scientific research", "A/B test design", "Debugging theories", "Market research"],
        "parameter_descriptions": {
            "observation": "The observation or data to explain",
            "domain": "Field or domain context",
        },
        "research_basis": "Popper (1959) Logic of Scientific Discovery; Platt (1964) strong inference; Peirce (1931) abductive reasoning.",
        "theme": "Data & Analytics",
    },

    # ── FREE — Creative (5) ──────────────────────────────────────────────
    "idea_generator": {
        "description": "Systematic generation of creative ideas using divergent thinking.",
        "use_cases": ["Product features", "Marketing campaigns", "Process improvements", "Hackathon ideation"],
        "parameter_descriptions": {
            "challenge": "The challenge or opportunity to generate ideas for",
            "context": "Constraints, industry, or audience context",
        },
        "research_basis": "Osborn (1953) Applied Imagination; Guilford (1967) divergent thinking; Amabile (1996) Creativity in Context.",
        "theme": "Innovation & Creativity",
    },
    "brainstormer": {
        "description": "Structured ideation with deferred judgment and quantity-first approach.",
        "use_cases": ["Team brainstorms", "Sprint planning", "Workshop facilitation", "Strategy sessions"],
        "parameter_descriptions": {
            "topic": "The topic or problem to brainstorm",
            "goal": "Desired outcome (e.g. 'Generate 10 creative solutions')",
        },
        "research_basis": "Osborn (1953) brainstorming rules; Dennis & Valacich (1993) electronic brainstorming; Isaksen & Gaulin (2005) facilitation techniques.",
        "theme": "Innovation & Creativity",
    },
    "innovation_framework": {
        "description": "Systematic approach to innovation using TRIZ and disruptive innovation theory.",
        "use_cases": ["New product development", "Business model innovation", "Process redesign", "Market disruption"],
        "parameter_descriptions": {
            "challenge": "The innovation challenge or opportunity",
            "context": "Industry, market, or organizational context",
        },
        "research_basis": "Christensen (1997) Innovator's Dilemma; Altshuller (1984) TRIZ inventive problem solving; Chesbrough (2003) Open Innovation.",
        "theme": "Innovation & Creativity",
    },
    "design_thinker": {
        "description": "Human-centered design process: empathize, define, ideate, prototype, test.",
        "use_cases": ["UX design", "Service design", "Product development", "Customer experience improvement"],
        "parameter_descriptions": {
            "challenge": "The design challenge to address",
            "users": "Target users or personas",
        },
        "research_basis": "Brown (2009) Change by Design; Norman (1988) Design of Everyday Things; Stanford d.school (Plattner et al., 2011).",
        "theme": "Innovation & Creativity",
    },
    "metaphor_generator": {
        "description": "Create explanatory metaphors that map familiar domains to complex concepts.",
        "use_cases": ["Technical presentations", "Teaching", "Marketing copy", "Onboarding materials"],
        "parameter_descriptions": {
            "concept": "The concept to create metaphors for",
            "audience": "Target audience's familiarity level",
        },
        "research_basis": "Lakoff & Johnson (1980) Metaphors We Live By; Gentner et al. (2001) metaphor as analogy; Aubusson et al. (2006) science education metaphors.",
        "theme": "Communication & Clarity",
    },

    # ── FREE — Communication (7) ─────────────────────────────────────────
    "technical_translator": {
        "description": "Translate technical jargon into language accessible to non-experts.",
        "use_cases": ["Executive summaries", "Client communications", "Documentation", "Press releases"],
        "parameter_descriptions": {
            "technical_text": "The technical content to translate",
            "target_audience": "Who needs to understand this (e.g. 'executives', 'customers')",
        },
        "research_basis": "Redish (2012) Letting Go of the Words; Olson (2015) science communication through narrative; Swaffield & Page (2009) jargon in communication.",
        "theme": "Communication & Clarity",
    },
    "simplification_engine": {
        "description": "Reduce complexity while preserving accuracy and meaning.",
        "use_cases": ["Policy simplification", "User guides", "Legal-to-plain-English", "Medical patient education"],
        "parameter_descriptions": {
            "complex_topic": "The complex information to simplify",
            "audience": "Target audience (e.g. 'general public', 'new employees')",
        },
        "research_basis": "Sweller (1988) cognitive load theory; Kintsch & van Dijk (1978) text comprehension model; Flesch (1948) readability metrics.",
        "theme": "Communication & Clarity",
    },
    "persuasion_framework": {
        "description": "Structured persuasive communication using proven psychological principles.",
        "use_cases": ["Sales pitches", "Proposals", "Fundraising", "Change management communications"],
        "parameter_descriptions": {
            "goal": "What you want to persuade the audience to do",
            "audience": "Target audience and their current stance",
        },
        "research_basis": "Cialdini (1984) six principles of persuasion; Petty & Cacioppo (1986) Elaboration Likelihood Model; Toulmin (1958) argumentation theory.",
        "theme": "Communication & Clarity",
    },
    "narrative_builder": {
        "description": "Craft compelling narratives with character, conflict, and resolution.",
        "use_cases": ["Case studies", "Keynote presentations", "Brand storytelling", "Annual reports"],
        "parameter_descriptions": {
            "topic": "The subject to build a narrative around",
            "audience": "Target audience",
        },
        "research_basis": "Campbell (1949) Hero's Journey; Bruner (1991) narrative construction of reality; Heath & Heath (2007) Made to Stick.",
        "theme": "Communication & Clarity",
    },
    "feedback_composer": {
        "description": "Compose constructive, actionable feedback that supports growth.",
        "use_cases": ["Performance reviews", "Code review comments", "Customer responses", "Peer feedback"],
        "parameter_descriptions": {
            "situation": "The situation requiring feedback",
            "goal": "Goal of the feedback (e.g. 'Support growth and retention')",
        },
        "research_basis": "Hattie & Timperley (2007) power of feedback; Shute (2008) formative feedback; Dweck (2006) growth mindset.",
        "theme": "Communication & Clarity",
    },
    "clarity_optimizer": {
        "description": "Improve text clarity, precision, and remove ambiguity.",
        "use_cases": ["Email drafts", "Requirements documents", "Contracts", "API documentation"],
        "parameter_descriptions": {
            "text": "The text to optimize for clarity",
            "goal": "Specific clarity goal (e.g. 'Maximum clarity', 'Remove jargon')",
        },
        "research_basis": "Grice (1975) cooperative principle and maxims; Williams & Bizup (2014) Style: Lessons in Clarity and Grace; Flesch (1948) readability.",
        "theme": "Communication & Clarity",
    },
    "audience_adapter": {
        "description": "Tailor communication style, tone, and detail level to a specific audience.",
        "use_cases": ["Multi-stakeholder reports", "Cross-department memos", "Training materials", "Marketing segments"],
        "parameter_descriptions": {
            "message": "The message or content to adapt",
            "current_audience": "Current audience context or source audience",
        },
        "research_basis": "Ede & Lunsford (1984) audience theory; Giles & Ogay (2007) Communication Accommodation Theory; Redish (2010) user-centered writing.",
        "theme": "Communication & Clarity",
    },

    # ── FREE — Planning (5) ──────────────────────────────────────────────
    "stakeholder_mapper": {
        "description": "Identify stakeholders and map their power, interest, and influence.",
        "use_cases": ["Project kickoffs", "Organizational change", "Product launches", "M&A due diligence"],
        "parameter_descriptions": {
            "project": "The project or initiative to map stakeholders for",
            "context": "Organizational or industry context",
        },
        "research_basis": "Freeman (1984) Stakeholder Theory; Mitchell et al. (1997) stakeholder salience; Mendelow (1981) power-interest grid.",
        "theme": "Project Management",
    },
    "scenario_planner": {
        "description": "Explore multiple future scenarios to prepare for uncertainty.",
        "use_cases": ["Strategic planning", "Market entry", "Technology roadmaps", "Crisis preparedness"],
        "parameter_descriptions": {
            "topic": "The subject or decision to plan scenarios for",
            "timeframe": "Planning horizon (e.g. '5 years', '2030')",
        },
        "research_basis": "Schwartz (1991) Art of the Long View; Schoemaker (1995) scenario planning for strategy; van der Heijden (2005) strategic conversation.",
        "theme": "Strategic Thinking",
    },
    "resource_allocator": {
        "description": "Optimally allocate limited resources across competing needs.",
        "use_cases": ["Budget allocation", "Team assignments", "Infrastructure planning", "Portfolio management"],
        "parameter_descriptions": {
            "resources": "Available resources to allocate",
            "needs": "Competing needs or demands",
        },
        "research_basis": "Dantzig (1963) linear programming; Barney (1991) resource-based view; Markowitz (1952) portfolio theory.",
        "theme": "Project Management",
    },
    "priority_setter": {
        "description": "Systematically prioritize items using established frameworks.",
        "use_cases": ["Sprint backlog", "Feature prioritization", "Task triage", "Strategic initiatives"],
        "parameter_descriptions": {
            "items": "Items or tasks to prioritize",
            "goal": "Prioritization criteria or strategic goal",
        },
        "research_basis": "Eisenhower Matrix (Covey, 1989); Saaty (1980) Analytic Hierarchy Process; MoSCoW method (Clegg & Barker, 1994).",
        "theme": "Project Management",
    },
    "deadline_manager": {
        "description": "Manage deadlines, dependencies, and critical paths.",
        "use_cases": ["Project timelines", "Release planning", "Event coordination", "Regulatory compliance deadlines"],
        "parameter_descriptions": {
            "tasks": "Tasks with their requirements and dependencies",
            "deadline": "Target deadline or delivery date",
        },
        "research_basis": "Kelley & Walker (1959) Critical Path Method; PERT (Malcolm et al., 1959); Goldratt (1997) Critical Chain.",
        "theme": "Project Management",
    },

    # ── FREE — Specialized (11) ──────────────────────────────────────────
    "code_reviewer": {
        "description": "Systematic code review for quality, security, and best practices.",
        "use_cases": ["Pull request reviews", "Security audits", "Onboarding code walkthroughs", "Tech debt assessment"],
        "parameter_descriptions": {
            "code": "The code to review",
            "context": "Language, framework, or project context",
        },
        "research_basis": "Fagan (1976) design and code inspections; Bacchelli & Bird (2013) modern code review at Microsoft; Chess & West (2007) static analysis.",
        "theme": "Evaluation & Quality",
    },
    "content_outliner": {
        "description": "Create structured, hierarchical content outlines.",
        "use_cases": ["Blog posts", "Whitepapers", "Course curriculum", "Documentation structure"],
        "parameter_descriptions": {
            "topic": "The topic to outline",
            "goal": "Purpose or target output format",
        },
        "research_basis": "Meyer (1975) prose organization and memory; Flower & Hayes (1981) cognitive process theory of writing; Halvorson & Rach (2012) content strategy.",
        "theme": "Communication & Clarity",
    },
    "socratic_questioner": {
        "description": "Use probing questions to reveal assumptions and deepen understanding.",
        "use_cases": ["Coaching sessions", "Requirements elicitation", "Critical thinking exercises", "Interview preparation"],
        "parameter_descriptions": {
            "statement": "The claim or idea to probe",
            "context": "Domain or conversation context",
        },
        "research_basis": "Paul & Elder (2007) critical thinking; Overholser (1993) Socratic method; Ennis (1989) critical thinking and subject specificity.",
        "theme": "Self-Improvement",
    },
    "intent_recognizer": {
        "description": "Identify underlying user intent and goals from text.",
        "use_cases": ["Customer support triage", "Product feedback analysis", "Chatbot design", "Survey analysis"],
        "parameter_descriptions": {
            "input": "The text to analyze for intent",
            "context": "Domain (e.g. 'product review', 'support ticket')",
            "depth": "Analysis depth: quick, standard, comprehensive",
        },
        "research_basis": "Austin (1962) speech act theory; Searle (1969) Speech Acts; Jurafsky & Martin (2023) NLP intent recognition.",
        "theme": "Data & Analytics",
    },
    "ambiguity_resolver": {
        "description": "Identify and resolve ambiguous wording, hedging, and unclear intent.",
        "use_cases": ["Requirements clarification", "Contract review", "Survey question design", "Bug report triage"],
        "parameter_descriptions": {
            "input": "The ambiguous text to resolve",
            "context": "Domain context for disambiguation",
            "depth": "How thorough the resolution should be",
        },
        "research_basis": "Grice (1975) cooperative principle; Lakoff (1973) hedges and fuzzy logic; Berry et al. (2003) requirements ambiguity.",
        "theme": "Communication & Clarity",
    },
    "risk_assessor": {
        "description": "Systematic risk identification and probability × impact assessment.",
        "use_cases": ["Project risk registers", "Investment due diligence", "Migration planning", "New feature rollout"],
        "parameter_descriptions": {
            "decision": "The decision, action, or project to assess risks for",
            "context": "Domain or organizational context",
        },
        "research_basis": "Kaplan & Garrick (1981) quantitative risk definition; ISO 31000:2018 risk management; Tversky & Kahneman (1974) heuristics and biases.",
        "theme": "Risk & Compliance",
    },
    "risk_mitigator": {
        "description": "Develop strategies to reduce, transfer, or manage identified risks.",
        "use_cases": ["Risk response planning", "Business continuity", "Disaster recovery", "Compliance remediation"],
        "parameter_descriptions": {
            "risk": "The risk to mitigate",
            "impact": "Expected impact if risk materializes",
        },
        "research_basis": "PMBOK Guide (2017) risk response strategies; Hopkin (2018) Fundamentals of Risk Management; Hollnagel et al. (2006) resilience engineering.",
        "theme": "Risk & Compliance",
    },
    "impact_assessor": {
        "description": "Assess consequences, downstream effects, and ripple impacts of actions.",
        "use_cases": ["Policy changes", "System migrations", "Organizational restructuring", "Product deprecation"],
        "parameter_descriptions": {
            "action": "The action or change to assess impact for",
            "context": "Scope and domain context",
        },
        "research_basis": "Glasson et al. (2012) impact assessment; Pearl (2009) causal impact analysis; Meadows (2008) systems thinking and ripple effects.",
        "theme": "Risk & Compliance",
    },
    "conflict_resolver": {
        "description": "Systematic approach to resolving conflicts through principled negotiation.",
        "use_cases": ["Team disputes", "Customer complaints", "Contract negotiations", "Cross-department alignment"],
        "parameter_descriptions": {
            "conflict": "The conflict situation to resolve",
            "parties": "Involved parties and their positions",
        },
        "research_basis": "Fisher, Ury & Patton (2011) Getting to Yes; Thomas & Kilmann (1974) conflict modes; Raiffa (1982) Art and Science of Negotiation.",
        "theme": "Communication & Clarity",
    },
    "concept_explainer": {
        "description": "Clear, accessible explanation of complex concepts using analogies and examples.",
        "use_cases": ["Technical documentation", "Training materials", "Client education", "Onboarding guides"],
        "parameter_descriptions": {
            "concept": "The concept to explain",
            "audience": "Target audience's expertise level",
        },
        "research_basis": "Ausubel (1968) meaningful learning theory; Chi et al. (1989) self-explanation effect; Mayer (2002) multimedia learning.",
        "theme": "Learning & Development",
    },
    "synthesis_builder": {
        "description": "Integrate diverse information sources into a coherent, unified understanding.",
        "use_cases": ["Literature reviews", "Market research synthesis", "Cross-team findings", "Board reports"],
        "parameter_descriptions": {
            "sources": "Sources or information to synthesize",
            "goal": "Purpose of the synthesis",
        },
        "research_basis": "Bloom (1956) synthesis in taxonomy; Linn & Eylon (2011) knowledge integration; Glass (1976) meta-analysis methodology.",
        "theme": "Data & Analytics",
    },

    # ── ENTERPRISE — Decision (5) ────────────────────────────────────────
    "decision_framework": {
        "description": "Structured decision-making with criteria weighting, options evaluation, and recommendations.",
        "use_cases": ["Technology selection", "Vendor evaluation", "Architecture decisions", "Strategic pivots"],
        "parameter_descriptions": {
            "decision": "The decision to be made",
        },
        "research_basis": "Hammond, Keeney & Raiffa (1999) Smart Choices; Simon (1955) bounded rationality; Klein (1998) naturalistic decision making.",
        "theme": "Strategic Thinking",
    },
    "comparative_analyzer": {
        "description": "Side-by-side comparison across multiple dimensions with explicit criteria.",
        "use_cases": ["Product comparison", "Architecture trade-offs", "Vendor evaluation", "Framework selection"],
        "parameter_descriptions": {
            "options": "Items to compare (comma-separated or list)",
            "criteria": "Evaluation criteria (e.g. 'cost, latency, team size')",
        },
        "research_basis": "Tversky (1972) elimination by aspects; Saaty (1980) Analytic Hierarchy Process; Keeney & Raiffa (1976) multi-attribute utility theory.",
        "theme": "Strategic Thinking",
    },
    "tradeoff_analyzer": {
        "description": "Explicit analysis of tradeoffs between competing objectives.",
        "use_cases": ["Build vs. buy", "Speed vs. quality", "Cost vs. features", "Security vs. usability"],
        "parameter_descriptions": {
            "situation": "The situation with competing objectives",
            "objectives": "Objectives that are in tension",
            "context": "Business or technical context",
        },
        "research_basis": "Keeney (1992) Value-Focused Thinking; Payne et al. (1993) Adaptive Decision Maker; Pareto (1896) optimality theory.",
        "theme": "Strategic Thinking",
    },
    "multi_objective_optimizer": {
        "description": "Optimize when multiple objectives conflict — find Pareto-optimal solutions.",
        "use_cases": ["Resource allocation with constraints", "Product feature prioritization", "Portfolio optimization", "Supply chain design"],
        "parameter_descriptions": {
            "objectives": "Competing objectives to optimize",
        },
        "research_basis": "Deb (2001) multi-objective evolutionary algorithms; Miettinen (1999) nonlinear multiobjective optimization; Zitzler & Thiele (1999) Pareto strength.",
        "theme": "Strategic Thinking",
    },
    "cost_benefit_analyzer": {
        "description": "Systematic comparison of costs vs. benefits including intangible factors.",
        "use_cases": ["Investment decisions", "Project proposals", "Policy evaluation", "ROI analysis"],
        "parameter_descriptions": {
            "decision": "The decision or investment to analyze",
        },
        "research_basis": "Boardman et al. (2017) Cost-Benefit Analysis; Arrow & Lind (1970) public investment under uncertainty; Kahneman et al. (1997) experienced utility.",
        "theme": "Strategic Thinking",
    },

    # ── ENTERPRISE — Problem Solving (6) ─────────────────────────────────
    "problem_decomposer": {
        "description": "Break complex problems into manageable, hierarchical sub-problems.",
        "use_cases": ["System architecture", "Large project scoping", "Bug triage", "Organizational challenges"],
        "parameter_descriptions": {
            "problem": "The complex problem to decompose",
        },
        "research_basis": "Simon (1962) architecture of complexity; Newell & Simon (1972) Human Problem Solving; INCOSE (2015) Systems Engineering Handbook.",
        "theme": "Problem Investigation",
    },
    "bottleneck_identifier": {
        "description": "Find performance-limiting constraints using Theory of Constraints.",
        "use_cases": ["Production bottlenecks", "CI/CD pipeline optimization", "Customer journey friction", "Hiring process"],
        "parameter_descriptions": {
            "system": "The system or process to analyze",
            "context": "Operational context and metrics",
        },
        "research_basis": "Goldratt & Cox (1984) The Goal (TOC); Little (1961) queueing formula L=λW; Jain (1991) performance analysis.",
        "theme": "Problem Investigation",
    },
    "constraint_optimizer": {
        "description": "Optimize outcomes within given constraints.",
        "use_cases": ["Budget-constrained projects", "Regulatory compliance", "Resource-limited design", "Scheduling"],
        "parameter_descriptions": {
            "objective": "What to optimize",
            "constraints": "Hard and soft constraints",
        },
        "research_basis": "Boyd & Vandenberghe (2004) Convex Optimization; Tsang (1993) constraint satisfaction; Lagrange (1788) constrained optimization foundations.",
        "theme": "Problem Investigation",
    },
    "dependency_mapper": {
        "description": "Map dependencies between components to reveal critical paths and risks.",
        "use_cases": ["Microservice architectures", "Project planning", "Supply chain mapping", "API dependency audit"],
        "parameter_descriptions": {
            "system": "The system or project with dependencies",
            "context": "Technical or organizational context",
        },
        "research_basis": "Eppinger & Browning (2012) Design Structure Matrix; Barabási (2002) network science; Diestel (2017) graph theory.",
        "theme": "Systems & Complexity",
    },
    "efficiency_analyzer": {
        "description": "Analyze process efficiency and identify waste using Lean principles.",
        "use_cases": ["Manufacturing optimization", "DevOps pipeline", "Meeting productivity", "Customer service workflow"],
        "parameter_descriptions": {
            "process": "The process to analyze for efficiency",
            "context": "Operational or business context",
        },
        "research_basis": "Womack & Jones (1996) Lean Thinking; Ohno (1988) Toyota Production System; Farrell (1957) productive efficiency measurement.",
        "theme": "Problem Investigation",
    },
    "trade_space_explorer": {
        "description": "Explore the space of possible solutions and design alternatives.",
        "use_cases": ["Architecture selection", "Product configuration", "Engineering design", "Market positioning"],
        "parameter_descriptions": {
            "problem": "The design problem to explore alternatives for",
            "context": "Constraints and domain context",
        },
        "research_basis": "Ross & Hastings (2005) tradespace exploration paradigm; Pahl et al. (2007) systematic engineering design; Deb et al. (2002) NSGA-II.",
        "theme": "Strategic Thinking",
    },

    # ── ENTERPRISE — Temporal (3) ────────────────────────────────────────
    "temporal_sequence_analyzer": {
        "description": "Analyze events in timeline order, identify causal sequences and turning points.",
        "use_cases": ["Incident timelines", "Product evolution analysis", "Market shift tracking", "Historical pattern recognition"],
        "parameter_descriptions": {
            "events": "Events or data points with timestamps",
            "time_span": "Time range (e.g. '12 months', 'Q1-Q3 2025')",
            "context": "Domain context for interpretation",
        },
        "research_basis": "Allen (1983) temporal interval logic; Box & Jenkins (1976) time series; Granger (1969) temporal causality.",
        "theme": "Data & Analytics",
    },
    "future_scenario_planner": {
        "description": "Generate and evaluate multiple plausible future scenarios.",
        "use_cases": ["5-year strategy", "Technology disruption planning", "Climate adaptation", "Regulatory change preparation"],
        "parameter_descriptions": {
            "focal_question": "The central question about the future",
            "time_horizon": "How far to project (e.g. '5 years')",
            "current_situation": "Current state description",
        },
        "research_basis": "Schwartz (1991) Art of the Long View; Armstrong (2001) Principles of Forecasting; Schoemaker (1995) scenario planning methodology.",
        "theme": "Strategic Thinking",
    },
    "historical_context_mapper": {
        "description": "Learn from historical precedents, patterns, and analogies.",
        "use_cases": ["Strategic lessons", "Policy precedents", "Industry evolution", "Technology adoption patterns"],
        "parameter_descriptions": {
            "current_situation": "The current situation to find precedents for",
            "question": "What to learn from history",
        },
        "research_basis": "Neustadt & May (1986) Thinking in Time; Khong (1992) historical analogies in policy; Santayana (1905) learning from history.",
        "theme": "Strategic Thinking",
    },

    # ── ENTERPRISE — Diagnostic (3) ──────────────────────────────────────
    "diagnostic_root_cause_analyzer": {
        "description": "Full diagnostic root cause analysis: Five Whys, Ishikawa, fault tree.",
        "use_cases": ["Critical incident analysis", "Manufacturing defects", "Customer satisfaction collapse", "System failures"],
        "parameter_descriptions": {
            "problem": "The problem to diagnose",
            "symptoms": "Observable symptoms and timeline",
        },
        "research_basis": "Ishikawa (1986) fishbone diagrams; Ohno (1988) Five Whys; Rooney & Vanden Heuvel (2004) RCA for beginners.",
        "theme": "Problem Investigation",
    },
    "differential_diagnoser": {
        "description": "Rule out hypotheses systematically to reach the correct diagnosis.",
        "use_cases": ["Complex bug diagnosis", "Medical diagnostics", "System failure analysis", "Customer churn investigation"],
        "parameter_descriptions": {
            "presenting_problem": "The presenting problem or symptoms",
            "observed_data": "Relevant data and observations",
            "domain": "Domain (e.g. 'software', 'medical', 'business')",
        },
        "research_basis": "Clinical reasoning frameworks; Bayesian diagnostic reasoning; evidence-based differential diagnosis methodology.",
        "theme": "Problem Investigation",
    },
    "system_health_auditor": {
        "description": "Audit system health across multiple dimensions systematically.",
        "use_cases": ["Infrastructure audit", "Application health check", "Organizational assessment", "Compliance review"],
        "parameter_descriptions": {
            "system": "The system to audit",
            "audit_focus": "Specific area of focus (e.g. 'security', 'performance')",
        },
        "research_basis": "ISO 27001 audit frameworks; COBIT IT governance; systematic health assessment methodologies.",
        "theme": "Risk & Compliance",
    },

    # ── ENTERPRISE — Synthesis (3) ───────────────────────────────────────
    "holistic_integrator": {
        "description": "Multi-perspective synthesis combining technical, business, and human viewpoints.",
        "use_cases": ["Cross-functional strategy", "M&A integration", "Change management", "Complex project reviews"],
        "parameter_descriptions": {
            "topic": "The topic to integrate perspectives on",
            "perspectives": "Different viewpoints to synthesize (e.g. 'Technical, Business, Cultural')",
        },
        "research_basis": "Systems thinking integration; Senge (1990) mental models and shared vision; multi-stakeholder synthesis frameworks.",
        "theme": "Systems & Complexity",
    },
    "pattern_recognition_engine": {
        "description": "Find recurring patterns, trends, and regularities in data or observations.",
        "use_cases": ["Customer behavior patterns", "Code smell detection", "Market cycles", "Sentiment trends"],
        "parameter_descriptions": {
            "data": "Data or observations to analyze for patterns",
            "pattern_focus": "What kind of patterns to look for",
        },
        "research_basis": "Statistical pattern recognition; Medin & Schaffer (1978) context theory of classification; machine learning pattern detection.",
        "theme": "Data & Analytics",
    },
    "cross_domain_synthesizer": {
        "description": "Borrow solutions and insights from other domains and industries.",
        "use_cases": ["Biomimicry in engineering", "Cross-industry innovation", "Analogical problem solving", "Technology transfer"],
        "parameter_descriptions": {
            "target_problem": "The problem to solve",
            "source_domains": "Domains to draw inspiration from",
        },
        "research_basis": "Gentner (1983) structure-mapping; Holyoak & Thagard (1995) analogical reasoning; TRIZ cross-domain inventive principles.",
        "theme": "Innovation & Creativity",
    },

    # ── ENTERPRISE — Systems Thinking (6) ────────────────────────────────
    "feedback_loop_identifier": {
        "description": "Map reinforcing and balancing feedback loops in complex systems.",
        "use_cases": ["Business model dynamics", "Organizational change", "Product growth loops", "Ecosystem analysis"],
        "parameter_descriptions": {
            "system": "The system to analyze for feedback loops",
            "behavior": "Observed behavior or pattern to explain",
        },
        "research_basis": "Meadows (2008) Thinking in Systems; Forrester (1961) Industrial Dynamics; Senge (1990) system archetypes.",
        "theme": "Systems & Complexity",
    },
    "leverage_point_finder": {
        "description": "Find high-impact intervention points using Meadows' 12 leverage points.",
        "use_cases": ["Organizational transformation", "Policy design", "Product strategy", "Process improvement"],
        "parameter_descriptions": {
            "system": "The system to find leverage points in",
            "goal": "Desired system change",
        },
        "research_basis": "Meadows (1999) 12 leverage points; Sterman (2000) Business Dynamics; Kim & Lannon (1997) applying systems archetypes.",
        "theme": "Systems & Complexity",
    },
    "emergence_detector": {
        "description": "Identify emergent properties arising from system interactions.",
        "use_cases": ["Organizational culture analysis", "Market dynamics", "Technology ecosystem evolution", "Team dynamics"],
        "parameter_descriptions": {
            "system": "The system to analyze for emergence",
            "components": "Key components and their interactions",
        },
        "research_basis": "Holland (1998) Emergence: From Chaos to Order; Johnson (2001) complex adaptive systems; Miller & Page (2007) computational social science.",
        "theme": "Systems & Complexity",
    },
    "system_archetype_analyzer": {
        "description": "Recognize common system patterns like 'Limits to Growth' and 'Shifting the Burden'.",
        "use_cases": ["Growth strategy", "Failure pattern diagnosis", "Policy pitfall avoidance", "Team dynamics"],
        "parameter_descriptions": {
            "system": "The system to analyze for archetypes",
            "pattern": "Suspected archetype or observed behavior pattern",
        },
        "research_basis": "Senge (1990) system archetypes (Limits to Growth, Shifting the Burden, etc.); Kim (1992) Systems Archetypes; Braun (2002) archetype modeling.",
        "theme": "Systems & Complexity",
    },
    "causal_loop_diagrammer": {
        "description": "Build causal loop diagrams to visualize system causality and feedback.",
        "use_cases": ["System dynamics modeling", "Strategy workshops", "Root cause visualization", "Policy analysis"],
        "parameter_descriptions": {
            "system": "The system to diagram",
            "variables": "Key variables and their relationships",
        },
        "research_basis": "Sterman (2000) CLD methodology; Forrester (1961) system dynamics; Richardson & Pugh (1981) system dynamics modeling.",
        "theme": "Systems & Complexity",
    },
    "stock_flow_analyzer": {
        "description": "Understand accumulations (stocks) and rates of change (flows) in systems.",
        "use_cases": ["Inventory management", "Cash flow analysis", "Technical debt accumulation", "Climate modeling"],
        "parameter_descriptions": {
            "system": "The system with stocks and flows",
            "focus": "Specific stock-flow relationship to analyze",
        },
        "research_basis": "Forrester (1961) stock-flow fundamentals; Cronin et al. (2009) bathtub dynamics; Sterman (2000) system delays and momentum.",
        "theme": "Systems & Complexity",
    },

    # ── ENTERPRISE — Metacognition (5) ───────────────────────────────────
    "metacognitive_monitor": {
        "description": "Monitor your own thinking process, detect errors, and adjust strategies.",
        "use_cases": ["Learning reflection", "Decision auditing", "Coaching sessions", "AI prompt refinement"],
        "parameter_descriptions": {
            "task_description": "The task you are working on",
            "current_approach": "Your current strategy or method",
            "progress_so_far": "What has been accomplished",
            "challenges": "Difficulties or roadblocks encountered",
        },
        "research_basis": "Flavell (1979) metacognition theory; Schraw & Dennison (1994) metacognitive awareness; Dunlosky & Metcalfe (2009) metamemory.",
        "theme": "Self-Improvement",
    },
    "self_regulation_framework": {
        "description": "Plan → Monitor → Evaluate your own performance in a cyclical process.",
        "use_cases": ["Goal setting", "Habit building", "Professional development", "Study planning"],
        "parameter_descriptions": {
            "goal": "The goal to self-regulate toward",
            "context": "Current situation and constraints",
        },
        "research_basis": "Zimmerman (2002) self-regulated learning; Pintrich (2000) goal orientation; Efklides (2024) MASRL framework.",
        "theme": "Self-Improvement",
    },
    "cognitive_strategy_selector": {
        "description": "Choose the most appropriate thinking strategy for a given task type.",
        "use_cases": ["Study method selection", "Problem-solving approach", "Team facilitation", "AI workflow design"],
        "parameter_descriptions": {
            "task_type": "The type of task (e.g. 'memorization', 'analysis', 'creative')",
            "context": "Task constraints and learner context",
        },
        "research_basis": "Pressley & Harris (2006) cognitive strategy instruction; Paris et al. (1983) conditional knowledge; SRSD methodology (Harris & Graham, 1996).",
        "theme": "Self-Improvement",
    },
    "learning_from_experience": {
        "description": "Extract transferable lessons from past successes and failures.",
        "use_cases": ["Project retrospectives", "After-action reviews", "Career reflection", "Organizational learning"],
        "parameter_descriptions": {
            "experience_description": "The experience to learn from",
            "context": "What happened and the outcomes",
        },
        "research_basis": "Kolb (1984) experiential learning cycle; Schön (1983) reflective practice; Ellis & Davidi (2005) after-event reviews.",
        "theme": "Self-Improvement",
    },
    "error_detection_framework": {
        "description": "Identify mistakes, biases, and flaws in reasoning systematically.",
        "use_cases": ["Proof review", "Decision auditing", "Code logic verification", "Bias checking"],
        "parameter_descriptions": {
            "work_to_check": "The work or reasoning to check for errors",
            "context": "Expected standards or criteria",
        },
        "research_basis": "Chi et al. (1989) self-explanation effect; Tversky & Kahneman (1974) cognitive biases; Lilienfeld et al. (2009) debiasing strategies.",
        "theme": "Self-Improvement",
    },

    # ── ENTERPRISE — Ethical Reasoning (5) ───────────────────────────────
    "ethical_framework_analyzer": {
        "description": "Apply six major ethical frameworks: Utilitarian, Rights, Justice, Common Good, Virtue, Care.",
        "use_cases": ["AI ethics review", "Corporate policy decisions", "Medical ethics", "Regulatory compliance"],
        "parameter_descriptions": {
            "decision": "The decision to analyze ethically",
            "context": "Stakeholders and situation context",
        },
        "research_basis": "Markkula Center (2015) ethical decision framework; Mill (1863) Utilitarianism; Kant (1785) Categorical Imperative; Rawls (1971) Theory of Justice.",
        "theme": "Ethics & Governance",
    },
    "moral_dilemma_resolver": {
        "description": "Navigate situations where ethical principles conflict.",
        "use_cases": ["AI safety decisions", "Medical triage", "Whistleblowing decisions", "Privacy vs. security"],
        "parameter_descriptions": {
            "dilemma": "The moral dilemma to resolve",
            "conflicting_principles": "Which principles are in tension",
            "context": "Situational context and stakeholders",
        },
        "research_basis": "Greene (2014) dual-process moral judgment; Kohlberg (1981) moral development stages; Foot (1967) doctrine of double effect.",
        "theme": "Ethics & Governance",
    },
    "stakeholder_ethics_assessor": {
        "description": "Assess ethical impact on all stakeholders, including marginalized groups.",
        "use_cases": ["AI fairness audit", "Environmental impact", "Community impact assessment", "Corporate social responsibility"],
        "parameter_descriptions": {
            "decision": "The decision to assess ethically",
            "stakeholders": "Affected parties and groups",
        },
        "research_basis": "Freeman (1984) stakeholder theory; Rawls (1971) veil of ignorance; Donaldson & Preston (1995) stakeholder corporation theory.",
        "theme": "Ethics & Governance",
    },
    "value_conflict_navigator": {
        "description": "Resolve situations where deeply held values compete (e.g. security vs. privacy).",
        "use_cases": ["Policy design", "Product feature trade-offs", "Organizational values alignment", "Personal decisions"],
        "parameter_descriptions": {
            "situation": "The situation with competing values",
            "competing_values": "Values in tension",
            "value_a": "First value",
            "value_b": "Opposing value",
        },
        "research_basis": "Rest (1986) four-component model of morality; Schwartz (1992) universal values circumplex; context-dependent moral flexibility.",
        "theme": "Ethics & Governance",
    },
    "consequentialist_analyzer": {
        "description": "Evaluate long-term ethical consequences across multiple time horizons.",
        "use_cases": ["Policy impact analysis", "Technology deployment ethics", "Environmental decisions", "Long-term strategy"],
        "parameter_descriptions": {
            "action": "The action to evaluate consequences of",
            "scope": "Scope of impact (e.g. 'team', 'company', 'society')",
        },
        "research_basis": "Smart & Williams (1973) Utilitarianism For and Against; Ord (2020) existential risk; MacAskill (2022) longtermism ethics.",
        "theme": "Ethics & Governance",
    },

    # ── ENTERPRISE — Learning (5) ────────────────────────────────────────
    "scaffolding_framework": {
        "description": "Provide structured support that gradually fades as competence increases.",
        "use_cases": ["Employee onboarding", "Student tutoring", "Skill development programs", "Knowledge transfer"],
        "parameter_descriptions": {
            "task": "The learning task or skill",
            "current_skill_level": "Learner's current level (beginner, intermediate, advanced)",
            "goal": "Target competency level",
        },
        "research_basis": "Vygotsky (1978) Zone of Proximal Development; Wood, Bruner & Ross (1976) scaffolding; Collins et al. (1989) cognitive apprenticeship.",
        "theme": "Learning & Development",
    },
    "spaced_repetition_optimizer": {
        "description": "Optimize learning schedules using spaced repetition and retrieval practice.",
        "use_cases": ["Language learning", "Certification prep", "Medical education", "Sales training"],
        "parameter_descriptions": {
            "learning_material": "Content to learn and retain",
            "initial_mastery": "Current knowledge level",
            "previous_performance": "Past quiz/test results",
        },
        "research_basis": "Ebbinghaus (1885) forgetting curve; Cepeda et al. (2006) distributed practice; Roediger & Butler (2011) retrieval practice.",
        "theme": "Learning & Development",
    },
    "zone_of_proximal_development": {
        "description": "Identify what a learner can achieve with guidance vs. independently.",
        "use_cases": ["Personalized learning paths", "Mentoring programs", "Adaptive curriculum", "Career development"],
        "parameter_descriptions": {
            "learner_current_abilities": "What the learner can do now",
            "learning_goal": "Target skill or knowledge",
        },
        "research_basis": "Vygotsky (1978) ZPD theory; Chaiklin (2003) zone of proximal development in analysis; dynamic assessment methodology.",
        "theme": "Learning & Development",
    },
    "cognitive_load_manager": {
        "description": "Manage intrinsic, extraneous, and germane cognitive load in learning.",
        "use_cases": ["Course design", "UI/UX simplification", "Training material creation", "Information architecture"],
        "parameter_descriptions": {
            "learning_material": "The content or task to manage load for",
            "learner_background": "Learner's prior knowledge and experience",
        },
        "research_basis": "Sweller (1988) cognitive load theory; Paas et al. (2003) CLT and instructional design; Chandler & Sweller (1991) format of instruction.",
        "theme": "Learning & Development",
    },
    "conceptual_change_analyzer": {
        "description": "Help learners overcome misconceptions and shift to correct mental models.",
        "use_cases": ["Science education", "Corporate culture change", "Paradigm shifts", "Correcting false beliefs"],
        "parameter_descriptions": {
            "topic": "The topic with potential misconceptions",
            "current_understanding": "Learner's current (possibly incorrect) understanding",
        },
        "research_basis": "Posner et al. (1982) conceptual change conditions; Vosniadou (1994) mental models in science; Chi (2005) ontological category shift.",
        "theme": "Learning & Development",
    },

    # ── ENTERPRISE — Evaluation (5) ──────────────────────────────────────
    "rubric_designer": {
        "description": "Create evaluation rubrics with criteria, performance levels, and descriptors.",
        "use_cases": ["Course assessment design", "Hiring scorecards", "Code review checklists", "Project evaluation"],
        "parameter_descriptions": {
            "assessment_task": "What is being assessed",
            "learning_objectives": "Goals or criteria to evaluate against",
            "rubric_type": "Rubric type: analytic (dimension-by-dimension) or holistic",
        },
        "research_basis": "Stevens & Levi (2013) rubric design; AAC&U (2009) VALUE rubrics; Jonsson & Svingby (2007) rubric reliability.",
        "theme": "Evaluation & Quality",
    },
    "formative_assessment_framework": {
        "description": "Design improvement-focused assessments that guide learning, not just grade.",
        "use_cases": ["Course checkpoints", "Sprint demos", "Progress reviews", "Coaching check-ins"],
        "parameter_descriptions": {
            "learning_unit": "The unit or module to assess",
            "learning_goal": "Target learning outcome",
        },
        "research_basis": "Black & Wiliam (1998) assessment for learning; Hattie (2009) Visible Learning (effect size 0.70); Shute (2008) formative feedback.",
        "theme": "Evaluation & Quality",
    },
    "summative_evaluator": {
        "description": "Evaluate overall performance or outcomes against established standards.",
        "use_cases": ["Final project evaluation", "Program review", "Annual performance review", "Certification exams"],
        "parameter_descriptions": {
            "course_title": "What is being evaluated",
            "learning_outcomes": "Expected outcomes or standards",
        },
        "research_basis": "Scriven (1991) Evaluation Thesaurus; Wiggins & McTighe (2005) backward design; Glaser (1963) criterion-referenced assessment.",
        "theme": "Evaluation & Quality",
    },
    "peer_assessment_structure": {
        "description": "Structure peer review processes for fairness and constructive feedback.",
        "use_cases": ["Code reviews", "Academic peer review", "360-degree feedback", "Team retrospectives"],
        "parameter_descriptions": {
            "assessment_task": "What peers are assessing",
            "learning_objective": "Purpose of the peer assessment",
        },
        "research_basis": "Topping (1998) peer assessment effectiveness; Falchikov & Goldfinch (2000) peer assessment validity; collaborative learning research.",
        "theme": "Evaluation & Quality",
    },
    "self_assessment_guide": {
        "description": "Guide systematic self-evaluation against clear success criteria.",
        "use_cases": ["Personal development plans", "Portfolio review", "Interview preparation", "Skill gap analysis"],
        "parameter_descriptions": {
            "work_to_assess": "The work or skills to self-assess",
            "success_criteria": "Criteria to evaluate against",
        },
        "research_basis": "Boud & Falchikov (1989) self-assessment accuracy; Zimmerman (2002) self-regulation; metacognitive monitoring research.",
        "theme": "Evaluation & Quality",
    },
}


# ---------------------------------------------------------------------------
# USE_CASE_PROMPTS — copy-pasteable example prompts per use-case, per template
# Each key is a template name; value is a dict of { use_case: example_prompt }.
# These are realistic, day-to-day prompts that users can copy into the
# Generic Prompt or Cognitive Context panels.
# ---------------------------------------------------------------------------
USE_CASE_PROMPTS: dict[str, dict[str, str]] = {
    # ── FREE — Analysis ──────────────────────────────────────────────────
    "question_analyzer": {
        "Unclear requirements": "Our client says they want 'better reporting' but hasn't specified which metrics, audience, or format. What should we clarify before starting?",
        "Multi-part questions": "Why did Q3 revenue drop, what regions were hit hardest, and what corrective actions should we take for Q4?",
        "Pre-analysis triage": "I have 6 months of customer feedback data. Before I dive in, what are the right questions to ask and where should I focus first?",
        "Customer support intake": "A customer wrote: 'The app is slow and sometimes crashes when I export.' Break this down into actionable investigation areas.",
    },
    "data_analyzer": {
        "Sales analysis": "Q3 sales by region: North +5%, South -12%, East +2%, West -8%. What's driving the divergence and where should we focus?",
        "Metrics review": "Our DAU is 45k, MAU is 120k, churn is 6.2%, NPS is 42. How healthy are these numbers for a B2B SaaS product?",
        "Dashboard insights": "Here's our weekly dashboard: signups up 15%, activation down 8%, revenue flat. What story does this data tell?",
        "Quarterly business reports": "Summarize these Q2 results into executive insights: ARR $4.2M (+18%), CAC $320 (+22%), LTV:CAC 2.8:1, churn 5.1%.",
    },
    "trend_identifier": {
        "Market trend analysis": "Monthly active users: Jan 10k, Feb 12k, Mar 11k, Apr 15k, May 18k, Jun 22k. What trends and inflection points do you see?",
        "KPI tracking": "Our support ticket volume over 12 months: 200, 210, 250, 230, 280, 310, 290, 350, 400, 380, 420, 450. What's the trend and forecast?",
        "Technology adoption curves": "React usage grew 30% last year while Angular stayed flat and Vue grew 10%. What does this signal for our tech stack decision?",
        "Social media monitoring": "Our brand mentions went from 50/day to 200/day after our product launch. How should we analyze this spike and plan next steps?",
    },
    "gap_analyzer": {
        "Requirements gap analysis": "We promised the client real-time dashboards, SSO, and API access. We've built dashboards and API. What gaps remain and what's the risk?",
        "Competitive gaps": "Competitor X has AI-powered search, mobile app, and 24/7 support. We have none of these. Prioritize what to build first.",
        "Skills assessment": "Our team knows Python and SQL but we need to ship a React frontend and deploy on Kubernetes. What's our skills gap?",
        "Process audit": "Our deployment takes 2 hours with manual steps and frequent rollbacks. The target is automated 10-minute deploys. What's missing?",
    },
    "swot_analyzer": {
        "Business strategy": "We're a 50-person SaaS startup considering expansion into the European market. What are our strengths, weaknesses, opportunities, and threats?",
        "Product launches": "We're launching a mobile banking app in Southeast Asia with 3 established competitors. Analyze our strategic position.",
        "Market positioning": "Our product is mid-priced in a market splitting into premium and budget segments. Where should we position?",
        "Team capability assessment": "Our engineering team is strong in backend but weak in mobile and ML. We need to build an AI-powered mobile app. Assess our readiness.",
    },
    "anomaly_detector": {
        "Fraud detection": "These 5 transactions look unusual: $10k at 3AM, $8k in a new country, $12k to a flagged account. Analyze what's anomalous and why.",
        "Quality control": "Our defect rate jumped from 0.5% to 3.2% on Tuesday. Nothing changed in our process. What should we investigate?",
        "System monitoring": "Server response times (ms): 120, 115, 130, 125, 890, 118, 122, 750, 119. What's happening with those spikes?",
        "Financial auditing": "Monthly expenses were steady at $50k then jumped to $85k. No new hires or contracts. Where should the auditor look?",
    },
    # ── FREE — Reasoning ─────────────────────────────────────────────────
    "root_cause_analyzer": {
        "Production outages": "Our main API went down for 45 minutes yesterday at peak hours. CloudWatch shows a memory spike. What's the root cause chain?",
        "Support ticket spikes": "Support tickets doubled after our v3.0 release. Most mention 'login issues' and 'slow loading.' Investigate the root causes.",
        "Performance degradation": "Page load time went from 1.2s to 4.8s over the past month. No major code changes. What could be causing this?",
        "Incident postmortems": "Our payment processing failed for 2 hours last Friday. The database connection pool was exhausted. Walk through the Five Whys.",
    },
    "step_by_step_reasoner": {
        "Logic walkthroughs": "Walk me through the logic of migrating a monolith to microservices for an e-commerce platform with 50k daily users.",
        "Troubleshooting guides": "Our Docker containers keep restarting in production. Walk me step-by-step through how to diagnose and fix this.",
        "Teaching explanations": "Explain how a neural network learns — step by step, as if I'm a business analyst with no ML background.",
        "Process documentation": "Document the step-by-step process for onboarding a new enterprise client, from contract signing to first value delivery.",
    },
    "causal_reasoner": {
        "Root cause chains": "Employee turnover increased 30% after switching to remote-first. What are the possible causal chains?",
        "Policy impact analysis": "We changed our refund policy from 30 days to 14 days. Customer complaints rose 40%. Trace the cause-effect relationships.",
        "Scientific reasoning": "A new drug shows 20% improvement in trials but 5% improvement in real-world use. What causal factors explain this gap?",
        "Debugging complex systems": "Users in Asia report slow API responses but US users are fine. Both hit the same servers. What's causing the difference?",
    },
    "analogical_reasoner": {
        "Explaining technical concepts": "Explain Kubernetes container orchestration using a restaurant kitchen analogy that a business stakeholder would understand.",
        "Cross-industry learning": "What can healthcare appointment scheduling teach us about improving our SaaS onboarding flow?",
        "Creative problem solving": "Our customer churn problem feels like a leaky bucket. What can plumbing teach us about fixing retention?",
        "Teaching": "Explain database indexing to a non-technical product manager using a library book catalog analogy.",
    },
    "hypothesis_generator": {
        "Scientific research": "Conversion rate dropped 15% last week despite no code changes. Generate testable hypotheses for what might have happened.",
        "A/B test design": "We think changing the CTA button from green to blue will improve signups. What hypotheses should we test and how?",
        "Debugging theories": "Our ML model's accuracy dropped from 92% to 78% after retraining. What hypotheses could explain this?",
        "Market research": "Sales are strong in urban areas but weak in suburbs for our delivery app. Generate hypotheses for why.",
    },
    # ── FREE — Creative ──────────────────────────────────────────────────
    "idea_generator": {
        "Product features": "Generate 10 innovative feature ideas for a project management tool that would differentiate us from Jira and Asana.",
        "Marketing campaigns": "We're launching an AI writing tool. Generate creative campaign ideas that would go viral on LinkedIn.",
        "Process improvements": "Our code review process takes 3 days on average. Generate ideas to speed it up without sacrificing quality.",
        "Hackathon ideation": "Our hackathon theme is 'AI for accessibility.' Generate diverse project ideas our team could build in 48 hours.",
    },
    "brainstormer": {
        "Team brainstorms": "Our team needs to reduce customer onboarding time from 2 weeks to 3 days. Brainstorm every possible approach.",
        "Sprint planning": "We have a 2-week sprint and need to decide between 3 features. Brainstorm criteria and approaches for prioritization.",
        "Workshop facilitation": "I'm running a workshop on improving developer experience. Generate a structured brainstorm agenda with prompts.",
        "Strategy sessions": "Our startup needs to reach $1M ARR in 12 months. Brainstorm all possible growth strategies, conventional and unconventional.",
    },
    "innovation_framework": {
        "New product development": "We want to build an AI-powered code review tool. Apply innovation frameworks to find unique angles competitors haven't explored.",
        "Business model innovation": "Our consulting business is project-based. Explore innovative business models that could create recurring revenue.",
        "Process redesign": "Our hiring process takes 6 weeks. Apply innovation thinking to redesign it from scratch.",
        "Market disruption": "How could a startup disrupt the traditional real estate industry using AI and blockchain? Explore systematically.",
    },
    "design_thinker": {
        "UX design": "Our SaaS dashboard has a 60% bounce rate. Apply design thinking to understand why and propose solutions.",
        "Service design": "Design a better experience for patients checking in at a hospital — from parking to seeing the doctor.",
        "Product development": "We're building a personal finance app for Gen Z. Walk through the design thinking process from empathy to testing.",
        "Customer experience improvement": "Our NPS dropped from 45 to 28 after a UI redesign. Use design thinking to find what went wrong and fix it.",
    },
    "metaphor_generator": {
        "Technical presentations": "Create a compelling metaphor to explain microservices architecture to a board of directors with no tech background.",
        "Teaching": "Generate metaphors that explain machine learning training to high school students using everyday experiences.",
        "Marketing copy": "Create metaphors for our cybersecurity product that make 'threat detection' feel urgent but not scary.",
        "Onboarding materials": "Generate metaphors to explain our company's CI/CD pipeline to new engineering hires on their first day.",
    },
    # ── FREE — Communication ─────────────────────────────────────────────
    "technical_translator": {
        "Executive summaries": "Translate this for our CEO: 'We need to refactor the ORM layer due to N+1 query issues causing P99 latency spikes in the GraphQL resolver.'",
        "Client communications": "Our client asked why the project is delayed. Translate 'technical debt in the authentication microservice' into business language.",
        "Documentation": "Rewrite our API rate-limiting documentation so a junior developer with 6 months experience can understand and implement it.",
        "Press releases": "Translate 'We implemented transformer-based NLP with fine-tuned BERT models' into a press release that a journalist would understand.",
    },
    "simplification_engine": {
        "Policy simplification": "Simplify our 10-page privacy policy into a 1-page summary that a regular user can understand in 2 minutes.",
        "User guides": "Our API documentation uses too much jargon. Simplify the authentication section for developers who are new to OAuth.",
        "Legal-to-plain-English": "Translate this clause: 'The indemnifying party shall hold harmless the indemnified party from all claims arising from...'",
        "Medical patient education": "Simplify this for patients: 'Hypertension management requires ACE inhibitor titration with regular eGFR monitoring.'",
    },
    "persuasion_framework": {
        "Sales pitches": "Help me craft a compelling pitch for our AI analytics tool to a CFO who thinks their Excel reports are 'good enough.'",
        "Proposals": "I need to persuade our VP of Engineering to invest 3 months in technical debt reduction instead of new features.",
        "Fundraising": "We're a seed-stage startup pitching to VCs. Our product reduces customer churn by 35%. Build a persuasive narrative.",
        "Change management communications": "We're moving from Slack to Teams. Many employees resist. Craft a persuasive communication plan.",
    },
    "narrative_builder": {
        "Case studies": "Build a compelling case study narrative: Client had 40% churn, used our tool, reduced to 12% in 6 months, saved $2M.",
        "Keynote presentations": "I'm giving a keynote on 'The Future of AI in Healthcare.' Build a narrative arc that hooks the audience in the first 30 seconds.",
        "Brand storytelling": "Our startup was born when our founder couldn't find affordable tutoring for her kids. Build our origin story.",
        "Annual reports": "Turn these dry numbers into a compelling narrative: Revenue +28%, customers +45%, employee satisfaction 4.2/5.",
    },
    "feedback_composer": {
        "Performance reviews": "A team member delivers great code but misses deadlines and doesn't communicate blockers. Compose constructive feedback.",
        "Code review comments": "This PR has good logic but poor error handling and no tests. Write feedback that's constructive and specific.",
        "Customer responses": "A customer left a 2-star review saying 'Too complicated, gave up after 30 minutes.' Compose an empathetic response.",
        "Peer feedback": "My colleague's presentation had great content but poor delivery — too fast, no eye contact. Help me give kind, useful feedback.",
    },
    "clarity_optimizer": {
        "Email drafts": "Optimize this email for clarity: 'I wanted to circle back on the thing we discussed about potentially maybe moving forward with the project.'",
        "Requirements documents": "This requirement is ambiguous: 'The system should be fast and handle many users.' Rewrite it with precision.",
        "Contracts": "Clarify this contract clause: 'Services will be delivered in a timely manner consistent with industry standards.'",
        "API documentation": "Our API docs say 'Returns an error if something goes wrong.' Rewrite all error documentation to be precise and actionable.",
    },
    "audience_adapter": {
        "Multi-stakeholder reports": "Adapt our Q3 performance report for three audiences: the board (strategic), engineering (technical), and sales (tactical).",
        "Cross-department memos": "Adapt this engineering postmortem so both the CTO and the Head of Customer Success get what they need from it.",
        "Training materials": "We have a Python tutorial for senior devs. Adapt it for business analysts who've never coded before.",
        "Marketing segments": "Adapt our product messaging for: enterprise CTOs (security-first), startup founders (speed-first), and developers (feature-first).",
    },
    # ── FREE — Planning ──────────────────────────────────────────────────
    "stakeholder_mapper": {
        "Project kickoffs": "We're launching a new CRM system. Map all stakeholders: sales, marketing, IT, executives, and end users — who has power, who has interest?",
        "Organizational change": "We're restructuring from functional teams to product teams. Map the stakeholders and their likely positions.",
        "Product launches": "We're launching a B2B payment feature. Map stakeholders across engineering, compliance, sales, and partner banks.",
        "M&A due diligence": "Our company is acquiring a 50-person startup. Map all stakeholders on both sides and their concerns.",
    },
    "scenario_planner": {
        "Strategic planning": "Plan 3 scenarios for our SaaS company in 2027: best case, worst case, and most likely. Revenue is currently $5M ARR.",
        "Market entry": "We're considering entering the Indian market. Plan optimistic, pessimistic, and baseline scenarios for year 1.",
        "Technology roadmaps": "AI coding assistants could automate 50% of junior dev tasks by 2028. Plan scenarios for our consulting business.",
        "Crisis preparedness": "Our main cloud provider has had 3 outages this year. Plan scenarios for a major 24-hour outage and our response.",
    },
    "resource_allocator": {
        "Budget allocation": "We have $500k for Q4. Competing needs: hire 2 engineers ($200k), marketing campaign ($150k), infrastructure upgrade ($200k), training ($50k).",
        "Team assignments": "I have 8 engineers and 3 projects due in 6 weeks. Project A needs 4 devs, B needs 3, C needs 5. How do I allocate?",
        "Infrastructure planning": "We have 100 CPU cores across 3 services. Service A handles payments, B handles search, C handles analytics. Optimize allocation.",
        "Portfolio management": "We have 12 product initiatives but budget for 5. Each has different ROI, risk, and strategic value. How should we allocate?",
    },
    "priority_setter": {
        "Sprint backlog": "We have 15 tickets for a 2-week sprint but capacity for 8. Help me prioritize using impact vs. effort.",
        "Feature prioritization": "Customers are asking for: dark mode, API access, mobile app, SSO, and better search. We can build 2 this quarter.",
        "Task triage": "I have 20 tasks due this week: 5 urgent bugs, 8 feature tasks, 4 meetings to prep for, and 3 documents to review. Prioritize them.",
        "Strategic initiatives": "Our leadership wants to pursue: international expansion, AI features, platform partnership, and cost reduction. Rank them.",
    },
    "deadline_manager": {
        "Project timelines": "We need to launch by March 15. Backend needs 4 weeks, frontend 3 weeks, QA 2 weeks, and design is 1 week behind. Plan the timeline.",
        "Release planning": "Plan a release schedule for v2.0 with these dependencies: API first, then UI, then mobile, then docs. Each takes 2-3 weeks.",
        "Event coordination": "We're hosting a 500-person conference in 8 weeks. Map all tasks, dependencies, and critical path items.",
        "Regulatory compliance deadlines": "We need SOC 2 compliance by June 1. Map the tasks: policy writing, technical controls, audit prep, and certification.",
    },
    # ── FREE — Specialized ───────────────────────────────────────────────
    "code_reviewer": {
        "Pull request reviews": "Review this Python function for bugs, security issues, and best practices: [paste your code here]",
        "Security audits": "Audit this authentication module for OWASP Top 10 vulnerabilities, especially injection and broken auth.",
        "Onboarding code walkthroughs": "I'm new to this codebase. Walk me through this service class — what does it do, why is it structured this way?",
        "Tech debt assessment": "This module was written 3 years ago and never refactored. Assess the tech debt and recommend what to fix first.",
    },
    "content_outliner": {
        "Blog posts": "Create an outline for a blog post: 'Why Most Companies Fail at Data-Driven Decision Making (And How to Fix It).'",
        "Whitepapers": "Outline a whitepaper on 'The ROI of AI-Powered Customer Support' targeting VP-level decision makers.",
        "Course curriculum": "Outline a 6-week course: 'Introduction to Machine Learning for Product Managers.' Include weekly topics and exercises.",
        "Documentation structure": "Outline the documentation structure for our REST API. We have 15 endpoints across 4 resource types.",
    },
    "socratic_questioner": {
        "Coaching sessions": "I want to switch careers from engineering to product management. Ask me probing questions to test if I've thought this through.",
        "Requirements elicitation": "A stakeholder says 'We need a dashboard.' Use Socratic questioning to uncover what they actually need.",
        "Critical thinking exercises": "Challenge this assumption: 'We should always prioritize speed to market over code quality.'",
        "Interview preparation": "Prepare Socratic questions to test a senior engineer candidate's system design thinking depth.",
    },
    "intent_recognizer": {
        "Customer support triage": "Classify and prioritize this ticket: 'Hi, I've been trying to export my data for 3 days now. Nothing works. I need this for a board meeting tomorrow.'",
        "Product feedback analysis": "What's the real intent behind this feedback: 'Your product is okay but I wish it was more like Notion'?",
        "Chatbot design": "Analyze these 10 customer messages and identify the top 5 intents we should train our chatbot to handle.",
        "Survey analysis": "Our NPS detractors say things like 'too expensive,' 'hard to use,' 'missing features.' What are the underlying intents?",
    },
    "ambiguity_resolver": {
        "Requirements clarification": "The spec says 'users should be able to manage their data easily.' Identify all ambiguities and propose clarifications.",
        "Contract review": "This contract says 'reasonable efforts' and 'timely delivery.' Flag every ambiguous term and suggest precise alternatives.",
        "Survey question design": "Is this survey question ambiguous? 'How often do you use our product?' Identify issues and rewrite it.",
        "Bug report triage": "A user reported: 'The button doesn't work sometimes.' Resolve the ambiguity — what questions should we ask?",
    },
    "risk_assessor": {
        "Project risk registers": "We're migrating from AWS to GCP in 3 months. Identify all risks, estimate probability and impact for each.",
        "Investment due diligence": "We're considering investing $2M in an early-stage AI startup. Assess the key risks across technology, market, and team.",
        "Migration planning": "We're moving from a monolith to microservices. Assess risks across technical, organizational, and business dimensions.",
        "New feature rollout": "We're launching AI-generated recommendations to 10M users next month. What could go wrong? Assess all risks.",
    },
    "risk_mitigator": {
        "Risk response planning": "Our biggest risk is key-person dependency — one engineer knows the entire payment system. Develop a mitigation plan.",
        "Business continuity": "If our primary data center goes offline for 48 hours, what's our continuity plan? Develop strategies for each critical system.",
        "Disaster recovery": "Develop a disaster recovery plan for our customer database. RTO: 4 hours, RPO: 1 hour. What strategies do we need?",
        "Compliance remediation": "Our security audit found 12 medium-severity vulnerabilities. Develop a prioritized mitigation plan with timelines.",
    },
    "impact_assessor": {
        "Policy changes": "We're changing our pricing from per-seat to usage-based. Assess the impact on revenue, churn, sales team, and customer satisfaction.",
        "System migrations": "Assess the downstream impact of replacing our PostgreSQL database with MongoDB across all 8 dependent services.",
        "Organizational restructuring": "We're merging the frontend and backend teams into full-stack squads. Assess impact on productivity, morale, and delivery.",
        "Product deprecation": "We're sunsetting our legacy API in 6 months. 200 customers still use it. Assess the impact and transition plan.",
    },
    "conflict_resolver": {
        "Team disputes": "Two senior engineers disagree on architecture: one wants microservices, the other wants a modular monolith. Help resolve this.",
        "Customer complaints": "A customer is threatening to cancel because a feature they were promised isn't ready. They're angry. Help de-escalate.",
        "Contract negotiations": "Our vendor wants to increase prices by 30%. We want to stay flat. Both sides have leverage. Help find a resolution.",
        "Cross-department alignment": "Marketing wants to launch in 2 weeks but engineering says the product isn't ready. Both have valid concerns. Resolve this.",
    },
    "concept_explainer": {
        "Technical documentation": "Explain Kubernetes pods, services, and deployments so that a frontend developer with no DevOps experience can understand.",
        "Training materials": "Explain the concept of technical debt to non-technical project managers using simple analogies and examples.",
        "Client education": "Explain to our enterprise client why their data needs to be normalized before we can build ML models on it.",
        "Onboarding guides": "Create an explanation of our microservices architecture for new hires — assume they only know basic web development.",
    },
    "synthesis_builder": {
        "Literature reviews": "Synthesize these 5 research papers on AI-assisted code review into a unified summary of findings and recommendations.",
        "Market research synthesis": "We have competitor analysis, customer interviews, and market size data. Synthesize into a single strategic narrative.",
        "Cross-team findings": "Three teams investigated our churn problem: product, support, and data. Each has different findings. Synthesize them.",
        "Board reports": "Synthesize Q3 data from finance, product, engineering, and HR into a cohesive board update that tells one story.",
    },
    # ── ENTERPRISE — Decision ────────────────────────────────────────────
    "decision_framework": {
        "Technology selection": "We need to choose between PostgreSQL, MongoDB, and DynamoDB for our new service. Guide me through a structured decision.",
        "Vendor evaluation": "Evaluate 3 CI/CD vendors: GitHub Actions, GitLab CI, and CircleCI for our 20-person engineering team.",
        "Architecture decisions": "Should we build a real-time feature using WebSockets, Server-Sent Events, or polling? Structure the decision.",
        "Strategic pivots": "Our B2C product is struggling but B2B interest is growing. Should we pivot? Guide the decision process.",
    },
    "comparative_analyzer": {
        "Product comparison": "Compare AWS Lambda vs. Google Cloud Functions vs. Azure Functions across cost, performance, DX, and ecosystem.",
        "Architecture trade-offs": "Compare REST vs. GraphQL vs. gRPC for our internal microservices communication layer.",
        "Vendor evaluation": "Compare Datadog vs. New Relic vs. Grafana for our observability stack. We have 50 services.",
        "Framework selection": "Compare Next.js vs. Remix vs. Astro for our marketing site rebuild. Criteria: SEO, performance, developer experience.",
    },
    "tradeoff_analyzer": {
        "Build vs. buy": "Should we build our own authentication system or use Auth0? Analyze the tradeoffs across cost, control, and time.",
        "Speed vs. quality": "We can ship in 2 weeks with shortcuts or 6 weeks with full test coverage. Analyze the tradeoffs.",
        "Cost vs. features": "Adding AI features would cost $200k/year in API calls but could increase conversion by 25%. Analyze the tradeoff.",
        "Security vs. usability": "Adding MFA reduces account takeover by 95% but increases login friction by 40%. Analyze the tradeoff.",
    },
    "multi_objective_optimizer": {
        "Resource allocation with constraints": "Optimize server allocation across 3 services: minimize cost, maximize uptime, stay under $10k/month budget.",
        "Product feature prioritization": "We have 10 features competing for 3 sprint slots. Optimize for user value, engineering effort, and strategic alignment.",
        "Portfolio optimization": "Optimize our project portfolio: maximize ROI, minimize risk, maintain team morale, deliver on strategic goals.",
        "Supply chain design": "Optimize our delivery network: minimize shipping cost, maximize delivery speed, maintain quality across 5 regions.",
    },
    "cost_benefit_analyzer": {
        "Investment decisions": "Analyze the costs vs. benefits of migrating to cloud-native: upfront migration cost $300k, expected savings $150k/year.",
        "Project proposals": "We want to build an internal developer platform. Cost: 6 engineer-months. Analyze the full cost-benefit over 3 years.",
        "Policy evaluation": "Should we implement a 4-day work week? Analyze costs (productivity risk) vs. benefits (retention, satisfaction).",
        "ROI analysis": "Calculate the ROI of implementing automated testing: cost of setup and maintenance vs. reduced bugs and faster releases.",
    },
    # ── ENTERPRISE — Problem Solving ─────────────────────────────────────
    "problem_decomposer": {
        "System architecture": "Decompose the problem of building a real-time collaborative editing system like Google Docs into sub-problems.",
        "Large project scoping": "We need to rebuild our entire frontend in React. Decompose this 6-month project into manageable milestones.",
        "Bug triage": "Users report intermittent 500 errors. Sometimes it works, sometimes it doesn't. Decompose the investigation.",
        "Organizational challenges": "Employee engagement is low across all departments. Decompose this complex problem into addressable sub-problems.",
    },
    "bottleneck_identifier": {
        "Production bottlenecks": "Our API handles 1000 req/s but users experience timeouts at 500 req/s. Find the bottleneck in our stack.",
        "CI/CD pipeline optimization": "Our CI pipeline takes 45 minutes. Tests: 20min, build: 15min, deploy: 10min. Where's the bottleneck?",
        "Customer journey friction": "Only 20% of signups complete onboarding. Walk through the journey and identify where users are dropping off.",
        "Hiring process": "Our hiring takes 8 weeks from application to offer. Identify the bottleneck stages slowing everything down.",
    },
    "constraint_optimizer": {
        "Budget-constrained projects": "Deliver maximum value with a $50k budget: we need a web app, mobile app, and admin dashboard. Optimize the approach.",
        "Regulatory compliance": "We must comply with GDPR, SOC 2, and HIPAA simultaneously. Optimize our approach to cover all three efficiently.",
        "Resource-limited design": "We have 2 engineers for 8 weeks. Optimize what we can deliver for our MVP launch.",
        "Scheduling": "5 teams need the staging environment but we only have 2 environments. Optimize the scheduling.",
    },
    "dependency_mapper": {
        "Microservice architectures": "Map dependencies between our 12 microservices. Identify circular dependencies and single points of failure.",
        "Project planning": "Map the dependencies for our product launch: design, engineering, QA, marketing, sales, and legal all need to coordinate.",
        "Supply chain mapping": "Map our software supply chain: third-party APIs, open-source libraries, cloud services. Where are we most vulnerable?",
        "API dependency audit": "We use 15 external APIs. Map which services depend on which APIs and what happens if each one goes down.",
    },
    "efficiency_analyzer": {
        "Manufacturing optimization": "Our deployment process has 12 steps and 3 manual approvals. Analyze waste and suggest lean improvements.",
        "DevOps pipeline": "Analyze our release pipeline: code review (2 days), QA (3 days), staging (1 day), deploy (2 hours). Where's the waste?",
        "Meeting productivity": "Our team spends 15 hours/week in meetings. Analyze which meetings add value and which are waste.",
        "Customer service workflow": "A support ticket goes through 5 handoffs before resolution. Average resolution: 4 days. Analyze the inefficiency.",
    },
    "trade_space_explorer": {
        "Architecture selection": "Explore the trade space for our data pipeline: batch vs. stream vs. hybrid, considering cost, latency, and complexity.",
        "Product configuration": "Explore pricing model options: freemium, trial, per-seat, usage-based, hybrid. Map the trade space for our SaaS.",
        "Engineering design": "We need a caching layer. Explore options: Redis, Memcached, CDN, application-level. Map tradeoffs.",
        "Market positioning": "Explore positioning options for our AI tool: developer-first, enterprise-first, or horizontal. Map the trade space.",
    },
    # ── ENTERPRISE — Temporal ────────────────────────────────────────────
    "temporal_sequence_analyzer": {
        "Incident timelines": "Plot this incident timeline: 2PM deploy, 2:15 first alert, 2:30 user reports, 3PM rollback, 3:15 resolution. Find turning points.",
        "Product evolution analysis": "Analyze our product evolution: MVP (Jan), v1.0 (Apr), enterprise features (Jul), mobile (Oct). What patterns emerge?",
        "Market shift tracking": "Track the AI market shift: ChatGPT (Nov 2022), GPT-4 (Mar 2023), Claude 2 (Jul 2023), Gemini (Dec 2023). What's the trajectory?",
        "Historical pattern recognition": "Our sales spike every Q4 (holiday), dip in Q1, recover Q2, grow Q3. Is this pattern changing? Analyze 3 years of data.",
    },
    "future_scenario_planner": {
        "5-year strategy": "Plan 3 scenarios for our company in 5 years. We're a $10M ARR SaaS in the HR tech space.",
        "Technology disruption planning": "AI agents could automate 40% of customer support by 2027. Plan scenarios for our 200-person support team.",
        "Climate adaptation": "Our supply chain relies on 3 coastal warehouses. Plan scenarios considering rising sea levels and extreme weather through 2035.",
        "Regulatory change preparation": "The EU AI Act takes effect in 2026. Plan scenarios for how it could affect our AI-powered products.",
    },
    "historical_context_mapper": {
        "Strategic lessons": "What can we learn from Netflix's pivot from DVD to streaming that's relevant to our digital transformation?",
        "Policy precedents": "We're implementing a remote-work policy. What historical precedents exist and what can we learn from companies that tried this before?",
        "Industry evolution": "Map how the CRM industry evolved from ACT! to Salesforce to AI CRMs. What patterns predict the next shift?",
        "Technology adoption patterns": "Map the adoption pattern of cloud computing from 2006-2020. How does AI adoption today compare?",
    },
    # ── ENTERPRISE — Diagnostic ──────────────────────────────────────────
    "diagnostic_root_cause_analyzer": {
        "Critical incident analysis": "Our payment system processed duplicate charges for 200 customers over 3 hours. Full diagnostic: timeline, root cause, fault tree.",
        "Manufacturing defects": "Product returns increased 300% this month. All returns cite 'battery issue.' Run a full diagnostic root cause analysis.",
        "Customer satisfaction collapse": "NPS dropped from 52 to 18 in one quarter. Customer comments mention 'unreliable' and 'slow support.' Diagnose why.",
        "System failures": "Our Kubernetes cluster had cascading failures across 4 services. Start from symptoms and trace to root cause using Ishikawa.",
    },
    "differential_diagnoser": {
        "Complex bug diagnosis": "Users intermittently get 403 errors. It happens across browsers, doesn't correlate with load, and started 2 weeks ago. Diagnose.",
        "Medical diagnostics": "Patient presents with fatigue, weight loss, and increased thirst. Walk through differential diagnosis systematically.",
        "System failure analysis": "Some API calls timeout at 30s while identical calls complete in 200ms. No pattern in time or user. Differential diagnosis.",
        "Customer churn investigation": "Enterprise customers churning cite different reasons: 'too expensive,' 'missing features,' 'poor support.' Differentially diagnose the real driver.",
    },
    "system_health_auditor": {
        "Infrastructure audit": "Audit our AWS infrastructure health: we run 15 EC2 instances, 3 RDS databases, S3, Lambda, and CloudFront.",
        "Application health check": "Audit the health of our Node.js API: uptime, error rates, response times, memory usage, dependency health.",
        "Organizational assessment": "Audit our engineering organization's health: team structure, hiring pipeline, tech debt levels, deployment frequency.",
        "Compliance review": "Audit our SOC 2 readiness across all 5 trust service criteria: security, availability, processing integrity, confidentiality, privacy.",
    },
    # ── ENTERPRISE — Synthesis ───────────────────────────────────────────
    "holistic_integrator": {
        "Cross-functional strategy": "Integrate technical, business, and people perspectives on our migration to microservices architecture.",
        "M&A integration": "We're acquiring a 30-person startup. Integrate technical (systems merge), business (revenue), and cultural perspectives.",
        "Change management": "We're adopting agile across the company. Synthesize engineering (process), HR (culture), and finance (planning) viewpoints.",
        "Complex project reviews": "Our ERP implementation is 6 months in. Integrate perspectives from IT, finance, operations, and end users.",
    },
    "pattern_recognition_engine": {
        "Customer behavior patterns": "Analyze these 1000 user sessions and find recurring patterns in how power users differ from churned users.",
        "Code smell detection": "Review these 5 modules and identify recurring patterns of tech debt, code smells, and architectural anti-patterns.",
        "Market cycles": "Analyze 10 years of our quarterly revenue data. What cyclical patterns exist and how can we predict the next cycle?",
        "Sentiment trends": "Analyze 6 months of customer reviews. Find recurring sentiment patterns and how they correlate with product releases.",
    },
    "cross_domain_synthesizer": {
        "Biomimicry in engineering": "How can ant colony optimization algorithms inspire our load-balancing architecture for distributed systems?",
        "Cross-industry innovation": "What can airline revenue management teach us about optimizing our SaaS pricing strategy?",
        "Analogical problem solving": "The healthcare industry solved patient scheduling with AI. How can we apply the same approach to developer tool usage?",
        "Technology transfer": "Autonomous vehicles use sensor fusion. How could similar fusion concepts improve our data pipeline architecture?",
    },
    # ── ENTERPRISE — Systems Thinking ────────────────────────────────────
    "feedback_loop_identifier": {
        "Business model dynamics": "Map the feedback loops in our SaaS growth model: more users → more data → better AI → more users. What loops could reverse?",
        "Organizational change": "We introduced OKRs but teams game metrics. Identify the reinforcing and balancing loops in our goal-setting system.",
        "Product growth loops": "Map the viral loops in our product: user invites → new signups → content creation → social sharing. Where are loops breaking?",
        "Ecosystem analysis": "Map the feedback loops in our developer ecosystem: SDKs → developer adoption → apps → user value → platform growth.",
    },
    "leverage_point_finder": {
        "Organizational transformation": "We want to become a data-driven company but culture resists. Where are the leverage points for maximum impact?",
        "Policy design": "Our remote work policy isn't working — people feel disconnected. Find leverage points to improve without mandating office return.",
        "Product strategy": "Our product has low activation (15%). Find the highest-leverage intervention points to get users to their 'aha moment.'",
        "Process improvement": "Our development cycle is 8 weeks. Find leverage points where small changes would dramatically shorten it.",
    },
    "emergence_detector": {
        "Organizational culture analysis": "Our 3 acquired teams were collaborative separately but became siloed together. What emergent behaviors are appearing?",
        "Market dynamics": "Remote work tools, AI assistants, and async communication are converging. What emergent market is forming?",
        "Technology ecosystem evolution": "LLMs, vector databases, and agent frameworks are combining. What emergent capabilities are appearing that didn't exist before?",
        "Team dynamics": "When we combined the frontend and backend teams, unexpected behaviors emerged. Identify and analyze them.",
    },
    "system_archetype_analyzer": {
        "Growth strategy": "Our growth is slowing despite increased marketing spend. Is this a 'Limits to Growth' archetype? Analyze.",
        "Failure pattern diagnosis": "We keep firefighting the same issues despite adding more engineers. Which system archetype is at play?",
        "Policy pitfall avoidance": "We're about to implement stricter performance metrics. Could this trigger a 'Shifting the Burden' archetype?",
        "Team dynamics": "Teams compete for resources and the winning team gets more resources, widening the gap. Identify the archetype.",
    },
    "causal_loop_diagrammer": {
        "System dynamics modeling": "Build a causal loop diagram for our customer lifecycle: acquisition → activation → engagement → expansion → churn.",
        "Strategy workshops": "Create a causal loop diagram showing how developer experience affects recruitment, retention, and product velocity.",
        "Root cause visualization": "Our costs are rising while revenue is flat. Build a CLD to visualize all the causal relationships.",
        "Policy analysis": "Build a causal loop diagram to analyze the effects of implementing a 4-day work week on productivity and retention.",
    },
    "stock_flow_analyzer": {
        "Inventory management": "Analyze the stock and flow dynamics of our content pipeline: ideas (stock) → drafts → review → published → archived.",
        "Cash flow analysis": "Analyze our cash flow dynamics: ARR $5M (stock), new sales +$200k/mo (inflow), churn -$100k/mo (outflow). When do we break even?",
        "Technical debt accumulation": "We ship 10 features/month (inflow) and fix 3 tech-debt items/month (outflow). Model the accumulation and its consequences.",
        "Climate modeling": "Model the stock-flow dynamics of our carbon footprint: emissions (inflow), offsets (outflow), cumulative footprint (stock).",
    },
    # ── ENTERPRISE — Metacognition ───────────────────────────────────────
    "metacognitive_monitor": {
        "Learning reflection": "I've been studying system design for 3 months but feel stuck. Monitor my learning strategy and suggest adjustments.",
        "Decision auditing": "I chose to rewrite our backend in Rust 6 months ago. Audit my decision-making process — was it sound?",
        "Coaching sessions": "I keep procrastinating on strategic work and defaulting to tactical tasks. Help me understand and fix my patterns.",
        "AI prompt refinement": "My prompts keep giving me generic answers. Monitor my prompting strategy and tell me what I'm doing wrong.",
    },
    "self_regulation_framework": {
        "Goal setting": "I want to transition from individual contributor to engineering manager in 12 months. Create a self-regulation plan.",
        "Habit building": "I want to write for 30 minutes every morning. Build a plan-monitor-evaluate cycle to make this stick.",
        "Professional development": "I need to learn cloud architecture well enough to pass the AWS Solutions Architect exam in 3 months. Plan my self-regulation.",
        "Study planning": "I'm preparing for a data science certification while working full-time. Build a sustainable study plan with self-monitoring.",
    },
    "cognitive_strategy_selector": {
        "Study method selection": "I need to memorize 200 API endpoints and their parameters. Which cognitive strategies are most effective?",
        "Problem-solving approach": "I'm facing a complex system design challenge. Help me choose the right thinking strategy.",
        "Team facilitation": "I'm facilitating a strategy session with 15 people who have conflicting views. Which cognitive approach works best?",
        "AI workflow design": "I'm building an AI workflow for document analysis. Which combination of cognitive patterns gives the best results?",
    },
    "learning_from_experience": {
        "Project retrospectives": "Our last product launch was 3 weeks late and over budget. Extract the transferable lessons for next time.",
        "After-action reviews": "We just resolved a critical outage in 4 hours instead of our usual 12. What did we do right that we should repeat?",
        "Career reflection": "I've been in 5 roles in 10 years, promoted twice, passed over twice, and chose to leave once. What patterns should I learn from?",
        "Organizational learning": "Three similar projects failed the same way: scope creep. What organizational lessons should we institutionalize?",
    },
    "error_detection_framework": {
        "Proof review": "Review my business plan for logical errors, unsupported assumptions, and reasoning gaps before I present to investors.",
        "Decision auditing": "We decided to enter the European market based on 3 data points. Check our reasoning for errors and biases.",
        "Code logic verification": "Verify the logic in my pricing algorithm. It should apply volume discounts progressively but I suspect edge cases.",
        "Bias checking": "Review our hiring criteria for cognitive biases: are we favoring familiarity, credentials, or in-group similarity?",
    },
    # ── ENTERPRISE — Ethical Reasoning ───────────────────────────────────
    "ethical_framework_analyzer": {
        "AI ethics review": "Our AI recommendation system shows different prices to different users based on browsing history. Analyze ethically.",
        "Corporate policy decisions": "Should we implement employee monitoring software for remote workers? Apply multiple ethical frameworks.",
        "Medical ethics": "An AI diagnostic tool is 95% accurate but the 5% errors disproportionately affect minority patients. Analyze ethically.",
        "Regulatory compliance": "We can technically comply with data privacy laws while still selling aggregated user data. Is this ethical?",
    },
    "moral_dilemma_resolver": {
        "AI safety decisions": "Our AI chatbot sometimes gives harmful advice. Removing the risky feature reduces harm but also removes value for 95% of users.",
        "Medical triage": "We have 10 ICU beds and 15 critical patients. How should we ethically decide who gets treated first?",
        "Whistleblowing decisions": "I discovered my company is misreporting emissions data. Reporting could cost me my job. Navigate this dilemma.",
        "Privacy vs. security": "We can prevent fraud by scanning all user messages but this violates privacy. Resolve this ethical tension.",
    },
    "stakeholder_ethics_assessor": {
        "AI fairness audit": "Our lending algorithm approves loans 20% less often for rural applicants. Assess the ethical impact on all stakeholders.",
        "Environmental impact": "Our data centers consume 500MW. Assess the ethical impact on the environment, local communities, and future generations.",
        "Community impact assessment": "We're building a warehouse that will create 200 jobs but increase traffic and noise. Assess stakeholder impact.",
        "Corporate social responsibility": "We use offshore labor at $5/hour for data labeling. Assess the ethical impact on all affected stakeholders.",
    },
    "value_conflict_navigator": {
        "Policy design": "Our AI should be transparent (explainable) but also protect proprietary algorithms (competitive advantage). Navigate this conflict.",
        "Product feature trade-offs": "Users want data portability (freedom) but we want lock-in (revenue). Navigate the value conflict.",
        "Organizational values alignment": "Our values say 'move fast' and 'never compromise quality.' When these conflict, which wins and when?",
        "Personal decisions": "I was offered a VP role at a competitor. More money and growth, but I'd leave my team during a critical project. Navigate this.",
    },
    "consequentialist_analyzer": {
        "Policy impact analysis": "Analyze the 1-year, 5-year, and 10-year consequences of making our SaaS product fully open-source.",
        "Technology deployment ethics": "Analyze the short and long-term consequences of deploying facial recognition in our office building.",
        "Environmental decisions": "Analyze the consequences of switching from cloud to on-premises servers in terms of cost, carbon, and operational impact.",
        "Long-term strategy": "Analyze the 1-year, 5-year, and 10-year consequences of aggressive AI automation across our customer service department.",
    },
    # ── ENTERPRISE — Learning ────────────────────────────────────────────
    "scaffolding_framework": {
        "Employee onboarding": "Design a scaffolded onboarding program for new engineers that goes from guided tutorials to independent contribution in 90 days.",
        "Student tutoring": "A student struggles with calculus derivatives. Design scaffolding that gradually removes support as they build confidence.",
        "Skill development programs": "Design a scaffolded learning path for a junior developer to become proficient in system design over 6 months.",
        "Knowledge transfer": "A senior engineer is leaving in 4 weeks. Design a scaffolded knowledge transfer plan for the team.",
    },
    "spaced_repetition_optimizer": {
        "Language learning": "I'm learning Japanese and need to memorize 500 kanji. Optimize my study schedule using spaced repetition principles.",
        "Certification prep": "I'm studying for the AWS Solutions Architect exam in 8 weeks. Design a spaced repetition schedule for key concepts.",
        "Medical education": "A medical student needs to learn 200 drug interactions. Optimize the review schedule to maximize long-term retention.",
        "Sales training": "Our sales team needs to memorize pricing for 50 products and 12 discount tiers. Design an optimal review schedule.",
    },
    "zone_of_proximal_development": {
        "Personalized learning paths": "I can write basic Python scripts but want to build production APIs. What's in my zone of proximal development?",
        "Mentoring programs": "My mentee can do frontend work independently but struggles with system design. Map their ZPD and plan next steps.",
        "Adaptive curriculum": "Our bootcamp has students at 5 different skill levels. Design adaptive exercises that meet each at their ZPD.",
        "Career development": "I'm a senior engineer wanting to grow into a staff role. Map what I can do now vs. what I need guided practice on.",
    },
    "cognitive_load_manager": {
        "Course design": "My ML course has too much content per session and students are overwhelmed. Analyze and restructure the cognitive load.",
        "UI/UX simplification": "Our settings page has 40+ options on one screen. Analyze the cognitive load and suggest how to restructure.",
        "Training material creation": "I'm writing a guide to Kubernetes. It covers pods, services, deployments, ingress, and volumes. Manage the cognitive load.",
        "Information architecture": "Our docs have 200 pages with no clear hierarchy. Analyze the cognitive load and suggest a better structure.",
    },
    "conceptual_change_analyzer": {
        "Science education": "Students believe heavier objects fall faster. Design a lesson that creates the necessary conceptual change.",
        "Corporate culture change": "Our team believes 'more hours = more productivity.' Help shift this to evidence-based productivity thinking.",
        "Paradigm shifts": "Our company is moving from waterfall to agile. Many managers think agile means 'no planning.' Address this misconception.",
        "Correcting false beliefs": "Our sales team believes lowering prices always increases revenue. Design a conceptual change intervention.",
    },
    # ── ENTERPRISE — Evaluation ──────────────────────────────────────────
    "rubric_designer": {
        "Course assessment design": "Design a rubric for evaluating a capstone machine learning project. Criteria: model quality, code, presentation, novelty.",
        "Hiring scorecards": "Design a rubric for evaluating senior software engineer candidates across coding, system design, collaboration, and leadership.",
        "Code review checklists": "Design a rubric for code review quality: correctness, readability, security, performance, and test coverage.",
        "Project evaluation": "Design a rubric to evaluate proposals for our $100k innovation fund. Criteria: impact, feasibility, alignment, team.",
    },
    "formative_assessment_framework": {
        "Course checkpoints": "Design formative assessments for a 12-week web development bootcamp. Weekly checkpoints that guide learning.",
        "Sprint demos": "Create a formative assessment framework for sprint demos that provides constructive feedback, not just sign-off.",
        "Progress reviews": "Design a monthly progress review framework for junior developers that focuses on growth, not just output.",
        "Coaching check-ins": "Create a formative assessment framework for weekly 1-on-1 coaching sessions with engineering managers.",
    },
    "summative_evaluator": {
        "Final project evaluation": "Evaluate this intern's final project against our criteria: technical depth, code quality, presentation, and impact.",
        "Program review": "Evaluate the effectiveness of our 6-month engineering mentorship program. 20 participants, 2 cohorts.",
        "Annual performance review": "Evaluate an engineer's annual performance against their goals, team contribution, and growth trajectory.",
        "Certification exams": "Design a summative assessment for our internal 'Senior Engineer Certification' covering all required competencies.",
    },
    "peer_assessment_structure": {
        "Code reviews": "Structure a peer code review process for a team of 10 engineers. Ensure fairness, learning, and no hierarchy bias.",
        "Academic peer review": "Structure a peer review process for internal tech talks. Reviewers should provide constructive, actionable feedback.",
        "360-degree feedback": "Design a 360-degree feedback structure for our engineering managers. Include peers, reports, and cross-functional partners.",
        "Team retrospectives": "Structure a peer assessment process for sprint retrospectives where team members give each other constructive feedback.",
    },
    "self_assessment_guide": {
        "Personal development plans": "Guide me through a self-assessment of my engineering skills. I'm a mid-level developer aiming for senior.",
        "Portfolio review": "Help me self-assess my project portfolio for a promotion case. What should I evaluate and against what criteria?",
        "Interview preparation": "Help me self-assess my readiness for a Staff Engineer interview at a FAANG company.",
        "Skill gap analysis": "Self-assess my data engineering skills against the requirements of a modern ML platform team. Find my gaps.",
    },
}


# ---------------------------------------------------------------------------
# TEMPLATE_EXAMPLES  –  example input values for all 85 templates
# ---------------------------------------------------------------------------
TEMPLATE_EXAMPLES: dict[str, dict[str, Any]] = {
    # ── FREE — Analysis ──────────────────────────────────────────────────
    "question_analyzer": {
        "question": "Why did churn spike? Timeline, root cause, and next steps.",
        "context": "Customer success",
        "depth": "comprehensive",
    },
    "data_analyzer": {
        "data_description": "Q3 sales by region: North +5%, South -12%, East +2%, West -8%",
        "goal": "Identify trends and anomalies",
        "context": "SaaS product quarterly review",
    },
    "trend_identifier": {
        "data_description": "Monthly active users: Jan 10k, Feb 12k, Mar 11k, Apr 15k, May 18k, Jun 22k",
        "domain": "SaaS product",
    },
    "gap_analyzer": {
        "current_state": "Manual deployment process taking 2 hours with frequent errors",
        "desired_state": "Automated CI/CD pipeline with <10 min deployments and zero-downtime",
    },
    "swot_analyzer": {
        "subject": "Our mobile app launch in APAC market",
        "context": "B2C fintech, entering market with 3 established competitors",
    },
    "anomaly_detector": {
        "data": "Server response times (ms): 120, 115, 130, 125, 890, 118, 122, 750, 119",
        "baseline": "Normal range 100-150ms",
    },

    # ── FREE — Reasoning ─────────────────────────────────────────────────
    "root_cause_analyzer": {
        "problem": "Support tickets doubled in Q2. Customer complaints up 40%.",
        "context": "SaaS support team, recently launched v3.0",
    },
    "step_by_step_reasoner": {
        "problem": "How should we migrate our monolith to microservices without downtime?",
        "context": "E-commerce platform, 50k daily users, Python/Django",
    },
    "causal_reasoner": {
        "phenomenon": "Employee turnover increased 30% after switching to remote-first policy",
        "context": "Mid-size tech company, 200 employees",
    },
    "analogical_reasoner": {
        "concept": "Kubernetes container orchestration",
        "domain": "Explain using a restaurant kitchen analogy",
    },
    "hypothesis_generator": {
        "observation": "Conversion rate dropped 15% last week despite no code changes",
        "domain": "E-commerce checkout flow",
    },

    # ── FREE — Creative ──────────────────────────────────────────────────
    "idea_generator": {
        "challenge": "Reduce user onboarding time from 15 minutes to under 3 minutes",
        "context": "B2B SaaS analytics platform",
    },
    "brainstormer": {
        "topic": "Ways to increase developer community engagement",
        "goal": "Generate 10 creative, low-cost solutions",
    },
    "innovation_framework": {
        "challenge": "Disrupting traditional real estate transactions",
        "context": "PropTech startup, early stage",
    },
    "design_thinker": {
        "challenge": "Redesign the patient check-in experience at hospitals",
        "users": "Elderly patients, busy nurses, hospital administrators",
    },
    "metaphor_generator": {
        "concept": "Machine learning model training",
        "audience": "Business executives with no technical background",
    },

    # ── FREE — Communication ─────────────────────────────────────────────
    "technical_translator": {
        "technical_text": "We implemented a Redis-backed LRU cache with a TTL of 300s and circuit-breaker pattern for the downstream gRPC service.",
        "target_audience": "Product managers",
    },
    "simplification_engine": {
        "complex_topic": "Quantum entanglement and its implications for secure communication",
        "audience": "High school students",
    },
    "persuasion_framework": {
        "goal": "Convince the board to invest $2M in AI infrastructure",
        "audience": "CFO and board members focused on ROI",
    },
    "narrative_builder": {
        "topic": "How our startup went from 0 to 1M users in 18 months",
        "audience": "Investors and potential partners",
    },
    "feedback_composer": {
        "situation": "Team member consistently delivers late but high-quality work",
        "goal": "Improve timeliness while maintaining quality and morale",
    },
    "clarity_optimizer": {
        "text": "We should probably look into maybe implementing some kind of caching solution that could potentially improve performance somewhat.",
        "goal": "Maximum clarity and decisiveness",
    },
    "audience_adapter": {
        "message": "Our API latency p99 is 450ms due to N+1 queries in the ORM layer, which we can fix with eager loading and query batching.",
        "current_audience": "Adapt for the CEO quarterly report",
    },

    # ── FREE — Planning ──────────────────────────────────────────────────
    "stakeholder_mapper": {
        "project": "Company-wide migration from on-premise to cloud infrastructure",
        "context": "Financial services company, 500 employees, regulatory requirements",
    },
    "scenario_planner": {
        "topic": "AI regulation impact on our SaaS product roadmap",
        "timeframe": "3 years (2026-2029)",
    },
    "resource_allocator": {
        "resources": "Engineering team of 12, $500k budget, 6-month timeline",
        "needs": ["New feature development", "Tech debt reduction", "Security improvements", "Customer support"],
    },
    "priority_setter": {
        "items": ["API redesign", "Mobile app launch", "Security audit", "Performance optimization", "Documentation overhaul"],
        "goal": "Maximize customer impact with limited engineering bandwidth",
    },
    "deadline_manager": {
        "tasks": ["Design (2w)", "Backend API (3w)", "Frontend (3w)", "Testing (2w)", "Security review (1w)", "Deployment (1w)"],
        "deadline": "Ship by April 30, 2026",
    },

    # ── FREE — Specialized ───────────────────────────────────────────────
    "code_reviewer": {
        "code": "def get_user(id):\n    user = db.query(f'SELECT * FROM users WHERE id = {id}')\n    return user",
        "context": "Python web application, security-focused review",
    },
    "content_outliner": {
        "topic": "Complete Guide to Context Engineering for LLMs",
        "goal": "Technical blog post for experienced developers, 3000 words",
    },
    "socratic_questioner": {
        "statement": "We should rewrite our entire backend in Rust for better performance.",
        "context": "Engineering team discussion, current stack is Python/FastAPI",
    },
    "intent_recognizer": {
        "input": "This product exceeded my expectations! Best purchase I've made all year. Would definitely recommend to friends.",
        "context": "Product review on e-commerce platform",
        "depth": "comprehensive",
    },
    "ambiguity_resolver": {
        "input": "It could go either way depending on how you look at it and what the team decides.",
        "context": "Decision feedback from a stakeholder meeting",
        "depth": "thorough",
    },
    "risk_assessor": {
        "decision": "Migrate production database from PostgreSQL to CockroachDB",
        "context": "Financial services, 99.99% uptime requirement, 2TB data",
    },
    "risk_mitigator": {
        "risk": "Key engineer leaving during critical migration phase",
        "impact": "3-month project delay, knowledge loss on legacy system",
    },
    "impact_assessor": {
        "action": "Deprecating v1 API and requiring all clients to migrate to v2",
        "context": "Public API with 500+ third-party integrations",
    },
    "conflict_resolver": {
        "conflict": "Frontend team wants React, backend team insists on server-rendered templates for SEO",
        "parties": "Frontend lead, Backend lead, Product manager",
    },
    "concept_explainer": {
        "concept": "Eventual consistency in distributed systems",
        "audience": "Junior developers joining the team",
    },
    "synthesis_builder": {
        "sources": "Customer surveys (NPS 45), support ticket analysis (top 5 issues), competitor benchmarking (3 competitors), sales team feedback",
        "goal": "Unified product improvement roadmap recommendation",
    },

    # ── ENTERPRISE — Decision ────────────────────────────────────────────
    "decision_framework": {
        "decision": "Choose primary database for new microservices architecture: PostgreSQL vs. MongoDB vs. DynamoDB",
    },
    "comparative_analyzer": {
        "options": "Kubernetes vs. Docker Swarm vs. AWS ECS",
        "criteria": "Cost, learning curve, scalability, community support, enterprise features",
    },
    "tradeoff_analyzer": {
        "situation": "Building in-house ML platform vs. using managed services (SageMaker/Vertex AI)",
        "objectives": "Cost control, team learning, time-to-market, customization",
        "context": "Series B startup, 8-person ML team",
    },
    "multi_objective_optimizer": {
        "objectives": "Minimize latency, maximize throughput, minimize cost, maintain 99.9% availability",
    },
    "cost_benefit_analyzer": {
        "decision": "Investing $500K in automated testing infrastructure",
    },

    # ── ENTERPRISE — Problem Solving ─────────────────────────────────────
    "problem_decomposer": {
        "problem": "Our platform takes 45 seconds to load for users in Asia-Pacific region",
    },
    "bottleneck_identifier": {
        "system": "E-commerce checkout flow: Browse → Cart → Address → Payment → Confirmation",
        "context": "70% drop-off between Cart and Payment steps",
    },
    "constraint_optimizer": {
        "objective": "Maximize feature delivery speed",
        "constraints": "Budget $200k, team of 5, must maintain SOC2 compliance, 6-month deadline",
    },
    "dependency_mapper": {
        "system": "Microservices: auth-service, user-service, payment-service, notification-service, analytics-service",
        "context": "Planning order of migration from monolith",
    },
    "efficiency_analyzer": {
        "process": "Code review process: Author submits PR → 2 reviewers assigned → Reviews completed → CI runs → Merge",
        "context": "Average PR takes 3.5 days to merge, team of 15 engineers",
    },
    "trade_space_explorer": {
        "problem": "Design a caching layer for our API: what are the architectures, trade-offs, and optimal configurations?",
        "context": "100k requests/min, 80% read traffic, 500MB working set",
    },

    # ── ENTERPRISE — Temporal ────────────────────────────────────────────
    "temporal_sequence_analyzer": {
        "events": "Q1: New competitor launched. Q2: Support tickets doubled. Q3: Customer complaints up 40%. Q4: Churn rate hit 8%.",
        "time_span": "12 months (2025)",
        "context": "B2B SaaS company decline analysis",
    },
    "future_scenario_planner": {
        "focal_question": "How will AI regulation affect our product in the EU market?",
        "time_horizon": "5 years (2026-2031)",
        "current_situation": "SaaS AI product serving 200 EU enterprise clients",
    },
    "historical_context_mapper": {
        "current_situation": "We're considering a major platform rewrite to gain performance",
        "question": "What historical precedents exist for successful (and failed) platform rewrites?",
    },

    # ── ENTERPRISE — Diagnostic ──────────────────────────────────────────
    "diagnostic_root_cause_analyzer": {
        "problem": "Customer satisfaction score collapsed from 85 to 52 in one quarter",
        "symptoms": "Q3: Complaints up 40%. Q2: New pricing launched. Q1: Support team reduced by 30%.",
    },
    "differential_diagnoser": {
        "presenting_problem": "Application intermittently returns 500 errors under load",
        "observed_data": "CPU normal, memory spikes to 95%, happens during peak hours, started after last deployment",
        "domain": "Cloud-hosted web application",
    },
    "system_health_auditor": {
        "system": "Production Kubernetes cluster (3 nodes, 45 pods, 12 services)",
        "audit_focus": "Security posture and resource utilization",
    },

    # ── ENTERPRISE — Synthesis ───────────────────────────────────────────
    "holistic_integrator": {
        "topic": "Post-acquisition integration strategy",
        "perspectives": "Technical: API compatibility. Business: revenue synergies. Cultural: team morale and retention.",
    },
    "pattern_recognition_engine": {
        "data": "Customer behavior: Users who complete onboarding in <5 min have 3x retention. Users from referrals convert 40% more. Enterprise users churn 50% less than SMB.",
        "pattern_focus": "Retention and growth drivers",
    },
    "cross_domain_synthesizer": {
        "target_problem": "Reducing technical debt in software projects",
        "source_domains": "Urban planning (infrastructure maintenance), Medicine (preventive care), Manufacturing (predictive maintenance)",
    },

    # ── ENTERPRISE — Systems Thinking ────────────────────────────────────
    "feedback_loop_identifier": {
        "system": "SaaS product growth: Users → Content → More Users → Revenue → Features → Users",
        "behavior": "Growth plateaued despite increasing marketing spend",
    },
    "leverage_point_finder": {
        "system": "Enterprise sales process: Lead gen → Qualification → Demo → Proposal → Close",
        "goal": "Double close rate from 15% to 30%",
    },
    "emergence_detector": {
        "system": "Remote-first engineering team of 50 across 8 time zones",
        "components": "Async communication, code reviews, stand-ups, documentation, social channels",
    },
    "system_archetype_analyzer": {
        "system": "Startup hiring: More features needed → Hire fast → Quality issues → More features needed to fix",
        "pattern": "Possible 'Fixes That Fail' or 'Shifting the Burden'",
    },
    "causal_loop_diagrammer": {
        "system": "Customer satisfaction ecosystem",
        "variables": "Product quality, Customer satisfaction, Word-of-mouth, New customers, Revenue, R&D investment",
    },
    "stock_flow_analyzer": {
        "system": "Technical debt in a growing codebase",
        "focus": "How tech debt accumulates (inflow from shortcuts) and depletes (outflow from refactoring)",
    },

    # ── ENTERPRISE — Metacognition ───────────────────────────────────────
    "metacognitive_monitor": {
        "task_description": "Designing a new authentication system for our platform",
        "current_approach": "Reviewing OAuth 2.0 + PKCE implementations",
        "progress_so_far": "Completed threat model, started sequence diagrams",
        "challenges": "Unsure whether to support SAML for enterprise clients",
    },
    "self_regulation_framework": {
        "goal": "Complete AWS Solutions Architect certification within 3 months",
        "context": "Full-time engineer, can dedicate 5 hours/week to study",
    },
    "cognitive_strategy_selector": {
        "task_type": "Understanding a large, unfamiliar codebase (200k lines) in a new language",
        "context": "New team member, Go/gRPC codebase, 2-week ramp-up goal",
    },
    "learning_from_experience": {
        "experience_description": "Our last product launch was 2 months late despite careful planning. Key factors: scope creep, underestimated QA, dependency on external API partner.",
        "context": "Planning next product launch, similar scale",
    },
    "error_detection_framework": {
        "work_to_check": "Our conclusion that users prefer feature A over feature B based on a survey of 50 users",
        "context": "Product decision impacting roadmap for next 2 quarters",
    },

    # ── ENTERPRISE — Ethical Reasoning ───────────────────────────────────
    "ethical_framework_analyzer": {
        "decision": "Whether to implement facial recognition in our retail stores for loss prevention",
        "context": "National retail chain, 500 stores, diverse customer base",
    },
    "moral_dilemma_resolver": {
        "dilemma": "Our AI model is more accurate but uses personal data users didn't explicitly consent to for training",
        "conflicting_principles": "Product quality vs. User privacy",
        "context": "Health-tech startup, regulatory grey area",
    },
    "stakeholder_ethics_assessor": {
        "decision": "Automating 200 customer service positions with AI chatbots",
        "stakeholders": "Employees (200 jobs), Customers, Shareholders, Local community",
    },
    "value_conflict_navigator": {
        "situation": "Open-sourcing our core algorithm vs. keeping it proprietary",
        "competing_values": "Community contribution and transparency vs. competitive advantage and revenue",
        "value_a": "Open-source community building",
        "value_b": "Business sustainability and competitive moat",
    },
    "consequentialist_analyzer": {
        "action": "Releasing an AI model that can generate realistic deepfakes",
        "scope": "Society-wide: creators, journalists, political actors, general public",
    },

    # ── ENTERPRISE — Learning ────────────────────────────────────────────
    "scaffolding_framework": {
        "task": "Learning to build and deploy machine learning models",
        "current_skill_level": "Intermediate Python, basic statistics, no ML experience",
        "goal": "Deploy a production ML model within 3 months",
    },
    "spaced_repetition_optimizer": {
        "learning_material": "AWS Certified Solutions Architect exam topics (networking, compute, storage, security, architecture)",
        "initial_mastery": "Familiar with EC2 and S3, new to VPC and IAM in-depth",
        "previous_performance": "Practice exam score: 62%",
    },
    "zone_of_proximal_development": {
        "learner_current_abilities": "Can write REST APIs, understands SQL, familiar with Docker basics",
        "learning_goal": "Build and operate a production Kubernetes deployment",
    },
    "cognitive_load_manager": {
        "learning_material": "Introduction to distributed systems: consensus algorithms, CAP theorem, eventual consistency, Raft, Paxos",
        "learner_background": "Senior frontend developer transitioning to backend/infrastructure",
    },
    "conceptual_change_analyzer": {
        "topic": "Asynchronous programming — from synchronous mental model to event-loop thinking",
        "current_understanding": "Believes code executes line-by-line, confused by callbacks and Promises",
    },

    # ── ENTERPRISE — Evaluation ──────────────────────────────────────────
    "rubric_designer": {
        "assessment_task": "Evaluate the quality of technical design documents",
        "learning_objectives": "Clarity, completeness, feasibility, risk identification, alignment with requirements",
        "rubric_type": "analytic",
    },
    "formative_assessment_framework": {
        "learning_unit": "Module 3: API Design Principles",
        "learning_goal": "Students can design RESTful APIs following best practices",
    },
    "summative_evaluator": {
        "course_title": "Full-Stack Web Development Bootcamp",
        "learning_outcomes": "Build and deploy a full-stack app, implement authentication, use CI/CD, write tests",
    },
    "peer_assessment_structure": {
        "assessment_task": "Review teammate's system design proposal",
        "learning_objective": "Improve design quality through constructive peer feedback",
    },
    "self_assessment_guide": {
        "work_to_assess": "My leadership effectiveness over the past quarter",
        "success_criteria": "Team satisfaction, project delivery, mentoring impact, communication clarity",
    },
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def _has_generic_prompt(name: str) -> bool:
    """Check if a template has a GENERIC_PROMPT defined."""
    if not get_pattern_class:
        return False
    try:
        klass = get_pattern_class(name, include_enterprise=True)
        return klass is not None and getattr(klass, "GENERIC_PROMPT", None) is not None
    except Exception:
        return False


def list_templates() -> list[dict[str, Any]]:
    """List all 85 templates with enriched metadata."""
    results = []
    for name, cat, desc in FULL_PATTERN_CATALOG:
        meta = TEMPLATE_METADATA.get(name, {})
        ex = TEMPLATE_EXAMPLES.get(name, {})
        reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("problem", {}))
        primary_key = reg[0] if reg else "problem"
        sample_prompt = ex.get(primary_key, next(iter(ex.values()), "")) if ex else ""
        results.append({
            "name": name,
            "category": cat,
            "description": meta.get("description", desc),
            "license": cat,
            "use_cases": meta.get("use_cases", []),
            "research_basis": meta.get("research_basis", ""),
            "theme": meta.get("theme", ""),
            "has_examples": name in TEMPLATE_EXAMPLES,
            "param_count": len(PATTERN_BUILD_CONTEXT_REGISTRY.get(name, ("", {}))[1]) + 1,
            "has_generic_prompt": _has_generic_prompt(name),
            "sample_prompt": str(sample_prompt)[:200] if sample_prompt else "",
            "use_case_prompts": USE_CASE_PROMPTS.get(name, {}),
        })
    return results


def get_template_params(name: str) -> dict[str, Any] | None:
    """Get build_context params (primary + defaults + metadata) for a template."""
    reg = PATTERN_BUILD_CONTEXT_REGISTRY.get(name)
    if not reg:
        return None
    primary, defaults = reg
    merged: dict[str, Any] = {"primary": primary, "defaults": dict(defaults)}
    examples = TEMPLATE_EXAMPLES.get(name)
    if examples:
        merged["example_values"] = examples
    meta = TEMPLATE_METADATA.get(name)
    if meta:
        merged["description"] = meta.get("description")
        merged["use_cases"] = meta.get("use_cases", [])
        merged["parameter_descriptions"] = meta.get("parameter_descriptions", {})
        merged["research_basis"] = meta.get("research_basis", "")
        merged["theme"] = meta.get("theme", "")
    merged["use_case_prompts"] = USE_CASE_PROMPTS.get(name, {})
    if "parameter_descriptions" not in merged:
        merged["parameter_descriptions"] = {primary: "Primary input"}
        merged["parameter_descriptions"].update({k: k.replace("_", " ") for k in defaults})
    return merged


def build_context(name: str, params: dict[str, Any]) -> Any:
    """Build context for a template. Returns Context or None."""
    if not get_pattern_class:
        return None
    Klass = get_pattern_class(name, include_enterprise=True)
    if not Klass:
        return None
    return Klass().build_context(**params)


def get_generic_prompt(name: str, question: str, include_enterprise: bool = True) -> str | None:
    """Get the filled generic prompt for a template. Returns prompt string or None."""
    if not get_generic_prompt_for:
        return None
    try:
        return get_generic_prompt_for(name, question, include_enterprise=include_enterprise)
    except Exception:
        return None
