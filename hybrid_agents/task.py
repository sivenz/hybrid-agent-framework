"""
Task definitions for hybrid agent framework
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class TaskType(str, Enum):
    """Types of tasks that can be executed"""
    CONVERSATION = "conversation"
    SYSTEM_OPERATION = "system_operation"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CODE_REVIEW = "code_review"
    DEPLOYMENT = "deployment"
    INCIDENT_RESPONSE = "incident_response"


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    ROUTING = "routing"
    IN_PROGRESS = "in_progress"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Unified task representation for hybrid agent platform"""

    description: str
    type: TaskType = TaskType.CONVERSATION
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    requires_system_access: bool = False
    requires_multi_step: bool = False
    context: Optional[Dict[str, Any]] = None
    priority: int = 3
    estimated_cost: float = 0.0
    timeout: int = 300

    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_platform: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}

    def mark_started(self, platform: str):
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.assigned_platform = platform

    def mark_completed(self, result: Dict[str, Any]):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

    def mark_failed(self, error: str):
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error
