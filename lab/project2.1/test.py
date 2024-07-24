import re

# TOKEN_TYPES = [
#     ('NUMBER', r'\d+(\.\d+)?'),      # Match numbers
#     ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # Match identifiers
#     ('SYMBOL', r'[\+\-\*\/\(\)]'),    # Match symbols
#     ('WHITESPACE', r'\s+'),            # Match whitespace
#     ('ERROR', r'.')                    # Match any other character (error)
# ]

NUMBER =  r'^\d+(\.\d+)?'
string = "3*(5+2/x-1)"
regex = re.compile(NUMBER)
match = regex.match(string)

print(match.end())
