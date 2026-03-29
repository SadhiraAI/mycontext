"""
Tests for the core Context class
"""
from mycontext import Context
from mycontext.foundation import Constraints, Directive, Guidance


class TestContextCreation:
    """Test Context creation and initialization"""

    def test_empty_context(self):
        """Test creating an empty context"""
        context = Context()
        assert context.guidance is None
        assert context.directive is None
        assert context.constraints is None
        assert context.knowledge is None
        assert context.data == {}

    def test_simple_string_guidance(self):
        """Test creating context with simple string guidance"""
        context = Context("You are a helpful assistant")
        assert context.guidance is not None
        assert context.guidance.role == "You are a helpful assistant"

    def test_with_guidance_object(self):
        """Test creating context with Guidance object"""
        guidance = Guidance(
            role="Expert Analyst",
            rules=["Be thorough", "Use examples"],
            style="professional"
        )
        context = Context(guidance=guidance)
        assert context.guidance.role == "Expert Analyst"
        assert len(context.guidance.rules) == 2
        assert context.guidance.style == "professional"

    def test_with_directive_string(self):
        """Test creating context with simple string directive"""
        context = Context(directive="Analyze the data")
        assert context.directive is not None
        assert context.directive.content == "Analyze the data"

    def test_with_directive_object(self):
        """Test creating context with Directive object"""
        directive = Directive(content="Review this code", priority=9)
        context = Context(directive=directive)
        assert context.directive.content == "Review this code"
        assert context.directive.priority == 9

    def test_with_knowledge(self):
        """Test creating context with knowledge field"""
        context = Context(
            guidance="Expert",
            knowledge="Retrieved information from documents"
        )
        assert context.knowledge == "Retrieved information from documents"

    def test_full_context(self):
        """Test creating context with all fields"""
        context = Context(
            guidance=Guidance(role="Expert"),
            directive=Directive(content="Analyze"),
            constraints=Constraints(
                must_include=["key points"],
                must_not_include=["speculation"]
            ),
            knowledge="Background information",
            data={"source": "test"}
        )
        assert context.guidance.role == "Expert"
        assert context.directive.content == "Analyze"
        assert len(context.constraints.must_include) == 1
        assert context.knowledge == "Background information"
        assert context.data["source"] == "test"


class TestContextAssembly:
    """Test Context.assemble() method"""

    def test_empty_context_assembly(self):
        """Test assembling empty context"""
        context = Context()
        assembled = context.assemble()
        assert assembled == ""

    def test_guidance_only(self):
        """Test assembling context with only guidance"""
        context = Context(guidance="Expert Analyst")
        assembled = context.assemble()
        assert "Expert Analyst" in assembled

    def test_directive_only(self):
        """Test assembling context with only directive"""
        context = Context(directive="Analyze the data")
        assembled = context.assemble()
        assert "Analyze the data" in assembled

    def test_knowledge_in_assembly(self):
        """Test that knowledge is included in assembly"""
        context = Context(
            guidance="Expert",
            knowledge="Here is some knowledge",
            directive="Analyze"
        )
        assembled = context.assemble()
        assert "Here is some knowledge" in assembled
        assert "# Knowledge" in assembled

    def test_full_assembly_order(self):
        """Test that components are assembled in correct order"""
        context = Context(
            guidance=Guidance(role="Expert"),
            constraints=Constraints(must_include=["data"]),
            knowledge="Background info",
            directive=Directive(content="Analyze")
        )
        assembled = context.assemble()

        # Check all parts are present
        assert "Expert" in assembled
        assert "Background info" in assembled
        assert "Analyze" in assembled

        # Check order: guidance, constraints, knowledge, directive
        guidance_pos = assembled.find("Expert")
        knowledge_pos = assembled.find("Background info")
        directive_pos = assembled.find("Analyze")

        assert guidance_pos < knowledge_pos < directive_pos


class TestContextExport:
    """Test Context export methods"""

    def test_to_dict(self):
        """Test converting context to dictionary"""
        context = Context(
            guidance="Expert",
            knowledge="Some knowledge"
        )
        data = context.to_dict()
        assert isinstance(data, dict)
        assert "guidance" in data
        assert "knowledge" in data
        assert data["knowledge"] == "Some knowledge"

    def test_to_json(self):
        """Test converting context to JSON"""
        context = Context(guidance="Expert", knowledge="Info")
        json_str = context.to_json()
        assert isinstance(json_str, str)
        assert "Expert" in json_str
        assert "Info" in json_str

    def test_from_json(self):
        """Test creating context from JSON"""
        context = Context(guidance="Expert", knowledge="Info")
        json_str = context.to_json()

        # Create new context from JSON
        restored = Context.from_json(json_str)
        assert restored.guidance.role == "Expert"
        assert restored.knowledge == "Info"

    def test_to_messages_without_user(self):
        """Test exporting to OpenAI messages format without user message"""
        context = Context(
            guidance="Expert",
            directive="Analyze"
        )
        messages = context.to_messages()

        assert len(messages) == 1
        assert messages[0]["role"] == "system"
        assert "Expert" in messages[0]["content"]
        assert "Analyze" in messages[0]["content"]

    def test_to_messages_with_user(self):
        """Test exporting to OpenAI messages format with user message"""
        context = Context(guidance="Expert")
        messages = context.to_messages(user_message="What is AI?")

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What is AI?"

    def test_to_messages_includes_knowledge(self):
        """Test that to_messages includes knowledge in system message"""
        context = Context(
            guidance="Expert",
            knowledge="Retrieved knowledge from documents"
        )
        messages = context.to_messages()

        assert len(messages) == 1
        assert "Retrieved knowledge" in messages[0]["content"]

    def test_to_langchain(self):
        """Test exporting to LangChain format"""
        context = Context(
            guidance="Expert",
            knowledge="Background info",
            directive="Analyze"
        )
        lc_format = context.to_langchain()

        assert isinstance(lc_format, dict)
        assert "system_message" in lc_format
        assert "context" in lc_format
        assert "knowledge" in lc_format
        assert lc_format["knowledge"] == "Background info"

    def test_to_markdown(self):
        """Test exporting to markdown format"""
        context = Context(
            guidance=Guidance(
                role="Expert Analyst",
                rules=["Be thorough"],
                style="professional"
            ),
            directive=Directive(content="Analyze data"),
            constraints=Constraints(
                must_include=["metrics"],
                must_not_include=["speculation"]
            ),
            knowledge="Background information"
        )
        markdown = context.to_markdown()

        assert "# Context" in markdown
        assert "## Guidance" in markdown
        assert "Expert Analyst" in markdown
        assert "## Directive" in markdown
        assert "Analyze data" in markdown
        assert "## Constraints" in markdown
        assert "## Knowledge" in markdown
        assert "Background information" in markdown


class TestResearchFlow:
    """Test the research-backed 9-section assembly"""

    def test_research_flow_flag_default_false(self):
        ctx = Context(guidance="Expert")
        assert ctx.research_flow is False

    def test_classic_assembly_unchanged(self):
        """Existing behavior must not change when research_flow=False"""
        ctx = Context(
            guidance=Guidance(role="Expert"),
            constraints=Constraints(must_include=["data"]),
            directive=Directive(content="Analyze")
        )
        assembled = ctx.assemble()
        assert "You are Expert" in assembled
        assert "CONSTRAINTS:" in assembled
        assert "Analyze" in assembled
        # Should NOT have research-flow headers
        assert "## ROLE" not in assembled
        assert "## YOUR TASK" not in assembled

    def test_research_flow_has_nine_sections(self):
        ctx = Context(
            guidance=Guidance(
                role="Expert Analyst",
                goal="Find insights",
                rules=["Be thorough", "Use data"],
                style="Professional",
            ),
            directive=Directive(content="Analyze the data"),
            constraints=Constraints(
                must_include=["metrics"],
                must_not_include=["opinions"],
                format_rules=["Use JSON"],
                output_schema=[{"name": "result", "type": "str"}],
            ),
            thinking_strategy="step_by_step",
            examples=[
                {"input": "Sales up 20%", "output": "Positive trend"},
            ],
            research_flow=True,
        )
        assembled = ctx.assemble()

        assert "## ROLE" in assembled
        assert "## GOAL" in assembled
        assert "## RULES" in assembled
        assert "## STYLE" in assembled
        assert "## REASONING APPROACH" in assembled
        assert "## EXAMPLES" in assembled
        assert "## OUTPUT FORMAT" in assembled
        assert "## GUARD RAILS" in assembled
        assert "## YOUR TASK" in assembled

    def test_research_flow_ordering(self):
        """ROLE first, TASK last; reasoning immediately before TASK (recency zone)."""
        ctx = Context(
            guidance=Guidance(role="Expert", goal="Win", rules=["Rule1"]),
            directive=Directive(content="Do it"),
            constraints=Constraints(must_include=["x"], must_not_include=["y"]),
            thinking_strategy="verify",
            examples=[{"input": "a", "output": "b"}],
            research_flow=True,
        )
        assembled = ctx.assemble()

        role_pos = assembled.find("## ROLE")
        goal_pos = assembled.find("## GOAL")
        rules_pos = assembled.find("## RULES")
        examples_pos = assembled.find("## EXAMPLES")
        guard_pos = assembled.find("## GUARD RAILS")
        reasoning_pos = assembled.find("## REASONING")
        task_pos = assembled.find("## YOUR TASK")

        assert role_pos < goal_pos < rules_pos
        # Examples now at ⑤ (before output format / guard rails)
        assert rules_pos < examples_pos < guard_pos
        # Reasoning now at ⑧.5 — after guard rails, before task
        assert guard_pos < reasoning_pos < task_pos

    def test_research_flow_emphasis(self):
        """Research flow should use bold/caps emphasis markers"""
        ctx = Context(
            guidance=Guidance(role="Expert", rules=["Be careful"]),
            directive=Directive(content="Analyze"),
            constraints=Constraints(must_not_include=["speculation"]),
            research_flow=True,
        )
        assembled = ctx.assemble()

        assert "You are Expert." in assembled
        assert "**You MUST follow" in assembled
        assert "Must NOT include" in assembled

    def test_research_flow_thinking_strategy(self):
        for strategy in ["step_by_step", "multiple_angles", "verify", "explain_simply", "creative"]:
            ctx = Context(
                guidance=Guidance(role="Expert"),
                thinking_strategy=strategy,
                research_flow=True,
            )
            assembled = ctx.assemble()
            assert "## REASONING APPROACH" in assembled

    def test_research_flow_examples(self):
        ctx = Context(
            guidance=Guidance(role="Expert"),
            examples=[
                {"input": "Hello", "output": "Greeting"},
                {"input": "Bye", "output": "Farewell"},
            ],
            research_flow=True,
        )
        assembled = ctx.assemble()
        assert "**Example 1:**" in assembled
        assert "**Example 2:**" in assembled
        assert "Hello" in assembled
        assert "Farewell" in assembled

    def test_research_flow_output_schema(self):
        ctx = Context(
            guidance=Guidance(role="Expert"),
            constraints=Constraints(
                output_schema=[
                    {"name": "sentiment", "type": "str"},
                    {"name": "confidence", "type": "float"},
                ]
            ),
            research_flow=True,
        )
        assembled = ctx.assemble()
        assert "## OUTPUT FORMAT" in assembled
        assert "`sentiment`" in assembled
        assert "`confidence`" in assembled
        assert "```json" in assembled

    def test_research_flow_minimal(self):
        """Even with minimal input, research flow should work"""
        ctx = Context(
            guidance=Guidance(role="Helper"),
            directive=Directive(content="Help me"),
            research_flow=True,
        )
        assembled = ctx.assemble()
        assert "## ROLE" in assembled
        assert "## YOUR TASK" in assembled
        assert "Help me" in assembled

    def test_research_flow_with_knowledge(self):
        ctx = Context(
            guidance=Guidance(role="Expert"),
            knowledge="Some retrieved documents",
            directive=Directive(content="Summarize"),
            research_flow=True,
        )
        assembled = ctx.assemble()
        assert "## KNOWLEDGE" in assembled
        assert "Some retrieved documents" in assembled
        task_pos = assembled.find("## YOUR TASK")
        knowledge_pos = assembled.find("## KNOWLEDGE")
        assert knowledge_pos < task_pos

    def test_research_flow_skips_empty_sections(self):
        ctx = Context(
            guidance=Guidance(role="Expert"),
            directive=Directive(content="Go"),
            research_flow=True,
        )
        assembled = ctx.assemble()
        assert "## GOAL" not in assembled
        assert "## RULES" not in assembled
        assert "## STYLE" not in assembled
        assert "## REASONING" not in assembled
        assert "## EXAMPLES" not in assembled
        assert "## OUTPUT FORMAT" not in assembled
        assert "## GUARD RAILS" not in assembled

    def test_all_exports_use_research_flow(self):
        """All export formats should benefit from research_flow"""
        ctx = Context(
            guidance=Guidance(role="Expert", goal="Win"),
            directive=Directive(content="Do it"),
            research_flow=True,
        )
        messages = ctx.to_messages()
        assert "## ROLE" in messages[0]["content"]

        openai = ctx.to_openai()
        assert "## ROLE" in openai["messages"][0]["content"]

        anthropic = ctx.to_anthropic()
        assert "## ROLE" in anthropic["system"]

        langchain = ctx.to_langchain()
        assert "## ROLE" in langchain["system_message"]

    def test_new_fields_in_to_markdown(self):
        ctx = Context(
            guidance=Guidance(role="Expert", goal="Find bugs"),
            constraints=Constraints(
                output_schema=[{"name": "bug", "type": "str"}]
            ),
            thinking_strategy="step_by_step",
            examples=[{"input": "code", "output": "bug report"}],
        )
        md = ctx.to_markdown()
        assert "**Goal:** Find bugs" in md
        assert "Chain of Thought" in md
        assert "Example 1" in md
        assert "bug (str)" in md

    def test_new_fields_in_to_xml(self):
        ctx = Context(
            guidance=Guidance(role="Expert", goal="Win"),
            thinking_strategy="verify",
            examples=[{"input": "x", "output": "y"}],
        )
        xml = ctx.to_xml()
        assert "<goal>Win</goal>" in xml
        assert "<thinking_strategy>verify</thinking_strategy>" in xml
        assert "<input>x</input>" in xml
        assert "<output>y</output>" in xml


class TestContextRepresentation:
    """Test Context string representation"""

    def test_repr_with_guidance(self):
        """Test __repr__ with guidance"""
        context = Context(guidance="Expert")
        repr_str = repr(context)
        assert "Context" in repr_str
        assert "guidance=Expert" in repr_str

    def test_repr_with_directive(self):
        """Test __repr__ with directive"""
        context = Context(directive="Analyze the data carefully")
        repr_str = repr(context)
        assert "Context" in repr_str
        assert "directive=Analyze the data" in repr_str
