import sys
from lexer import tokenizer_tokens

def main():
    file_name = "test.he"
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            source_code = file.read()

    except FileNotFoundError:
        print(f"File {file_name} not found!!!")
        return
    token_list = tokenizer_tokens(source_code)
    for token in token_list:
        print(token)

if __name__ == "__main__":
    main()