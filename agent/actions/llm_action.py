from typing import Optional, Dict, Any

from agent.actions.base import BaseAction, ActionType, Observation

class LLMAction(BaseAction):
    prompt: str # user prompt
    system_prompt: Optional[str] = None
    model: str = "default" # name of the model
    
    def __init__(self, **data) -> None:
       super().__init__(
           action_type=ActionType.LLM,
           name="llm_action",
           **data
       )
       
    def execute(self) -> Observation:
        raise RuntimeError(
            "LLMAction.execute() should be handled by an LLM executor adapter"
        )
