"""
Agent definitions for hybrid agent framework
"""

from enum import Enum
from typing import Optional, Dict, Any


class AgentType(str, Enum):
    """Agent platform types"""
    OPENAI = "openai"
    CLAUDE = "claude"


class AgentRole(str, Enum):
    """Agent role specializations"""
    COORDINATOR = "coordinator"
    ANALYST = "analyst"
    EXECUTOR = "executor"
    VERIFIER = "verifier"
    COMMUNICATOR = "communicator"
    RESEARCHER = "researcher"


class AgentCapability:
    """Define what each agent type can do"""

    OPENAI_STRENGTHS = {
        "conversation", "planning", "orchestration",
        "data_analysis", "multi_agent_coordination",
        "reasoning", "synthesis"
    }

    CLAUDE_STRENGTHS = {
        "system_operations", "bash_execution", "code_generation",
        "deep_research", "file_manipulation", "verification",
        "mcp_integration"
    }

    @classmethod
    def get_best_platform(cls, requirements: set) -> AgentType:
        """Determine best platform based on requirements"""
        openai_match = len(requirements & cls.OPENAI_STRENGTHS)
        claude_match = len(requirements & cls.CLAUDE_STRENGTHS)

        return AgentType.CLAUDE if claude_match > openai_match else AgentType.OPENAI


class Agent:
    """Base agent class"""

    def __init__(self, name: str, role: AgentRole, agent_type: AgentType, instructions: str):
        self.name = name
        self.role = role
        self.agent_type = agent_type
        self.instructions = instructions
        self.context = {}

    def handoff(self, to: str, context: Optional[Dict[str, Any]] = None):
        """Hand off to another agent"""
        return {
            "action": "handoff",
            "from": self.name,
            "to": to,
            "context": context or {}
        }
