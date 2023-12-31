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

    def simulate(self, input_string):
        current_states = {self.start_state}

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                transitions = self.transitions.get((state, symbol), set())
                next_states = next_states.union(transitions)
            current_states = next_states

        for state in current_states:
            if self.is_accept_state(state):
                return True
        return False


# TESTING CENTER
nfa = NFA()

# Add states
nfa.add_state("q0", accept_state=True)
nfa.add_state("q1")
nfa.add_state("q2", accept_state=True)

# Add transitions
nfa.add_transition("q0", 'a', "q1")
nfa.add_transition("q1", 'b', "q2")
nfa.add_transition("q2", 'a', "q0")

# Set start state
nfa.set_start_state("q0")

# Test strings
test_strings = ["ab", "aba", "abab", "aaab"]

for test_string in test_strings:
    if nfa.simulate(test_string):
        print(f"String '{test_string}' is accepted")
    else:
        print(f"String '{test_string}' is rejected.")
