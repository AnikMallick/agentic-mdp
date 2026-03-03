from typing import Callable, Dict, Any
from agent.actions.base import BaseAction, ActionType, Observation


class ToolAction(BaseAction):
    tool_name: str
    tool_fn: Callable[..., Any]
    tool_args: Dict[str, Any] = {}

    def __init__(self, **data):
        super().__init__(
            action_type=ActionType.TOOL,
            name="tool_action",
            **data
        )

    def execute(self) -> Observation:
        try:
            result = self.tool_fn(**self.tool_args)
            return Observation(
                success=True,
                data={"result": result}
            )
        except Exception as e:
            return Observation(
                success=False,
                error=str(e)
            )
