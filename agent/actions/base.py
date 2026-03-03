from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    LLM = "llm"
    TOOL = "tool"
    NOOP = "noop"


class Observation(BaseModel):
    success: bool
    data: Dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    tokens_used: int = 0
    cost: float = 0.0


class BaseAction(BaseModel, ABC):
    action_type: ActionType
    name: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @abstractmethod
    def execute(self) -> Observation:
        raise NotImplementedError
