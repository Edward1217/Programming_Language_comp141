class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse_expression(self):
        ast = self.parse_term()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] in ('+', '-'):
            operator = self.tokens[self.current_token_index][1]
            self.current_token_index += 1
            right = self.parse_term()
            ast = (operator, ast, right)
        return ast

    def parse_term(self):
        ast = self.parse_factor()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] in ('*', '/'):
            operator = self.tokens[self.current_token_index][1]
            self.current_token_index += 1
            right = self.parse_factor()
            ast = (operator, ast, right)
        return ast

    def parse_factor(self):
        token = self.tokens[self.current_token_index]
        if token[0] == 'NUMBER' or token[0] == 'IDENTIFIER':
            self.current_token_index += 1
            return token[1]
        elif token[1] == '(':
            self.current_token_index += 1
            ast = self.parse_expression()
            if self.tokens[self.current_token_index][1] == ')':
                self.current_token_index += 1
                return ast
            else:
                raise ValueError('Expected closing parenthesis')
        else:
            raise ValueError('Invalid token: {}'.format(token[1]))
