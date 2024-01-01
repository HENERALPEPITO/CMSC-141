from nfa import NFA, State  


class ENFA(NFA):
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

    def epsilon_closure(self, state):
        closure = set()
        stack = [state]

        while stack:
            current_state = stack.pop()
            epsilon_transitions = self.transitions.get((current_state, None), set())
            closure.add(current_state)

            for epsilon_state in epsilon_transitions:
                if epsilon_state not in closure:
                    stack.append(epsilon_state)
                    closure.add(epsilon_state)  

        return list(closure)

    def delta(self, current_states, symbol):
        next_states = set()

        for state in current_states:
            epsilon_states = self.epsilon_closure(state)
            transitions = self.transitions.get((state, symbol), set())

            for epsilon_state in epsilon_states:
                transitions |= self.transitions.get((epsilon_state, symbol), set())

            next_states |= transitions

        return list(next_states)

    def simulate(self, input_string):
        current_states = self.epsilon_closure(self.start_state)

        for symbol in input_string:
            next_states = self.delta(current_states, symbol)
            current_states = next_states

        return any(self.is_accept_state(state) for state in current_states)


# TESTING CENTER
enfa = ENFA()

# Add states
enfa.add_state(State("q0"))
enfa.add_state(State("q1"))
enfa.add_state(State("q2"))
enfa.add_state(State("q3"))
enfa.add_state(State("q4"), accept_state=True)

# Add transitions
enfa.add_transition(State("q0"), '0', State("q1"))
enfa.add_epsilon_transition(State("q0"), State("q2"))
enfa.add_transition(State("q1"), '1', State("q2"))
enfa.add_transition(State("q2"), '1', State("q3"))
enfa.add_transition(State("q2"), '1', State("q4"))
enfa.add_transition(State("q3"), '1', State("q4"))
enfa.add_transition(State("q3"), '0', State("q2"))

# Set start state
enfa.set_start_state(State("q0"))

# Test strings
test_strings = ["1101"]

for test_string in test_strings:
    if enfa.simulate(test_string):
        print(f"String '{test_string}' is accepted.")
    else:
        print(f"String '{test_string}' is rejected.")
