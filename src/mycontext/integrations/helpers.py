"""
Integration Helpers - Seamless integration with popular AI frameworks

Makes mycontext work effortlessly with LangChain, LlamaIndex, CrewAI, AutoGen, and more.
"""

from typing import Any

from ..core import Context


class LangChainHelper:
    """
    Helper for LangChain integration.
    
    Makes it easy to use mycontext contexts with LangChain.
    
    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import LangChainHelper
        >>> 
        >>> context = Context(guidance="Expert analyst")
        >>> helper = LangChainHelper()
        >>> 
        >>> # Get LangChain messages
        >>> messages = helper.to_messages(context)
        >>> 
        >>> # Use with LangChain
        >>> from langchain_openai import ChatOpenAI
        >>> chat = ChatOpenAI()
        >>> response = chat(messages)
    """

    @staticmethod
    def to_messages(context: Context, user_message: str | None = None):
        """Convert context to LangChain messages."""
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
        except ImportError:
            raise ImportError(
                "langchain-core is not installed. Install with: pip install langchain-core"
            )

        messages = []

        system_content = context.assemble()
        if system_content:
            messages.append(SystemMessage(content=system_content))

        if user_message:
            messages.append(HumanMessage(content=user_message))

        return messages

    @staticmethod
    def to_prompt_template(context: Context):
        """Convert context to LangChain PromptTemplate."""
        try:
            from langchain_core.prompts import PromptTemplate

            template = context.assemble()
            if context.data:
                # Extract variables from data
                variables = list(context.data.keys())
                return PromptTemplate(template=template, input_variables=variables)

            return PromptTemplate(template=template, input_variables=[])
        except ImportError:
            raise ImportError(
                "langchain-core is not installed. Install with: pip install langchain-core"
            )

    @staticmethod
    def to_chat_prompt(context: Context):
        """Convert context to LangChain ChatPromptTemplate."""
        try:
            from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

            system_template = context.assemble()
            system_message = SystemMessagePromptTemplate.from_template(system_template)

            return ChatPromptTemplate.from_messages([system_message])
        except ImportError:
            raise ImportError(
                "langchain-core is not installed. Install with: pip install langchain-core"
            )


class LlamaIndexHelper:
    """
    Helper for LlamaIndex integration.
    
    Makes it easy to use mycontext contexts with LlamaIndex.
    
    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import LlamaIndexHelper
        >>> 
        >>> context = Context(guidance="Expert", directive="Analyze docs")
        >>> helper = LlamaIndexHelper()
        >>> 
        >>> # Create query engine with context
        >>> from llama_index import VectorStoreIndex
        >>> index = VectorStoreIndex.from_documents(docs)
        >>> query_engine = helper.create_query_engine(index, context)
    """

    @staticmethod
    def to_prompt(context: Context) -> str:
        """Convert context to LlamaIndex prompt."""
        return context.assemble()

    @staticmethod
    def create_query_engine(index: Any, context: Context, **kwargs):
        """Create a LlamaIndex query engine with mycontext context."""
        try:
            prompt_template = context.assemble()

            return index.as_query_engine(
                text_qa_template=prompt_template,
                **kwargs
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to create query engine. Make sure LlamaIndex is installed: {e}"
            )

    @staticmethod
    def create_chat_engine(index: Any, context: Context, **kwargs):
        """Create a LlamaIndex chat engine with mycontext context."""
        try:
            system_prompt = context.assemble()

            return index.as_chat_engine(
                system_prompt=system_prompt,
                **kwargs
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to create chat engine. Make sure LlamaIndex is installed: {e}"
            )


class CrewAIHelper:
    """
    Helper for CrewAI integration.
    
    Makes it easy to use mycontext contexts with CrewAI agents.
    
    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import CrewAIHelper
        >>> 
        >>> context = Context(guidance="Expert researcher")
        >>> helper = CrewAIHelper()
        >>> 
        >>> # Create CrewAI agent
        >>> agent = helper.create_agent(
        ...     context,
        ...     name="researcher",
        ...     tools=my_tools
        ... )
    """

    @staticmethod
    def create_agent(
        context: Context,
        name: str = "agent",
        tools: list | None = None,
        **kwargs
    ):
        """Create a CrewAI agent with mycontext context."""
        try:
            from crewai import Agent

            crew_config = context.to_crewai()

            return Agent(
                role=crew_config['role'],
                goal=crew_config['goal'],
                backstory=crew_config['backstory'],
                tools=tools or [],
                verbose=crew_config.get('verbose', True),
                **kwargs
            )
        except ImportError:
            raise ImportError(
                "CrewAI is not installed. Install with: pip install crewai"
            )

    @staticmethod
    def create_task(
        context: Context,
        description: str | None = None,
        agent: Any | None = None,
        expected_output: str | None = None,
        **kwargs
    ):
        """Create a CrewAI task with mycontext context."""
        try:
            from crewai import Task

            task_description = description or (
                context.directive.content if context.directive else "Complete the task"
            )
            # CrewAI Task requires expected_output (required since crewai 1.x)
            # Derive from context.to_crewai() so we generate per CrewAI framework
            output = expected_output or kwargs.pop("expected_output", None)
            if output is None:
                crew_config = context.to_crewai()
                output = crew_config.get("expected_output", "A complete, actionable response addressing the task.")

            return Task(
                description=task_description,
                expected_output=output,
                agent=agent,
                **kwargs
            )
        except ImportError:
            raise ImportError(
                "CrewAI is not installed. Install with: pip install crewai"
            )


class AutoGenHelper:
    """
    Helper for Microsoft AutoGen integration.
    
    Makes it easy to use mycontext contexts with AutoGen agents.
    
    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import AutoGenHelper
        >>> 
        >>> context = Context(guidance="Expert coder")
        >>> helper = AutoGenHelper()
        >>> 
        >>> # Create AutoGen agent
        >>> agent = helper.create_assistant(
        ...     context,
        ...     name="coding_expert"
        ... )
    """

    @staticmethod
    def create_assistant(
        context: Context,
        name: str = "assistant",
        llm_config: dict | None = None,
        **kwargs
    ):
        """Create an AutoGen assistant agent with mycontext context."""
        try:
            from autogen import AssistantAgent

            autogen_config = context.to_autogen()

            return AssistantAgent(
                name=name,
                system_message=autogen_config['system_message'],
                llm_config=llm_config or {},
                **kwargs
            )
        except ImportError:
            raise ImportError(
                "AutoGen is not installed. Install with: pip install pyautogen"
            )

    @staticmethod
    def create_user_proxy(
        name: str = "user",
        **kwargs
    ):
        """Create an AutoGen user proxy agent."""
        try:
            from autogen import UserProxyAgent

            return UserProxyAgent(
                name=name,
                human_input_mode="TERMINATE",
                **kwargs
            )
        except ImportError:
            raise ImportError(
                "AutoGen is not installed. Install with: pip install pyautogen"
            )


class DSPyHelper:
    """
    Helper for DSPy integration.
    
    Makes it easy to use mycontext contexts with DSPy.
    
    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import DSPyHelper
        >>> 
        >>> context = Context(guidance="Expert")
        >>> helper = DSPyHelper()
        >>> 
        >>> # Get DSPy-compatible format
        >>> prompt = helper.to_prompt(context)
    """

    @staticmethod
    def to_prompt(context: Context) -> str:
        """Convert context to DSPy prompt."""
        return context.assemble()

    @staticmethod
    def to_signature(context: Context) -> dict[str, Any]:
        """Convert context to DSPy signature format."""
        return {
            "instructions": context.assemble(),
            "context": context.to_dict()
        }


class SemanticKernelHelper:
    """
    Helper for Microsoft Semantic Kernel integration.
    
    Makes it easy to use mycontext contexts with Semantic Kernel.
    
    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import SemanticKernelHelper
        >>> 
        >>> context = Context(guidance="Expert")
        >>> helper = SemanticKernelHelper()
        >>> 
        >>> # Create semantic function
        >>> func = helper.create_semantic_function(kernel, context)
    """

    @staticmethod
    def to_prompt_template(context: Context) -> str:
        """Convert context to Semantic Kernel prompt template."""
        return context.assemble()

    @staticmethod
    def create_semantic_function(
        kernel,
        context,
        function_name: str = "mycontext_function",
        plugin_name: str = "mycontext",
        **kwargs
    ):
        """Create a Semantic Kernel function with mycontext context.

        Compatible with Semantic Kernel 1.x (kernel.add_function).
        """
        try:
            from semantic_kernel.functions import KernelFunctionFromPrompt

            prompt_template = context.assemble()
            fn = KernelFunctionFromPrompt(
                function_name=function_name,
                plugin_name=plugin_name,
                prompt=prompt_template,
                **kwargs
            )
            kernel.add_function(plugin_name=plugin_name, function=fn)
            return fn
        except ImportError:
            raise ImportError(
                "Semantic Kernel is not installed. Install with: pip install semantic-kernel"
            )


class GoogleADKHelper:
    """
    Helper for Google Agent Development Kit (ADK) integration.

    Uses mycontext context as the agent's instruction.

    Example:
        >>> from mycontext import Context
        >>> from mycontext.integrations import GoogleADKHelper
        >>> context = Context(guidance="Expert explainer", directive="Explain X")
        >>> agent = GoogleADKHelper.create_agent(context, name="explainer")
    """

    @staticmethod
    def to_instruction(context: Context) -> str:
        """Convert context to ADK agent instruction string."""
        return context.assemble()

    @staticmethod
    def create_agent(
        context: Context,
        name: str = "agent",
        model: str = "gemini-2.0-flash",
        description: str | None = None,
        tools: list | None = None,
        **kwargs
    ):
        """Create a Google ADK Agent with mycontext context as instruction."""
        try:
            from google.adk.agents import Agent

            instruction = context.assemble()
            desc = description or (
                context.directive.content[:200] if context.directive else "mycontext-powered agent"
            )
            return Agent(
                model=model,
                name=name,
                instruction=instruction,
                description=desc,
                tools=tools or [],
                **kwargs
            )
        except ImportError:
            raise ImportError(
                "Google ADK is not installed. Install with: pip install google-adk"
            )


# Convenience function to auto-detect and integrate
def auto_integrate(context: Context, framework: str, **kwargs) -> Any:
    """
    Automatically integrate context with specified framework.
    
    Args:
        context: mycontext Context object
        framework: Framework name ("langchain", "llamaindex", "crewai", "autogen", "dspy", "semantic_kernel")
        **kwargs: Framework-specific parameters
    
    Returns:
        Framework-specific object
    
    Example:
        >>> context = Context(guidance="Expert")
        >>> 
        >>> # Auto-integrate with LangChain
        >>> messages = auto_integrate(context, "langchain")
        >>> 
        >>> # Auto-integrate with CrewAI
        >>> agent = auto_integrate(context, "crewai", name="analyst", tools=tools)
    """
    framework = framework.lower()

    if framework == "langchain":
        return LangChainHelper.to_messages(context, **kwargs)
    elif framework == "llamaindex":
        return LlamaIndexHelper.to_prompt(context)
    elif framework == "crewai":
        return CrewAIHelper.create_agent(context, **kwargs)
    elif framework == "autogen":
        return AutoGenHelper.create_assistant(context, **kwargs)
    elif framework == "dspy":
        return DSPyHelper.to_prompt(context)
    elif framework == "semantic_kernel" or framework == "semantickernel":
        return SemanticKernelHelper.to_prompt_template(context)
    elif framework == "google_adk" or framework == "adk":
        return GoogleADKHelper.create_agent(context, **kwargs)
    else:
        raise ValueError(
            f"Unknown framework: {framework}. "
            f"Supported: langchain, llamaindex, crewai, autogen, dspy, semantic_kernel, google_adk"
        )
