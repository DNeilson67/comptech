from anytree import Node, RenderTree

# Global variables to hold grammar and stack
grammar = {}
stack = []
parse_tree_root = None  # Root node for parse tree

# Reads the grammar.txt file
def load_grammar(filename):
    global grammar
    with open(filename, 'r') as file:
        for line in file:
            non_terminal, production = line.strip().split("->")
            grammar[non_terminal.strip()] = [p.strip() for p in production.split('|')]

# Parsing method
def parse(input_string):
    global parse_tree_root, stack

    # Treat 'ε' input as an empty string
    if input_string == 'ε':
        input_string = ''

    parse_tree_root = Node("A")  # Root node for A (start symbol)
    stack = [(parse_tree_root, 'A')]  # Stack holds tuples of (node, grammar symbol)
    index = 0

    while stack:
        current_node, top = stack.pop()
        
        if top == 'ε':
            Node("ε", parent=current_node) 
            continue
        
        elif top == 'A':
            # Match "0 B 1" or "C" production for A
            if index < len(input_string) and input_string[index] == '0':
                node_0 = Node("0", parent=current_node)
                node_B = Node("B", parent=current_node)
                node_1 = Node("1", parent=current_node)
                stack.append((node_1, '1'))
                stack.append((node_B, 'B'))
                stack.append((node_0, '0'))
            elif index < len(input_string) and input_string[index] == '#':
                # Match "C" production for A
                node_C = Node("C", parent=current_node)
                stack.append((node_C, 'C'))
            else:
                print("Parse Error: Unmatched symbol at A", index)
                return False

        elif top == 'B':
            # Match "+" or "ε" production for B
            if index < len(input_string) and input_string[index] == '+':
                node_plus = Node("+", parent=current_node)
                stack.append((node_plus, '+'))
            elif index >= len(input_string) or input_string[index] not in ('+', '1', '0', '#'):
                # ε production for B (empty production)
                Node("ε", parent=current_node)

        elif top == 'C':
            # Match "#" production for C
            if index < len(input_string) and input_string[index] == '#':
                node_hash = Node("#", parent=current_node)
                stack.append((node_hash, '#'))

        elif index < len(input_string) and input_string[index] == top:
            index += 1  # Advance input pointer when top matches with input
        else:
            print("Parse Error: Unmatched symbol at", index)
            return False

    if index == len(input_string):
        print("Parse Successful")
        return True
    else:
        print("Parse Error: Remaining unparsed input")
        return False

# Display parse tree if input is valid
def display_parse_tree():
    print("Parse Tree:")
    # Color the resulted string
    def colorize(node_name):
        if node_name in {'0', '1', 'ε', '#', '+'}:
            return f"{node_name}"
        return node_name

    for pre, fill, node in RenderTree(parse_tree_root):
        print(f"{pre}{colorize(node.name)}")


# Main execution
if __name__ == "__main__":
    print("THIS IS A SIMPLE LL(1) PARSER")
    
    # Input for grammar file (the file needs to be created and saved with the grammar in the format: A -> 0 B 1 | C)
    grammar_file = input("Please, input the grammar file: ")

    load_grammar(grammar_file)
    print("Loaded grammar:", grammar)
    
    # Input for string
    input_string = input("Please, input the string: ")

    if parse(input_string):
        display_parse_tree()
    else:
        print("Error in parsing the input string.")
