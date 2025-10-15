"""
Example: Automated Research Pipeline

This example demonstrates:
1. Literature review coordination (OpenAI)
2. Web scraping and data collection (Claude)
3. Multi-researcher collaboration
4. Hypothesis generation and testing
5. Report compilation
"""

import asyncio
from hybrid_agents import HybridPlatform, Task, TaskType


async def main():
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    print("=" * 60)
    print("AUTOMATED RESEARCH PIPELINE")
    print("Research Topic: AI Agent Architectures")
    print("=" * 60)
    print()

    research_task = Task(
        id="research_ai_agents_2024",
        type=TaskType.RESEARCH,
        description="""
        Conduct comprehensive literature review on AI Agent Architectures

        Research objectives:
        1. Review recent papers (2024-2025) on AI agents
        2. Identify key architectural patterns
        3. Compare OpenAI vs Claude agent approaches
        4. Analyze production deployment challenges
        5. Synthesize findings into research report

        Data sources:
        - ArXiv papers on AI agents
        - GitHub repositories
        - Technical blog posts
        - Industry case studies

        Deliverables:
        - Literature review summary
        - Architectural pattern taxonomy
        - Comparative analysis
        - Research recommendations
        """,
        requires_system_access=True,
        requires_multi_step=True,
        context={
            "search_keywords": ["ai agents", "agent architectures", "llm orchestration"],
            "date_range": "2024-2025",
            "min_citations": 5,
            "output_format": "markdown"
        }
    )

    result = await platform.run(research_task)

    print("\n" + "=" * 60)
    print("RESEARCH RESULTS")
    print("=" * 60)

    if result['platform'] == 'hybrid':
        print("\n📚 Stage 1 - Research Planning (OpenAI):")
        print(f"  {result['stages']['planning']['output']['result']}")

        print("\n🔍 Stage 2 - Data Collection (Claude):")
        print(f"  {result['stages']['execution']['output']['result']}")

        print("\n📝 Stage 3 - Synthesis & Report (OpenAI):")
        print(f"  {result['stages']['verification']['output']['result']}")

    print("\n" + "=" * 60)
    print("Expected Impact:")
    print("  - Research time: 2 weeks → 2 days (7x faster)")
    print("  - Papers reviewed: 10 → 100+ (10x scale)")
    print("  - Consistency: Automated analysis")
    print("  - Collaboration: Multi-researcher workflows")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
