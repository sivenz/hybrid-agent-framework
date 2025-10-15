# Architecture Deep Dive

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────┐
│                   HybridPlatform                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Task Router & Orchestrator               │   │
│  │    (Intelligent routing based on requirements)   │   │
│  └──────────────┬──────────────────────────────────┘   │
│                 │                                        │
│    ┌────────────┴────────────┐                         │
│    │                          │                         │
│    ▼                          ▼                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │ OpenAI Layer │      │ Claude Layer  │               │
│  │              │      │               │               │
│  │ • Coordinator│      │ • Executor    │               │
│  │ • Analyst    │      │ • Researcher  │               │
│  │ • Validator  │      │ • Verifier    │               │
│  └──────────────┘      └──────────────┘               │
│         │                      │                        │
│         │    ┌─────────────┐  │                       │
│         └───→│  Guardrails │←─┘                       │
│              │   Engine    │                           │
│              └─────────────┘                           │
└─────────────────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. Task System

**Task**: The fundamental unit of work

```python
@dataclass
class Task:
    description: str              # What to do
    type: TaskType               # Category of work
    requires_system_access: bool # Needs bash/files?
    requires_multi_step: bool    # Complex workflow?
    context: Dict[str, Any]      # Additional data
    priority: int                # 1-5 (5 = highest)
```

**Task Lifecycle**:
```
PENDING → ROUTING → IN_PROGRESS → COMPLETED
                          ↓
                       FAILED
```

### 2. Intelligent Router

The router analyzes tasks and selects the optimal execution strategy:

```python
async def route_task(task: Task) -> str:
    # Decision tree:
    if task.requires_system_access:
        return "claude"  # Needs bash/file access

    if task.requires_multi_step:
        return "hybrid"  # Complex workflow

    if task.type in [CONVERSATION, ANALYSIS]:
        return "openai"  # Best for reasoning

    if task.type in [SYSTEM_OPERATION, RESEARCH]:
        return "claude"  # Best for execution
```

**Routing Matrix**:

| Task Attribute | OpenAI | Claude | Hybrid |
|---------------|--------|--------|--------|
| System access | ❌ | ✅ | ✅ |
| Multi-agent coordination | ✅ | ❌ | ✅ |
| Bash execution | ❌ | ✅ | ✅ |
| Conversation | ✅ | ✅ | ✅ |
| MCP integration | ❌ | ✅ | ✅ |
| Guardrails | ✅ | ⚠️ | ✅ |
| Verification loops | ⚠️ | ✅ | ✅ |

### 3. Execution Modes

#### Mode A: Single Platform

```
Task → Router → Single Platform → Result
```

Example:
```python
# Simple conversation → OpenAI
task = Task(description="Explain quantum computing")
result = await platform.run(task)
```

#### Mode B: Hybrid Workflow

```
Task → Router → Hybrid Orchestrator
                      ↓
        ┌────────────┴────────────┐
        ▼                          ▼
    OpenAI (Plan)             Claude (Execute)
        │                          │
        └──────────┬───────────────┘
                   ▼
            OpenAI (Verify)
                   ↓
                Result
```

Example:
```python
# Complex task → Hybrid
task = Task(
    description="Audit codebase for security issues",
    requires_system_access=True,
    requires_multi_step=True
)
result = await platform.run(task)

# Returns:
# {
#   "stages": {
#     "planning": {...},     # OpenAI analysis
#     "execution": {...},    # Claude scans files
#     "verification": {...}  # OpenAI summarizes
#   }
# }
```

### 4. Guardrail Engine

Guardrails provide safety checks before execution:

```python
class GuardrailType:
    VALIDATION       # Input validation
    BLOCK           # Hard stop
    APPROVAL_REQUIRED # Human-in-loop
    RATE_LIMIT      # Prevent abuse
    COST_LIMIT      # Budget control
```

**Guardrail Evaluation**:
```
Task → Guardrail Engine
         ↓
    For each guardrail:
      - Evaluate condition
      - If triggered:
          - BLOCK → Reject task
          - APPROVAL_REQUIRED → Wait for approval
         ↓
    All pass → Proceed to execution
```

Example:
```python
platform.add_guardrail(
    Guardrail(
        name="cost_limit",
        type=GuardrailType.BLOCK,
        condition=lambda task: task.estimated_cost > 10.0,
        message="Task exceeds $10 cost limit"
    )
)
```

## 🔄 Workflow Examples

### Example 1: DevOps Incident Response

```
1. INCIDENT DETECTED
   ↓
2. Task Created (requires_multi_step=True)
   ↓
3. ROUTER → "hybrid"
   ↓
4. STAGE 1: OpenAI Coordinator
   - Analyzes incident severity
   - Creates diagnostic plan
   - Notifies on-call team
   ↓
5. STAGE 2: Claude Executor (parallel)
   - SSH into affected servers
   - Run diagnostic commands:
     • top, ps aux, netstat
     • tail /var/log/app.log
     • mysql slow-query-log
   - Identify root cause
   ↓
6. STAGE 3: OpenAI Verifier
   - Aggregates results
   - Recommends fix
   - Requests approval if needed
   ↓
7. (If approved) STAGE 4: Claude Executor
   - Apply fix (restart service, add index, etc.)
   - Verification loop: Check if fixed
   ↓
8. STAGE 5: OpenAI Communicator
   - Update incident ticket
   - Notify team
   - Create post-mortem
   ↓
9. COMPLETE
```

### Example 2: Code Review → Deploy

```
1. PR OPENED
   ↓
2. STAGE 1: OpenAI Analyst
   - Review PR description
   - Identify security concerns
   - Check for breaking changes
   ↓
3. STAGE 2: Claude Executor
   Parallel execution:
   - git clone && checkout branch
   - npm test (or pytest, cargo test, etc.)
   - npm run lint
   - npm run security-scan
   - Coverage report
   ↓
4. STAGE 3: OpenAI Decision Agent
   - Aggregate test results
   - Apply guardrails:
     • Tests must pass
     • Coverage > 80%
     • No critical security issues
   - Decision: APPROVE or REJECT
   ↓
5. (If approved) STAGE 4: Claude Deployer
   - git merge to main
   - Trigger CI/CD pipeline
   - kubectl apply -f deployment.yaml
   - Health check verification loop
   ↓
6. STAGE 5: OpenAI Notifier
   - Update PR status
   - Post deployment summary
   - Notify team in Slack
   ↓
7. COMPLETE
```

## 🔐 Security Architecture

### Principle of Least Privilege

```python
# Claude agents have restricted permissions
claude_config = {
    "allowed_commands": [
        "ls", "cat", "grep", "ps", "top",
        "git status", "npm test"
    ],
    "forbidden_commands": [
        "rm -rf", "DROP TABLE", "DELETE FROM",
        "sudo", "chmod 777"
    ],
    "require_approval": [
        "git push", "kubectl apply",
        "systemctl restart"
    ]
}
```

### Audit Trail

Every agent action is logged:

```python
{
    "task_id": "incident_001",
    "timestamp": "2025-10-15T23:47:00Z",
    "agent": "claude_executor",
    "action": "bash_command",
    "command": "systemctl status nginx",
    "output": "...",
    "user": "system",
    "approved_by": "ops-team@company.com"
}
```

### Guardrail Layers

```
Layer 1: Input Validation (before routing)
    ↓
Layer 2: Platform Guardrails (OpenAI validates)
    ↓
Layer 3: Execution Validation (Claude pre-check)
    ↓
Layer 4: Output Verification (OpenAI verifies)
```

## 📊 Performance Optimizations

### 1. Parallel Execution

```python
# Claude can run multiple operations in parallel
async def execute_parallel_diagnostics():
    tasks = [
        check_cpu(),
        check_memory(),
        check_disk(),
        check_network()
    ]
    results = await asyncio.gather(*tasks)
```

### 2. Context Caching

```python
# Cache expensive operations
@cache(ttl=300)  # 5 minutes
async def analyze_codebase(repo_path):
    # Expensive file analysis
    pass
```

### 3. Streaming Results

```python
# Stream long-running operations
async for update in platform.run_streaming(task):
    print(f"Progress: {update.status}")
```

## 🧪 Testing Strategy

### Unit Tests
```python
def test_route_task_with_system_access():
    task = Task(requires_system_access=True)
    result = route_task(task)
    assert result == "claude"
```

### Integration Tests
```python
async def test_hybrid_workflow():
    platform = HybridPlatform(...)
    task = Task(requires_multi_step=True)
    result = await platform.run(task)
    assert result["platform"] == "hybrid"
    assert len(result["stages"]) == 3
```

### End-to-End Tests
```python
async def test_incident_response_e2e():
    # Simulate real incident
    result = await platform.run(incident_task)
    assert result["stages"]["execution"]["tools_used"] == ["bash"]
    assert "resolved" in result["stages"]["verification"]["output"]
```

## 🔍 Observability

### Tracing

```python
platform.enable_tracing(
    destination="logfire",
    api_key="..."
)

# Every operation is traced:
# - Task routing decisions
# - Agent interactions
# - Tool invocations
# - Handoffs
# - Results
```

### Metrics

```python
platform.get_metrics()
# Returns:
# {
#   "tasks_executed": 1234,
#   "avg_execution_time": 5.2,
#   "platform_distribution": {
#     "openai": 45%,
#     "claude": 35%,
#     "hybrid": 20%
#   },
#   "success_rate": 98.5%
# }
```

## 🎯 Extension Points

### Custom Agents

```python
class CustomAgent(Agent):
    def handle(self, task):
        # Your custom logic
        pass

platform.register_agent("custom", CustomAgent())
```

### Custom Platforms

```python
class GeminiIntegration:
    async def execute(self, task):
        # Integrate Google Gemini
        pass

platform.register_platform("gemini", GeminiIntegration())
```

### Custom Guardrails

```python
class CustomGuardrail(Guardrail):
    def evaluate(self, task):
        # Your validation logic
        return condition_met
```

## 📚 Learn More

- **[Getting Started](./getting-started.md)** - Quick start guide
- **[Use Cases](./use-cases.md)** - Production examples
- **[Best Practices](./best-practices.md)** - Security and optimization
- **[API Reference](./api-reference.md)** - Complete API docs
