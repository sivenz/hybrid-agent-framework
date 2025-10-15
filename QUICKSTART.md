# Quick Start Guide

Get started with Hybrid Agent Framework in 5 minutes!

## Installation

```bash
pip install hybrid-agent-framework
```

## Setup

```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key" > .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> .env
```

## Your First Agent

```python
import asyncio
from hybrid_agents import HybridPlatform, Task

async def main():
    # Initialize
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    # Create task
    task = Task(
        description="Check server health: CPU, memory, disk",
        requires_system_access=True
    )

    # Run it!
    result = await platform.run(task)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## What Just Happened?

1. ✅ Task was analyzed
2. ✅ Routed to Claude (needs system access)
3. ✅ Executed bash commands
4. ✅ Results returned

## Next Steps

- **Examples**: Check `examples/` for production use cases
- **Documentation**: Read `docs/getting-started.md`
- **API Reference**: See `docs/api-reference.md`

## Need Help?

- 📖 [Full Documentation](docs/getting-started.md)
- 💬 [GitHub Discussions](https://github.com/cogniolab/hybrid-agent-framework/discussions)
- 🐛 [Report Issues](https://github.com/cogniolab/hybrid-agent-framework/issues)
