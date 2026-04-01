"""
Output Parsers - Extract structured data from LLM responses.

Parse JSON, XML, code blocks, lists, and other formats from LLM outputs.
"""

import json
import re
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Any


class OutputParser(ABC):
    """Base class for output parsers."""

    @abstractmethod
    def parse(self, text: str) -> Any:
        """Parse text and return structured data."""
        pass

    @abstractmethod
    def get_format_instruction(self) -> str:
        """Get instruction to add to prompt for this format."""
        pass


class JSONParser(OutputParser):
    """Parse JSON from LLM output."""

    def __init__(self, strict: bool = True):
        """
        Initialize JSON parser.

        Args:
            strict: If True, raise error on parse failure
        """
        self.strict = strict

    def parse(self, text: str) -> dict | list | None:
        """
        Extract and parse JSON from text.

        Args:
            text: Text containing JSON

        Returns:
            Parsed JSON (dict or list) or None if not found
        """
        # Try code blocks first
        pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0].strip())
            except json.JSONDecodeError as e:
                if self.strict:
                    raise ValueError(f"Invalid JSON in code block: {e}")

        # Try finding raw JSON
        json_pattern = r"(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\])"
        matches = re.findall(json_pattern, text, re.DOTALL)

        for match in sorted(matches, key=len, reverse=True):
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

        if self.strict:
            raise ValueError("No valid JSON found in response")
        return None

    def get_format_instruction(self) -> str:
        """Get JSON format instruction."""
        return """
**OUTPUT FORMAT**: Respond with valid JSON only.

Example:
```json
{
    "field1": "value1",
    "field2": 123,
    "field3": ["item1", "item2"]
}
```

Ensure your response is parseable JSON."""


class ListParser(OutputParser):
    """Parse lists from LLM output."""

    def __init__(self, numbered: bool = True, bullet: bool = True):
        """
        Initialize list parser.

        Args:
            numbered: Parse numbered lists (1. 2. 3.)
            bullet: Parse bullet lists (- * •)
        """
        self.numbered = numbered
        self.bullet = bullet

    def parse(self, text: str) -> list[str]:
        """
        Extract list items from text.

        Args:
            text: Text containing lists

        Returns:
            List of extracted items
        """
        items = []

        if self.numbered:
            # Match: 1. Item, 2. Item, etc.
            pattern = r"^\s*\d+[\.)]\s+(.+)$"
            items.extend(re.findall(pattern, text, re.MULTILINE))

        if self.bullet:
            # Match: - Item, * Item, • Item
            pattern = r"^\s*[-*•]\s+(.+)$"
            items.extend(re.findall(pattern, text, re.MULTILINE))

        return [item.strip() for item in items if item.strip()]

    def get_format_instruction(self) -> str:
        """Get list format instruction."""
        if self.numbered:
            return """
**OUTPUT FORMAT**: Respond with a numbered list.

Example:
1. First item
2. Second item
3. Third item"""
        else:
            return """
**OUTPUT FORMAT**: Respond with a bullet list.

Example:
- First item
- Second item
- Third item"""


class CodeBlockParser(OutputParser):
    """Parse code blocks from markdown."""

    def __init__(self, language: str | None = None):
        """
        Initialize code block parser.

        Args:
            language: Specific language to extract (None = all)
        """
        self.language = language

    def parse(self, text: str) -> str | dict[str, str]:
        """
        Extract code blocks from markdown.

        Args:
            text: Text containing code blocks

        Returns:
            If language specified: single code string
            If language not specified: dict of {language: code}
        """
        if self.language:
            pattern = f"```{self.language}\\s*\\n(.*?)\\n```"
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            return matches[0] if matches else ""
        else:
            # Extract all code blocks with languages
            pattern = r"```(\w+)?\s*\n(.*?)\n```"
            matches = re.findall(pattern, text, re.DOTALL)

            result = {}
            for i, (lang, code) in enumerate(matches):
                key = lang if lang else f"block_{i}"
                result[key] = code.strip()

            return result

    def get_format_instruction(self) -> str:
        """Get code block format instruction."""
        lang = self.language or "python"
        return f"""
**OUTPUT FORMAT**: Respond with code in a code block.

Example:
```{lang}
# Your code here
def example():
    pass
```"""


class MarkdownParser(OutputParser):
    """Parse markdown structure."""

    def parse(self, text: str) -> dict[str, Any]:
        """
        Parse markdown into structured format.

        Args:
            text: Markdown text

        Returns:
            Dict with sections, headers, lists, code blocks
        """
        structure = {
            "headers": [],
            "sections": {},
            "lists": [],
            "code_blocks": [],
            "links": [],
        }

        # Extract headers
        header_pattern = r"^(#{1,6})\s+(.+)$"
        for match in re.finditer(header_pattern, text, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            structure["headers"].append({"level": level, "title": title, "position": match.start()})

        # Extract lists
        list_parser = ListParser()
        structure["lists"] = list_parser.parse(text)

        # Extract code blocks
        code_parser = CodeBlockParser()
        structure["code_blocks"] = code_parser.parse(text)

        # Extract links
        link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
        structure["links"] = [
            {"text": m.group(1), "url": m.group(2)} for m in re.finditer(link_pattern, text)
        ]

        return structure

    def get_format_instruction(self) -> str:
        """Get markdown format instruction."""
        return """
**OUTPUT FORMAT**: Use proper Markdown formatting.

- Headers: ## Title
- Lists: - item or 1. item
- Code: ```language ... ```
- Emphasis: **bold**, *italic*"""


class XMLParser(OutputParser):
    """Parse XML from LLM output."""

    def parse(self, text: str) -> ET.Element | None:
        """
        Extract and parse XML from text.

        Args:
            text: Text containing XML

        Returns:
            Parsed XML Element or None
        """
        # Try to find XML in code blocks
        pattern = r"```(?:xml)?\s*\n?(.*?)\n?```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            try:
                return ET.fromstring(matches[0].strip())
            except ET.ParseError:
                pass

        # Try to find raw XML
        xml_pattern = r"<\?xml.*?\?>.*?</.*?>"
        matches = re.findall(xml_pattern, text, re.DOTALL)
        if matches:
            try:
                return ET.fromstring(matches[0])
            except ET.ParseError:
                pass

        return None

    def get_format_instruction(self) -> str:
        """Get XML format instruction."""
        return """
**OUTPUT FORMAT**: Respond with valid XML.

Example:
```xml
<?xml version="1.0"?>
<response>
    <item>Value</item>
</response>
```"""


# Convenience functions


def parse_json_response(text: str, strict: bool = True) -> dict | list | None:
    """Quick JSON parsing."""
    parser = JSONParser(strict=strict)
    return parser.parse(text)


def parse_code_blocks(text: str, language: str | None = None) -> str | dict[str, str]:
    """Quick code block extraction."""
    parser = CodeBlockParser(language=language)
    return parser.parse(text)


def parse_list_items(text: str) -> list[str]:
    """Quick list extraction."""
    parser = ListParser()
    return parser.parse(text)


def parse_markdown_structure(text: str) -> dict[str, Any]:
    """Quick markdown parsing."""
    parser = MarkdownParser()
    return parser.parse(text)
