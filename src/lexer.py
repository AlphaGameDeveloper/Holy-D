class Lexer:
    def __init__(self, source_code=""):
        self.source_code = source_code
        self.position = 0
        self.line = 1  # Track current line
        self.column = 1  # Track current column
        self.current_char = self.source_code[self.position] if self.source_code else None
        self.tokens = []
        
        # Keywords in Holy-D
        self.keywords = {
            'func': 'FUNC',
            'enter': 'ENTER',
            'call': 'CALL',
            'print': 'PRINT',
            'println': 'PRINTLN',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'for': 'FOR',
            'return': 'RETURN',
            'assign': 'ASSIGN'
        }

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()

    def identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if identifier is a keyword
        token_type = self.keywords.get(result, 'IDENTIFIER')
        return (token_type, result)

    def number(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return ('FLOAT', float(result))
        
        return ('NUMBER', int(result))

    def string(self):
        result = ''
        # Skip the opening quote
        self.advance()
        
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\' and self.position + 1 < len(self.source_code):
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()
        
        # Skip the closing quote
        if self.current_char == '"':
            self.advance()
        else:
            raise ValueError("Unclosed string literal")
            
        return ('STRING', result)

    def get_next_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def tokenize(self, source_code=None):
        if source_code:
            self.source_code = source_code
            self.position = 0
            self.line = 1
            self.column = 1
            self.current_char = self.source_code[self.position] if self.source_code else None
            self.tokens = []

        tokens = []
        
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char == '/' and self.position + 1 < len(self.source_code) and self.source_code[self.position + 1] == '/':
                self.advance()  # Skip first '/'
                self.advance()  # Skip second '/'
                self.skip_comment()
                continue
                
            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.identifier())
                continue
                
            if self.current_char.isdigit():
                tokens.append(self.number())
                continue
                
            if self.current_char == '"':
                tokens.append(self.string())
                continue
                
            # Special characters and operators
            if self.current_char == '{':
                tokens.append(('LBRACE', '{', self.line, self.column))
                self.advance()
                continue
                
            if self.current_char == '}':
                tokens.append(('RBRACE', '}', self.line, self.column))
                self.advance()
                continue
                
            if self.current_char == '(':
                tokens.append(('LPAREN', '(', self.line, self.column))
                self.advance()
                continue
                
            if self.current_char == ')':
                tokens.append(('RPAREN', ')', self.line, self.column))
                self.advance()
                continue
                
            if self.current_char == ';':
                tokens.append(('SEMICOLON', ';'))
                self.advance()
                continue
                
            if self.current_char == ',':
                tokens.append(('COMMA', ','))
                self.advance()
                continue
                
            if self.current_char == '+':
                tokens.append(('PLUS', '+'))
                self.advance()
                continue
                
            if self.current_char == '-':
                tokens.append(('MINUS', '-'))
                self.advance()
                continue
                
            if self.current_char == '*':
                tokens.append(('MULTIPLY', '*'))
                self.advance()
                continue
                
            if self.current_char == '/':
                tokens.append(('DIVIDE', '/'))
                self.advance()
                continue
                
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(('EQUALS', '=='))
                    self.advance()
                else:
                    tokens.append(('ASSIGN', '='))
                continue
                
            if self.current_char == ':':
                tokens.append(('COLON', ':'))
                self.advance()
                continue
            
            # If we get here, character is not recognized
            raise ValueError(f"Unrecognized character: '{self.current_char}' at position {self.position}, line {self.line}, column {self.column}")
            
        return tokens