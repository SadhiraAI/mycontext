"""
Structured Output - Generate and validate structured outputs from LLMs.

This module provides utilities for getting structured data (JSON, Pydantic models)
from LLM responses with automatic validation and parsing.
"""

import json
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError


T = TypeVar('T', bound=BaseModel)


class StructuredOutputMixin:
    """
    Mixin for templates that support structured output.
    
    Usage:
        class MyTemplate(Pattern, StructuredOutputMixin):
            def execute_structured(self, output_model: Type[T], **kwargs) -> T:
                result = self.execute(**kwargs)
                return self.parse_structured(result.response, output_model)
    """
    
    @staticmethod
    def parse_structured(text: str, model: Type[T]) -> T:
        """
        Parse LLM output into Pydantic model.
        
        Args:
            text: LLM response text
            model: Pydantic model class
            
        Returns:
            Validated Pydantic model instance
            
        Raises:
            ValidationError: If parsing or validation fails
        """
        # Try to extract JSON from text
        json_str = extract_json(text)
        
        if not json_str:
            raise ValueError("No JSON found in response")
        
        # Parse JSON
        data = json.loads(json_str)
        
        # Validate with Pydantic
        return model(**data)
    
    @staticmethod
    def parse_json(text: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM output.
        
        Args:
            text: LLM response text
            
        Returns:
            Parsed JSON dictionary
        """
        json_str = extract_json(text)
        if not json_str:
            raise ValueError("No JSON found in response")
        return json.loads(json_str)


class JSONOutput:
    """
    Decorator/wrapper for generating JSON output.
    
    Usage:
        @JSONOutput(schema={
            "name": str,
            "age": int,
            "skills": list
        })
        def analyze_person(text):
            return template.execute(user=text)
    """
    
    def __init__(self, schema: Optional[Dict[str, Type]] = None, strict: bool = True):
        """
        Initialize JSON output wrapper.
        
        Args:
            schema: Expected JSON schema (field: type pairs)
            strict: Whether to enforce schema strictly
        """
        self.schema = schema
        self.strict = strict
    
    def __call__(self, func):
        """Wrap function to return structured JSON."""
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Extract response text
            if hasattr(result, 'response'):
                text = result.response
            else:
                text = str(result)
            
            # Parse JSON
            json_str = extract_json(text)
            if not json_str:
                raise ValueError("No JSON found in response")
            
            data = json.loads(json_str)
            
            # Validate schema if provided
            if self.schema and self.strict:
                validate_schema(data, self.schema)
            
            return data
        
        return wrapper


class PydanticOutput:
    """
    Decorator for generating Pydantic model output.
    
    Usage:
        class PersonInfo(BaseModel):
            name: str
            age: int
            skills: List[str]
        
        @PydanticOutput(PersonInfo)
        def analyze_person(text):
            return template.execute(user=text)
    """
    
    def __init__(self, model: Type[T]):
        """
        Initialize Pydantic output wrapper.
        
        Args:
            model: Pydantic model class
        """
        self.model = model
    
    def __call__(self, func):
        """Wrap function to return Pydantic model."""
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Extract response text
            if hasattr(result, 'response'):
                text = result.response
            else:
                text = str(result)
            
            # Parse and validate
            return StructuredOutputMixin.parse_structured(text, self.model)
        
        return wrapper


def output_format(format_type: str, **format_options) -> str:
    """
    Generate output format instruction for prompts.
    
    Args:
        format_type: Type of output ("json", "yaml", "xml", "markdown", "code")
        **format_options: Additional format options
        
    Returns:
        Formatted instruction string to add to prompts
        
    Example:
        >>> instruction = output_format("json", schema={"name": "str", "age": "int"})
        >>> context = Context(directive=f"Analyze this. {instruction}")
    """
    if format_type == "json":
        schema = format_options.get("schema", {})
        schema_str = json.dumps(schema, indent=2) if schema else "{}"
        return f"""
**OUTPUT FORMAT**: Respond with valid JSON only. No additional text.

**Expected JSON Schema**:
```json
{schema_str}
```

Ensure your response is parseable JSON matching this schema."""
    
    elif format_type == "yaml":
        return """
**OUTPUT FORMAT**: Respond with valid YAML only. No additional text.
Use proper YAML formatting with correct indentation."""
    
    elif format_type == "xml":
        return """
**OUTPUT FORMAT**: Respond with valid XML only. No additional text.
Use proper XML structure with opening and closing tags."""
    
    elif format_type == "markdown":
        return """
**OUTPUT FORMAT**: Respond using proper Markdown formatting.
Use headers (##), lists (-), code blocks (```), and emphasis (**bold**, *italic*)."""
    
    elif format_type == "code":
        language = format_options.get("language", "python")
        return f"""
**OUTPUT FORMAT**: Respond with executable {language} code only.
Format as a code block:
```{language}
# Your code here
```
No explanations outside the code block."""
    
    else:
        return f"**OUTPUT FORMAT**: {format_type}"


# Helper functions

def extract_json(text: str) -> Optional[str]:
    """
    Extract JSON string from text (handles code blocks, markdown).
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Extracted JSON string or None
    """
    import re
    
    # Try to find JSON in code blocks first
    json_block_pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
    matches = re.findall(json_block_pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    
    # Try to find JSON object/array
    # Look for { } or [ ]
    json_pattern = r'(\{.*\}|\[.*\])'
    matches = re.findall(json_pattern, text, re.DOTALL)
    if matches:
        # Return the longest match (most likely to be complete)
        return max(matches, key=len)
    
    return None


def validate_schema(data: Dict[str, Any], schema: Dict[str, Type]) -> None:
    """
    Validate data against simple schema.
    
    Args:
        data: Data to validate
        schema: Schema (field: type pairs)
        
    Raises:
        ValidationError: If validation fails
    """
    for field, expected_type in schema.items():
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
        
        actual_value = data[field]
        if not isinstance(actual_value, expected_type):
            raise ValidationError(
                f"Field '{field}' should be {expected_type.__name__}, "
                f"got {type(actual_value).__name__}"
            )


# Example usage and exports

class CodeReviewOutput(BaseModel):
    """Example Pydantic model for structured output."""
    issues: list
    security_score: int
    performance_score: int
    recommendations: list


def example_structured_output():
    """Example of using structured output."""
    from mycontext.templates.free import CodeReviewer
    
    reviewer = CodeReviewer()
    
    # Add JSON output format to the template
    code = "def foo(): pass"
    
    # Method 1: Parse manually
    result = reviewer.execute(
        provider="gemini",
        code=code,
        language="Python"
    )
    
    try:
        json_data = extract_json(result.response)
        if json_data:
            parsed = json.loads(json_data)
            print("Parsed JSON:", parsed)
    except Exception as e:
        print(f"Parsing failed: {e}")
    
    # Method 2: Use Pydantic (if template supports it)
    # structured_result = reviewer.execute_structured(
    #     output_model=CodeReviewOutput,
    #     code=code,
    #     language="Python"
    # )


if __name__ == "__main__":
    # Test extraction
    test_text = """
    Here's the analysis:
    ```json
    {
        "name": "Test",
        "score": 95
    }
    ```
    """
    
    result = extract_json(test_text)
    print("Extracted JSON:", result)
