import re

with open('input.txt', 'r') as input_file: # Read the content of input.txt
    Lines = input_file.readlines() # read file line by line

IDENIFIER = re.compile("^([A-Za-z])([A-Z]|[a-z]|[0-9])*$")
NUMBER = re.compile("^[0-9]+$")
SYMBOL = re.compile("^\+|\-|\*|\/|\(|\)$")

NUMBER1 = re.compile("^\d+")
IDENIFIER1 = re.compile(r"([A-Za-z][A-Za-z0-9]*)")
SYMBOL1 = re.compile(r"\+|\-|\*|\/|\(|\)$")
SPECIAL_SYMBOL = re.compile(r"(?![\+\-\*\/\(\)\d])[^\s]+")

for i in range(len(Lines)):
    Lines[i] = Lines[i].split()

def analyze_lines(lines):
    new_dict = {}
    for line in lines:
        
        if bool(IDENIFIER.search(line)):
            new_dict[line] = "Identifier"
        elif bool(NUMBER.search(line)):
            new_dict[line] = "Number"
        elif bool(SYMBOL.search(line)):
            new_dict[line] = "Symbol"
        else:
            if bool(IDENIFIER1.findall(line)):
                x = IDENIFIER1.findall(line)
                for i in x:
                    new_dict[i] = 'Identifier'           
            if bool(NUMBER1.findall(line)):   
                y = NUMBER1.findall(line)
                for i in y:
                    new_dict[i] = 'Number'
            if bool(SYMBOL1.findall(line)):
                z = SYMBOL1.findall(line)
                for i in z:
                    new_dict[i] = 'Symbol'
            if SPECIAL_SYMBOL.findall(line):
                w = SPECIAL_SYMBOL.findall(line)
                for i in w:
                    new_dict[i] ='Error'
    return new_dict


with open('output.txt', 'w') as output_file:
    for line in Lines:
        output_file.write('Line: ' + ' '.join(line) + '\n')
        new_dict = analyze_lines(line)
        for k, v in new_dict.items():
            output_file.write(f'{k} : {v}\n')