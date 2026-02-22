"""
Validators - Validate contexts, outputs, and schemas.

Ensure data quality and catch issues before expensive LLM calls.
"""

from typing import Any

from pydantic import BaseModel, ValidationError


class ContextValidator:
    """
    Validate contexts before execution.
    
    Catch issues before making expensive LLM calls.
    """

    @staticmethod
    def validate_context(context: Any) -> dict[str, Any]:
        """
        Validate a context object.
        
        Args:
            context: Context to validate
            
        Returns:
            Validation result with issues
        """
        issues = []
        warnings = []

        # Get context text
        if hasattr(context, 'assemble'):
            text = context.assemble()
        else:
            text = str(context)

        # Check length
        if len(text) < 10:
            issues.append("Context is too short (<10 chars)")

        if len(text) > 100000:
            warnings.append("Context is very long (>100k chars) - may be expensive")

        # Check for empty directives
        if hasattr(context, 'directive') and context.directive is None:
            warnings.append("No directive provided - context may be vague")

        # Check for placeholder text
        placeholders = ['{', '{{', '[placeholder]', 'TODO', 'FIXME']
        for placeholder in placeholders:
            if placeholder in text:
                issues.append(f"Placeholder text found: '{placeholder}'")

        # Estimate tokens (rough)
        estimated_tokens = len(text) // 4
        if estimated_tokens > 8000:
            warnings.append(f"High token count (~{estimated_tokens}) - consider compression")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "estimated_tokens": estimated_tokens,
            "text_length": len(text)
        }

    @staticmethod
    def validate_inputs(inputs: dict[str, Any], required: list[str]) -> dict[str, Any]:
        """
        Validate template inputs.
        
        Args:
            inputs: Input dictionary
            required: List of required field names
            
        Returns:
            Validation result
        """
        issues = []

        for field in required:
            if field not in inputs:
                issues.append(f"Missing required field: '{field}'")
            elif inputs[field] is None or inputs[field] == "":
                issues.append(f"Field '{field}' is empty")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }


class OutputValidator:
    """
    Validate LLM outputs against expectations.
    
    Ensure outputs meet quality and format requirements.
    """

    @staticmethod
    def validate_json(text: str, schema: dict[str, type] | None = None) -> dict[str, Any]:
        """
        Validate JSON output.
        
        Args:
            text: Text to validate
            schema: Expected schema (field: type pairs)
            
        Returns:
            Validation result
        """
        issues = []

        # Try to parse JSON
        from mycontext.utils.parsers import JSONParser

        parser = JSONParser(strict=False)
        try:
            data = parser.parse(text)

            if data is None:
                issues.append("No JSON found in response")
            elif schema:
                # Validate schema
                for field, expected_type in schema.items():
                    if field not in data:
                        issues.append(f"Missing field: '{field}'")
                    elif not isinstance(data[field], expected_type):
                        issues.append(
                            f"Field '{field}' has wrong type: "
                            f"expected {expected_type.__name__}, "
                            f"got {type(data[field]).__name__}"
                        )

        except Exception as e:
            issues.append(f"JSON parsing failed: {e}")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    @staticmethod
    def validate_code(text: str, language: str) -> dict[str, Any]:
        """
        Validate code output.
        
        Args:
            text: Text to validate
            language: Expected language
            
        Returns:
            Validation result
        """
        issues = []

        from mycontext.utils.parsers import CodeBlockParser

        parser = CodeBlockParser(language=language)
        code = parser.parse(text)

        if not code:
            issues.append(f"No {language} code block found")
        elif isinstance(code, dict):
            if language not in code:
                issues.append(f"No {language} code block found")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    @staticmethod
    def validate_completeness(text: str, required_sections: list[str]) -> dict[str, Any]:
        """
        Validate that output contains required sections.
        
        Args:
            text: Text to validate
            required_sections: List of required section headers
            
        Returns:
            Validation result
        """
        issues = []

        text_lower = text.lower()
        for section in required_sections:
            if section.lower() not in text_lower:
                issues.append(f"Missing required section: '{section}'")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "missing_sections": [s for s in required_sections if s.lower() not in text_lower]
        }


class SchemaValidator:
    """Validate Pydantic schemas."""

    @staticmethod
    def validate_model(data: dict[str, Any], model: type[BaseModel]) -> dict[str, Any]:
        """
        Validate data against Pydantic model.
        
        Args:
            data: Data to validate
            model: Pydantic model class
            
        Returns:
            Validation result with details
        """
        try:
            validated = model(**data)
            return {
                "valid": True,
                "issues": [],
                "validated_data": validated.model_dump()
            }
        except ValidationError as e:
            return {
                "valid": False,
                "issues": [str(err) for err in e.errors()],
                "error_count": len(e.errors())
            }
