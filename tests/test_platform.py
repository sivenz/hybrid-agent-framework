"""
Tests for HybridPlatform core functionality
"""

import pytest
import asyncio
from hybrid_agents import HybridPlatform, Task, TaskType, Guardrail, GuardrailType


@pytest.fixture
def platform():
    """Create platform instance for testing"""
    return HybridPlatform(
        openai_api_key="test-key",
        anthropic_api_key="test-key"
    )


class TestTaskRouting:
    """Test intelligent task routing"""

    @pytest.mark.asyncio
    async def test_route_system_access_to_claude(self, platform):
        """Tasks requiring system access should route to Claude"""
        task = Task(
            description="Check server health",
            requires_system_access=True
        )
        result = await platform.route_task(task)
        assert result == "claude"

    @pytest.mark.asyncio
    async def test_route_multi_step_to_hybrid(self, platform):
        """Multi-step tasks should use hybrid workflow"""
        task = Task(
            description="Complex analysis",
            requires_multi_step=True
        )
        result = await platform.route_task(task)
        assert result == "hybrid"

    @pytest.mark.asyncio
    async def test_route_conversation_to_openai(self, platform):
        """Conversational tasks should route to OpenAI"""
        task = Task(
            description="Explain quantum computing",
            type=TaskType.CONVERSATION
        )
        result = await platform.route_task(task)
        assert result == "openai"


class TestGuardrails:
    """Test guardrail functionality"""

    def test_add_guardrail(self, platform):
        """Should be able to add guardrails"""
        guardrail = Guardrail(
            name="test",
            type=GuardrailType.BLOCK,
            condition=lambda task: "bad" in task.description,
            message="Blocked"
        )
        platform.add_guardrail(guardrail)
        assert len(platform.guardrails.guardrails) == 1

    @pytest.mark.asyncio
    async def test_guardrail_blocks_task(self, platform):
        """Guardrail should block matching tasks"""
        platform.add_guardrail(
            Guardrail(
                name="block_destructive",
                type=GuardrailType.BLOCK,
                condition=lambda task: "DROP TABLE" in task.description,
                message="Destructive operation blocked"
            )
        )

        task = Task(description="DROP TABLE users")
        result = await platform.run(task)

        assert result["status"] == "blocked"
        assert "Destructive" in result["message"]


class TestTaskExecution:
    """Test task execution"""

    @pytest.mark.asyncio
    async def test_execute_with_openai(self, platform):
        """Should execute task with OpenAI"""
        task = Task(description="Test task")
        result = await platform.execute_with_openai(task)

        assert result["platform"] == "openai"
        assert result["task_id"] == task.id
        assert task.status.value == "completed"

    @pytest.mark.asyncio
    async def test_execute_with_claude(self, platform):
        """Should execute task with Claude"""
        task = Task(description="Test task", requires_system_access=True)
        result = await platform.execute_with_claude(task)

        assert result["platform"] == "claude"
        assert result["task_id"] == task.id
        assert task.status.value == "completed"

    @pytest.mark.asyncio
    async def test_hybrid_workflow(self, platform):
        """Should execute hybrid workflow with multiple stages"""
        task = Task(
            description="Test hybrid",
            requires_multi_step=True
        )
        result = await platform.execute_hybrid_workflow(task)

        assert result["platform"] == "hybrid"
        assert "stages" in result
        assert "planning" in result["stages"]
        assert "execution" in result["stages"]
        assert "verification" in result["stages"]


class TestTaskHistory:
    """Test task history tracking"""

    @pytest.mark.asyncio
    async def test_task_history_recorded(self, platform):
        """Tasks should be recorded in history"""
        task = Task(description="Test")
        await platform.run(task)

        history = platform.get_task_history()
        assert len(history) == 1
        assert history[0]["description"] == "Test"
