"""
Pattern Catalog - Single source of truth for all 88 cognitive patterns.

Contains pattern metadata, keyword mappings, and derived lookup dicts.
Extracted from pattern_suggester.py for single-responsibility.
"""


ENTERPRISE_LICENSE_NOTE = " Requires enterprise license. Set include_enterprise=True to use."


# (name, category, one-line description) for all 88 templates (all unique names)
FULL_PATTERN_CATALOG: list[tuple[str, str, str]] = [
    # FREE - Analysis (2)
    ("question_analyzer", "free", "Decomposes a question into sub-questions, identifies assumptions, clarifies scope"),
    ("data_analyzer", "free", "Structured data analysis: extract patterns, trends, metrics, and actionable insights"),
    ("trend_identifier", "enterprise", "Identifies trends, inflection points, and patterns over time in data"),
    ("gap_analyzer", "enterprise", "Finds gaps between current state and desired state; identifies what's missing"),
    ("swot_analyzer", "enterprise", "Strengths, Weaknesses, Opportunities, Threats framework for strategic analysis"),
    ("anomaly_detector", "enterprise", "Detects outliers, anomalies, and unusual patterns in data or processes"),
    # FREE - Reasoning (3)
    ("root_cause_analyzer", "free", "Five Whys + Ishikawa root cause investigation for problems and failures"),
    ("step_by_step_reasoner", "free", "Breaks complex reasoning into explicit logical steps with justification"),
    ("causal_reasoner", "enterprise", "Traces cause-and-effect chains: why did X happen, what led to Y"),
    ("analogical_reasoner", "enterprise", "Draws parallels from similar domains or situations to generate insight"),
    ("hypothesis_generator", "free", "Generates testable hypotheses from observations and evidence"),
    # FREE - Creative (1)
    ("idea_generator", "enterprise", "Divergent thinking to generate novel ideas with structured evaluation"),
    ("brainstormer", "free", "Structured brainstorming with quantity, diversity, and no-judgment rules"),
    ("innovation_framework", "enterprise", "Innovation methodology: reframe problems, find novel approaches"),
    ("design_thinker", "enterprise", "Design thinking: empathize, define, ideate, prototype, test"),
    ("metaphor_generator", "enterprise", "Creates illuminating metaphors and analogies for complex concepts"),
    # FREE - Communication (2)
    ("technical_translator", "free", "Translates technical jargon into plain language for non-technical audiences"),
    ("simplification_engine", "enterprise", "Simplifies complex content while preserving accuracy and nuance"),
    ("persuasion_framework", "enterprise", "Structures persuasive arguments with evidence, logic, and emotional appeal"),
    ("narrative_builder", "enterprise", "Builds compelling narratives with story structure and engagement hooks"),
    ("feedback_composer", "enterprise", "Composes constructive, actionable feedback with specific examples"),
    ("clarity_optimizer", "enterprise", "Optimizes text for clarity, removing ambiguity and improving readability"),
    ("audience_adapter", "free", "Adapts content for specific audience expertise level and interests"),
    # FREE - Planning (2)
    ("stakeholder_mapper", "free", "Maps stakeholders by influence, interest, and impact; identifies key players"),
    ("scenario_planner", "free", "Creates multiple future scenarios with probabilities and contingency plans"),
    ("resource_allocator", "enterprise", "Optimal resource allocation across competing priorities and constraints"),
    ("priority_setter", "enterprise", "Ranks priorities using weighted criteria and urgency/importance matrix"),
    ("deadline_manager", "enterprise", "Creates timeline with milestones, dependencies, and buffer management"),
    # FREE - Specialized (6)
    ("code_reviewer", "free", "Risk-aware code review: orient-then-analyze cognitive flow across 7 dimensions (correctness, security, performance, design, resilience, testing, maintainability)"),
    ("content_outliner", "enterprise", "Creates structured content outlines with hierarchy and flow"),
    ("socratic_questioner", "free", "Asks probing questions to uncover hidden assumptions and deepen understanding"),
    ("intent_recognizer", "free", "Identifies the core intent, goals, and motivations behind a query"),
    ("ambiguity_resolver", "enterprise", "Identifies and resolves ambiguous terms, phrases, and requirements"),
    ("risk_assessor", "free", "Evaluates risks by likelihood, impact, and suggests mitigation strategies"),
    ("risk_mitigator", "enterprise", "Develops specific risk mitigation plans with contingencies"),
    ("impact_assessor", "enterprise", "Assesses downstream effects and consequences of decisions or changes"),
    ("conflict_resolver", "free", "Mediates conflicts by identifying interests, finding common ground"),
    ("concept_explainer", "enterprise", "Explains complex concepts using layered depth: simple → technical → expert"),
    ("synthesis_builder", "free", "Synthesizes multiple sources into a coherent, integrated summary"),
    ("rag_answerer", "enterprise", "Grounded answer generation from retrieved context with citation and abstention"),
    ("query_planner", "enterprise", "Pre-retrieval query analysis: classify, decompose, rewrite (HyDE + step-back), and plan retrieval strategy for RAG pipelines"),
    ("memory_compressor", "enterprise", "Compress conversations and documents into structured state for long-context memory"),
    # ENTERPRISE - Decision (5)
    ("decision_framework", "enterprise", "Structured decision-making with weighted criteria, options evaluation, and recommendations"),
    ("comparative_analyzer", "enterprise", "Side-by-side comparison across multiple dimensions with explicit scoring"),
    ("tradeoff_analyzer", "enterprise", "Analyzes trade-offs with pros/cons, risk profiles, and recommended path"),
    ("multi_objective_optimizer", "enterprise", "Optimizes across multiple competing objectives using Pareto analysis"),
    ("cost_benefit_analyzer", "enterprise", "Comprehensive cost-benefit analysis with ROI, payback period, risk-adjusted returns"),
    # ENTERPRISE - Problem Solving (6)
    ("problem_decomposer", "enterprise", "Decomposes complex problems into manageable sub-problems with dependencies"),
    ("bottleneck_identifier", "enterprise", "Identifies bottlenecks and constraints limiting system performance"),
    ("constraint_optimizer", "enterprise", "Finds optimal solutions within hard and soft constraints"),
    ("dependency_mapper", "enterprise", "Maps dependencies between components, teams, and processes"),
    ("efficiency_analyzer", "enterprise", "Analyzes process efficiency: waste, redundancy, optimization opportunities"),
    ("trade_space_explorer", "enterprise", "Explores the design space of alternatives and their feasibility"),
    # ENTERPRISE - Temporal (3)
    ("temporal_sequence_analyzer", "enterprise", "Builds event timelines, identifies causal sequences and trigger points"),
    ("future_scenario_planner", "enterprise", "Creates 2x2 scenario matrices for strategic planning and what-if analysis"),
    ("historical_context_mapper", "enterprise", "Extracts lessons from historical precedents and analogous situations"),
    # ENTERPRISE - Diagnostic (3)
    ("diagnostic_root_cause_analyzer", "enterprise", "Full diagnostic: Five Whys + Ishikawa + fault tree + systemic failure analysis"),
    ("differential_diagnoser", "enterprise", "Systematically rules out hypotheses to arrive at most likely diagnosis"),
    ("system_health_auditor", "enterprise", "Comprehensive system audit across reliability, performance, security dimensions"),
    # ENTERPRISE - Synthesis (3)
    ("holistic_integrator", "enterprise", "Integrates multiple perspectives into unified, multi-dimensional analysis"),
    ("pattern_recognition_engine", "enterprise", "Identifies recurring patterns, correlations, and hidden structures in data"),
    ("cross_domain_synthesizer", "enterprise", "Borrows proven solutions from other industries and domains"),
    # ENTERPRISE - Systems Thinking (6)
    ("feedback_loop_identifier", "enterprise", "Identifies reinforcing and balancing feedback loops in complex systems"),
    ("leverage_point_finder", "enterprise", "Finds high-impact intervention points where small changes create large effects"),
    ("emergence_detector", "enterprise", "Detects emergent properties arising from system interactions"),
    ("system_archetype_analyzer", "enterprise", "Applies system archetypes (tragedy of commons, fixes that fail, etc.)"),
    ("causal_loop_diagrammer", "enterprise", "Creates causal loop diagrams showing system dynamics"),
    ("stock_flow_analyzer", "enterprise", "Analyzes stocks, flows, and accumulation in dynamic systems"),
    # ENTERPRISE - Metacognition (5)
    ("metacognitive_monitor", "enterprise", "Monitors and improves the thinking process itself"),
    ("self_regulation_framework", "enterprise", "Framework for self-regulation: plan, monitor, evaluate, adjust"),
    ("cognitive_strategy_selector", "enterprise", "Selects optimal cognitive strategies for different problem types"),
    ("learning_from_experience", "enterprise", "Structured after-action review to extract lessons learned"),
    ("error_detection_framework", "enterprise", "Detects reasoning errors, biases, and logical fallacies"),
    # ENTERPRISE - Ethical Reasoning (5)
    ("ethical_framework_analyzer", "enterprise", "Applies multiple ethical frameworks: deontological, utilitarian, virtue ethics"),
    ("moral_dilemma_resolver", "enterprise", "Navigates moral dilemmas with structured analysis of competing values"),
    ("stakeholder_ethics_assessor", "enterprise", "Assesses ethical impact on all stakeholders"),
    ("value_conflict_navigator", "enterprise", "Navigates conflicts between competing values and principles"),
    ("consequentialist_analyzer", "enterprise", "Analyzes decisions by their consequences across stakeholders"),
    # ENTERPRISE - Learning (5)
    ("scaffolding_framework", "enterprise", "Provides progressive learning scaffolding matched to skill level"),
    ("spaced_repetition_optimizer", "enterprise", "Optimizes retention through spaced repetition scheduling"),
    ("zone_of_proximal_development", "enterprise", "Identifies the learner's ZPD for optimal challenge level"),
    ("cognitive_load_manager", "enterprise", "Manages cognitive load to prevent overwhelm and optimize learning"),
    ("conceptual_change_analyzer", "enterprise", "Facilitates conceptual change by addressing misconceptions"),
    # ENTERPRISE - Evaluation (5)
    ("rubric_designer", "enterprise", "Designs assessment rubrics with clear criteria and performance levels"),
    ("formative_assessment_framework", "enterprise", "Creates formative assessments for continuous improvement"),
    ("summative_evaluator", "enterprise", "Comprehensive summative evaluation with criteria-based scoring"),
    ("peer_assessment_structure", "enterprise", "Structures effective peer assessment with calibration"),
    ("self_assessment_guide", "enterprise", "Guides self-assessment with reflection prompts and benchmarks"),
]

NAME_TO_CATEGORY = {name: cat for name, cat, _ in FULL_PATTERN_CATALOG}
NAME_TO_DESCRIPTION = {name: desc for name, _, desc in FULL_PATTERN_CATALOG}
VALID_PATTERN_NAMES = set(NAME_TO_CATEGORY.keys())
PATTERN_CATALOG = "\n".join(f"{n} [{c}]: {d}" for n, c, d in FULL_PATTERN_CATALOG)

# ---------------------------------------------------------------------------
# ENRICHED_CATALOG — when_to_use, use_cases, theme for all 88 templates.
# Bridges rich metadata from template_service.py into the SDK intelligence layer.
# ---------------------------------------------------------------------------
ENRICHED_CATALOG: dict = {
    # Analysis
    "question_analyzer": {"theme": "Data & Analytics", "when_to_use": "Use when the question is multi-part, ambiguous, or needs decomposition before analysis.", "use_cases": ["Unclear requirements", "Multi-part questions", "Pre-analysis triage"], "output_type": "Decomposed sub-questions with scope and assumptions"},
    "data_analyzer": {"theme": "Data & Analytics", "when_to_use": "Use when the question involves interpreting datasets, metrics, or quantitative evidence.", "use_cases": ["Sales analysis", "Metrics review", "Dashboard insights"], "output_type": "Statistical findings, patterns, and actionable insights report"},
    "trend_identifier": {"theme": "Data & Analytics", "when_to_use": "Use when the question involves time-series data or detecting patterns over time.", "use_cases": ["KPI tracking", "Market trend analysis", "Technology adoption curves"], "output_type": "Trend analysis with inflection points and trajectories"},
    "gap_analyzer": {"theme": "Strategic Thinking", "when_to_use": "Use when the question compares a current state to a desired state and asks what's missing.", "use_cases": ["Requirements gaps", "Competitive gaps", "Skills assessment"], "output_type": "Gap analysis comparing current vs desired state"},
    "swot_analyzer": {"theme": "Strategic Thinking", "when_to_use": "Use when the question requires strategic assessment of strengths, weaknesses, opportunities, and threats.", "use_cases": ["Business strategy", "Product launches", "Market positioning"], "output_type": "SWOT matrix with strategic implications"},
    "anomaly_detector": {"theme": "Data & Analytics", "when_to_use": "Use when the question involves finding outliers or unexpected patterns in data.", "use_cases": ["Fraud detection", "Quality control", "System monitoring"], "output_type": "Anomaly report with outliers and unusual patterns"},
    # Reasoning
    "root_cause_analyzer": {"theme": "Problem Investigation", "when_to_use": "Use when the question asks WHY something failed or went wrong and needs systematic root cause identification.", "use_cases": ["Production outages", "Support ticket spikes", "Performance degradation", "Incident postmortems"], "output_type": "Root cause analysis with evidence chains"},
    "step_by_step_reasoner": {"theme": "Problem Investigation", "when_to_use": "Use when the question needs clear sequential logic or a walkthrough explanation.", "use_cases": ["Logic walkthroughs", "Troubleshooting guides", "Teaching explanations"], "output_type": "Step-by-step logical walkthrough with justification"},
    "causal_reasoner": {"theme": "Problem Investigation", "when_to_use": "Use when the question asks about cause-and-effect chains — what led to an outcome.", "use_cases": ["Root cause chains", "Policy impact analysis", "Debugging complex systems"], "output_type": "Cause-effect chain analysis"},
    "analogical_reasoner": {"theme": "Innovation & Creativity", "when_to_use": "Use when explaining something unfamiliar by drawing parallels to a familiar domain.", "use_cases": ["Explaining technical concepts", "Cross-industry learning", "Creative problem solving"], "output_type": "Cross-domain analogies and transferable insights"},
    "hypothesis_generator": {"theme": "Data & Analytics", "when_to_use": "Use when the question requires generating testable explanations for observed phenomena.", "use_cases": ["Scientific research", "A/B test design", "Market research"], "output_type": "Testable hypotheses with evidence mapping"},
    # Creative
    "idea_generator": {"theme": "Innovation & Creativity", "when_to_use": "Use when the question asks for novel ideas or creative solutions.", "use_cases": ["Product features", "Marketing campaigns", "Process improvements"], "output_type": "Ranked novel ideas with structured evaluation"},
    "brainstormer": {"theme": "Innovation & Creativity", "when_to_use": "Use when the question needs divergent thinking and quantity of ideas.", "use_cases": ["Team brainstorms", "Sprint planning", "Strategy sessions"], "output_type": "Diverse idea set with categorization"},
    "innovation_framework": {"theme": "Innovation & Creativity", "when_to_use": "Use when the question involves disruptive innovation or reframing an industry problem.", "use_cases": ["New product development", "Business model innovation", "Market disruption"], "output_type": "Innovation proposals with feasibility assessment"},
    "design_thinker": {"theme": "Innovation & Creativity", "when_to_use": "Use when the question involves user-centered design or improving a human experience.", "use_cases": ["UX design", "Service design", "Product development"], "output_type": "Design thinking artifacts with user-centered insights"},
    "metaphor_generator": {"theme": "Communication & Clarity", "when_to_use": "Use when the question needs illuminating metaphors to explain complex concepts.", "use_cases": ["Technical presentations", "Teaching", "Marketing copy"], "output_type": "Illuminating metaphors and analogies"},
    # Communication
    "technical_translator": {"theme": "Communication & Clarity", "when_to_use": "Use when technical jargon needs to be translated for non-technical audiences.", "use_cases": ["Executive summaries", "Client communications", "Documentation"], "output_type": "Plain-language translation of technical content"},
    "simplification_engine": {"theme": "Communication & Clarity", "when_to_use": "Use when complex content needs to be simplified while preserving accuracy.", "use_cases": ["Policy simplification", "User guides", "Patient education"], "output_type": "Simplified content preserving accuracy"},
    "persuasion_framework": {"theme": "Communication & Clarity", "when_to_use": "Use when the question requires building a persuasive argument or proposal.", "use_cases": ["Sales pitches", "Proposals", "Fundraising"], "output_type": "Structured persuasive argument with evidence"},
    "narrative_builder": {"theme": "Communication & Clarity", "when_to_use": "Use when the question needs a compelling story or narrative structure.", "use_cases": ["Case studies", "Keynote presentations", "Brand storytelling"], "output_type": "Compelling narrative with story structure"},
    "feedback_composer": {"theme": "Communication & Clarity", "when_to_use": "Use when the question involves giving constructive, actionable feedback.", "use_cases": ["Performance reviews", "Code review comments", "Customer responses"], "output_type": "Constructive actionable feedback with examples"},
    "clarity_optimizer": {"theme": "Communication & Clarity", "when_to_use": "Use when text needs to be made clearer and less ambiguous.", "use_cases": ["Email drafts", "Requirements documents", "Contracts"], "output_type": "Clarity-optimized text"},
    "audience_adapter": {"theme": "Communication & Clarity", "when_to_use": "Use when content needs to be tailored for a specific audience's expertise level.", "use_cases": ["Multi-stakeholder reports", "Training materials", "Marketing segments"], "output_type": "Audience-adapted content"},
    # Planning
    "stakeholder_mapper": {"theme": "Project Management", "when_to_use": "Use when the question involves identifying who is affected by or influences a decision.", "use_cases": ["Project kickoffs", "Organizational change", "Product launches"], "output_type": "Stakeholder map with influence and interest analysis"},
    "scenario_planner": {"theme": "Strategic Thinking", "when_to_use": "Use when the question requires exploring multiple future possibilities and contingencies.", "use_cases": ["Strategic planning", "Market entry", "Crisis preparedness"], "output_type": "Multiple future scenarios with probabilities and contingencies"},
    "resource_allocator": {"theme": "Project Management", "when_to_use": "Use when the question involves distributing limited resources (budget, people, time) across competing needs.", "use_cases": ["Budget allocation", "Team assignments", "Portfolio management"], "output_type": "Resource allocation plan with trade-offs"},
    "priority_setter": {"theme": "Project Management", "when_to_use": "Use when the question requires ranking items by importance, urgency, or impact.", "use_cases": ["Sprint backlog", "Feature prioritization", "Strategic initiatives"], "output_type": "Prioritized ranking with weighted criteria"},
    "deadline_manager": {"theme": "Project Management", "when_to_use": "Use when the question involves managing timelines, milestones, and dependencies.", "use_cases": ["Project timelines", "Release planning", "Event coordination"], "output_type": "Timeline with milestones and dependencies"},
    # Specialized
    "code_reviewer": {"theme": "Evaluation & Quality", "when_to_use": "Use when the question involves reviewing code for correctness, security, resilience, or design — uses a risk-weighted cognitive flow that skips style (linters handle that).", "use_cases": ["Pull request reviews", "Security audits", "Failure-mode analysis", "Pre-merge risk assessment"], "output_type": "Risk-weighted code review across 7 dimensions"},
    "content_outliner": {"theme": "Communication & Clarity", "when_to_use": "Use when the question needs a structured content outline or hierarchy.", "use_cases": ["Blog posts", "Whitepapers", "Course curriculum"], "output_type": "Structured content outline with hierarchy"},
    "socratic_questioner": {"theme": "Self-Improvement", "when_to_use": "Use when the question benefits from probing deeper to uncover hidden assumptions.", "use_cases": ["Coaching sessions", "Requirements elicitation", "Critical thinking"], "output_type": "Probing questions exposing hidden assumptions"},
    "intent_recognizer": {"theme": "Data & Analytics", "when_to_use": "Use when the question involves understanding the underlying intent or motivation in text.", "use_cases": ["Customer support triage", "Chatbot design", "Survey analysis"], "output_type": "Intent classification with confidence and goals"},
    "ambiguity_resolver": {"theme": "Communication & Clarity", "when_to_use": "Use when the question involves text with unclear wording, hedging, or multiple interpretations.", "use_cases": ["Requirements clarification", "Contract review", "Bug report triage"], "output_type": "Disambiguated requirements with resolved interpretations"},
    "risk_assessor": {"theme": "Risk & Compliance", "when_to_use": "Use when the question asks about potential risks, threats, or what could go wrong.", "use_cases": ["Project risk registers", "Investment due diligence", "Migration planning"], "output_type": "Risk matrix with likelihood, impact, and mitigations"},
    "risk_mitigator": {"theme": "Risk & Compliance", "when_to_use": "Use when identified risks need specific mitigation plans and contingencies.", "use_cases": ["Risk response planning", "Business continuity", "Disaster recovery"], "output_type": "Mitigation plans with contingencies"},
    "impact_assessor": {"theme": "Risk & Compliance", "when_to_use": "Use when the question asks about downstream effects and consequences of a change.", "use_cases": ["Policy changes", "System migrations", "Product deprecation"], "output_type": "Impact assessment of downstream effects"},
    "conflict_resolver": {"theme": "Communication & Clarity", "when_to_use": "Use when the question involves mediating disagreements or finding common ground.", "use_cases": ["Team disputes", "Customer complaints", "Contract negotiations"], "output_type": "Conflict resolution path with common ground"},
    "concept_explainer": {"theme": "Learning & Development", "when_to_use": "Use when a complex concept needs clear, layered explanation for different skill levels.", "use_cases": ["Technical documentation", "Training materials", "Onboarding guides"], "output_type": "Layered explanation from simple to expert"},
    "synthesis_builder": {"theme": "Data & Analytics", "when_to_use": "Use when multiple information sources need to be combined into a coherent summary.", "use_cases": ["Literature reviews", "Market research synthesis", "Board reports"], "output_type": "Synthesized summary integrating multiple sources"},
    "rag_answerer": {"theme": "Data & Analytics", "when_to_use": "Use when answering questions from retrieved documents (RAG pipelines).", "use_cases": ["Q&A over docs", "Knowledge base chatbots", "Document summarization", "Evidence-based synthesis"], "output_type": "Cited answer grounded in retrieved documents"},
    "query_planner": {"theme": "Data & Analytics", "when_to_use": "Use before retrieval to analyze, decompose, and rewrite queries for better RAG results. Complements rag_answerer.", "use_cases": ["Multi-hop question decomposition", "Query rewriting for better retrieval", "HyDE document generation", "RAG query routing"], "output_type": "Decomposed and rewritten queries for retrieval"},
    "memory_compressor": {"theme": "Data & Analytics", "when_to_use": "Use when compressing long conversations or documents into structured memory state.", "use_cases": ["Multi-turn agent memory", "Context window management", "Progressive summarization", "Long-context retention"], "output_type": "Compressed memory state preserving key information"},
    # Decision
    "decision_framework": {"theme": "Strategic Thinking", "when_to_use": "Use when the question requires choosing between options with weighted criteria evaluation.", "use_cases": ["Technology selection", "Vendor evaluation", "Architecture decisions"], "output_type": "Decision matrix with weighted criteria evaluation"},
    "comparative_analyzer": {"theme": "Strategic Thinking", "when_to_use": "Use when the question asks to compare multiple options side-by-side across dimensions.", "use_cases": ["Product comparison", "Framework selection", "Vendor evaluation"], "output_type": "Side-by-side comparison across dimensions"},
    "tradeoff_analyzer": {"theme": "Strategic Thinking", "when_to_use": "Use when the question involves competing objectives and explicit trade-offs (pros vs cons).", "use_cases": ["Build vs buy", "Speed vs quality", "Cost vs features"], "output_type": "Trade-off analysis with pros and cons"},
    "multi_objective_optimizer": {"theme": "Strategic Thinking", "when_to_use": "Use when multiple conflicting objectives need Pareto-optimal solutions.", "use_cases": ["Portfolio optimization", "Feature prioritization", "Supply chain design"], "output_type": "Pareto-optimal solutions across objectives"},
    "cost_benefit_analyzer": {"theme": "Strategic Thinking", "when_to_use": "Use when the question requires ROI analysis or comparing costs against benefits.", "use_cases": ["Investment decisions", "Project proposals", "Policy evaluation"], "output_type": "Cost-benefit analysis with ROI calculation"},
    # Problem Solving
    "problem_decomposer": {"theme": "Problem Investigation", "when_to_use": "Use when a complex problem needs to be broken into smaller, manageable sub-problems.", "use_cases": ["System architecture", "Large project scoping", "Organizational challenges"], "output_type": "Decomposed sub-problems with dependencies"},
    "bottleneck_identifier": {"theme": "Problem Investigation", "when_to_use": "Use when the question involves finding what's limiting performance or throughput.", "use_cases": ["Production bottlenecks", "CI/CD optimization", "Customer journey friction"], "output_type": "Identified bottlenecks with throughput analysis"},
    "constraint_optimizer": {"theme": "Problem Investigation", "when_to_use": "Use when the question involves optimizing within given hard and soft constraints.", "use_cases": ["Budget-constrained projects", "Regulatory compliance", "Scheduling"], "output_type": "Optimized solution within constraints"},
    "dependency_mapper": {"theme": "Systems & Complexity", "when_to_use": "Use when the question involves mapping dependencies between components, teams, or processes.", "use_cases": ["Microservice architectures", "Project planning", "Supply chain mapping"], "output_type": "Dependency map with critical path"},
    "efficiency_analyzer": {"theme": "Problem Investigation", "when_to_use": "Use when the question involves finding waste, redundancy, or optimization opportunities.", "use_cases": ["Manufacturing optimization", "DevOps pipeline", "Meeting productivity"], "output_type": "Efficiency analysis with optimization opportunities"},
    "trade_space_explorer": {"theme": "Strategic Thinking", "when_to_use": "Use when the question requires exploring a design space of alternatives and feasibility.", "use_cases": ["Architecture selection", "Product configuration", "Engineering design"], "output_type": "Design space exploration with feasibility assessment"},
    # Temporal
    "temporal_sequence_analyzer": {"theme": "Data & Analytics", "when_to_use": "Use when the question involves building timelines or finding causal sequences in events.", "use_cases": ["Incident timelines", "Product evolution analysis", "Market shift tracking"], "output_type": "Timeline of events with causal sequence"},
    "future_scenario_planner": {"theme": "Strategic Thinking", "when_to_use": "Use when the question requires generating and evaluating multiple plausible future scenarios.", "use_cases": ["5-year strategy", "Technology disruption planning", "Regulatory change"], "output_type": "Future scenarios with probability and contingency"},
    "historical_context_mapper": {"theme": "Strategic Thinking", "when_to_use": "Use when the question benefits from learning from historical precedents and analogies.", "use_cases": ["Strategic lessons", "Policy precedents", "Industry evolution"], "output_type": "Historical lessons and precedent analysis"},
    # Diagnostic
    "diagnostic_root_cause_analyzer": {"theme": "Problem Investigation", "when_to_use": "Use for deep diagnostic investigations requiring Five Whys + Ishikawa + fault tree + systemic failure analysis.", "use_cases": ["Critical incidents", "Manufacturing defects", "Customer satisfaction collapse"], "output_type": "Deep diagnostic investigation with fault tree"},
    "differential_diagnoser": {"theme": "Problem Investigation", "when_to_use": "Use when multiple possible causes exist and hypotheses must be systematically ruled out.", "use_cases": ["Complex bug diagnosis", "Medical diagnostics", "System failure analysis"], "output_type": "Differential diagnosis with ruled-in/out hypotheses"},
    "system_health_auditor": {"theme": "Risk & Compliance", "when_to_use": "Use when a system needs comprehensive health assessment across multiple dimensions.", "use_cases": ["Infrastructure audit", "Application health check", "Compliance review"], "output_type": "System health audit across dimensions"},
    # Synthesis
    "holistic_integrator": {"theme": "Systems & Complexity", "when_to_use": "Use when the question requires combining technical, business, and human perspectives into a unified view.", "use_cases": ["Cross-functional strategy", "M&A integration", "Change management"], "output_type": "Unified cross-functional perspective"},
    "pattern_recognition_engine": {"theme": "Data & Analytics", "when_to_use": "Use when the question involves finding recurring patterns, correlations, or hidden structures.", "use_cases": ["Customer behavior patterns", "Code smell detection", "Market cycles"], "output_type": "Identified patterns and correlations"},
    "cross_domain_synthesizer": {"theme": "Innovation & Creativity", "when_to_use": "Use when solutions can be borrowed from other industries or domains.", "use_cases": ["Biomimicry", "Cross-industry innovation", "Technology transfer"], "output_type": "Cross-domain synthesis with transferable insights"},
    # Systems Thinking
    "feedback_loop_identifier": {"theme": "Systems & Complexity", "when_to_use": "Use when the question involves understanding reinforcing or balancing feedback loops.", "use_cases": ["Business model dynamics", "Product growth loops", "Ecosystem analysis"], "output_type": "Identified feedback loops with dynamics"},
    "leverage_point_finder": {"theme": "Systems & Complexity", "when_to_use": "Use when the question asks where small interventions can create the largest system change.", "use_cases": ["Organizational transformation", "Policy design", "Process improvement"], "output_type": "High-leverage intervention points"},
    "emergence_detector": {"theme": "Systems & Complexity", "when_to_use": "Use when the question involves emergent properties arising from system interactions.", "use_cases": ["Organizational culture", "Market dynamics", "Team dynamics"], "output_type": "Emergent properties and system interactions"},
    "system_archetype_analyzer": {"theme": "Systems & Complexity", "when_to_use": "Use when the question matches common system patterns like 'Limits to Growth' or 'Shifting the Burden'.", "use_cases": ["Growth strategy", "Failure pattern diagnosis", "Policy pitfall avoidance"], "output_type": "System archetype diagnosis with intervention strategy"},
    "causal_loop_diagrammer": {"theme": "Systems & Complexity", "when_to_use": "Use when the question requires visualizing system causality and feedback relationships.", "use_cases": ["System dynamics modeling", "Strategy workshops", "Root cause visualization"], "output_type": "Causal loop diagram with feedback relationships"},
    "stock_flow_analyzer": {"theme": "Systems & Complexity", "when_to_use": "Use when the question involves accumulations (stocks) and rates of change (flows).", "use_cases": ["Inventory management", "Cash flow analysis", "Technical debt accumulation"], "output_type": "Stock-flow analysis with accumulation dynamics"},
    # Metacognition
    "metacognitive_monitor": {"theme": "Self-Improvement", "when_to_use": "Use when the question involves monitoring and improving one's own thinking process.", "use_cases": ["Learning reflection", "Decision auditing", "AI prompt refinement"], "output_type": "Thinking process audit with improvement suggestions"},
    "self_regulation_framework": {"theme": "Self-Improvement", "when_to_use": "Use when the question involves goal setting and self-regulated performance improvement.", "use_cases": ["Goal setting", "Habit building", "Professional development"], "output_type": "Self-regulated performance improvement plan"},
    "cognitive_strategy_selector": {"theme": "Self-Improvement", "when_to_use": "Use when choosing the best thinking strategy for a particular task type.", "use_cases": ["Study method selection", "Problem-solving approach", "AI workflow design"], "output_type": "Recommended cognitive strategies for the task"},
    "learning_from_experience": {"theme": "Self-Improvement", "when_to_use": "Use when the question involves extracting lessons from past successes or failures.", "use_cases": ["Project retrospectives", "After-action reviews", "Career reflection"], "output_type": "Lessons learned with actionable takeaways"},
    "error_detection_framework": {"theme": "Self-Improvement", "when_to_use": "Use when reasoning, work, or decisions need to be checked for errors, biases, or logical fallacies.", "use_cases": ["Proof review", "Decision auditing", "Bias checking"], "output_type": "Error and bias detection report"},
    # Ethical Reasoning
    "ethical_framework_analyzer": {"theme": "Ethics & Governance", "when_to_use": "Use when the question requires applying ethical frameworks (utilitarian, deontological, virtue, etc.).", "use_cases": ["AI ethics review", "Corporate policy decisions", "Regulatory compliance"], "output_type": "Multi-framework ethical analysis"},
    "moral_dilemma_resolver": {"theme": "Ethics & Governance", "when_to_use": "Use when ethical principles are in direct conflict and a resolution is needed.", "use_cases": ["AI safety decisions", "Medical triage", "Privacy vs security"], "output_type": "Ethical dilemma resolution with reasoning"},
    "stakeholder_ethics_assessor": {"theme": "Ethics & Governance", "when_to_use": "Use when assessing the ethical impact of a decision on all affected stakeholders.", "use_cases": ["AI fairness audit", "Environmental impact", "Corporate social responsibility"], "output_type": "Stakeholder ethical impact assessment"},
    "value_conflict_navigator": {"theme": "Ethics & Governance", "when_to_use": "Use when deeply held values compete (e.g., security vs privacy, profit vs purpose).", "use_cases": ["Policy design", "Product feature trade-offs", "Organizational values alignment"], "output_type": "Value conflict resolution path"},
    "consequentialist_analyzer": {"theme": "Ethics & Governance", "when_to_use": "Use when evaluating decisions by their long-term consequences across stakeholders.", "use_cases": ["Policy impact analysis", "Technology deployment ethics", "Environmental decisions"], "output_type": "Long-term consequence analysis across stakeholders"},
    # Learning
    "scaffolding_framework": {"theme": "Learning & Development", "when_to_use": "Use when building progressive learning support matched to skill level.", "use_cases": ["Employee onboarding", "Student tutoring", "Skill development programs"], "output_type": "Progressive learning scaffolds by skill level"},
    "spaced_repetition_optimizer": {"theme": "Learning & Development", "when_to_use": "Use when optimizing retention through spaced learning schedules.", "use_cases": ["Language learning", "Certification prep", "Sales training"], "output_type": "Optimized spaced learning schedule"},
    "zone_of_proximal_development": {"theme": "Learning & Development", "when_to_use": "Use when determining optimal challenge level for a learner.", "use_cases": ["Personalized learning paths", "Mentoring programs", "Adaptive curriculum"], "output_type": "Optimal challenge level assessment"},
    "cognitive_load_manager": {"theme": "Learning & Development", "when_to_use": "Use when learning content risks overwhelming the learner.", "use_cases": ["Course design", "UI/UX simplification", "Information architecture"], "output_type": "Cognitive load reduction strategy"},
    "conceptual_change_analyzer": {"theme": "Learning & Development", "when_to_use": "Use when learners have misconceptions that need to be corrected.", "use_cases": ["Science education", "Corporate culture change", "Paradigm shifts"], "output_type": "Misconception correction strategy"},
    # Evaluation
    "rubric_designer": {"theme": "Evaluation & Quality", "when_to_use": "Use when creating assessment criteria with clear performance levels.", "use_cases": ["Course assessment design", "Hiring scorecards", "Code review checklists"], "output_type": "Assessment rubric with performance levels"},
    "formative_assessment_framework": {"theme": "Evaluation & Quality", "when_to_use": "Use when designing improvement-focused assessments for ongoing learning.", "use_cases": ["Course checkpoints", "Sprint demos", "Coaching check-ins"], "output_type": "Formative assessment design for ongoing improvement"},
    "summative_evaluator": {"theme": "Evaluation & Quality", "when_to_use": "Use when evaluating overall performance against established standards.", "use_cases": ["Final project evaluation", "Program review", "Certification exams"], "output_type": "Summative evaluation against standards"},
    "peer_assessment_structure": {"theme": "Evaluation & Quality", "when_to_use": "Use when structuring peer review for fairness and constructive feedback.", "use_cases": ["Code reviews", "Academic peer review", "360-degree feedback"], "output_type": "Structured peer review protocol"},
    "self_assessment_guide": {"theme": "Evaluation & Quality", "when_to_use": "Use when guiding systematic self-evaluation against success criteria.", "use_cases": ["Personal development plans", "Portfolio review", "Skill gap analysis"], "output_type": "Self-assessment guide with criteria"},
}

# Generate theme-grouped, enriched catalog text for LLM consumption
_BY_THEME: dict = {}
for _n, _c, _d in FULL_PATTERN_CATALOG:
    _enr = ENRICHED_CATALOG.get(_n, {})
    _theme = _enr.get("theme", "Other")
    _BY_THEME.setdefault(_theme, []).append((_n, _c, _d, _enr))

_THEME_ORDER = [
    "Problem Investigation", "Strategic Thinking", "Data & Analytics",
    "Risk & Compliance", "Communication & Clarity", "Project Management",
    "Innovation & Creativity", "Systems & Complexity", "Ethics & Governance",
    "Learning & Development", "Evaluation & Quality", "Self-Improvement",
]

ENRICHED_CATALOG_TEXT = ""
for _theme in _THEME_ORDER:
    _items = _BY_THEME.get(_theme, [])
    if not _items:
        continue
    ENRICHED_CATALOG_TEXT += f"\n## {_theme}\n"
    for _n, _c, _d, _enr in _items:
        _wtu = _enr.get("when_to_use", "")
        _uc = ", ".join(_enr.get("use_cases", [])[:3])
        _ot = _enr.get("output_type", "")
        ENRICHED_CATALOG_TEXT += f"  {_n} [{_c}]: {_d}\n"
        if _wtu:
            ENRICHED_CATALOG_TEXT += f"    WHEN: {_wtu}\n"
        if _ot:
            ENRICHED_CATALOG_TEXT += f"    PRODUCES: {_ot}\n"
        if _uc:
            ENRICHED_CATALOG_TEXT += f"    USE CASES: {_uc}\n"

# Keep the flat catalog for backward compatibility
_GROUPED: dict = {}
for _n, _c, _d in FULL_PATTERN_CATALOG:
    _group = _c
    _GROUPED.setdefault(_group, []).append((_n, _d))

CATALOG_FOR_LLM = ""
for _tier in ("free", "enterprise"):
    CATALOG_FOR_LLM += f"\n{'FREE' if _tier == 'free' else 'ENTERPRISE'} TEMPLATES:\n"
    for _n, _d in _GROUPED.get(_tier, []):
        CATALOG_FOR_LLM += f"  {_n}: {_d}\n"


# Keyword -> (pattern_name, category, reason_snippet) - ALL 88 templates
PATTERN_MAP: list[tuple[list[str], tuple[str, str, str]]] = [
    # FREE - Analysis
    (["question", "analyze", "clarify", "what is", "unclear"], ("question_analyzer", "free", "Question analysis")),
    (["data", "trend", "metrics", "numbers", "dataset", "csv"], ("data_analyzer", "free", "Data analysis")),
    (["trend", "trends", "over time", "pattern in data"], ("trend_identifier", "enterprise", "Trend identification")),
    (["gap", "gaps", "missing", "lacks", "shortfall"], ("gap_analyzer", "enterprise", "Gap analysis")),
    (["swot", "strengths", "weaknesses", "opportunities", "threats"], ("swot_analyzer", "enterprise", "SWOT analysis")),
    (["anomaly", "anomalies", "outlier", "outliers", "unusual"], ("anomaly_detector", "enterprise", "Anomaly detection")),
    # FREE - Reasoning
    (["step by step", "explain", "how does", "reasoning", "logic", "walk through"], ("step_by_step_reasoner", "free", "Step-by-step reasoning")),
    (["cause", "causes", "causal", "why", "because", "led to", "resulted in", "reason for", "what caused"], ("causal_reasoner", "enterprise", "Causal reasoning")),
    (["analogy", "analogous", "like", "similar to", "compare to"], ("analogical_reasoner", "enterprise", "Analogical reasoning")),
    (["hypothesis", "hypotheses", "test", "guess", "suppose"], ("hypothesis_generator", "free", "Hypothesis generation")),
    # FREE - Creative
    (["idea", "ideas", "brainstorm", "come up with"], ("idea_generator", "enterprise", "Idea generation")),
    (["brainstorm", "ideation", "creative"], ("brainstormer", "free", "Brainstorming")),
    (["innovate", "innovation", "new approach", "novel"], ("innovation_framework", "enterprise", "Innovation")),
    (["design thinking", "design", "user-centric"], ("design_thinker", "enterprise", "Design thinking")),
    (["metaphor", "metaphors", "like a", "analogy"], ("metaphor_generator", "enterprise", "Metaphor generation")),
    # FREE - Communication
    (["translate", "technical", "non-technical", "explain to"], ("technical_translator", "free", "Technical translation")),
    (["simplify", "simple", "simplification", "clearer"], ("simplification_engine", "enterprise", "Simplification")),
    (["persuade", "persuasion", "convince", "argue for"], ("persuasion_framework", "enterprise", "Persuasion")),
    (["narrative", "story", "storytelling"], ("narrative_builder", "enterprise", "Narrative building")),
    (["feedback", "give feedback", "constructive"], ("feedback_composer", "enterprise", "Feedback composition")),
    (["clarity", "clear", "lucid", "unclear"], ("clarity_optimizer", "enterprise", "Clarity optimization")),
    (["audience", "adapt", "tailor", "target"], ("audience_adapter", "free", "Audience adaptation")),
    # FREE - Planning
    (["stakeholder", "stakeholders", "who is involved"], ("stakeholder_mapper", "free", "Stakeholder mapping")),
    (["scenario", "scenarios", "plan for"], ("scenario_planner", "free", "Scenario planning")),
    (["resource", "resources", "allocate", "budget"], ("resource_allocator", "enterprise", "Resource allocation")),
    (["priority", "priorities", "prioritize", "rank"], ("priority_setter", "enterprise", "Priority setting")),
    (["deadline", "deadlines", "timeline", "due date"], ("deadline_manager", "enterprise", "Deadline management")),
    # FREE - Specialized
    (["code", "review", "pull request", "implementation", "codereview"], ("code_reviewer", "free", "Code review")),
    (["outline", "content", "structure"], ("content_outliner", "enterprise", "Content outlining")),
    (["socratic", "probe", "question", "explore"], ("socratic_questioner", "free", "Socratic questioning")),
    (["intent", "what do they want", "goal"], ("intent_recognizer", "free", "Intent recognition")),
    (["ambiguity", "ambiguous", "unclear meaning"], ("ambiguity_resolver", "enterprise", "Ambiguity resolution")),
    (["risk", "risks", "what could go wrong", "threat"], ("risk_assessor", "free", "Risk assessment")),
    (["mitigate", "mitigation", "reduce risk"], ("risk_mitigator", "enterprise", "Risk mitigation")),
    (["impact", "affect", "effect", "consequences"], ("impact_assessor", "enterprise", "Impact assessment")),
    (["conflict", "conflicts", "disagree", "dispute"], ("conflict_resolver", "free", "Conflict resolution")),
    (["concept", "concepts", "explain", "define"], ("concept_explainer", "enterprise", "Concept explanation")),
    (["synthesis", "synthesize", "combine"], ("synthesis_builder", "free", "Synthesis building")),
    (["rag", "retrieval", "retrieved", "grounded", "knowledge base", "document qa", "citation"], ("rag_answerer", "enterprise", "RAG answer generation")),
    (["query plan", "decompose query", "sub-query", "hyde", "pre-retrieval", "query rewrite", "query routing", "multi-hop"], ("query_planner", "enterprise", "Query planning for RAG")),
    (["memory", "compress", "compression", "summarize conversation", "agent memory", "context window"], ("memory_compressor", "enterprise", "Memory compression")),
    # ENTERPRISE - Decision
    (["should we", "should i", "decide", "decision", "choose between"], ("decision_framework", "enterprise", "Decision framework")),
    (["compare", "versus", "vs", "better", "difference between"], ("comparative_analyzer", "enterprise", "Comparison analysis")),
    (["trade-off", "tradeoff", "trade off", "pros and cons"], ("tradeoff_analyzer", "enterprise", "Trade-off analysis")),
    (["multi-objective", "multiple goals", "pareto", "optimize"], ("multi_objective_optimizer", "enterprise", "Multi-objective optimization")),
    (["cost benefit", "cost-benefit", "roi", "payback"], ("cost_benefit_analyzer", "enterprise", "Cost-benefit analysis")),
    # ENTERPRISE - Problem Solving / FREE root cause
    (["problem", "fix", "solve", "issue", "troubleshoot", "outage", "failure", "crash", "bug", "broken", "went wrong"], ("root_cause_analyzer", "free", "Problem investigation (free RCA)")),
    (["decompose", "break down", "analyze parts", "components"], ("problem_decomposer", "enterprise", "Problem decomposition")),
    (["bottleneck", "bottlenecks", "constraint", "limiting"], ("bottleneck_identifier", "enterprise", "Bottleneck identification")),
    (["constraint", "constraints", "optimize within"], ("constraint_optimizer", "enterprise", "Constraint optimization")),
    (["dependency", "dependencies", "depends on"], ("dependency_mapper", "enterprise", "Dependency mapping")),
    (["efficiency", "efficient", "optimize process"], ("efficiency_analyzer", "enterprise", "Efficiency analysis")),
    (["trade space", "design space", "alternatives"], ("trade_space_explorer", "enterprise", "Trade space exploration")),
    # ENTERPRISE - Temporal
    (["timeline", "sequence", "when did", "order of events", "chronological", "over time"], ("temporal_sequence_analyzer", "enterprise", "Events/sequence analysis")),
    (["scenario", "future", "what if", "planning horizon", "5 years", "10 years"], ("future_scenario_planner", "enterprise", "Future scenario planning")),
    (["historical", "precedent", "past", "learn from history"], ("historical_context_mapper", "enterprise", "Historical context")),
    # ENTERPRISE - Diagnostic (full RCA, requires license)
    (["root cause", "root causes", "why did", "why is", "why does", "why was", "why are",
      "five whys", "fishbone", "ishikawa", "what caused", "spike", "drop",
      "churn", "decline", "incident", "outage", "degradation"], ("diagnostic_root_cause_analyzer", "enterprise", "Full diagnostic root cause analysis")),
    (["diagnose", "differential", "multiple possible", "hypothesis", "ruled out"], ("differential_diagnoser", "enterprise", "Differential diagnosis")),
    (["system health", "audit", "check", "status", "health check"], ("system_health_auditor", "enterprise", "System health audit")),
    # ENTERPRISE - Synthesis
    (["integrate", "holistic", "multiple perspectives", "combine", "synthesize"], ("holistic_integrator", "enterprise", "Multi-perspective synthesis")),
    (["pattern", "recognize", "recurring", "trend in data", "identify pattern"], ("pattern_recognition_engine", "enterprise", "Pattern recognition")),
    (["cross-domain", "borrow from", "analogy", "other industry", "innovation"], ("cross_domain_synthesizer", "enterprise", "Cross-domain synthesis")),
    # ENTERPRISE - Systems Thinking
    (["feedback loop", "reinforcing", "balancing", "system dynamics"], ("feedback_loop_identifier", "enterprise", "Feedback loop analysis")),
    (["leverage point", "intervention", "high impact", "where to act"], ("leverage_point_finder", "enterprise", "Leverage point identification")),
    (["emergence", "emergent", "emerging properties"], ("emergence_detector", "enterprise", "Emergence detection")),
    (["archetype", "system archetype"], ("system_archetype_analyzer", "enterprise", "System archetype analysis")),
    (["causal loop", "loop diagram"], ("causal_loop_diagrammer", "enterprise", "Causal loop diagramming")),
    (["stock", "flow", "accumulation", "stocks and flows"], ("stock_flow_analyzer", "enterprise", "Stock-flow analysis")),
    # ENTERPRISE - Metacognition
    (["metacogn", "self-monitor", "thinking about thinking"], ("metacognitive_monitor", "enterprise", "Metacognitive monitoring")),
    (["self-regulat", "self regulation", "regulate"], ("self_regulation_framework", "enterprise", "Self-regulation")),
    (["cognitive strategy", "strategy selection"], ("cognitive_strategy_selector", "enterprise", "Cognitive strategy selection")),
    (["learn from experience", "after action", "retrospective"], ("learning_from_experience", "enterprise", "Learning from experience")),
    (["error detection", "detect error", "mistake"], ("error_detection_framework", "enterprise", "Error detection")),
    # ENTERPRISE - Ethical Reasoning
    (["ethical", "ethics", "moral", "dilemma", "right or wrong"], ("ethical_framework_analyzer", "enterprise", "Ethical analysis")),
    (["moral dilemma", "ethical dilemma"], ("moral_dilemma_resolver", "enterprise", "Moral dilemma resolution")),
    (["stakeholder", "who is affected", "impact on"], ("stakeholder_ethics_assessor", "enterprise", "Stakeholder ethics")),
    (["value conflict", "values conflict"], ("value_conflict_navigator", "enterprise", "Value conflict navigation")),
    (["consequentialist", "consequences", "utilitarian"], ("consequentialist_analyzer", "enterprise", "Consequentialist analysis")),
    # ENTERPRISE - Learning
    (["learn", "teaching", "scaffold", "skill level", "zone of proximal"], ("scaffolding_framework", "enterprise", "Learning scaffolding")),
    (["spaced repetition", "spacing", "retention"], ("spaced_repetition_optimizer", "enterprise", "Spaced repetition")),
    (["zpd", "zone of proximal", "proximal development"], ("zone_of_proximal_development", "enterprise", "Zone of proximal development")),
    (["cognitive load", "load", "working memory"], ("cognitive_load_manager", "enterprise", "Cognitive load management")),
    (["conceptual change", "misconception", "conceptual"], ("conceptual_change_analyzer", "enterprise", "Conceptual change analysis")),
    # ENTERPRISE - Evaluation
    (["assess", "evaluate", "rubric", "criteria", "score"], ("rubric_designer", "enterprise", "Assessment rubric")),
    (["formative", "formative assessment"], ("formative_assessment_framework", "enterprise", "Formative assessment")),
    (["summative", "summative assessment", "final eval"], ("summative_evaluator", "enterprise", "Summative evaluation")),
    (["peer assess", "peer evaluation", "peer review"], ("peer_assessment_structure", "enterprise", "Peer assessment")),
    (["self assess", "self-assessment", "self eval"], ("self_assessment_guide", "enterprise", "Self-assessment")),
]


# ---------------------------------------------------------------------------
# GENERIC_PROMPT_FALLBACK — maps enterprise templates to the closest free
# template that has a GENERIC_PROMPT.  Used when the complexity router
# selects an enterprise template but the user needs a generic prompt
# (e.g. free-tier, or static compilation).
# ---------------------------------------------------------------------------
GENERIC_PROMPT_FALLBACK: dict = {
    # Reasoning
    "causal_reasoner": "root_cause_analyzer",
    "analogical_reasoner": "hypothesis_generator",
    # Analysis
    "trend_identifier": "data_analyzer",
    "gap_analyzer": "question_analyzer",
    "swot_analyzer": "data_analyzer",
    "anomaly_detector": "data_analyzer",
    # Creative
    "idea_generator": "brainstormer",
    "innovation_framework": "brainstormer",
    "design_thinker": "brainstormer",
    "metaphor_generator": "brainstormer",
    # Communication
    "simplification_engine": "technical_translator",
    "persuasion_framework": "audience_adapter",
    "narrative_builder": "audience_adapter",
    "feedback_composer": "audience_adapter",
    "clarity_optimizer": "technical_translator",
    # Planning
    "resource_allocator": "risk_assessor",
    "priority_setter": "risk_assessor",
    "deadline_manager": "scenario_planner",
    # Decision
    "decision_framework": "risk_assessor",
    "comparative_analyzer": "data_analyzer",
    "tradeoff_analyzer": "risk_assessor",
    "multi_objective_optimizer": "risk_assessor",
    "cost_benefit_analyzer": "data_analyzer",
    # Problem Solving
    "problem_decomposer": "step_by_step_reasoner",
    "bottleneck_identifier": "root_cause_analyzer",
    "constraint_optimizer": "step_by_step_reasoner",
    "dependency_mapper": "stakeholder_mapper",
    "efficiency_analyzer": "data_analyzer",
    "trade_space_explorer": "scenario_planner",
    # Temporal
    "temporal_sequence_analyzer": "data_analyzer",
    "future_scenario_planner": "scenario_planner",
    "historical_context_mapper": "synthesis_builder",
    # Diagnostic
    "diagnostic_root_cause_analyzer": "root_cause_analyzer",
    "differential_diagnoser": "root_cause_analyzer",
    "system_health_auditor": "code_reviewer",
    # Synthesis
    "holistic_integrator": "synthesis_builder",
    "pattern_recognition_engine": "data_analyzer",
    "cross_domain_synthesizer": "synthesis_builder",
    # Systems Thinking
    "feedback_loop_identifier": "root_cause_analyzer",
    "leverage_point_finder": "root_cause_analyzer",
    "emergence_detector": "hypothesis_generator",
    "system_archetype_analyzer": "root_cause_analyzer",
    "causal_loop_diagrammer": "root_cause_analyzer",
    "stock_flow_analyzer": "data_analyzer",
    # Metacognition
    "metacognitive_monitor": "socratic_questioner",
    "self_regulation_framework": "step_by_step_reasoner",
    "cognitive_strategy_selector": "question_analyzer",
    "learning_from_experience": "synthesis_builder",
    "error_detection_framework": "root_cause_analyzer",
    # Ethical Reasoning
    "ethical_framework_analyzer": "stakeholder_mapper",
    "moral_dilemma_resolver": "conflict_resolver",
    "stakeholder_ethics_assessor": "stakeholder_mapper",
    "value_conflict_navigator": "conflict_resolver",
    "consequentialist_analyzer": "risk_assessor",
    # Learning
    "scaffolding_framework": "step_by_step_reasoner",
    "spaced_repetition_optimizer": "step_by_step_reasoner",
    "zone_of_proximal_development": "question_analyzer",
    "cognitive_load_manager": "question_analyzer",
    "conceptual_change_analyzer": "socratic_questioner",
    # Evaluation
    "rubric_designer": "data_analyzer",
    "formative_assessment_framework": "question_analyzer",
    "summative_evaluator": "synthesis_builder",
    "peer_assessment_structure": "code_reviewer",
    "self_assessment_guide": "socratic_questioner",
}
