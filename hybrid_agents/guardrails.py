"""
Guardrails for hybrid agent framework
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any, Optional


class GuardrailType(str, Enum):
    """Types of guardrails"""
    VALIDATION = "validation"
    BLOCK = "block"
    APPROVAL_REQUIRED = "approval_required"
    RATE_LIMIT = "rate_limit"
    COST_LIMIT = "cost_limit"


@dataclass
class Guardrail:
    """
    Guardrail definition

    Attributes:
        name: Unique guardrail name
        type: Type of guardrail
        condition: Function that evaluates if guardrail applies
        message: Message to display when guardrail triggers
        approver: Optional approver identifier (email, slack channel, etc.)
    """
    name: str
    type: GuardrailType
    condition: Callable[[Any], bool]
    message: str
    approver: Optional[str] = None

    def evaluate(self, task) -> bool:
        """Evaluate if this guardrail should trigger"""
        return self.condition(task)


class GuardrailEngine:
    """Engine for evaluating guardrails"""

    def __init__(self):
        self.guardrails = []

    def add_guardrail(self, guardrail: Guardrail):
        """Add a guardrail"""
        self.guardrails.append(guardrail)

    def check(self, task) -> tuple[bool, Optional[str], Optional[Guardrail]]:
        """
        Check all guardrails for a task

        Returns:
            (can_proceed, message, triggered_guardrail)
        """
        for guardrail in self.guardrails:
            if guardrail.evaluate(task):
                if guardrail.type == GuardrailType.BLOCK:
                    return False, guardrail.message, guardrail
                elif guardrail.type == GuardrailType.APPROVAL_REQUIRED:
                    return False, f"{guardrail.message} (Approval required from {guardrail.approver})", guardrail

        return True, None, None
