import re
import os.path

# Regular expressions
identifier = re.compile(r'([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*')
number = re.compile(r'[0-9]+')
symbol = re.compile(r'(\+|\-|\*|/|\(|\)|:=|;)')
keyword = re.compile(r'(if|then|else|endif|while|do|endwhile|skip)')

class Token:
    def __init__(self, tokenStr, tokenType):
        self.tokenStr = tokenStr
        self.tokenType = tokenType

    def getToken(self):
        return self.tokenStr

    def getTokenType(self):
        return self.tokenType

class Stack:
    def __init__(self):
        self.data = []

    def push(self, elem):
        self.data.append(elem)

    def pop(self):
        elem = self.data[-1]
        self.data.pop()
        return elem

    def length(self):
        return len(self.data)

def scan(inFile, outFile):
    strings = None
    tokens = []

    for line in inFile:
        outFile.write("LINE : " + line)
        strings = re.split("\s", line)
        for i in strings:
            while i != "":
                if re.fullmatch(keyword, i):
                    outFile.write("KEYWORD : " + i + "\n")
                    token = Token(i, "KEYWORD")
                    tokens.append(token)
                    i = ""
                elif re.fullmatch(identifier, i):
                    outFile.write("IDENTIFIER : " + i + "\n")
                    token = Token(i, "IDENTIFIER")
                    tokens.append(token)
                    i = ""
                elif re.fullmatch(":=", i):
                    outFile.write("SYMBOL : " + i + "\n")
                    token = Token(i, "SYMBOL")
                    tokens.append(token)
                    i = ""
                elif re.fullmatch(symbol, i):
                    outFile.write("SYMBOL : " + i + "\n")
                    token = Token(i, "SYMBOL")
                    tokens.append(token)
                    i = ""
                elif re.fullmatch(number, i):
                    outFile.write("NUMBER : " + i + "\n")
                    token = Token(i, "NUMBER")
                    tokens.append(token)
                    i = ""
                else:
                    partNum = re.match(number, i)
                    partID = re.match(identifier, i)
                    partSym = re.match(":=", i)
                    if partSym is None:
                        partSym = re.match(symbol, i)
                    if partNum is not None:
                        start = min(partNum.span())
                        end = max(partNum.span())
                        partToken = i[start:end]
                        token = Token(partToken, "NUMBER")
                        tokens.append(token)
                        outFile.write("NUMBER : " + partToken + "\n")
                        token = i[end:len(i)]
                        i = token
                    elif partID is not None:
                        start = min(partID.span())
                        end = max(partID.span())
                        partToken = i[start:end]
                        if partToken in ["if", "then", "else", "endif", "while", "do", "endwhile", "skip"]:
                            token = Token(partToken, "KEYWORD")
                            tokens.append(token)
                            outFile.write("KEYWORD : " + partToken + "\n")
                        else:
                            token = Token(partToken, "IDENTIFIER")
                            tokens.append(token)
                            outFile.write("IDENTIFIER : " + partToken + "\n")
                        token = i[end:len(i)]
                        i = token
                    elif partSym is not None:
                        start = min(partSym.span())
                        end = max(partSym.span())
                        partToken = i[start:end]
                        token = Token(partToken, "SYMBOL")
                        tokens.append(token)
                        outFile.write("SYMBOL : " + partToken + "\n")
                        token = i[end:len(i)]
                        i = token
                    else:
                        if i != "":
                            token = Token(i, "ERROR")
                            tokens.append(token)
                            outFile.write("ERROR ON TOKEN : " + i + "\n\n")
                            return tokens
        outFile.write("\n")
    return tokens

class Tree:
    def __init__(self, left, middle, right, data):
        self.left = left
        self.middle = middle
        self.right = right
        self.data = data
        self.stackError = False

    def treeTraversal(self, node, outFile, indent, stack):
        if node is None:
            return None
        token = node.data
        if re.fullmatch(keyword, token):
            type = "KEYWORD"
        elif re.fullmatch(identifier, token):
            type = "IDENTIFIER"
        elif re.fullmatch(number, token):
            type = "NUMBER"
        elif re.fullmatch(symbol, token):
            type = "SYMBOL"
        outFile.write(indent + token + " : " + type + "\n")

        indent += "  "
        stack.push(token)

        while stack.length() >= 3:
            elem1 = stack.pop()
            if re.fullmatch(number, elem1):
                elem2 = stack.pop()
                if re.fullmatch(number, elem2):
                    elem3 = stack.pop()
                    if re.fullmatch(symbol, elem3):
                        elem2 = int(elem2)
                        elem1 = int(elem1)
                        if elem3 == "+":
                            temp = elem2 + elem1
                            newElem = str(temp)
                            stack.push(newElem)
                        elif elem3 == "-":
                            temp = elem2 - elem1
                            if temp < 0:
                                temp = 0
                            newElem = str(temp)
                            stack.push(newElem)
                        elif elem3 == "*":
                            temp = elem2 * elem1
                            newElem = str(temp)
                            stack.push(newElem)
                        elif elem3 == "/":
                            if elem1 == 0:
                                self.stackError = True
                                break
                            temp = elem2 // elem1
                            newElem = str(temp)
                            stack.push(newElem)
                    else:
                        stack.push(elem3)
                        stack.push(elem2)
                        stack.push(elem1)
                        break
                else:
                    stack.push(elem2)
                    stack.push(elem1)
                    break
            else:
                stack.push(elem1)
                break

        self.treeTraversal(node.left, outFile, indent, stack)
        self.treeTraversal(node.middle, outFile, indent, stack)
        self.treeTraversal(node.right, outFile, indent, stack)

class Parser:
    def __init__(self, tokens, outFile):
        self.tokens = tokens
        self.outFile = outFile
        self.index = 0
        self.currentToken = self.tokens[self.index]
        self.parenthesesBalance = 0

    def consumeToken(self):
        if self.index < (len(self.tokens) - 1):
            self.index = self.index + 1
        self.currentToken = self.tokens[self.index]
        return self.currentToken

    def parseTokens(self):
        if self.tokens[len(self.tokens) - 1].getTokenType() != "ERROR":
            parseTree = self.expr()
            if parseTree is not None:
                if self.parenthesesBalance == 0:
                    self.outFile.write("AST:\n")
                    return parseTree
        return None

    def expr(self):
        parseTree = self.term()
        if parseTree is None:
            return None
        while self.currentToken.getToken() == "+":
            self.consumeToken()
            rightTree = self.term()
            if rightTree is None:
                return None
            parseTree = Tree(parseTree, None, rightTree, "+")
        return parseTree

    def term(self):
        parseTree = self.factor()
        if parseTree is None:
            return None
        while self.currentToken.getToken() == "-":
            self.consumeToken()
            rightTree = self.factor()
            if rightTree is None:
                return None
            parseTree = Tree(parseTree, None, rightTree, "-")
        return parseTree

    def factor(self):
        parseTree = self.piece()
        if parseTree is None:
            return None
        while self.currentToken.getToken() == "/":
            self.consumeToken()
            rightTree = self.piece()
            if rightTree is None:
                return None
            parseTree = Tree(parseTree, None, rightTree, "/")
        return parseTree

    def piece(self):
        parseTree = self.element()
        if parseTree is None:
            return None
        while self.currentToken.getToken() == "*":
            self.consumeToken()
            rightTree = self.element()
            if rightTree is None:
                return None
            parseTree = Tree(parseTree, None, rightTree, "*")
        return parseTree

    def element(self):
        if self.currentToken.getToken() == "(":
            self.parenthesesBalance = self.parenthesesBalance - 1
            self.consumeToken()
            parseTree = self.expr()
            if parseTree is None:
                if self.currentToken.getToken() == ")":
                    self.parenthesesBalance = self.parenthesesBalance + 1
                    if self.parenthesesBalance > 0:
                        self.outFile.write("ERROR: MORE R PARENTHESES THAN LEFT\n")
                        return None
                    self.consumeToken()
                    self.outFile.write("ERROR: INVALID (expr), EMPTY PARENTHESES\n")
                    return None
            if self.currentToken.getToken() == ")":
                self.parenthesesBalance = self.parenthesesBalance + 1
                if self.parenthesesBalance > 0:
                    self.outFile.write("ERROR: MORE R PARENTHESES THAN LEFT\n")
                    return None
                self.consumeToken()
                return parseTree
            self.outFile.write("ERROR: UNABLE TO FIND R PARENTHESIS \n")
            return None
        elif self.currentToken.getTokenType() == "NUMBER":
            parseTree = Tree(None, None, None, self.currentToken.getToken())
            self.consumeToken()
            if self.currentToken.getToken() == "(":
                self.outFile.write("ERROR: CANNOT HAVE L PARENTHESIS AFTER NUMBER\n")
                return None
            if self.currentToken.getToken() == ")":
                if self.parenthesesBalance == 0:
                    self.outFile.write("ERROR: MORE R PARENTHESES THAN L\n")
                    return None
            return parseTree
        elif self.currentToken.getTokenType() == "IDENTIFIER":
            parseTree = Tree(None, None, None, self.currentToken.getToken())
            self.consumeToken()
            if self.currentToken.getToken() == "(":
                self.outFile.write("ERROR: CANNOT HAVE L PARENTHESIS AFTER IDENTIFIER\n")
                return None
            if self.currentToken.getToken() == ")":
                if self.parenthesesBalance == 0:
                    self.outFile.write("ERROR: MORE R PARENTHESES THAN L\n")
                    return None
            return parseTree
        elif self.currentToken.getToken() == ")":
            if self.parenthesesBalance == 0:
                self.outFile.write("ERROR: R PARENTHESIS WITHOUT LEFT\n")
                return None
        self.outFile.write("ERROR: INVALID ELEMENT\n")
        return None

    def statement(self):
        parseTree = self.baseStatement()
        if parseTree is None:
            return None
        while self.currentToken.getToken() == ';':
            self.consumeToken()
            baseStatement = self.baseStatement()
            if baseStatement is None:
                return None
            parseTree = Tree(parseTree, None, baseStatement, ';')
        return parseTree

    def baseStatement(self):
        if self.currentToken.getToken() == "if":
            parseTree = self.ifStatement()
            return parseTree
        elif self.currentToken.getTokenType() == "IDENTIFIER":
            parseTree = self.assignment()
            return parseTree
        elif self.currentToken.getToken() == "while":
            parseTree = self.whileStatement()
            return parseTree
        elif self.currentToken.getToken() == "skip":
            tempToken = self.currentToken.getToken()
            self.consumeToken()
            parseTree = Tree(None, None, None, tempToken)
            return parseTree
        self.outFile.write("ERROR: INVALID BASE STATEMENT\n")
        return None

    def assignment(self):
        if self.currentToken.getTokenType() == "IDENTIFIER":
            tempToken = self.currentToken.getToken()
            self.consumeToken()
            if self.currentToken.getToken() == ":=":
                self.consumeToken()
                lTree = Tree(None, None, None, tempToken)
                expr = self.expr()
                if expr is None:
                    return None
                parseTree = Tree(lTree, None, expr, ":=")
                return parseTree
        self.outFile.write("ERROR: INVALID ASSIGNMENT\n")
        return None

    def ifStatement(self):
        if self.currentToken.getToken() == "if":
            tempToken = self.currentToken.getToken()
            self.consumeToken()
            expr = self.expr()
            if expr is None:
                return None
            if self.currentToken.getToken() == "then":
                self.consumeToken()
                statement1 = self.statement()
                if statement1 is None:
                    return None
                if self.currentToken.getToken() == "else":
                    self.consumeToken()
                    statement2 = self.statement()
                    if statement2 is None:
                        return None
                    if self.currentToken.getToken() == "endif":
                        self.consumeToken()
                        parseTree = Tree(expr, statement1, statement2, tempToken)
                        return parseTree
        self.outFile.write("ERROR: INVALID IF STATEMENT\n")
        return None

    def whileStatement(self):
        if self.currentToken.getToken() == "while":
            tempToken = self.currentToken.getToken()
            self.consumeToken()
            expr = self.expr()
            if expr is None:
                return None
            if self.currentToken.getToken() == "do":
                self.consumeToken()
                statement = self.statement()
                if statement is None:
                    return None
                if self.currentToken.getToken() == "endwhile":
                    self.consumeToken()
                    parseTree = Tree(expr, None, statement, tempToken)
                    return parseTree
        self.outFile.write("ERROR: INVALID WHILE STATEMENT\n")
        return None

def main():
    input_file = "input.txt"
    output_file = "output.txt"

    with open(input_file, 'r') as inFile, open(output_file, 'w') as outFile:
        tokens = scan(inFile, outFile)
        parse = Parser(tokens, outFile)
        AST = parse.parseTokens()

        stack = Stack()

        if AST is not None:
            AST.treeTraversal(AST, outFile, "", stack)
            if not AST.stackError:
                outFile.write("\nOutput: ")
                outFile.write(stack.pop() + "\n")
            else:
                outFile.write("\nERROR: INCOMPLETE EXPRESSION\n")
        else:
            outFile.write("\nERROR: CANNOT DIVIDE BY 0\n")

main()
