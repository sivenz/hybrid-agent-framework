"""
Example: Automated Code Review and Deployment Pipeline

This example demonstrates:
1. OpenAI reviews PR for security/breaking changes
2. Claude runs tests, linters, security scans
3. OpenAI decides on approval with guardrails
4. Claude deploys if approved
5. Claude runs health checks
6. OpenAI notifies team
"""

import asyncio
from hybrid_agents import HybridPlatform, Task, TaskType, Guardrail, GuardrailType


async def main():
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    # Add code review guardrails
    platform.add_guardrail(
        Guardrail(
            name="security_review",
            type=GuardrailType.APPROVAL_REQUIRED,
            condition=lambda task: "security" in task.description.lower() or "auth" in task.description.lower(),
            message="Security-related changes require manual review",
            approver="security-team@company.com"
        )
    )

    platform.add_guardrail(
        Guardrail(
            name="breaking_changes",
            type=GuardrailType.BLOCK,
            condition=lambda task: task.context.get("breaking_changes", False),
            message="Breaking changes detected - requires manual deployment"
        )
    )

    print("=" * 60)
    print("AUTOMATED CODE REVIEW & DEPLOYMENT PIPELINE")
    print("=" * 60)
    print()

    # PR Review Task
    pr_task = Task(
        id="pr_456",
        type=TaskType.CODE_REVIEW,
        description="""
        Review Pull Request #456: Add user authentication middleware

        Changes:
        - New JWT authentication middleware
        - Updated user model with password hashing
        - Added authentication tests

        Tasks:
        1. Review code for security issues
        2. Run test suite
        3. Run security scans (dependency check, static analysis)
        4. Verify no breaking changes
        5. Deploy to staging if all checks pass
        6. Run smoke tests
        """,
        requires_system_access=True,
        requires_multi_step=True,
        context={
            "repo": "company/api-service",
            "pr_number": 456,
            "branch": "feature/auth-middleware",
            "author": "developer@company.com",
            "breaking_changes": False
        }
    )

    result = await platform.run(pr_task)

    print("\n" + "=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)

    if result['platform'] == 'hybrid':
        print("\n✓ Stage 1 - Code Review (OpenAI):")
        print(f"  {result['stages']['planning']['output']['result']}")

        print("\n✓ Stage 2 - Testing & Deployment (Claude):")
        print(f"  {result['stages']['execution']['output']['result']}")

        print("\n✓ Stage 3 - Verification & Notification (OpenAI):")
        print(f"  {result['stages']['verification']['output']['result']}")

    print("\n" + "=" * 60)
    print("Expected Impact:")
    print("  - Deployment time: 2 hours → 20 minutes")
    print("  - Zero security issues deployed")
    print("  - Automatic rollback on failed health checks")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
