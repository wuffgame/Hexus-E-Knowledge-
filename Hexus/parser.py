class SendCommandNode:
    def __init__(self, text_value):
        self.text_value = text_value

    def __repr__(self):
        return f"SendCommandNode(text={self.text_value})"

class HexusParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos <len(self.tokens):
            return self.tokens[self.pos]
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

    def parse_send(self):
        self.consume("KEYWORD")
        text = self.consume("STRING")
        self.consume_value("KEYWORD", "to")
        self.consume_value("KEYWORD", "console")
        self.consume_end_of_statement()
        return SendCommandNode(text)


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
            else:
                raise SyntaxError(f"Unknown start instruction: {token_type} ('{value}')")
        return program_nodes
