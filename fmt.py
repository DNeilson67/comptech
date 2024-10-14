import re

# Define the automaton class
class FMTAutomaton:
    def __init__(self):
        self.state = 'S0'
    
    def reset(self):
        self.state = 'S0'
    
    def process(self, token):
        if self.state == 'S0' and token == '%':
            self.state = 'S1'
        elif self.state == 'S1' and re.match(r'^\d+$', token):
            self.state = 'S1'  # Stay in S1 for digits
        elif self.state == 'S1' and token in ('d', 'c', 'f', 's'):
            self.state = 'S2'  # Transition to final state
        else:
            self.state = 'ERROR'
    
    def is_accepting(self):
        return self.state == 'S2'

# Lexical function to split the input
def tokenize(fmt_string):
    # This regex handles the "number" part based on the provided rule (number -> digit digit* | digit* (.digit | digit .) digit*)
    number_pattern = r'(\d+|\d*\.\d+|\.\d+)'
    tokens = re.findall(r'%|\d+|d|c|f|s', fmt_string)
    return tokens

# Function to test the automaton
def test_fmt_automaton(fmt_string):
    automaton = FMTAutomaton()
    tokens = tokenize(fmt_string)
    
    for token in tokens:
        automaton.process(token)
        if automaton.state == 'ERROR':
            return False  # Reject if any invalid transition happens
    
    return automaton.is_accepting()

# Testing the automaton
test_strings = [
    "%d",      
    "%10d",    
    "%f",      
    "%10.2f", 
    "%cs",     
    "%d123",  
    "10%s"    
]

for test_str in test_strings:
    result = test_fmt_automaton(test_str)
    print(f"Test '{test_str}': {'Accepted' if result else 'Rejected'}")
