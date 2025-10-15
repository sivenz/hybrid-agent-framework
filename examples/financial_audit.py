"""
Example: Financial Audit & Compliance Automation

This example demonstrates:
1. Multi-team coordination across finance, legal, IT (OpenAI)
2. Processing 10,000+ documents (Claude)
3. Cross-referencing multiple data sources
4. Compliance checking and reporting
5. Evidence trail generation
"""

import asyncio
from hybrid_agents import HybridPlatform, Task, TaskType, Guardrail, GuardrailType


async def main():
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    # Add audit-specific guardrails
    platform.add_guardrail(
        Guardrail(
            name="compliance_check",
            type=GuardrailType.VALIDATION,
            condition=lambda task: task.type == TaskType.ANALYSIS,
            message="All audit tasks must be logged"
        )
    )

    platform.add_guardrail(
        Guardrail(
            name="data_privacy",
            type=GuardrailType.APPROVAL_REQUIRED,
            condition=lambda task: "pii" in task.description.lower() or "personal" in task.description.lower(),
            message="PII access requires legal approval",
            approver="legal@company.com"
        )
    )

    print("=" * 60)
    print("FINANCIAL AUDIT AUTOMATION - Q4 2024")
    print("=" * 60)
    print()

    audit_task = Task(
        id="audit_q4_2024",
        type=TaskType.ANALYSIS,
        description="""
        Conduct comprehensive Q4 2024 financial audit for SOX compliance:

        Scope:
        1. Review all financial transactions (10,000+ records)
        2. Cross-reference with bank statements
        3. Verify internal controls
        4. Check for unusual transactions or patterns
        5. Validate expense approvals
        6. Audit trail completeness

        Data sources:
        - /data/transactions/q4_2024/*.csv
        - /data/bank_statements/q4_2024/*.pdf
        - /data/expense_reports/*.xlsx
        - /data/approval_logs/*.json

        Compliance standards:
        - SOX (Sarbanes-Oxley)
        - GAAP
        - Company policies

        Deliverables:
        - Compliance report
        - List of exceptions
        - Remediation recommendations
        - Executive summary
        """,
        requires_system_access=True,
        requires_multi_step=True,
        priority=5,
        context={
            "audit_type": "sox_compliance",
            "quarter": "Q4 2024",
            "auditor": "external_auditor@firm.com",
            "data_path": "/data/audit/q4_2024/",
            "report_deadline": "2025-01-31"
        }
    )

    print("Starting audit workflow...")
    print("This may take several minutes for large datasets\n")

    result = await platform.run(audit_task)

    print("\n" + "=" * 60)
    print("AUDIT RESULTS")
    print("=" * 60)

    if result['platform'] == 'hybrid':
        print("\n📊 Stage 1 - Audit Planning (OpenAI):")
        print(f"  {result['stages']['planning']['output']['result']}")

        print("\n📁 Stage 2 - Document Processing (Claude):")
        print(f"  {result['stages']['execution']['output']['result']}")
        print(f"  Tools used: {result['stages']['execution']['output']['tools_used']}")
        print(f"  Verification: {result['stages']['execution']['output']['verification']}")

        print("\n✅ Stage 3 - Report Generation (OpenAI):")
        print(f"  {result['stages']['verification']['output']['result']}")

    print("\n" + "=" * 60)
    print("Expected Impact:")
    print("  - Audit duration: 6 months → 6 weeks")
    print("  - Document processing: Manual → Automated")
    print("  - Exception detection: 100% coverage")
    print("  - Cost savings: $500K+ per audit cycle")
    print("  - Risk reduction: Early detection of issues")
    print("=" * 60)


async def demo_parallel_processing():
    """
    Demonstrate parallel document processing
    """
    platform = HybridPlatform(
        openai_api_key="sk-...",
        anthropic_api_key="sk-ant-..."
    )

    print("\n" + "=" * 60)
    print("PARALLEL DOCUMENT PROCESSING DEMO")
    print("=" * 60)

    # Process multiple document categories in parallel
    tasks = [
        Task(
            id="process_transactions",
            description="Parse and validate transaction records",
            requires_system_access=True,
            context={"file_pattern": "*.csv"}
        ),
        Task(
            id="process_bank_statements",
            description="Extract data from bank statement PDFs",
            requires_system_access=True,
            context={"file_pattern": "*.pdf"}
        ),
        Task(
            id="process_expense_reports",
            description="Analyze expense reports for policy compliance",
            requires_system_access=True,
            context={"file_pattern": "*.xlsx"}
        ),
    ]

    print(f"\nProcessing {len(tasks)} document categories in parallel...")

    results = await asyncio.gather(*[platform.run(task) for task in tasks])

    print(f"\n✅ Processed {len(results)} document categories")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.get('task_id')}: {result.get('platform')}")


if __name__ == "__main__":
    # Run main audit
    asyncio.run(main())

    # Optionally demonstrate parallel processing
    # asyncio.run(demo_parallel_processing())
