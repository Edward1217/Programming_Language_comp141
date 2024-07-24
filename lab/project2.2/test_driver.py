from scanner import scan
from parser1 import generate_ast

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            try:
                tokens = scan(line)
                f.write("Tokens:\n")
                for token in tokens:
                    f.write(f"{token[0]} {token[1]}\n")

                ast = generate_ast(line)
                f.write("AST:\n")
                print_ast(ast, f, 0)

            except ValueError as e:
                f.write(f"Error: {str(e)}\n")
                f.write(f"Input line: {line}\n")
                break

def print_ast(node, f, indent):
    f.write(" " * indent + str(node) + "\n")
    for child in node.children:
        print_ast(child, f, indent + 4)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python test_driver.py input_file output_file")
    else:
        main(sys.argv[1], sys.argv[2])
