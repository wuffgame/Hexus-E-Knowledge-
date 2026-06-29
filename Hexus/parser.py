class NumberNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberNode({self.value})"

class VariableNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"VariableNode({self.name})"

class SendCommandNode:
    def __init__(self, text_value):
        self.text_value = text_value

    def __repr__(self):
        return f"SendCommandNode(text={self.text_value})"
class ReadCommandNode:
    def __init__(self, text_value, var_name):
        self.text_value = text_value
        self.var_name = var_name

    def __repr__(self):
        return f"ReadCommandNode(text={self.text_value}, var={self.var_name})"

class StopNode:
    def __repr__(self):
        return f"StopNode()"

class SetVar:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"SetVarNode(var= {self.var_name}, value={self.value})"

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op} {self.right})"

class HexusParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset <len(self.tokens):
            return self.tokens[self.pos + offset]
        return ("EOF", "EOF")

    def consume(self, expected_type):
        token_type, value = self.peek()

        if token_type == expected_type:
            self.pos += 1
            return value
        else:
            raise SyntaxError(
                f"Expected token of type '{expected_type}', "
                f"but found '{token_type}' with value '{value}' at position {self.pos}."
            )

    def consume_value(self, expected_type, expected_value):
        token_type, value = self.peek()
        if token_type == expected_type and value == expected_value:
            self.pos += 1
            return value
        else:
            raise SyntaxError(
                f"Syntax error: Expected '{expected_value}', but found '{value}'."
            )

    def consume_end_of_statement(self):
        token_type, _ = self.peek()
        if token_type == "NEWLINE":
            self.consume("NEWLINE")
        elif token_type == "EOF":
            pass
        else:
            raise SyntaxError(f"SynaxError: Expected end of line, but found token of type '{token_type}'")

    def parse_value(self):
        token_type, value = self.peek()

        if token_type == "INT":
            self.consume("INT")
            return NumberNode(value)
        elif token_type == "VAR":
            self.consume("VAR")
            return VariableNode(value)
        else:
            raise SyntaxError(f"SyntaxError: Expect number or variable, but found '{token_type}' ('{value}')")

    def parse_expression(self):
        left = self.parse_value()

        token_type, value = self.peek()

        if token_type == "PLUS":
            self.consume("PLUS")
            op = "+"
        elif token_type == "MINUS":
            self.consume("MINUS")
            op = "-"
        elif token_type == "MUL":
            self.consume("MUL")
            op = "*"
        elif token_type == "DIV":
            self.consume("DIV")
            op = "/"
        else:
            raise SyntaxError(f"Expected a mathematical operator, but found {token_type}")

        right = self.parse_value()
        self.consume_end_of_statement()
        return BinaryOpNode(left, op, right)

    def parse_var(self):
        var = self.consume("VAR")
        token_type, value = self.peek()
        if token_type == "EQUAL":
            self.consume("EQUAL")
            token_type, value = self.peek()
            if token_type == "INT":
                value = self.consume("INT")
            elif token_type == "STRING":
                value = self.consume("STRING")
            else:
                raise SyntaxError(f"SyntaxError: Expected string or number, but found {token_type}")

        elif token_type == "KEYWORD" and value == "is":
            self.consume("KEYWORD")
            token_type, value = self.peek()
            if token_type == "INT":
                value = self.consume("INT")
            elif token_type == "STRING":
                value = self.consume("STRING")
            else:
                raise SyntaxError(f"SyntaxError: Expected string or number, but found {token_type}")
        else:
            raise SyntaxError(f"SyntaxError: Expected '=' or 'is', but found {token_type} ('{value}')")

        self.consume_end_of_statement()
        return SetVar(var, value)



    def parse_send(self):
        self.consume("KEYWORD")
        text = self.consume("STRING")
        self.consume_value("KEYWORD", "to")
        self.consume_value("KEYWORD", "console")
        self.consume_end_of_statement()
        return SendCommandNode(text)

    def parse_read(self):
        self.consume("KEYWORD")
        text = self.consume("STRING")
        self.consume_value("KEYWORD", "to")
        var = self.consume("VAR")
        self.consume_value("KEYWORD", "from")
        self.consume_value("KEYWORD", "console")
        self.consume_end_of_statement()
        return ReadCommandNode(text, var)

    def parse_stop(self):
        self.consume("KEYWORD")
        self.consume_end_of_statement()
        return StopNode()

    def parse(self):
        program_nodes = []

        while self.peek()[0] != "EOF":
            if self.peek()[0] == "NEWLINE":
                self.consume("NEWLINE")
                continue

            token_type, value = self.peek()

            if token_type == "KEYWORD" and value == "send":
                node = self.parse_send()
                program_nodes.append(node)
            elif token_type == "KEYWORD" and value == "read":
                node = self.parse_read()
                program_nodes.append(node)
            elif token_type == "KEYWORD" and value == "stop":
                node = self.parse_stop()
                program_nodes.append(node)
            elif token_type == "INT" or token_type == "VAR":
                next_type, next_value = self.peek(1)
                if token_type == "VAR" and (next_type == "EQUAL" or (next_type == "KEYWORD" and next_value == "is")):
                    node = self.parse_var()
                else:
                    node = self.parse_expression()
                program_nodes.append(node)
            else:
                raise SyntaxError(f"Unknown start instruction: {token_type} ('{value}')")
        return program_nodes
