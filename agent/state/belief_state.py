from typing import Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field, NonNegativeFloat, NonNegativeInt

# -----------------------------
# Task & lifecycle definitions
# -----------------------------

class TaskStage(str, Enum):
    INIT = "init"
    PLAN = "plan"
    EXECUTE = "execute"
    VERIFY = "verify"
    FINALIZE = "finalize"

class TerminationReason(str, Enum):
    SUCCESS = "success"
    BUDGET_EXHAUSTED = "budget_exhausted"
    MAX_STEPS_REACHED = "max_steps_reached"
    POLICY_STOP = "policy_stop"
    FAILURE = "failure"

class FailureType(str, Enum):
    TIMEOUT = "timeout"
    INTERNAL_ERROR = "internal_error"
    INVALID_OUTPUT = "invalid_output"

class Task(BaseModel):
    task_id: str = Field(..., description="Holds name or id of the task.")
    current_stage: TaskStage = Field(TaskStage.INIT, description="Current stage of the task.")
    is_complete: bool = Field(False, description="Is the task complete.")


# -----------------------------
# Belief State
# -----------------------------


class State(BaseModel):
    # Task context
    current_task: Task = Field(..., description="Currently running task.")
    memory: str = Field("", description="Memory of past messages. Rolling summary.")
    
    # belief and uncertainty
    current_confidence: NonNegativeFloat = Field(1.0, le=1.0, 
                                                 description="Confidence score of the current belief. Range: 0.0 to 1.0")
    current_uncertainty: NonNegativeFloat = Field(0.0, le=1.0, 
                                                  description="Uncertainty score of the current belief. Range: 0.0 to 1.0")
    
    # Resource 
    total_budget: NonNegativeFloat = Field(1.0, description="Total budget of the current process.")
    budget_remaining: NonNegativeFloat = Field(1.0, description="Remaining budget of the current process.")
    token_used: int = Field(0, ge=0, 
                            description="Total tokens used in the current process.")
    
    # execution tracking
    retry_count: int = Field(0, ge=0, description="Total no of retries used in the current process.")
    step_count: int  = Field(0, ge=0, description="Total steps taken in the process.")
    max_steps: int  = Field(..., gt=0, description="Max allowed steps.")
    
    # Outcome tracking
    last_action_outcome: Optional[Literal["failed", "success", "partial"]]  = Field("success", 
                                                                                    description="Last action outcome. True is success.")
    failure_type: Optional[FailureType] = Field(None, description="Failure type.")
    termination_reason: Optional[TerminationReason] = Field(None, description="Termination reason.")
    
    # Episode
    is_terminal: bool = Field(False, description="Whether the episode has terminated")
    