"""
Tests for the core Context class
"""
from src.mycontext import Context
from src.mycontext.foundation import Constraints, Directive, Guidance


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
