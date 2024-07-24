import re

# Define regular expressions for tokens
IDENIFIER = re.compile("^([A-Za-z])([A-Z]|[a-z]|[0-9])*$")
NUMBER = re.compile("^[0-9]+$")
SYMBOL = re.compile("^(\+|\-|\*|\/|\(|\)|\:=)$")
SPECIAL_SYMBOL = re.compile(r"[^\+\-\*\/\(\)\:=\;\+\w]")

# Define your test token
token = "12^2;"

# Combine all patterns into one
combined_pattern = f"({IDENIFIER.pattern})|({NUMBER.pattern}|{SYMBOL.pattern}|{SPECIAL_SYMBOL.pattern})"

print("Combined Pattern:", combined_pattern)

# Initialize an empty list to store tokens
token_list = []

# Initialize indices for substring iteration
i = 0
j = i + 1

# Iterate over the input string
while i < len(token):
    substring = token[i:j]
    print("Substring:", substring)
    
    # Use re.match to check if the substring matches the combined pattern
    match = re.match(combined_pattern, substring)
    print("Match Result:", match)
    
    # Adjust indices based on match
    if match and j < len(token) + 1:
        j += 1
    else:
        # If no match found, process the substring
        substring = token[i:j-1]
        print("Processing Substring:", substring)
        
        # Determine the type of token based on regex patterns
        if bool(NUMBER.search(substring)):
            token_list.append("Number")
        elif bool(IDENIFIER.search(substring)):
            token_list.append("Identifier")
        elif bool(SYMBOL.search(substring)):
            token_list.append("Symbol")
        elif bool(SPECIAL_SYMBOL.search(substring)):
            token_list.append("Special Symbol")
        
        # Move indices to the next substring
        i = j - 1
        j = i + 1

print("Final Token List:", token_list)
