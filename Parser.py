from ASTNodeDefs import *
from typing import List, Tuple, Union
import re

"""
This is the skeleton code for the Parser with a Lexer
Feel free to modify anything in this file as needed
To run tests, use Verify.py
"""


class Lexer:
    """
    The Lexer (also known as a tokenizer or scanner) is responsible for breaking
    the raw source code string into a stream of meaningful tokens.
    """

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Tuple[str, str]] = []  # List of (token_type, token_value)
        self.token_specs = [
            ("ASSIGN", r":="),
            ("SEMICOLON", r";"),
            # Fill in more token specifications here
            ("DOTDOT", r"\.\."), ("EQ", r"="),("NEQ", r"/="),("LTE", r"<="),("GTE", r">="),("LT", r"<"),("GT", r">"),
            ("PLUS", r"\+"),("MINUS", r"-"),("MUL", r"\*"),("DIV", r"/"),("LPAREN", r"\("),("RPAREN", r"\)"),
            ("PUT", r"\bPut\b"),("IF", r"\bif\b"),("THEN", r"\bthen\b"),("ELSE", r"\belse\b"),("END", r"\bend\b"),
            ("WHILE", r"\bwhile\b"),("LOOP", r"\bloop\b"),("FOR", r"\bfor\b"),("IN", r"\bin\b"),("OR", r"\bor\b"),
            ("AND", r"\band\b"),("MOD", r"\bmod\b"),("TRUE", r"\bTrue\b"),("FALSE", r"\bFalse\b"),
            ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),("INTEGER", r"[0-9]+"), ("SKIP", r"[ \t\n\r]+"), ("MISMATCH", r"."),
            
        ]
        self.token_regex = re.compile(
            "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specs)
        )

    def tokenize(self) -> List[Tuple[str, str]]:
        """
        Tokenizes the input code into a list of tokens.
        Each token is represented as a tuple (token_type, token_value).
        """
        for mo in self.token_regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            else:
                self.tokens.append((kind, value))
        self.tokens.append(("EOF", ""))  # End-of-file token
        return self.tokens


class Parser:
    def __init__(self, tokens: List[Tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0  # Current position in the token list

    def current_token(self) -> Tuple[str, str]:
        # Returns the current token without consuming it
        return self.tokens[self.pos]

    def advance(self) -> None:
        # Advances to the next token
        self.pos += 1

    def expect(self, token_type: str) -> Tuple[str, str]:
        # Consumes the current token if it matches the expected type and returns it
        current_type, current_value = self.current_token()
        if current_type == token_type:
            self.advance()
            return (current_type, current_value)
        else:
            raise RuntimeError(
                f"Expected token type {token_type}, got type {current_type}"
            )

    def parse(self) -> ASTNode:
        block = self.parse_block()
        self.expect("EOF")
        return block

    def parse_block(self) -> Block:
        # Implementation Required
        statement_list = []
        is_parsing_block = True #Trying to make sure that it doesnt parse past the block
        while is_parsing_block == True:
            current_type = self.current_token()[0]
            if current_type == 'EOF':
                is_parsing_block = False
            elif current_type == 'END':
                is_parsing_block = False
            elif current_type == 'ELSE':
                is_parsing_block = False
            else:   # if the type of statement is not eof end or else then it is a statement so add it to the list
                statement = self.parse_statement()
                statement_list.append(statement)
        return Block(statement_list)    #return a block node of the list of statements

    def parse_statement(self) -> Union[Assign, Put, If, WhileLoop, ForLoop]:
        # Implementation Required
        current_type = self.current_token()[0]
        if current_type == 'ID':    #find out what statement is being parsed by looking at the first token
            return self.parse_assign_statement()
        elif current_type == 'PUT':
            return self.parse_put_statement()
        elif current_type == 'IF':
            return self.parse_if_statement()
        elif current_type == 'WHILE':
            return self.parse_while_statement()
        elif current_type == 'FOR':
            return self.parse_for_statement()
        else:
            raise RuntimeError(f"Unexpected token: {current_type}")

    # More parsing methods as needed

    def parse_assign_statement(self):
        id_token = self.expect("ID")
        self.expect("ASSIGN")
        expression = self.parse_expression()
        self.expect("SEMICOLON")
        id_node = Identifier(id_token[1])   #Create identifier node and assign that node
        assign_node = Assign(id_node, expression)
        return assign_node

    def parse_put_statement(self):
        self.expect("PUT")  # checking the format of the put statement Put(expression);
        self.expect("LPAREN")
        expr_to_put = self.parse_expression()
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        return Put(expr_to_put)

    def parse_while_statement(self):
        self.expect("WHILE")
        cond_expr = self.parse_expression()
        self.expect("LOOP")
        loop_body = self.parse_block()
        self.expect("END")
        self.expect("LOOP")
        self.expect("SEMICOLON")
        return WhileLoop(cond_expr, loop_body)  # if it finds all the required elements return the values

    def parse_for_statement(self):
        self.expect("FOR")  #checking the format of for statements
        id_tok = self.expect("ID")
        self.expect("IN")
        start_expr = self.parse_expression()
        self.expect("DOTDOT")
        end_expr = self.parse_expression()
        self.expect("LOOP")
        loop_body = self.parse_block()
        self.expect("END")
        self.expect("LOOP")
        self.expect("SEMICOLON")
        id_node = Identifier(id_tok[1])
        return ForLoop(id_node, start_expr, end_expr, loop_body)

    def parse_if_statement(self):
        self.expect("IF")
        condition_expr = self.parse_expression()
        self.expect("THEN")
        then_block = self.parse_block()
        else_block = None  # Default else block to None b/c it is optional
        if self.current_token()[0] == "ELSE":
            self.advance()
            else_block = self.parse_block() # if there is an else block then parse it
        self.expect("END")
        self.expect("IF")
        self.expect("SEMICOLON")
        if_node = If(condition_expr, then_block, else_block)
        return if_node

    def parse_expression(self):
        or_pieces = [self.parse_and_level()]
        while self.current_token()[0] == "OR":  #if the current token is or skip it and get an 'and' token b/c or is
            self.advance()                      #lower precedence
            next_piece = self.parse_and_level()
            or_pieces.append(next_piece)
        if len(or_pieces) == 1: # if there is only one peice then it isnt an or operation
            return or_pieces[0]
        return Or(or_pieces)    #if there are more than 1 peices wrap it in an or AST node

    def parse_and_level(self):
        and_pieces = [self.parse_compare_level()]
        while self.current_token()[0] == "AND": #checking if there are and tokens connected
            self.advance()  #if there is skip it
            next_piece = self.parse_compare_level()
            and_pieces.append(next_piece)
        if len(and_pieces) == 1:    #if it is only one peice of and token skip it
            return and_pieces[0]
        return And(and_pieces)

    def parse_compare_level(self):
        pass

        
    