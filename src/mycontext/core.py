"""
Core Context class - The heart of mycontext

This is where Context as Code™ comes to life.

Research-backed prompt flow (when ``research_flow=True``):

  PRIMACY ZONE    → ① Role  ② Goal          (Liu et al. 2023)
  INSTRUCTIONS    → ③ Rules  ④ Style         (OpenAI guide)
  MIDDLE          → ⑤ Reasoning  ⑥ Examples  (Li et al. 2025)
  LATE            → ⑦ Output Format  ⑧ Guard Rails  (CO-STAR)
  RECENCY ZONE    → ⑨ Task (ALWAYS LAST)     (Li et al. 2023)

See docs/PROMPT_FLOW_RESEARCH.md for full references.
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .foundation import Constraints, Directive, Guidance

# ── Thinking-strategy registry ────────────────────────────────────
THINKING_STRATEGIES: dict[str, tuple[str, str]] = {
    "step_by_step": (
        "Chain of Thought",
        "Think through this step by step. Break the problem down into "
        "stages, show your reasoning at each stage, then give your final answer.",
    ),
    "multiple_angles": (
        "Tree of Thought",
        "Before answering, brainstorm at least 3 different approaches or "
        "perspectives. Briefly evaluate the strengths and weaknesses of each, "
        "then choose the best approach and explain why.",
    ),
    "verify": (
        "Self-Reflection",
        "After providing your answer, critically review it. Check for errors, "
        "missing information, unsupported claims, or logical gaps. If you find "
        "issues, revise your answer.",
    ),
    "explain_simply": (
        "Simplification",
        "Explain your reasoning in simple, everyday language that anyone can "
        "understand. Avoid jargon and technical terms. Use analogies where helpful.",
    ),
    "creative": (
        "Divergent Thinking",
        "Explore unconventional, surprising, and creative ideas. Don't limit "
        "yourself to the obvious answer. Challenge assumptions and consider "
        "perspectives that others might miss.",
    ),
}


class Context(BaseModel):
    """
    Core Context class that represents a complete contextual environment for LLM interaction.

    The Context is the fundamental building block that combines:
    - Guidance (system-level behavioral rules)
    - Directives (specific instructions)
    - Knowledge (memory, documents, state)
    - Data (user inputs and parameters)

    Example:
        ```python
        from mycontext import Context, Guidance

        # Simple usage
        context = Context("You are a helpful assistant")

        # Research-backed flow with all the bells and whistles
        context = Context(
            guidance=Guidance(
                role="Expert code reviewer",
                goal="Find security vulnerabilities",
                rules=["Focus on OWASP Top 10"],
                style="Direct and actionable",
            ),
            directive=Directive("Review this code: ..."),
            constraints=Constraints(
                must_not_include=["personal opinions"],
                output_schema=[{"name": "severity", "type": "str"}],
            ),
            thinking_strategy="verify",
            examples=[
                {"input": "eval(user_input)", "output": "Critical: code injection"},
            ],
            research_flow=True,
        )
        ```
    """

    guidance: Guidance | None = Field(
        default=None,
        description="System-level behavioral guidance"
    )

    directive: Directive | None = Field(
        default=None,
        description="Specific instruction for this interaction"
    )

    constraints: Constraints | None = Field(
        default=None,
        description="Hard constraints and guardrails"
    )

    knowledge: str | None = Field(
        default=None,
        description="Retrieved knowledge, documents, or memory context"
    )

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data and parameters"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about this context (tags, version, etc.)"
    )

    # ── Research-flow extensions (all optional, backward-compatible) ──

    thinking_strategy: str | None = Field(
        default=None,
        description=(
            "Reasoning strategy key — one of: step_by_step, multiple_angles, "
            "verify, explain_simply, creative"
        ),
    )

    examples: list[dict[str, str]] | None = Field(
        default=None,
        description="Few-shot examples — list of {'input': str, 'output': str}",
    )

    research_flow: bool = Field(
        default=False,
        description=(
            "When True, assemble() uses the research-backed 9-section ordering "
            "with emphasis formatting.  When False (default), classic assembly."
        ),
    )

    def __init__(
        self,
        guidance: str | Guidance | None = None,
        directive: str | Directive | None = None,
        **kwargs
    ):
        """
        Initialize a Context.

        Args:
            guidance: System-level guidance (can be string or Guidance object)
            directive: Specific directive (can be string or Directive object)
            **kwargs: Additional parameters (data, constraints, etc.)
        """
        # Convert simple strings to appropriate objects
        if isinstance(guidance, str):
            guidance = Guidance(role=guidance)

        if isinstance(directive, str):
            directive = Directive(content=directive)

        super().__init__(guidance=guidance, directive=directive, **kwargs)

    @classmethod
    def from_skill(
        cls,
        skill_or_path: Path | str | Any,
        task: str | None = None,
        include_references: bool = True,
        **params: Any,
    ) -> "Context":
        """
        Build a Context from an Agent Skill (SKILL.md). Convenience for SkillRunner.build_context().

        Args:
            skill_or_path: Path to a directory containing SKILL.md, or a loaded Skill instance.
            task: Optional task text (appended or fused with the skill).
            include_references: Include the skill's references/ folder in knowledge.
            **params: Skill parameters (for input_schema) and pattern inputs.

        Returns:
            Context built from the skill (with pattern fusion if the skill declares a pattern).

        Example:
            >>> from mycontext import Context
            >>> from pathlib import Path
            >>> ctx = Context.from_skill(Path("my_skill"), task="Compare A and B")
        """
        from .skills import SkillRunner
        from .skills.skill import Skill
        if isinstance(skill_or_path, (Path, str)):
            skill = Skill.load(Path(skill_or_path))
        else:
            skill = skill_or_path
        return SkillRunner().build_context(skill, task=task, include_references=include_references, **params)

    def assemble(self) -> str:
        """
        Assemble the complete context into a formatted string.

        When ``research_flow`` is False (default), uses classic ordering:
            Guidance → Constraints → Knowledge → Directive

        When ``research_flow`` is True, uses the research-backed 9-section
        ordering with emphasis formatting:
            Role → Goal → Rules → Style → Reasoning → Examples →
            Output Format → Guard Rails → Task

        Returns:
            Assembled context as a formatted string
        """
        if self.research_flow:
            return self._assemble_research_flow()

        parts = []

        if self.guidance:
            parts.append(self.guidance.render())

        if self.constraints:
            parts.append(self.constraints.render())

        if self.knowledge:
            parts.append(f"# Knowledge\n\n{self.knowledge}")

        if self.directive:
            parts.append(self.directive.render())

        return "\n\n".join(filter(None, parts))

    # ── Research-backed assembly engine ───────────────────────────

    def _assemble_research_flow(self) -> str:
        """Build prompt in the research-backed 9-section order.

        Zones (Liu et al. 2023 — primacy / recency bias):
          PRIMACY    ① Role  ② Goal         — strongest recall
          EARLY      ③ Rules  ④ Style        — instructions first (OpenAI)
          MIDDLE     ⑤ Reasoning  ⑥ Examples — demos stabilize (Li et al. 2025)
          LATE       ⑦ Output Format  ⑧ Guard Rails — near the ask (CO-STAR)
          RECENCY    ⑨ Task                  — always last (+9.7 BLEU)
        """
        sections: list[str] = []

        # ① ROLE (primacy zone)
        if self.guidance:
            sections.append(f"## ROLE\n\n**You are {self.guidance.role}.**")

        # ② GOAL
        goal = getattr(self.guidance, "goal", None) if self.guidance else None
        if goal:
            sections.append(f"## GOAL\n\n**Objective:** {goal}")

        # ③ RULES (hard → easy, Zhang et al. 2025)
        rules = getattr(self.guidance, "rules", []) if self.guidance else []
        if rules:
            items = "\n".join(f"  {i+1}. {r}" for i, r in enumerate(rules))
            sections.append(
                f"## RULES\n\n**You MUST follow these rules at all times:**\n{items}"
            )

        # ④ STYLE
        style = getattr(self.guidance, "style", None) if self.guidance else None
        if style:
            sections.append(f"## STYLE\n\n**Tone & voice:** {style}")

        # ⑤ REASONING APPROACH
        if self.thinking_strategy and self.thinking_strategy in THINKING_STRATEGIES:
            label, injection = THINKING_STRATEGIES[self.thinking_strategy]
            sections.append(
                f"## REASONING APPROACH ({label})\n\n**Important — {injection}**"
            )

        # ⑥ EXAMPLES (few-shot, middle zone)
        if self.examples:
            pairs = []
            for i, ex in enumerate(self.examples, 1):
                inp = ex.get("input", "").strip()
                out = ex.get("output", "").strip()
                if inp and out:
                    pairs.append(f"**Example {i}:**\nInput: {inp}\nOutput: {out}")
            if pairs:
                sections.append(
                    "## EXAMPLES\n\nLearn from these examples of expected "
                    "input \u2192 output:\n\n" + "\n\n".join(pairs)
                )

        # Knowledge slots into the middle zone too
        if self.knowledge:
            sections.append(f"## KNOWLEDGE\n\n{self.knowledge}")

        # ⑦ OUTPUT FORMAT
        schema = (
            getattr(self.constraints, "output_schema", None)
            if self.constraints else None
        )
        if schema:
            fields = [f for f in schema if f.get("name")]
            if fields:
                lines = [
                    "## OUTPUT FORMAT",
                    "",
                    "**Return your response as a JSON object** with these required fields:",
                    "",
                ]
                for f in fields:
                    lines.append(f"- **`{f['name']}`** ({f.get('type', 'str')})")
                lines.append("")
                skeleton = ", ".join('"' + f["name"] + '": ...' for f in fields)
                lines.append("```json\n{" + skeleton + "}\n```")
                sections.append("\n".join(lines))

        # ⑧ GUARD RAILS (hard constraints first — Zhang et al. 2025)
        if self.constraints:
            guard = self._render_guard_rails(self.constraints)
            if guard:
                sections.append(guard)

        # ⑨ TASK (recency zone — ALWAYS LAST)
        if self.directive:
            sections.append(f"---\n\n## YOUR TASK\n\n{self.directive.render()}")

        return "\n\n".join(s for s in sections if s)

    @staticmethod
    def _render_guard_rails(c: Constraints) -> str:
        parts: list[str] = ["## GUARD RAILS"]
        must_not = [i for i in (c.must_not_include or []) if i]
        must = [i for i in (c.must_include or []) if i]
        fmt = [i for i in (c.format_rules or []) if i]

        if not must_not and not must and not fmt:
            return ""

        if must_not:
            items = "\n".join(f"  - {i}" for i in must_not)
            parts.append(f"\n**NEVER include the following:**\n{items}")
        if must:
            items = "\n".join(f"  - {i}" for i in must)
            parts.append(f"\n**ALWAYS include the following:**\n{items}")
        if fmt:
            items = "\n".join(f"  - {i}" for i in fmt)
            parts.append(f"\n**Format rules:**\n{items}")

        if c.max_length:
            parts.append(f"\n**Maximum length:** {c.max_length}")
        if c.language:
            parts.append(f"\n**Language:** {c.language}")

        return "\n".join(parts)

    def execute(self, provider: str = "openai", **kwargs) -> Any:
        """
        Execute this context with an LLM provider.

        Args:
            provider: Provider name ('openai', 'anthropic', 'google', etc.)
            **kwargs: Additional parameters for the provider

        Returns:
            Provider response

        Example:
            ```python
            context = Context("You are a helpful assistant")
            result = context.execute(
                user="What is context engineering?",
                provider="gpt-4"
            )
            print(result.response)
            ```
        """
        from .providers import get_provider

        api_key = kwargs.pop("api_key", None)
        provider_instance = get_provider(provider, api_key=api_key)
        return provider_instance.generate(self, **kwargs)

    def to_prompt(
        self,
        refine: bool = False,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        **kwargs,
    ) -> str:
        """
        Convert this context into an optimized, self-contained prompt string.

        Two modes:
          - **Zero-cost** (``refine=False``): restructures the assembled
            context into a clean prompt with no API call.
          - **LLM-refined** (``refine=True``): uses a lightweight LLM call
            to distill the cognitive framework into a concise, natural prompt.

        The returned prompt is provider-agnostic — it can be sent to any LLM.

        Args:
            refine: If True, use an LLM to distill the context into a
                    polished prompt.  If False, zero-cost formatting.
            provider: LLM provider for refinement (only when refine=True).
            model: Model for refinement (default ``gpt-4o-mini``).

        Returns:
            Optimized prompt string.

        Example::

            >>> ctx = RootCauseAnalyzer().build_context(problem="server outage")
            >>> prompt = ctx.to_prompt()          # zero-cost
            >>> prompt = ctx.to_prompt(refine=True)  # LLM-refined
        """
        assembled = self.assemble()

        if not refine:
            parts = []
            if self.guidance:
                role = getattr(self.guidance, "role", "")
                rules = getattr(self.guidance, "rules", [])
                if role:
                    parts.append(f"Act as {role}.")
                if rules:
                    rules_text = " ".join(f"({i+1}) {r}" for i, r in enumerate(rules))
                    parts.append(f"Rules: {rules_text}")
            if self.directive:
                content = getattr(self.directive, "content", "")
                if content:
                    parts.append(content)
            return "\n\n".join(parts) if parts else assembled

        meta_prompt = (
            "You are a prompt engineer. Distill the analytical framework below "
            "into a single, self-contained prompt (800-1200 characters) that "
            "another LLM can execute directly to produce a high-quality answer.\n\n"
            "RULES:\n"
            "- Preserve the core reasoning methodology (e.g., root cause analysis, "
            "comparative framework, ethical lenses).\n"
            "- Include clear output structure expectations.\n"
            "- Do NOT answer the question — produce only the optimized PROMPT.\n"
            "- The prompt must be provider-agnostic (works with any LLM).\n\n"
            f"FRAMEWORK TO DISTILL:\n{assembled[:6000]}\n\n"
            "OUTPUT THE OPTIMIZED PROMPT ONLY:"
        )

        try:
            from .foundation import Directive, Guidance
            refine_ctx = self.__class__(
                guidance=Guidance(
                    role="Expert prompt engineer specializing in cognitive reasoning frameworks",
                    rules=["Output ONLY the optimized prompt, nothing else"],
                ),
                directive=Directive(content=meta_prompt),
            )
            result = refine_ctx.execute(provider=provider, model=model, **kwargs)
            refined = result.response.strip()
            if refined.startswith("```"):
                lines = refined.split("\n")
                refined = "\n".join(lines[1:-1]).strip()
            return refined
        except Exception:
            return self.to_prompt(refine=False)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert context to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return self.model_dump()

    def to_messages(self, user_message: str | None = None) -> list:
        """
        Export context as OpenAI-style message array.

        Universal format compatible with OpenAI, Anthropic, and most LLM providers.

        Args:
            user_message: Optional user message to append

        Returns:
            List of message dictionaries [{"role": "system", "content": "..."}, ...]

        Example:
            ```python
            context = Context(guidance="Expert analyst")
            messages = context.to_messages(user_message="Analyze this data")
            # Use with any provider that accepts messages format
            openai.chat.completions.create(messages=messages, model="gpt-4")
            ```
        """
        messages = []

        # System message from assembled context
        assembled = self.assemble()
        if assembled:
            messages.append({"role": "system", "content": assembled})

        # Optional user message
        if user_message:
            messages.append({"role": "user", "content": user_message})

        return messages

    def to_langchain(self):
        """
        Export context for LangChain/LangGraph integration.

        Returns:
            Dictionary with 'system_message' and 'context' keys

        Example:
            ```python
            context = Context(guidance="Expert", directive="Analyze")
            lc_format = context.to_langchain()

            # Use in LangChain
            from langchain_core.messages import SystemMessage
            system_msg = SystemMessage(content=lc_format['system_message'])
            ```
        """
        return {
            "system_message": self.assemble(),
            "context": self.to_dict(),
            "guidance": self.guidance.model_dump() if self.guidance else None,
            "directive": self.directive.model_dump() if self.directive else None,
            "knowledge": self.knowledge,
        }

    def to_markdown(self) -> str:
        """
        Export context as human-readable Markdown.

        Useful for documentation, debugging, or human review.

        Returns:
            Markdown-formatted string

        Example:
            ```python
            context = Context(guidance="Expert", directive="Analyze this")
            print(context.to_markdown())
            # Output:
            # # Context
            # ## Guidance
            # Role: Expert
            # ...
            ```
        """
        lines = ["# Context\n"]

        if self.guidance:
            lines.append("## Guidance\n")
            lines.append(f"**Role:** {self.guidance.role}\n")
            if self.guidance.goal:
                lines.append(f"**Goal:** {self.guidance.goal}\n")
            if self.guidance.rules:
                lines.append("**Rules:**\n")
                for rule in self.guidance.rules:
                    lines.append(f"- {rule}\n")
            if self.guidance.style:
                lines.append(f"**Style:** {self.guidance.style}\n")

        if self.directive:
            lines.append("\n## Directive\n")
            lines.append(f"{self.directive.content}\n")

        if self.constraints:
            lines.append("\n## Constraints\n")
            if self.constraints.must_include:
                lines.append("**Must Include:**\n")
                for item in self.constraints.must_include:
                    lines.append(f"- {item}\n")
            if self.constraints.must_not_include:
                lines.append("**Must NOT Include:**\n")
                for item in self.constraints.must_not_include:
                    lines.append(f"- {item}\n")
            if self.constraints.format_rules:
                lines.append("**Format Rules:**\n")
                for rule in self.constraints.format_rules:
                    lines.append(f"- {rule}\n")
            if self.constraints.output_schema:
                lines.append("**Output Schema:**\n")
                for f in self.constraints.output_schema:
                    if f.get("name"):
                        lines.append(f"- {f['name']} ({f.get('type', 'str')})\n")

        if self.thinking_strategy and self.thinking_strategy in THINKING_STRATEGIES:
            label, _ = THINKING_STRATEGIES[self.thinking_strategy]
            lines.append("\n## Thinking Strategy\n")
            lines.append(f"**{label}** ({self.thinking_strategy})\n")

        if self.examples:
            lines.append("\n## Examples\n")
            for i, ex in enumerate(self.examples, 1):
                lines.append(f"**Example {i}:**\n")
                lines.append(f"- Input: {ex.get('input', '')}\n")
                lines.append(f"- Output: {ex.get('output', '')}\n")

        if self.knowledge:
            lines.append("\n## Knowledge\n")
            lines.append(f"{self.knowledge}\n")

        if self.data:
            lines.append("\n## Data\n")
            for key, value in self.data.items():
                lines.append(f"**{key}:** {value}\n")

        return "".join(lines)

    def to_json(self) -> str:
        """
        Export context as JSON string.

        Useful for API transmission, storage, or language-agnostic consumption.

        Returns:
            JSON string representation

        Example:
            ```python
            context = Context(guidance="Expert")
            json_str = context.to_json()
            # Send via API, save to file, etc.
            ```
        """
        import json
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Context":
        """
        Create context from dictionary.

        Args:
            data: Dictionary representation

        Returns:
            Context instance
        """
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "Context":
        """
        Create context from JSON string.

        Args:
            json_str: JSON string representation

        Returns:
            Context instance
        """
        import json
        return cls.from_dict(json.loads(json_str))

    def to_llamaindex(self) -> dict[str, Any]:
        """
        Export context for LlamaIndex integration.

        Returns:
            Dictionary compatible with LlamaIndex query engines

        Example:
            ```python
            from llama_index import VectorStoreIndex
            context = Context(guidance="Expert", directive="Analyze")

            index = VectorStoreIndex.from_documents(docs)
            query_engine = index.as_query_engine(
                text_qa_template=context.to_llamaindex()['template']
            )
            ```
        """
        assembled = self.assemble()
        return {
            "template": assembled,
            "system_prompt": self.guidance.render() if self.guidance else "",
            "query_instruction": self.directive.render() if self.directive else "",
            "context_str": assembled,
            "metadata": self.metadata
        }

    def to_crewai(self) -> dict[str, Any]:
        """
        Export context for CrewAI integration.

        Returns:
            Dictionary compatible with CrewAI agents and tasks:
            - role, goal, backstory: for Agent
            - expected_output: for Task (derived from constraints.must_include)

        Example:
            ```python
            from crewai import Agent, Task
            context = Context(guidance="Expert Analyst", directive="Research topic")
            crew = context.to_crewai()
            agent = Agent(role=crew['role'], goal=crew['goal'], backstory=crew['backstory'])
            task = Task(description=crew['goal'], expected_output=crew['expected_output'])
            ```
        """
        # Derive expected_output for CrewAI Task from constraints
        expected_output = "A complete, actionable response addressing the task."
        if self.constraints and self.constraints.must_include:
            parts = ", ".join(self.constraints.must_include)
            expected_output = f"Output must include: {parts}"

        return {
            "role": self.guidance.role if self.guidance else "Assistant",
            "goal": self.directive.content if self.directive else "",
            "backstory": self.guidance.render() if self.guidance else "",
            "context": self.assemble(),
            "expected_output": expected_output,
            "tools": [],  # User provides tools
            "verbose": True
        }

    def to_autogen(self) -> dict[str, Any]:
        """
        Export context for AutoGen multi-agent integration.

        Returns:
            Dictionary compatible with AutoGen agents

        Example:
            ```python
            from autogen import AssistantAgent
            context = Context(guidance="Expert", directive="Solve problem")

            agent = AssistantAgent(
                name="analyst",
                system_message=context.to_autogen()['system_message']
            )
            ```
        """
        return {
            "system_message": self.assemble(),
            "description": self.directive.content if self.directive else "",
            "max_consecutive_auto_reply": 10,
            "human_input_mode": "NEVER",
            "code_execution_config": False,
        }

    def to_yaml(self) -> str:
        """
        Export context as YAML string.

        Returns:
            YAML-formatted string

        Raises:
            ImportError: If pyyaml is not installed.

        Example:
            ```python
            context = Context(guidance="Expert")
            yaml_str = context.to_yaml()
            # Save to config file or transmit
            ```
        """
        try:
            import yaml
        except ImportError as err:
            raise ImportError(
                "pyyaml is not installed. Install with: pip install pyyaml"
            ) from err
        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)

    def to_xml(self) -> str:
        """Export context as XML string including all fields."""
        from xml.dom import minidom
        from xml.etree.ElementTree import Element, SubElement, tostring

        def _safe_text(value: object) -> str:
            """Ensure text is XML-safe (no None values)."""
            return str(value) if value is not None else ""

        root = Element("context")

        if self.guidance:
            guidance_elem = SubElement(root, "guidance")
            SubElement(guidance_elem, "role").text = _safe_text(self.guidance.role)
            if self.guidance.goal:
                SubElement(guidance_elem, "goal").text = _safe_text(self.guidance.goal)
            if self.guidance.rules:
                rules_elem = SubElement(guidance_elem, "rules")
                for rule in self.guidance.rules:
                    SubElement(rules_elem, "rule").text = _safe_text(rule)
            if self.guidance.style:
                SubElement(guidance_elem, "style").text = _safe_text(self.guidance.style)

        if self.thinking_strategy:
            SubElement(root, "thinking_strategy").text = _safe_text(self.thinking_strategy)

        if self.examples:
            examples_elem = SubElement(root, "examples")
            for ex in self.examples:
                ex_elem = SubElement(examples_elem, "example")
                SubElement(ex_elem, "input").text = _safe_text(ex.get("input", ""))
                SubElement(ex_elem, "output").text = _safe_text(ex.get("output", ""))

        if self.directive:
            directive_elem = SubElement(root, "directive")
            SubElement(directive_elem, "content").text = _safe_text(self.directive.content)
            SubElement(directive_elem, "priority").text = str(self.directive.priority)

        if self.constraints:
            constraints_elem = SubElement(root, "constraints")
            if self.constraints.must_include:
                mi_elem = SubElement(constraints_elem, "must_include")
                for item in self.constraints.must_include:
                    SubElement(mi_elem, "item").text = _safe_text(item)
            if self.constraints.must_not_include:
                mni_elem = SubElement(constraints_elem, "must_not_include")
                for item in self.constraints.must_not_include:
                    SubElement(mni_elem, "item").text = _safe_text(item)
            if self.constraints.format_rules:
                fr_elem = SubElement(constraints_elem, "format_rules")
                for rule in self.constraints.format_rules:
                    SubElement(fr_elem, "rule").text = _safe_text(rule)
            if self.constraints.max_length:
                SubElement(constraints_elem, "max_length").text = str(self.constraints.max_length)
            if self.constraints.language:
                SubElement(constraints_elem, "language").text = _safe_text(self.constraints.language)

        if self.knowledge:
            SubElement(root, "knowledge").text = _safe_text(self.knowledge)

        if self.data:
            data_elem = SubElement(root, "data")
            for key, val in self.data.items():
                SubElement(data_elem, str(key)).text = _safe_text(val)

        try:
            rough_string = tostring(root, encoding="unicode")
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        except Exception:
            return tostring(root, encoding="unicode")

    def to_anthropic(self) -> dict[str, Any]:
        """
        Export context optimized for Anthropic Claude.

        Returns:
            Dictionary with Anthropic-specific format

        Example:
            ```python
            from anthropic import Anthropic
            context = Context(guidance="Expert")

            client = Anthropic()
            response = client.messages.create(
                **context.to_anthropic(),
                model="claude-3-5-sonnet-20241022"
            )
            ```
        """
        messages = []

        # Anthropic prefers structured system messages
        if self.guidance or self.directive or self.knowledge:
            system_content = self.assemble()
            return {
                "system": system_content,
                "messages": messages,
                "max_tokens": 4096
            }

        return {"messages": messages, "max_tokens": 4096}

    def to_openai(self) -> dict[str, Any]:
        """
        Export context optimized for OpenAI.

        Returns:
            Dictionary with OpenAI-specific format

        Example:
            ```python
            from openai import OpenAI
            context = Context(guidance="Expert")

            client = OpenAI()
            response = client.chat.completions.create(
                **context.to_openai(),
                model="gpt-4o-mini"
            )
            ```
        """
        return {
            "messages": self.to_messages(),
            "temperature": 0.7,
            "max_tokens": 4096
        }

    def to_google(self) -> dict[str, Any]:
        """
        Export context optimized for Google Gemini.

        Returns:
            Dictionary with Google-specific format

        Example:
            ```python
            from google import genai
            context = Context(guidance="Expert")

            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(**context.to_google())
            ```
        """
        return {
            "contents": self.assemble(),
            "generation_config": {
                "temperature": 0.7,
                "max_output_tokens": 4096
            }
        }

    def __repr__(self) -> str:
        """String representation"""
        parts = []
        if self.guidance:
            parts.append(f"guidance={self.guidance.role}")
        if self.directive:
            parts.append(f"directive={self.directive.content[:50]}...")
        return f"Context({', '.join(parts)})"
