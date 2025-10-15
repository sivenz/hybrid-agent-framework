# Getting Started with Hybrid Agent Framework

## 🚀 Quick Start (5 minutes)

### 1. Installation

```bash
pip install hybrid-agent-framework
```

### 2. Set Up API Keys

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or create a `.env` file:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Your First Hybrid Agent

```python
import asyncio
from hybrid_agents import HybridPlatform, Task

async def main():
    # Initialize platform
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    # Create a simple task
    task = Task(
        description="Analyze the current directory structure and summarize",
        requires_system_access=True
    )

    # Run it
    result = await platform.run(task)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎓 Core Concepts

### Tasks

Tasks are the fundamental unit of work. They can be:
- **Conversational**: Q&A, explanations
- **System Operations**: File access, bash commands
- **Research**: Deep analysis, web scraping
- **Analysis**: Data processing, insights
- **Code Review**: PR analysis, security scans
- **Deployment**: CI/CD automation

```python
from hybrid_agents import Task, TaskType

task = Task(
    description="What you want the agent to do",
    type=TaskType.SYSTEM_OPERATION,
    requires_system_access=True,
    requires_multi_step=False,
    context={"key": "value"}
)
```

### Intelligent Routing

The framework automatically routes tasks to the best platform:

```
Task → Platform Analysis
  ├─ System access needed? → Claude
  ├─ Multi-step workflow? → Hybrid
  ├─ Conversation/analysis? → OpenAI
  └─ Complex coordination? → OpenAI
```

### Hybrid Workflows

Complex tasks use both platforms:

```
1. OpenAI Plans → "Here's how to solve this"
2. Claude Executes → "Running commands..."
3. OpenAI Verifies → "Results look good!"
```

## 📚 Common Patterns

### Pattern 1: System Diagnostics

```python
diagnostic_task = Task(
    type=TaskType.SYSTEM_OPERATION,
    description="Check server health: CPU, memory, disk, network",
    requires_system_access=True
)

result = await platform.run(diagnostic_task)
```

### Pattern 2: Multi-Stage Analysis

```python
analysis_task = Task(
    type=TaskType.RESEARCH,
    description="Analyze codebase for security vulnerabilities",
    requires_system_access=True,
    requires_multi_step=True  # Forces hybrid workflow
)

result = await platform.run(analysis_task)
# Stage 1: OpenAI plans the analysis
# Stage 2: Claude scans files
# Stage 3: OpenAI summarizes findings
```

### Pattern 3: With Guardrails

```python
from hybrid_agents import Guardrail, GuardrailType

# Add safety check
platform.add_guardrail(
    Guardrail(
        name="no_destructive_ops",
        type=GuardrailType.BLOCK,
        condition=lambda task: "DROP" in task.description.upper(),
        message="Destructive operations are blocked"
    )
)

# This will be blocked
task = Task(description="DROP TABLE users")
result = await platform.run(task)
# Returns: {"status": "blocked", "message": "..."}
```

## 🎯 Real-World Example

Here's a complete incident response workflow:

```python
import asyncio
from hybrid_agents import HybridPlatform, Task, TaskType, Guardrail, GuardrailType

async def incident_response():
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    # Add guardrails
    platform.add_guardrail(
        Guardrail(
            name="production_safety",
            type=GuardrailType.APPROVAL_REQUIRED,
            condition=lambda task: task.context.get("env") == "production",
            message="Production changes require approval",
            approver="ops-team@company.com"
        )
    )

    # Create incident task
    incident = Task(
        type=TaskType.INCIDENT_RESPONSE,
        description="""
        Database CPU is at 100%. Diagnose and recommend fixes.
        Check for: long queries, missing indexes, connection issues
        """,
        requires_system_access=True,
        requires_multi_step=True,
        context={"env": "production", "server": "db-01"}
    )

    # Execute
    result = await platform.run(incident)

    # Result contains:
    # - Planning stage (OpenAI)
    # - Execution stage (Claude with bash access)
    # - Verification stage (OpenAI)

    return result

if __name__ == "__main__":
    result = asyncio.run(incident_response())
    print(result)
```

## 🔍 What's Next?

- **[Architecture Deep Dive](./architecture.md)** - How it works under the hood
- **[Use Case Library](./use-cases.md)** - Production examples
- **[Best Practices](./best-practices.md)** - Security and optimization
- **[API Reference](./api-reference.md)** - Complete API docs

## 💡 Tips

1. **Start Simple**: Begin with single-platform tasks before hybrid workflows
2. **Use Type Hints**: Leverage IDE autocomplete with proper types
3. **Add Guardrails Early**: Prevent issues before they happen
4. **Enable Tracing**: Debug issues with full execution logs
5. **Check Examples**: See `examples/` for complete implementations

## ❓ Common Questions

**Q: Do I need both API keys?**
A: Yes, for hybrid workflows. Single-platform tasks only need one.

**Q: What's the cost?**
A: Standard API pricing applies. Use `estimated_cost` to track.

**Q: Can I use other LLMs?**
A: Yes! The architecture is extensible. See [Custom Providers](./custom-providers.md).

**Q: Is it production-ready?**
A: Yes! Used in production with proper guardrails and monitoring.

## 🆘 Need Help?

- **Bug?** [Open an issue](https://github.com/mosesrajan/hybrid-agent-framework/issues)
- **Question?** [Start a discussion](https://github.com/mosesrajan/hybrid-agent-framework/discussions)
- **Security?** Email moses@cogniolab.com
