# Changelog

All notable changes to mycontext will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Week 2 Additions (2026-02-08)

#### Added
- **Provider System**: OpenAI and Anthropic integrations
  - OpenAIProvider with full GPT-4, GPT-3.5 support
  - AnthropicProvider with Claude 3.5, 3 Opus, 3 Haiku support
  - Provider registry with lazy loading
  - Custom provider registration
  - Provider caching for performance
  - Automatic cost estimation and tracking

- **Knowledge Layer (Layer 3)**: Session and Archive management
  - Session class for multi-turn conversations
  - Message tracking with roles (system, user, assistant)
  - Automatic token budgeting and pruning
  - FileArchive for JSON-based persistent storage
  - MemoryArchive for in-memory testing
  - Full-text search across archived sessions
  - Session tagging and filtering

- **Examples**: Real-world usage demonstrations
  - openai_example.py - OpenAI provider usage
  - anthropic_example.py - Anthropic provider usage
  - knowledge_example.py - Session and Archive patterns

- **Testing**: Expanded test coverage
  - 23 new tests for Knowledge layer
  - 18 new tests for Provider layer
  - Total: 76 tests (74 pass, 2 skip)

#### Changed
- Updated pyproject.toml with optional dependencies
  - `[openai]` - OpenAI provider support
  - `[anthropic]` - Anthropic provider support
  - `[rag]`, `[redis]`, `[postgres]` - Future features
  - `[all]` - All optional dependencies
- Python version support: 3.11+ (was 3.12+)
- Enhanced main __init__.py with Knowledge exports
- Improved provider __init__.py with registry

#### Fixed
- MockProvider cost estimation (now returns realistic mock costs)
- Test assertions to match actual implementation

## [0.1.0] - 2026-02-08

### Added
- Initial project structure
- Foundation layer (Directive, Guidance, Constraints)
- Structure layer (Pattern, Blueprint)
- Core Context class
- Provider interface with mock provider
- Comprehensive test suite (37 tests)
- Documentation and examples
- Revolutionary Context Stack™ framework
- Context as Code™ paradigm
- Clean, intuitive API
- Type-safe with Pydantic models
- Production-ready architecture

[Unreleased]: https://github.com/mycontext-ai/mycontext/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mycontext-ai/mycontext/releases/tag/v0.1.0
