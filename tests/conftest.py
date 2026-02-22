"""
Test configuration and fixtures
"""
import os

import pytest


@pytest.fixture
def sample_question():
    """Sample question for testing transformations"""
    return "Should I invest in solar panels for my home?"


@pytest.fixture
def sample_context():
    """Sample context string"""
    return """
    Home Details:
    - Location: California
    - Size: 2000 sq ft
    - Current electric bill: $200/month
    - Budget: $30,000 available
    """


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a test response."
                }
            }
        ],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150
        }
    }


@pytest.fixture
def setup_env():
    """Setup environment variables for testing"""
    # Save original values
    original_openai = os.environ.get("OPENAI_API_KEY")
    original_anthropic = os.environ.get("ANTHROPIC_API_KEY")

    # Set test values
    os.environ["OPENAI_API_KEY"] = "test-key-123"
    os.environ["ANTHROPIC_API_KEY"] = "test-key-456"

    yield

    # Restore original values
    if original_openai:
        os.environ["OPENAI_API_KEY"] = original_openai
    else:
        os.environ.pop("OPENAI_API_KEY", None)

    if original_anthropic:
        os.environ["ANTHROPIC_API_KEY"] = original_anthropic
    else:
        os.environ.pop("ANTHROPIC_API_KEY", None)
