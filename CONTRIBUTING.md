# Contributing to mycontext

Thank you for your interest in contributing to mycontext! 🎉

## Ways to Contribute

### 1. Report Bugs
Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

### 2. Suggest Features
Have an idea? Open an issue describing:
- The problem it solves
- How it would work
- Example use cases

### 3. Add Cognitive Patterns
Want to add a new pattern?

```python
from mycontext.structure import Pattern
from mycontext.foundation import Guidance, Directive

class YourPattern(Pattern):
    """
    Brief description of what this pattern does.
    
    Based on: [Research paper or methodology]
    
    Example:
        ```python
        pattern = YourPattern()
        context = pattern.build_context(...)
        ```
    """
    
    def __init__(self):
        super().__init__(
            name="your_pattern",
            description="One-line description",
            guidance=Guidance(...),
            directive_template="Template with {variables}"
        )
```

**Requirements:**
- Research-backed (cite sources)
- Clear documentation
- Input validation
- Tests included

### 4. Improve Documentation
- Fix typos
- Add examples
- Clarify explanations
- Create tutorials

### 5. Write Tests
- Add test cases
- Improve coverage
- Test edge cases

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mycontext.git
cd mycontext

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## Code Standards

### Style
- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused

### Testing
- Write tests for new features
- Maintain 100% pass rate
- Test edge cases

### Documentation
- Update README if needed
- Add docstrings to all public APIs
- Include examples

## Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-pattern`)
3. **Make** your changes
4. **Test** thoroughly (`pytest tests/`)
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open** a Pull Request

### PR Checklist
- [ ] Tests pass (`pytest tests/`)
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if user-facing)
- [ ] Clear commit messages

## Commit Message Format

```
type: short description

Longer description if needed

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `chore`: Maintenance

## Questions?

Open an issue or reach out to the maintainers!

---

**Thank you for contributing to mycontext!** 🚀
