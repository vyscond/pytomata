__version__ = '2.0.0'

from yaml import load as yload
from yaml import dump as ydump


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

CONSUMER = '*'
PRODUCE = '='

WHITE_SPACES = {
    '\t': '\\t',
    '\n': '\\n',
    '\r': '\\r',
    '\f': '\\f',
    '\v': '\\v'
}

class State(object):

    def __init__(self, name, istate=False, fstate=False, transitions=None):
        self.name = name
        self.istate = istate
        self.fstate = fstate
        self.transitions = transitions or {}

    def next(self, token):
        try:
            return self.transitions[token]
        except KeyError:
            return None

    def __mul__(self, token):
        return self.next(token)

    def __str__(self):
        return self.name


class Automata(object):

    def __init__(self, config):
        ''' config: can be a .yml or .dfa file '''
        self.config = yload(open(config), Loader=Loader)
        # - Setup the Automata
        self._load_tree()

    def __str__(self):
        return ydump(self.config, Dumper=Dumper)

    def _load_tree(self):
        self.states = {}
        # Setup possible states
        for state in self.config['states']:
            self.states[state] = State(state)
        # Binding/update the possible transistions
        # c_state = current_state
        # n_state = next_state
        for transition in self.config['transitions']:
            # print('[transition] {}'.format(transition))
            c_state, token, n_state = self._split_transition(transition)
            print('[transition] {} * {} -> {}'.format(c_state, token, n_state))
            self.states[c_state].transitions[token] = self.states[n_state]
        # Root/Initial state
        self.root_state = self.states[self.config['initial_state']]
        self.root_state.istate = True
        # Tagging last states
        for state in self.config['final_states']:
            self.states[state].fstate = True

    def _split_transition(self, transition):
        current_state, transition = transition.split(CONSUMER)
        token, next_state = transition.split(PRODUCE)

        current_state = current_state.strip()
        # if the consumer token is wrapped with single quote
        # token = token.replace("'","")
        token = token.strip()
        next_state = next_state.strip()

        return (current_state, token, next_state)

    def validate(self, entry, filepath=False, replacements=()):
        # c_state = current_state
        # n_state = next_state
        if filepath:
            entry = open(entry).read()
        for replacement in replacements:
            entry = entry.replace(replacement[0], replacement[1])
        print('[validating]\n# - BGN ---\n{}\n# - END ---'.format(entry))
        c_state = self.root_state
        for char in entry:
            if char in WHITE_SPACES.keys():
                char = WHITE_SPACES[char]
            n_state = c_state.next(char)
            print('({}) * ({}) -> ({})'.format(c_state, char, n_state))
            if n_state:
                c_state = n_state
            else:
                break

        return c_state.fstate
