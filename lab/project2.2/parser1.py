# Chi Hao Tu and Yaoyao Liu
from scanner import Scanner, Token

class ASTNode:
    def __init__(self, value, type, left=None, right=None):
        self.value = value
        self.type = type
        self.left = left
        self.right = right

class Parser:
    def __init__(self, input_string):
        self.scanner = Scanner(input_string)
        self.tokens = self.scanner.lex()
        self.current_position = 0

    def parse(self):
        return self.statement()

    def statement(self):
        base_statement_node = self.base_statement()

        while self.current_token() is not None and self.current_token().type == "SYMBOL" and self.current_token().value == ";":
            self.consume_token()
            base_statement_node = ["SYMBOL : ;", base_statement_node, self.base_statement()]

        return base_statement_node

    def base_statement(self):
        node = self.current_token()
        if node.type == "IDENTIFIER":
            return self.assignment()
        elif node.type == "KEYWORD" and node.value == "if":
            return self.if_statement()
        elif node.type == "KEYWORD" and node.value == "while":
            return self.while_statement()
        elif node.type == "KEYWORD" and node.value == "skip":
            return self.skip()
        else:
            raise ValueError("Invalid syntax")

    def assignment(self):
        identifier_node = self.identifier()
        if self.current_token().type == "SYMBOL" and self.current_token().value == ":=":
            self.consume_token()
            expression_node = self.expression()
            return ["SYMBOL : :=", identifier_node, expression_node]

        raise ValueError("Invalid syntax")

    def if_statement(self):
        if_node = self.keyword("if")
        expression_node = self.expression()
        then_node = self.keyword("then")
        statement_node = self.statement()
        else_node = self.keyword("else")
        else_statement_node = self.statement()
        endif_node = self.keyword("endif")

        return ["IF-STATEMENT", expression_node,  statement_node,  else_statement_node]

    def while_statement(self):
        while_node = self.keyword("while")
        expression_node = self.expression()
        do_node = self.keyword("do")
        statement_node = self.statement()
        return ["WHILE-LOOP", expression_node, statement_node]

    def skip(self):
        return self.keyword("skip")

    def identifier(self):
        node = self.current_token()
        if node.type == "IDENTIFIER":
            self.consume_token()
            return node
        else:
            raise ValueError("Invalid syntax")

    def keyword(self, value):
        node = self.current_token()
        if node.type == "KEYWORD" and node.value == value:
            self.consume_token()
            return value
        else:
            raise ValueError("Invalid syntax")

    def expression(self):
        term_node = self.term()

        if self.current_token() is not None and self.current_token().type == "SYMBOL":
            if self.current_token().value in ["+", "-"]:
                symbol_node = self.symbol()
                expression_node = self.expression()
                return [symbol_node, term_node, expression_node]

        return term_node

    def term(self):
        factor_node = self.factor()

        if self.current_token() is not None and self.current_token().type == "SYMBOL":
            if self.current_token().value in ["*", "/"]:
                symbol_node = self.symbol()
                term_node = self.term()
                return [symbol_node, factor_node, term_node]

        return factor_node

    def factor(self):
        node = self.current_token()
        if node.type == "NUMBER" or node.type == "IDENTIFIER":
            self.consume_token()
            return node
        elif node.type == "SYMBOL" and node.value == "(":
            self.consume_token()
            expression_node = self.expression()
            if self.current_token().type == "SYMBOL" and self.current_token().value == ")":
                self.consume_token()
                return expression_node

        raise ValueError("Invalid syntax")

    def symbol(self):
        node = self.current_token()
        if node.type == "SYMBOL":
            self.consume_token()
            return node
        else:
            raise ValueError("Invalid syntax")

    def current_token(self):
        if self.current_position < len(self.tokens):
            return self.tokens[self.current_position]

        return None

    def consume_token(self):
        if self.current_position < len(self.tokens):
            self.current_position += 1
        else:
            raise ValueError("Unexpected end of input")


if __name__ == "__main__":
    output_file = open("output.txt", "w")
    with open('testinput.txt', 'r') as file:
        phrases = file.readlines()

    scanner = Scanner(phrases)
    tokens = scanner.lex()
    parser = Parser(phrases)
    ast = parser.parse()
    output_file.write("Tokens:\n")
    for token in tokens:
        output_file.write(f"{token.type} : {token.value}\n")


    def print_ast(node, indent=0):
        if isinstance(node, list):
            for n in node:
                print_ast(n, indent + 4)
        elif isinstance(node, Token):
            output_file.write(" " * indent + f"{node.type} : {node.value}" + "\n")
        else:
            output_file.write(" " * indent + node + "\n")

        return


    output_file.write("AST:\n")
    print_ast(ast)
    output_file.close()