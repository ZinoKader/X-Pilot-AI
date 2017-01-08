class StateHandler:

    states = ["ready", "attacking", "pathfinding"]
    state = None

    def __init__(self, initstate = "ready"):
        self.set_current_state(initstate)

    def set_current_state(self, state):
        self.state = state

    def get_current_state(self):
        return self.state

    def get_all_states(self):
        return self.states

    def is_ready(self):
        return self.state == "ready"

    def is_attacking(self):
        return self.state == "attacking"

    def is_pathfinding(self):
        return self.state == "pathfinding"
