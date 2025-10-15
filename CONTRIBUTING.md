# Contributing to Hybrid Agent Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Relevant logs or error messages

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use case and motivation
- Example code or API design (if applicable)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Write clear commit messages** following conventional commits format
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** (`pytest tests/`)
6. **Run code formatting** (`black . && ruff check .`)
7. **Submit your PR** with a clear description

## 🏗️ Development Setup

```bash
# Clone the repository
git clone https://github.com/mosesrajan/hybrid-agent-framework.git
cd hybrid-agent-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run formatting
black hybrid_agents/ examples/ tests/
ruff check hybrid_agents/ examples/ tests/
```

## 📝 Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public APIs (Google style)
- Keep functions focused and small
- Add comments for complex logic

## ✅ Testing Guidelines

- Write unit tests for new functionality
- Add integration tests for multi-component features
- Aim for >80% code coverage
- Use descriptive test names: `test_<what>_<condition>_<expected_result>`

Example:
```python
def test_route_task_with_system_access_routes_to_claude():
    platform = HybridPlatform("key1", "key2")
    task = Task(description="test", requires_system_access=True)
    result = asyncio.run(platform.route_task(task))
    assert result == "claude"
```

## 🌟 Areas We Need Help

- **Use case examples**: Real-world implementations
- **Platform integrations**: Gemini, Mistral, etc.
- **Performance optimizations**: Parallel execution, caching
- **Documentation**: Tutorials, guides, API docs
- **Tests**: Increase coverage, edge cases
- **Bug fixes**: Check open issues

## 📦 Submitting Examples

If you've built something cool with the framework, we'd love to include it in `examples/`:

1. Create a new file in `examples/your_use_case.py`
2. Add clear comments explaining the workflow
3. Include expected outcomes and business impact
4. Update `examples/README.md` with your example

## 🤝 Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Credit others' work appropriately

## 📧 Questions?

- **General questions**: Open a GitHub discussion
- **Bug reports**: Create an issue
- **Security concerns**: Email moses@cogniolab.com

## 🎓 First Time Contributing?

Check out these "good first issue" labels:
- `good-first-issue`: Simple tasks for newcomers
- `documentation`: Help improve docs
- `examples`: Add new use cases

Thank you for making the Hybrid Agent Framework better! 🚀
