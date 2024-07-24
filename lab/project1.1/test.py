import re
import sys

# Define regular expressions for tokens
IDENTIFIER_REGEX = r'[a-zA-Z]([a-zA-Z0-9])*'
NUMBER_REGEX = r'[0-9]+'
SYMBOL_REGEX = r'\+|\-|\*|\/|\(|\)'

# Compile regular expressions for efficiency
identifier_pattern = re.compile(IDENTIFIER_REGEX)
number_pattern = re.compile(NUMBER_REGEX)
symbol_pattern = re.compile(SYMBOL_REGEX)

def scan_line(line):
    tokens = []

    # Scan the line for tokens
    while line:
        # Remove leading whitespace
        line = line.lstrip()

        # Check for identifier
        match = identifier_pattern.match(line)
        if match:
            token = match.group(0)
            tokens.append(('IDENTIFIER', token))
            line = line[len(token):]
            continue

        # Check for number
        match = number_pattern.match(line)
        if match:
            token = match.group(0)
            tokens.append(('NUMBER', token))
            line = line[len(token):]
            continue

        # Check for symbol
        match = symbol_pattern.match(line)
        if match:
            token = match.group(0)
            tokens.append(('SYMBOL', token))
            line = line[len(token):]
            continue

        # If none of the patterns match, report error and break
        if line[0].isspace():
            line = line.lstrip()
            continue
        else:
            print("ERROR READING LINE:", line)
            break

    return tokens

def main(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                line = line.strip()
                print("Line:", line, file=outfile)
                tokens = scan_line(line)
                for token_type, token_value in tokens:
                    print(f"{token_value} : {token_type}", file=outfile)
                print("", file=outfile)  # Empty line between lines in output
    except FileNotFoundError:
        print("Error: Input file not found.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scanner.py input_file output_file")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)
