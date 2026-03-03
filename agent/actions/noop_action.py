from agent.actions.base import Action, ActionType, Observation


class NoOpAction(Action):
    def __init__(self):
        super().__init__(
            action_type=ActionType.NOOP,
            name="noop"
        )

    def execute(self) -> Observation:
        return Observation(success=True)
