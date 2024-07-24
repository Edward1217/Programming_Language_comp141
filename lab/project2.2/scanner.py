import re

class Token:
    def __init__(self, value, token_type):
        self.value = value
        self.type = token_type

    def __repr__(self):
        return f"{self.value} : {self.type}"

class Scanner:
    def __init__(self, phrases):
        self.phrases = phrases
        self.tokens = []

    def lex(self):
        for phrase in self.phrases:
            current_position = 0
            while current_position < len(phrase):
                matches = ""
                if phrase[current_position].isalpha():
                    identifier = re.match(r"([a-zA-Z])([a-zA-Z0-9]){0,99}", phrase[current_position:])
                    matches += identifier.group()
                    if re.match(r"(if|then|else|endif|while|do|endwhile|skip)", matches):
                        token = Token(matches, "KEYWORD")
                    else:
                        token = Token(matches, "IDENTIFIER")
                    self.tokens.append(token)
                    current_position += len(identifier.group())
                elif phrase[current_position].isdigit():
                    number = re.match(r"[0-9]{1,100}", phrase[current_position:])
                    matches += number.group()
                    token = Token(number.group(), "NUMBER")
                    self.tokens.append(token)
                    current_position += len(number.group())
                elif phrase[current_position].isspace():
                    current_position += 1  # skip whitespace
                else:
                    symbol = re.match(r"\+|\-|\*|/|\(|\)|:=|;", phrase[current_position:])
                    if symbol is None:
                        raise ValueError(f"Invalid syntax at position {current_position} in phrase '{phrase}'")
                    matches += symbol.group()
                    token = Token(symbol.group(), "SYMBOL")
                    self.tokens.append(token)
                    current_position += len(symbol.group())
        return self.tokens
