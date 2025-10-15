"""
Hybrid Agent Framework - OpenAI + Claude Power Duo
Combine OpenAI's orchestration with Claude's system execution
"""

from .platform import HybridPlatform
from .task import Task, TaskType
from .guardrails import Guardrail, GuardrailType
from .agents import AgentType, AgentRole

__version__ = "0.1.0"

__all__ = [
    "HybridPlatform",
    "Task",
    "TaskType",
    "Guardrail",
    "GuardrailType",
    "AgentType",
    "AgentRole",
]
