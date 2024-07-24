import re

TOKEN_TYPES = [
    ('NUMBER', r'\d+(\.\d+)?'),      # Match numbers
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),  # Match identifiers
    ('SYMBOL', r'[\+\-\*\/\(\)]'),    # Match symbols
    ('WHITESPACE', r'\s+'),            # Match whitespace
    ('ERROR', r'.')                    # Match any other character (error)
]

class Scanner:
    def __init__(self, input_string):
        self.input_string = input_string
        self.tokens = []

    def scan(self):
        while self.input_string:
            matched = False
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile('^' + pattern)
                match = regex.match(self.input_string)
                if match:
                    if token_type != 'WHITESPACE':
                        self.tokens.append((token_type, match.group()))
                    self.input_string = self.input_string[match.end():]
                    matched = True
                    break
            if not matched:
                self.tokens.append(('ERROR', self.input_string[0]))
                self.input_string = self.input_string[1:]

    def get_tokens(self):
        return self.tokens

