from enum import Enum
from typing import Any

WHITESPACE = (' ', '\n', '\t', '\v', '\r')

def is_digit(char: str) -> bool: 
    return char >= '0' and char <= '9'
def is_alpha(char: str) -> bool: 
    return char >= 'a' and char <= 'z' or char >= 'A' and char <= 'Z'


class TokenType(Enum):
    INVALID_ID = "INVALID ID"
    INVALID_NUMBER = "INVALID NUMBER"

    UNKNOWN_TOKEN = "UNKNOWN_TOKEN"
    
    ID = "ID"

    NUMBER = "NUMBER"

    ASSIGN = "ASSIGN"

    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIV = "DIV"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    
    COMMENT = "COMMENT"

INVALID = (TokenType.INVALID_ID, TokenType.INVALID_NUMBER, TokenType.UNKNOWN_TOKEN)

class Token:
    def __init__(self, type: TokenType, literal: Any, line_no: int, position: int) -> None:
        self.type = type
        self.literal = literal
        self.line_no = line_no
        self.position = position

    def __str__(self) -> str:
        if self.type in INVALID:
            return f"Line {self.line_no}\tColumn {self.position}\t:{self.type}"
        return f"{self.type}: {self.literal}"

    def __repr__(self) -> str:
        return self.__str__()
    
class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source

        self.position: int = -1
        self.read_position: int = 0
        self.line_no: int = 0
        self.line_pos: int = 0

        self.current_char: str | None = None

        self.__read_char()
    
    def __read_char(self) -> None:
        if self.read_position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.read_position]

        self.line_pos += 1
        self.position = self.read_position    
        self.read_position += 1

    def __skip_whitespace(self) -> None:
        while self.current_char in WHITESPACE:
            if(self.current_char == '\n'):
                self.line_no += 1
                self.line_pos = 0

            self.__read_char()

    def __new_token(self, tt: TokenType, literal: Any) -> Token:
        return Token(type=tt, literal=literal, line_no=self.line_no, position=self.line_pos)
    
    def __read_number(self) -> Token:
        start_pos: int = self.position
        dot_count: int = 0

        output: str = ""
        while is_digit(self.current_char) or self.current_char == '.':
            if self.current_char == '.':
                if dot_count:
                    return self.__new_token(TokenType.INVALID_NUMBER, self.source[self.position])
                dot_count += 1
            
            output += self.current_char
            self.__read_char()
            
            if self.current_char == None:
                break
        
        if self.current_char != None and is_alpha(self.current_char):
            return self.__new_token(TokenType.INVALID_ID, start_pos)
        
        return self.__new_token(TokenType.NUMBER, output)
    
    def __read_assign(self) -> Token:
        if self.source[self.read_position] != '=':
            return self.__new_token(TokenType.UNKNOWN_TOKEN, self.source[self.position])
        
        self.__read_char()
        return self.__new_token(TokenType.ASSIGN, ":=")
    
    def __read_id(self) -> Token:
        start_pos: int = self.position
        output: str = ""

        while (is_digit(self.current_char) and len(output)) or is_alpha(self.current_char):
            output += self.current_char
            self.__read_char()
        
        if self.current_char not in ('+', '-', '*', '/', ':', '(', ')') and self.current_char not in WHITESPACE:
            return self.__new_token(TokenType.INVALID_ID, self.current_char)
        
        return self.__new_token(TokenType.ID, output)

    def next_token(self) -> Token:
        token: Token = None

        self.__skip_whitespace()

        match self.current_char:
            case '+':
                token = self.__new_token(TokenType.PLUS, self.current_char)
            case '-':
                token = self.__new_token(TokenType.MINUS, self.current_char)
            case '*':
                token = self.__new_token(TokenType.TIMES, self.current_char)
            case '/':
                token = self.__new_token(TokenType.DIV, self.current_char)
            case '(':
                token = self.__new_token(TokenType.LPAREN, self.current_char)
            case ')':
                token = self.__new_token(TokenType.RPAREN, self.current_char)
            case ':':
                token = self.__read_assign()

            case _:
                if is_digit(self.current_char): 
                    token = self.__read_number()
                   
                elif is_alpha(self.current_char):
                    token = self.__read_id()
            
                else: token = self.__new_token(TokenType.UNKNOWN_TOKEN, self.current_char)

        self.__read_char()
        self.__skip_whitespace()
        return token

def main() -> None:
    input = """
    3Celsius := 100.0\n
    Fahrenheit$ := (9../5)*Celsius+%32
    """

    lexer = Lexer(input)
    tokens: list[Token] = list()
    invalid_tokens: list[Token]= list()
    valid_tokens: list[Token]= list()
    while lexer.current_char != None:
        tokens.append(lexer.next_token())
    

    for token in tokens: (invalid_tokens if token.type in INVALID else valid_tokens).append(token)
    
    for token in valid_tokens: print(token)
    for token in invalid_tokens: print(token)

if __name__ == "__main__":
    main()