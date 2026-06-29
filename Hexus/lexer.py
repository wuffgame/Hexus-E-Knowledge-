import re

token_pattern = [
        ("INT", r"\d+"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("EQUALS", r'=='),
        ("EQUAL", r"="),
        ("MUL", r"\*"),
        ("DIV", r"/"),
        ("STRING", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ("KEYWORD", r'\b(send|to|console|read|from|if|is|or|else|stop)\b'),
        ("VAR", r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ("LBRACE", r'\{'),
        ("RBRACE", r'\}'),
        ("SKIP", r'[ \t]+'),
        ("NEWLINE", r'\n')
    ]

def tokenizer(text, definition):
    patter = []
    for name, regex in definition:
        patter.append(f"(?P<{name}>{regex})")

    full_regex = "|".join(patter)

    tokens = []

    for match in re.finditer(full_regex, text):
        kind = match.lastgroup
        value = match.group()

        tokens.append((kind, value))

    return tokens

def tokenizer_tokens(text):
    tokens = tokenizer(text, token_pattern)
    return tokens