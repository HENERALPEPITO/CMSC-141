class ENFA:
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

    def add_epsilon_transition(self, from_state, to_state):
        self.transitions.setdefault((from_state, None), set()).add(to_state)

    def set_start_state(self, state):
        self.start_state = state

    def is_accept_state(self, state):
        return state in self.accept_states

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current_state = stack.pop()
            epsilon_transitions = self.transitions.get((current_state, None), set())
            for state in epsilon_transitions:
                if state not in closure:
                    closure.add(state)
                    stack.append(state)

        return closure

    def simulate(self, input_string):
        current_states = self.epsilon_closure([self.start_state])

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                transitions = self.transitions.get((state, symbol), set())
                next_states = next_states.union(transitions)

            current_states = self.epsilon_closure(next_states)

        for state in current_states:
            if self.is_accept_state(state):
                return True
        return False

#TESTING CENTER
enfa = ENFA()

# Add states
enfa.add_state("q0")
enfa.add_state("q1")
enfa.add_state("q2")
enfa.add_state("q3")
enfa.add_state("q4", accept_state=True)

# Add transitions
enfa.add_transition("q0", '0', "q1")
enfa.add_epsilon_transition("q0", "q2")
enfa.add_transition("q1", '1', "q2")
enfa.add_transition("q2", '1', "q3")
enfa.add_transition("q2","1", "q4")
enfa.add_transition("q3","1", "q4")
enfa.add_transition("q3", '0', "q2")

# Set start state
enfa.set_start_state("q0")


# Test strings
test_strings = ["01"]

for test_string in test_strings:
    if enfa.simulate(test_string):
        print(f"String '{test_string}' is TUMPAK GANERN.")
    else:
        print(f"String '{test_string}' is INDI ABOTS.")
