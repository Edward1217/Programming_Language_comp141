from scanner import Scanner
from parser1 import Parser

def main():
    input_file = 'test_input.txt'
    output_file = 'test_output.txt'

    try:
        with open(input_file, 'r') as f:
            expression = f.readline().strip()

        # Scanner
        scanner = Scanner(expression)
        scanner.scan()
        tokens = scanner.get_tokens()

        # Write tokens to output file
        with open(output_file, 'w') as f:
            f.write('Tokens:\n')
            for token in tokens:
                f.write('{} : {}\n'.format(token[0], token[1]))

        # Parser
        parser = Parser(tokens)
        ast = parser.parse_expression()

        # Write AST to output file
        with open(output_file, 'a') as f:
            f.write('AST:\n')
            _print_ast(ast, f, 0)

    except Exception as e:
        # Error handling
        with open(output_file, 'w') as f:
            f.write('Error: {}\n'.format(str(e)))

def _print_ast(ast, f, indent):
    if isinstance(ast, tuple):
        f.write('{}{} : {}\n'.format(' ' * indent, ast[0], 'SYMBOL'))
        _print_ast(ast[1], f, indent + 8)
        _print_ast(ast[2], f, indent + 8)
    else:
        f.write('{}{} : {}\n'.format(' ' * indent, ast, 'NUMBER' if ast.isdigit() else 'IDENTIFIER'))

if __name__ == '__main__':
    main()
