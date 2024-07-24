import re

with open('input.txt', 'r') as input_file: # Read the content of input.txt
    Lines = input_file.readlines() # read file line by line

IDENIFIER = re.compile("^([A-Za-z_])([A-Z]|[a-z]|[0-9])*$")
NUMBER = re.compile("^[0-9]+$")
SYMBOL = re.compile("^\+|\-|\*|\/|\(|\)$")

NUMBER1 = re.compile("^\d+")
IDENIFIER1 = re.compile(r"([A-Za-z][A-Za-z0-9]*)")
SYMBOL1 = re.compile(r"\+|\-|\*|\/|\(|\)$")
SPECIAL_SYMBOL = re.compile(r"(?![\+\-\*\/\(\)\d])[^\s]+")

for i in range(len(Lines)):
    Lines[i] = Lines[i].split()

def analyze_lines(lines):
    output_file.write(f"Line: {' '.join(lines)}\n")
    new_list = []
    for line in lines:
        if bool(IDENIFIER.search(line)):
            new_list.append(("Identifier",line))
        elif bool(NUMBER.search(line)):
            new_list.append(("Number",line))
        elif bool(SYMBOL.search(line)):
            new_list.append(("Symbol",line))
        else:
            if NUMBER1.match(line):   
                match = NUMBER1.match(line)
                new_list.append(("Number",match.group()))
                line = line[match.end():]           
            if IDENIFIER1.match(line):
                match = IDENIFIER1.match(line)
                new_list.append(("Identifier",match.group()))
                line = line[match.end():]
            
            if SYMBOL1.match(line):
                match = SYMBOL1.match(line)
                new_list.append(("Symbol",match.group()))
            if SPECIAL_SYMBOL.match(line):
                match = SPECIAL_SYMBOL.match(line)
                output_file.write(f'ERROR READING {match.group()}\n')
                break

    return new_list


with open('output.txt', 'w') as output_file:
    for line in Lines:
        output_file.write('Line: ' + ' '.join(line) + '\n')
        new_list = analyze_lines(line)
        for k, v in new_list:
            output_file.write(f'{k} : {v}\n')