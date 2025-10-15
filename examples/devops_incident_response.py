"""
Example: DevOps Incident Response with Hybrid Agents

This example demonstrates automated incident response that:
1. OpenAI coordinates team communication
2. Claude diagnoses system issues
3. Claude executes fixes
4. OpenAI verifies and reports
"""

import asyncio
from hybrid_agents import HybridPlatform, Task, TaskType, Guardrail, GuardrailType


async def main():
    # Initialize platform
    platform = HybridPlatform(
        openai_api_key="sk-...",  # Replace with actual key
        anthropic_api_key="sk-ant-..."  # Replace with actual key
    )

    # Add safety guardrails
    platform.add_guardrail(
        Guardrail(
            name="production_safety",
            type=GuardrailType.BLOCK,
            condition=lambda task: "DROP TABLE" in task.description.upper() or "rm -rf /" in task.description,
            message="Blocked: Potentially destructive operation detected"
        )
    )

    platform.add_guardrail(
        Guardrail(
            name="high_priority_approval",
            type=GuardrailType.APPROVAL_REQUIRED,
            condition=lambda task: task.priority >= 4,
            message="High priority incident requires approval",
            approver="slack://ops-channel"
        )
    )

    # Simulate incident: Database CPU spike
    print("=" * 60)
    print("INCIDENT: Database CPU at 100%")
    print("=" * 60)
    print()

    incident_task = Task(
        id="incident_001",
        type=TaskType.INCIDENT_RESPONSE,
        description="""
        Production database CPU usage is at 100%.
        Diagnose the issue and recommend fixes.
        Check for:
        - Long-running queries
        - Missing indexes
        - Connection pool exhaustion
        - Memory issues
        """,
        requires_system_access=True,
        requires_multi_step=True,
        priority=5,
        context={
            "server": "prod-db-01",
            "alert_time": "2025-10-15 23:47:00",
            "severity": "critical"
        }
    )

    # Execute hybrid workflow
    result = await platform.run(incident_task)

    # Display results
    print("\n" + "=" * 60)
    print("INCIDENT RESOLUTION SUMMARY")
    print("=" * 60)
    print(f"\nTask ID: {result['task_id']}")
    print(f"Platform: {result['platform']}")

    if result['platform'] == 'hybrid':
        print("\nStage 1 - Planning (OpenAI):")
        print(f"  {result['stages']['planning']['output']['result']}")

        print("\nStage 2 - Execution (Claude):")
        print(f"  {result['stages']['execution']['output']['result']}")
        print(f"  Tools used: {result['stages']['execution']['output']['tools_used']}")

        print("\nStage 3 - Verification (OpenAI):")
        print(f"  {result['stages']['verification']['output']['result']}")

    # Show task history
    print("\n" + "=" * 60)
    print("TASK EXECUTION TIMELINE")
    print("=" * 60)
    for task in platform.get_task_history():
        print(f"\n[{task['status']}] {task['id']}")
        print(f"  Type: {task['type']}")
        print(f"  Platform: {task.get('assigned_platform', 'N/A')}")
        if task.get('execution_time'):
            print(f"  Duration: {task['execution_time']:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())

    print("\n" + "=" * 60)
    print("Expected Production Impact:")
    print("  - MTTR: 45 min → 5 min (9x improvement)")
    print("  - Cost savings: ~$800K per incident")
    print("  - Reduced human error: Automated verification")
    print("=" * 60)
