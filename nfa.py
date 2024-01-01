class State:
    def __init__(self, name):
        self.name = name

class NFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def add_state(self, state, accept_state=False):
        self.states.add(state)
        if accept_state:
            self.accept_states.add(state)

    def add_transition(self, from_state, symbol, to_state):
        self.transitions.setdefault((from_state, symbol), set()).add(to_state)

    def set_start_state(self, state):
        self.start_state = state

    def is_accept_state(self, state):
        return state in self.accept_states

    def delta(self, current_state, symbol):
        return self.transitions.get((current_state, symbol), set())

    def simulate(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            current_state = self.delta(current_state, symbol)
            if not current_state:
                return False

        return self.is_accept_state(current_state)


