"""
Core Context class - The heart of mycontext

This is where Context as Code™ comes to life.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field

from .foundation import Directive, Guidance, Constraints


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
        
        # Advanced usage
        context = Context(
            guidance=Guidance(role="Expert code reviewer", rules=["Be thorough"]),
            directive=Directive("Review this code for security issues")
        )
        ```
    """
    
    guidance: Optional[Guidance] = Field(
        default=None,
        description="System-level behavioral guidance"
    )
    
    directive: Optional[Directive] = Field(
        default=None,
        description="Specific instruction for this interaction"
    )
    
    constraints: Optional[Constraints] = Field(
        default=None,
        description="Hard constraints and guardrails"
    )
    
    knowledge: Optional[str] = Field(
        default=None,
        description="Retrieved knowledge, documents, or memory context"
    )
    
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data and parameters"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about this context (tags, version, etc.)"
    )
    
    def __init__(
        self,
        guidance: Union[str, Guidance, None] = None,
        directive: Union[str, Directive, None] = None,
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
        skill_or_path: Union[Path, str, Any],
        task: Optional[str] = None,
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
        
        This is where the magic happens - combining all components
        into a coherent context that can be sent to an LLM.
        
        Returns:
            Assembled context as a formatted string
        """
        parts = []
        
        # Add guidance (system-level)
        if self.guidance:
            parts.append(self.guidance.render())
        
        # Add constraints (boundaries)
        if self.constraints:
            parts.append(self.constraints.render())
        
        # Add knowledge (retrieved information)
        if self.knowledge:
            parts.append(f"# Knowledge\n\n{self.knowledge}")
        
        # Add directive (specific instruction)
        if self.directive:
            parts.append(self.directive.render())
        
        # Join with double newlines for clarity
        return "\n\n".join(filter(None, parts))
    
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert context to dictionary for serialization.
        
        Returns:
            Dictionary representation
        """
        return self.model_dump()
    
    def to_messages(self, user_message: Optional[str] = None) -> list:
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
    def from_dict(cls, data: Dict[str, Any]) -> "Context":
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
    
    def to_llamaindex(self) -> Dict[str, Any]:
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
    
    def to_crewai(self) -> Dict[str, Any]:
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
    
    def to_autogen(self) -> Dict[str, Any]:
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
        except ImportError:
            raise ImportError(
                "pyyaml is not installed. Install with: pip install pyyaml"
            )
        return yaml.dump(self.to_dict(), default_flow_style=False, sort_keys=False)
    
    def to_xml(self) -> str:
        """Export context as XML string including all fields."""
        from xml.etree.ElementTree import Element, SubElement, tostring
        from xml.dom import minidom

        def _safe_text(value: object) -> str:
            """Ensure text is XML-safe (no None values)."""
            return str(value) if value is not None else ""

        root = Element("context")

        if self.guidance:
            guidance_elem = SubElement(root, "guidance")
            SubElement(guidance_elem, "role").text = _safe_text(self.guidance.role)
            if self.guidance.rules:
                rules_elem = SubElement(guidance_elem, "rules")
                for rule in self.guidance.rules:
                    SubElement(rules_elem, "rule").text = _safe_text(rule)
            if self.guidance.style:
                SubElement(guidance_elem, "style").text = _safe_text(self.guidance.style)

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

    def to_anthropic(self) -> Dict[str, Any]:
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
    
    def to_openai(self) -> Dict[str, Any]:
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
    
    def to_google(self) -> Dict[str, Any]:
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
