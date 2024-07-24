import re

# Token specification
token_specs = [
    ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9]*'),
    ('NUMBER', r'[0-9]+'),
    ('SYMBOL',
     r'\+|-|\*|/|\(|\)|:=|;|>|<|>=|<=|==|!='),  # Include comparison operators
    ('KEYWORD', r'if|then|else|endif|while|do|endwhile|skip')
]


# Scanner
def tokenize(code):
  tokens = []
  while code:
    for token_type, pattern in token_specs:
      regex = re.compile('^' + pattern)
      match = regex.match(code)
      if match:
        value = match.group(0)
        if token_type != 'WHITESPACE':
          tokens.append((token_type, value))
        code = code[len(value):].lstrip()
        break
    else:
      raise Exception('Invalid character: ' + code[0])
  return tokens


# Parser
class ASTNode:
  pass


class BinaryOp(ASTNode):

  def __init__(self, operator, left, right):
    self.operator = operator
    self.left = left
    self.right = right


class LeafNode(ASTNode):

  def __init__(self, value):
    self.value = value


# Function to parse expressions
def parse_expression(tokens):
  if not tokens:
    raise Exception("Expression parsing error")
  term = parse_term(tokens)
  while tokens and tokens[0][0] == 'SYMBOL' and tokens[0][1] in ('+', '-'):
    operator = tokens.pop(0)[1]
    term2 = parse_term(tokens)
    term = BinaryOp(operator, term, term2)
  return term


# Function to parse terms
def parse_term(tokens):
  if not tokens:
    raise Exception("Term parsing error")
  factor = parse_factor(tokens)
  while tokens and tokens[0][0] == 'SYMBOL' and tokens[0][1] in ('*', '/'):
    operator = tokens.pop(0)[1]
    factor2 = parse_factor(tokens)
    factor = BinaryOp(operator, factor, factor2)
  return factor


# Function to parse factors
def parse_factor(tokens):
  if not tokens:
    raise Exception("Factor parsing error")
  piece = parse_piece(tokens)
  while tokens and tokens[0][0] == 'SYMBOL' and tokens[0][1] in ('+', '-'):
    operator = tokens.pop(0)[1]
    piece2 = parse_piece(tokens)
    piece = BinaryOp(operator, piece, piece2)
  return piece


# Function to parse pieces
def parse_piece(tokens):
  if not tokens:
    raise Exception("Piece parsing error")
  element = parse_element(tokens)
  while tokens and tokens[0][0] == 'SYMBOL' and tokens[0][1] in ('*', '/'):
    operator = tokens.pop(0)[1]
    element2 = parse_element(tokens)
    element = BinaryOp(operator, element, element2)
  return element


# Function to parse elements
def parse_element(tokens):
  if not tokens:
    raise Exception("Element parsing error")
  if tokens[0][0] == 'NUMBER':
    return LeafNode(tokens.pop(0)[1])
  elif tokens[0][0] == 'IDENTIFIER':
    return LeafNode(tokens.pop(0)[1])
  elif tokens[0][0] == 'SYMBOL' and tokens[0][1] == '(':
    tokens.pop(0)  # Consume '('
    expression = parse_expression(tokens)
    if tokens[0][0] == 'SYMBOL' and tokens[0][1] == ')':
      tokens.pop(0)  # Consume ')'
      return expression
  else:
    raise Exception("Invalid element")


# Main function
def main():
  input_expression = "(1 + qq - 2 * 4) + c4 - s * 2 / 4 + 2"
  tokens = tokenize(input_expression)

  # Open an output file for writing the tokens
  with open("test_output.txt", "w") as output_file:
    output_file.write("Tokens:\n")
    for token in tokens:
      output_file.write(f"{token[0]} {token[1]}\n")

  # Parse the input and generate the AST for the expression
  root = parse_expression(tokens)

  # Open an output file for writing the AST
  with open("test_output.txt", "a") as output_file:
    output_file.write("\nAST:\n")
    print_ast(root, output_file)


# Function to print the AST in a hierarchical format
def print_ast(node, output_file, level=0):
  if isinstance(node, BinaryOp):
    output_file.write("  " * level + node.operator + "\n")
    print_ast(node.left, output_file, level + 1)
    print_ast(node.right, output_file, level + 1)
  elif isinstance(node, LeafNode):
    output_file.write("  " * level + node.value + "\n")


# Check if the script is executed as the main program
if __name__ == "__main__":
  main()