import re

with open('input1.txt', 'r') as input_file: # Read the content of input.txt
    Lines = input_file.readlines() # read file line by line

IDENIFIER = re.compile("^([A-Za-z])([A-Z]|[a-z]|[0-9])*$")
NUMBER = re.compile("^[0-9]+$")
SYMBOL = re.compile("^(\+|\-|\*|\/|\(|\)|\:=)$")
KEYWORD = re.compile("^(if|then|else|endif|while|do|endwhile|skip)$")

NUMBER1 = re.compile("\d+")
IDENIFIER1 = re.compile("[A-Za-z][A-Za-z0-9]*")
SYMBOL1 = re.compile("^\+|\-|\*|\/|\(|\)|\;|\:=")
SPECIAL_SYMBOL = re.compile(r"[^\+\-\*\/\(\)\:=\;\+\w]")
SPECIAL_SYMBOL1 = re.compile(r"^[^\+\-\*\/\(\)\:=\;\+\w]$")

combined_pattern = f"({IDENIFIER.pattern})|({NUMBER.pattern}|{SYMBOL.pattern}|{SPECIAL_SYMBOL})"

for i in range(len(Lines)):
    Lines[i] = Lines[i].split()

def analyze_lines(lines):
    new_dict = {}
    for line in lines:
        if len(line) > 100:
            output_file.write('Token is too big')
            break
        if bool(KEYWORD.search (line)):
            new_dict[line] = "Keyword"
        elif bool(IDENIFIER.search(line)):
            new_dict[line] = "Identifier"
        elif bool(NUMBER.search(line)):
            new_dict[line] = "Number"
        elif bool(SYMBOL.search(line)):
            new_dict[line] = "Symbol"       
        else:
            if bool(SPECIAL_SYMBOL.search(line)):
                i = 0
                j = i + 1
                substring=''
                while i < len(line):
                    subtring = line[i:j]
                    match = re.match(combined_pattern, subtring)
                    match_special= re.match(SPECIAL_SYMBOL1, subtring)
                    if match_special:
                        output_file.write(f'ERROR READING {subtring}')
                        output_file.write('\n')
                        i = i + len(line)
                        j = i
                        break
                    if match and j < len(line) + 1:
                        j += 1
                    else:
                        substring = line[i:j - 1]
                        if bool(NUMBER.search(substring)):
                            new_dict[substring] = "Number"
                        if bool(SYMBOL.search(substring)):
                            new_dict[substring] = "Symbol"
                        if bool(IDENIFIER.search(substring)):
                            new_dict[substring] = "Identifier"
                        i = j -1
                        j = i + 1
            
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
            
    return new_dict


with open('output1.txt', 'w') as output_file:
    for line in Lines:
        output_file.write('Line: ' + ' '.join(line) + '\n')
        new_dict = analyze_lines(line)
        for k, v in new_dict.items():
            output_file.write(f'{k} : {v}\n')
        output_file.write('\n')