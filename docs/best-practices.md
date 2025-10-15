# Best Practices

## 🔒 Security

### 1. API Key Management

**❌ Don't**: Hardcode API keys
```python
platform = HybridPlatform(
    openai_api_key="sk-hardcoded-key",  # BAD!
    anthropic_api_key="sk-ant-hardcoded"
)
```

**✅ Do**: Use environment variables
```python
import os
platform = HybridPlatform(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

### 2. Guardrails Are Essential

Always add guardrails for:
- Destructive operations
- Production systems
- High-cost operations
- Sensitive data access

```python
# Production safety
platform.add_guardrail(
    Guardrail(
        name="production_safety",
        type=GuardrailType.APPROVAL_REQUIRED,
        condition=lambda task: task.context.get("env") == "production",
        message="Production changes require approval",
        approver="ops-team@company.com"
    )
)

# Cost control
platform.add_guardrail(
    Guardrail(
        name="cost_limit",
        type=GuardrailType.BLOCK,
        condition=lambda task: task.estimated_cost > 10.0,
        message="Task exceeds $10 cost limit"
    )
)

# Destructive operation prevention
platform.add_guardrail(
    Guardrail(
        name="no_destructive_ops",
        type=GuardrailType.BLOCK,
        condition=lambda task: any(cmd in task.description.upper() for cmd in ["DROP", "DELETE", "rm -rf"]),
        message="Destructive operations blocked"
    )
)
```

### 3. Principle of Least Privilege

Configure Claude agents with minimal necessary permissions:

```python
# Only allow necessary commands
allowed_commands = [
    "ls", "cat", "grep", "ps", "top", "df",
    "git status", "git log", "git diff",
    "npm test", "pytest", "docker ps"
]

# Block dangerous commands
forbidden_commands = [
    "rm -rf", "sudo", "chmod 777",
    "DROP TABLE", "DELETE FROM",
    "curl | bash", "wget | bash"
]

# Require approval for sensitive operations
require_approval = [
    "git push", "npm publish",
    "kubectl apply", "terraform apply",
    "systemctl restart"
]
```

### 4. Audit Logging

Enable comprehensive logging for compliance:

```python
platform.enable_audit_log(
    destination="s3://audit-logs/agents/",
    include_context=True,
    include_results=True,
    retention_days=365
)

# Every action is logged:
# - Who triggered it
# - What was executed
# - When it ran
# - What the result was
# - Who approved it (if applicable)
```

## ⚡ Performance

### 1. Use Appropriate Execution Modes

```python
# Simple tasks → Single platform
task = Task(description="Explain X")  # Fast, efficient

# Complex tasks → Hybrid only when needed
task = Task(
    description="Complex multi-step task",
    requires_multi_step=True  # Only when necessary
)
```

### 2. Leverage Parallel Execution

```python
# When tasks are independent, run in parallel
tasks = [
    Task(description="Check server 1", requires_system_access=True),
    Task(description="Check server 2", requires_system_access=True),
    Task(description="Check server 3", requires_system_access=True)
]

results = await asyncio.gather(*[platform.run(task) for task in tasks])
```

### 3. Set Appropriate Timeouts

```python
# Short timeout for simple tasks
task = Task(description="Quick check", timeout=30)

# Longer timeout for complex operations
task = Task(
    description="Full codebase analysis",
    requires_system_access=True,
    timeout=600  # 10 minutes
)
```

### 4. Use Context Caching

```python
# Cache expensive operations
@cache(ttl=300)  # Cache for 5 minutes
async def analyze_large_dataset(data_path):
    # Expensive analysis
    pass
```

## 📊 Cost Optimization

### 1. Estimate Costs Upfront

```python
task = Task(
    description="Large analysis task",
    estimated_cost=5.0  # Set reasonable limit
)

# Add cost guardrail
platform.add_guardrail(
    Guardrail(
        name="budget_control",
        type=GuardrailType.BLOCK,
        condition=lambda task: task.estimated_cost > 10.0,
        message="Exceeds budget"
    )
)
```

### 2. Use the Right Platform

```python
# OpenAI is more cost-effective for:
# - Simple conversations
# - Planning and reasoning
# - Text analysis

# Claude is more cost-effective for:
# - System operations (bash is free!)
# - File processing
# - Long-context tasks
```

### 3. Monitor Usage

```python
# Track token usage
metrics = platform.get_metrics()
print(f"Total tokens used: {metrics['total_tokens']}")
print(f"Estimated cost: ${metrics['estimated_cost']:.2f}")

# Set daily limits
platform.set_rate_limits(
    max_tasks_per_day=1000,
    max_cost_per_day=100.0
)
```

## 🧪 Testing

### 1. Test Routing Logic

```python
def test_routing():
    # Test that system tasks go to Claude
    task = Task(requires_system_access=True)
    assert platform.route_task(task) == "claude"

    # Test that conversations go to OpenAI
    task = Task(type=TaskType.CONVERSATION)
    assert platform.route_task(task) == "openai"
```

### 2. Test Guardrails

```python
def test_guardrails():
    platform.add_guardrail(
        Guardrail(
            name="test",
            type=GuardrailType.BLOCK,
            condition=lambda task: "bad" in task.description,
            message="Blocked"
        )
    )

    task = Task(description="This is bad")
    result = platform.run(task)
    assert result["status"] == "blocked"
```

### 3. Mock External APIs in Tests

```python
@pytest.fixture
def mock_platform(monkeypatch):
    # Mock OpenAI/Claude API calls for fast tests
    def mock_openai_call(*args, **kwargs):
        return {"result": "mocked"}

    monkeypatch.setattr("openai.chat.completions.create", mock_openai_call)
    return HybridPlatform("test-key", "test-key")
```

## 📝 Code Organization

### 1. Structure Your Tasks

```python
# ❌ Don't: Vague descriptions
task = Task(description="Do something")

# ✅ Do: Clear, specific descriptions
task = Task(
    type=TaskType.SYSTEM_OPERATION,
    description="""
    Check production database health:
    1. CPU and memory usage
    2. Active connections
    3. Slow query log
    4. Replication lag
    """,
    requires_system_access=True,
    context={
        "server": "prod-db-01",
        "alert_threshold": 80
    }
)
```

### 2. Use Context Effectively

```python
task = Task(
    description="Deploy application",
    context={
        "environment": "staging",
        "version": "v2.1.0",
        "rollback_version": "v2.0.5",
        "health_check_url": "https://api.example.com/health",
        "notify_channels": ["#deployments", "#engineering"]
    }
)
```

### 3. Organize Guardrails

```python
class GuardrailPresets:
    """Reusable guardrail configurations"""

    @staticmethod
    def production_safety(approver: str):
        return Guardrail(
            name="production_safety",
            type=GuardrailType.APPROVAL_REQUIRED,
            condition=lambda task: task.context.get("env") == "production",
            message="Production changes require approval",
            approver=approver
        )

    @staticmethod
    def cost_limit(max_cost: float):
        return Guardrail(
            name="cost_limit",
            type=GuardrailType.BLOCK,
            condition=lambda task: task.estimated_cost > max_cost,
            message=f"Exceeds ${max_cost} cost limit"
        )

# Use presets
platform.add_guardrail(GuardrailPresets.production_safety("ops-team@company.com"))
platform.add_guardrail(GuardrailPresets.cost_limit(10.0))
```

## 🔍 Debugging

### 1. Enable Tracing

```python
platform.enable_tracing(
    destination="logfire",
    api_key=os.getenv("LOGFIRE_API_KEY")
)

# All operations are traced:
# - Task routing decisions
# - Agent interactions
# - Tool invocations
# - Handoffs
```

### 2. Use Descriptive Task IDs

```python
# ❌ Don't: Auto-generated IDs only
task = Task(description="...")  # id: "123e4567-e89b-12d3..."

# ✅ Do: Meaningful IDs
task = Task(
    id="incident_prod_db_20251015_2347",
    description="..."
)
```

### 3. Check Task History

```python
# Review what happened
history = platform.get_task_history()
for task in history:
    print(f"{task['id']}: {task['status']} in {task['execution_time']:.2f}s")
```

## 🚀 Production Deployment

### 1. Use Environment-Specific Configuration

```python
# config/production.py
GUARDRAILS = [
    GuardrailPresets.production_safety("ops-team@company.com"),
    GuardrailPresets.cost_limit(50.0),
]

RATE_LIMITS = {
    "max_tasks_per_minute": 10,
    "max_claude_executions_per_hour": 100
}

# config/staging.py
GUARDRAILS = [
    GuardrailPresets.cost_limit(10.0),
]

RATE_LIMITS = {
    "max_tasks_per_minute": 50,
}
```

### 2. Health Checks

```python
async def health_check():
    """Verify platform is operational"""
    test_task = Task(description="Health check test")
    try:
        result = await platform.run(test_task)
        return {"status": "healthy", "response_time": result.get("execution_time")}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### 3. Monitoring

```python
# Set up metrics
metrics = platform.get_metrics()

# Alert on anomalies
if metrics["success_rate"] < 0.95:
    alert("Agent success rate dropped below 95%")

if metrics["avg_execution_time"] > 30:
    alert("Agent execution time increased")
```

## 📚 Documentation

### 1. Document Your Workflows

```python
async def incident_response_workflow(incident_details):
    """
    Automated incident response workflow

    This workflow:
    1. Analyzes incident severity (OpenAI)
    2. Runs diagnostics on affected systems (Claude)
    3. Recommends fixes (OpenAI)
    4. Executes approved fixes (Claude)
    5. Verifies resolution (Claude)
    6. Notifies stakeholders (OpenAI)

    Args:
        incident_details: Dict containing incident information

    Returns:
        Dict with resolution details and timeline

    Expected Impact:
        - MTTR: 45 min → 5 min
        - Human intervention: Approval only
        - Accuracy: 98%+
    """
    # Implementation...
```

### 2. Include Examples in Docstrings

```python
def create_deployment_task(version: str, environment: str) -> Task:
    """
    Create a deployment task

    Example:
        >>> task = create_deployment_task("v2.1.0", "staging")
        >>> result = await platform.run(task)
        >>> print(result["status"])
        "completed"
    """
```

## ⚠️ Common Pitfalls

### 1. Don't Over-Orchestrate

```python
# ❌ Don't: Force hybrid when not needed
task = Task(
    description="Simple question",
    requires_multi_step=True  # Unnecessary overhead
)

# ✅ Do: Let router decide
task = Task(description="Simple question")  # Efficient
```

### 2. Don't Ignore Failures

```python
# ❌ Don't: Ignore errors
result = await platform.run(task)

# ✅ Do: Handle failures
try:
    result = await platform.run(task)
    if result.get("status") == "failed":
        # Handle failure
        logger.error(f"Task failed: {result.get('error')}")
        # Retry or alert
except Exception as e:
    # Handle exception
    logger.exception("Task execution exception")
```

### 3. Don't Skip Guardrails

```python
# ❌ Don't: Run without guardrails in production
platform = HybridPlatform(...)
result = await platform.run(risky_task)  # Dangerous!

# ✅ Do: Always use guardrails
platform.add_guardrail(GuardrailPresets.production_safety(...))
platform.add_guardrail(GuardrailPresets.cost_limit(...))
result = await platform.run(task)  # Safe
```

## 🎯 Summary

**Key Takeaways:**
1. ✅ Always use guardrails for production
2. ✅ Enable audit logging for compliance
3. ✅ Use appropriate execution modes
4. ✅ Monitor costs and performance
5. ✅ Test routing and guardrails
6. ✅ Document your workflows
7. ✅ Handle errors gracefully
8. ✅ Use least privilege for Claude agents

Following these best practices will help you build secure, efficient, and maintainable agent systems.
