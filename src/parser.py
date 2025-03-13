class Parser:
    def __init__(self, tokens=None):
        self.tokens = tokens or []
        self.position = 0
        self.current_token = self.tokens[0] if self.tokens else None

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
        return self.current_token

    def peek(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def expect(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            token = self.current_token
            self.advance()
            return token
        line = self.current_token[2] if len(self.current_token) > 2 else "unknown"
        column = self.current_token[3] if len(self.current_token) > 3 else "unknown"
        raise SyntaxError(f"Expected {token_type}, got {self.current_token[0]} at line {line}, column {column}")

    def parse(self, tokens=None):
        if tokens:
            self.tokens = tokens
            self.position = 0
            self.current_token = self.tokens[0] if self.tokens else None
        
        program = {"type": "Program", "body": []}
        
        # Process each top-level construct
        while self.current_token:
            if self.current_token[0] == 'FUNC':
                program["body"].append(self.parse_function_declaration())
            elif self.current_token[0] == 'ENTER':
                program["body"].append(self.parse_enter_block())
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token}")
                
        return program

    def parse_function_declaration(self):
        self.expect('FUNC')
        self.expect('COLON')
        
        # Get function name
        name_token = self.expect('IDENTIFIER')
        
        # Check for parameters
        params = []
        if self.current_token and self.current_token[0] == 'LPAREN':
            self.advance()  # consume '('
            
            # Parse parameters if any
            if self.current_token and self.current_token[0] != 'RPAREN':
                params.append(self.expect('IDENTIFIER')[1])
                
                while self.current_token and self.current_token[0] == 'COMMA':
                    self.advance()  # consume ','
                    params.append(self.expect('IDENTIFIER')[1])
            
            self.expect('RPAREN')
        
        # Parse function body
        body = self.parse_block()
        
        return {
            "type": "FunctionDeclaration",
            "name": name_token[1],
            "params": params,
            "body": body
        }

    def parse_enter_block(self):
        self.expect('ENTER')
        body = self.parse_block()
        
        return {
            "type": "EntryPoint",
            "body": body
        }

    def parse_block(self):
        self.expect('LBRACE')
        statements = []
        
        while self.current_token and self.current_token[0] != 'RBRACE':
            statements.append(self.parse_statement())
        
        self.expect('RBRACE')
        return statements

    def parse_statement(self):
        if not self.current_token:
            raise SyntaxError("Unexpected end of input")
            
        if self.current_token[0] == 'PRINT':
            return self.parse_print_statement()
        elif self.current_token[0] == 'PRINTLN':
            return self.parse_println_statement()
        elif self.current_token[0] == 'CALL':
            return self.parse_call_statement()
        elif self.current_token[0] == 'IF':
            return self.parse_if_statement()
        elif self.current_token[0] == 'WHILE':
            return self.parse_while_statement()
        elif self.current_token[0] == 'FOR':
            return self.parse_for_statement()
        elif self.current_token[0] == 'RETURN':
            return self.parse_return_statement()
        elif self.current_token[0] == 'ASSIGN':
            return self.parse_assignment_statement()
        elif self.current_token[0] == 'IDENTIFIER':
            # Assignment statement
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def parse_assignment_statement(self):
        """Parse an assignment statement: assign x = expression;"""
        token = self.expect('ASSIGN')
        line = token[2] if len(token) > 2 else "unknown"
        
        # Get the variable name
        var_name = self.expect('IDENTIFIER')[1]
        
        # Expect equals sign
        self.expect('ASSIGN')
        
        # Parse the expression to be assigned
        expression = self.parse_expression()
        
        # Expect semicolon
        self.expect('SEMICOLON')
        
        return {
            "type": "AssignmentStatement",
            "name": var_name,
            "value": expression,
            "line": line
        }

    def parse_print_statement(self):
        token = self.expect('PRINT')
        line = token[2] if len(token) > 2 else "unknown"
        
        # Handle function calls with parentheses
        if self.current_token and self.current_token[0] == 'LPAREN':
            self.expect('LPAREN')
            expr = self.parse_expression()
            self.expect('RPAREN')
        else:
            expr = self.parse_expression()
            
        self.expect('SEMICOLON')
        
        return {
            "type": "PrintStatement",
            "expression": expr,
            "newline": False,
            "line": line
        }

    def parse_println_statement(self):
        token = self.expect('PRINTLN')
        line = token[2] if len(token) > 2 else "unknown"
        
        # Handle function calls with parentheses
        if self.current_token and self.current_token[0] == 'LPAREN':
            self.expect('LPAREN')
            expr = self.parse_expression()
            self.expect('RPAREN')
        else:
            expr = self.parse_expression()
            
        self.expect('SEMICOLON')
        
        return {
            "type": "PrintStatement",
            "expression": expr,
            "newline": True,
            "line": line
        }

    def parse_call_statement(self):
        self.expect('CALL')
        func_name = self.expect('IDENTIFIER')[1]
        
        # Check for arguments in parentheses
        args = []
        if self.current_token and self.current_token[0] == 'LPAREN':
            self.advance()  # consume '('
            
            # Parse arguments if any
            if self.current_token and self.current_token[0] != 'RPAREN':
                args.append(self.parse_expression())
                
                while self.current_token and self.current_token[0] == 'COMMA':
                    self.advance()  # consume ','
                    args.append(self.parse_expression())
            
            self.expect('RPAREN')
        
        self.expect('SEMICOLON')
        
        return {
            "type": "CallStatement",
            "name": func_name,
            "arguments": args
        }

    def parse_expression(self):
        """Parse an expression which could be a primary expression or a binary expression"""
        return self.parse_binary_expression()
    
    def parse_binary_expression(self):
        """Parse a binary expression or a single primary expression"""
        left = self.parse_primary_expression()
        
        # Check if followed by an operator
        if self.current_token and self.current_token[0] == 'PLUS':
            operator = '+'
            line = self.current_token[2] if len(self.current_token) > 2 else "unknown"
            self.advance()  # consume operator
            right = self.parse_binary_expression()  # right side could be another binary expression
            return {
                "type": "BinaryExpression",
                "operator": operator,
                "left": left,
                "right": right,
                "line": line
            }
        
        return left
    
    def parse_primary_expression(self):
        """Parse a primary expression (literal, identifier, or parenthesized expression)"""
        if self.current_token[0] == 'LPAREN':
            # Handle parenthesized expressions
            self.advance()  # consume '('
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
            
        elif self.current_token[0] == 'STRING':
            value = self.current_token[1]
            line = self.current_token[2] if len(self.current_token) > 2 else "unknown"
            self.advance()
            return {"type": "StringLiteral", "value": value, "line": line}
            
        elif self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            line = self.current_token[2] if len(self.current_token) > 2 else "unknown"
            self.advance()
            return {"type": "NumericLiteral", "value": value, "line": line}
            
        elif self.current_token[0] == 'IDENTIFIER':
            value = self.current_token[1]
            line = self.current_token[2] if len(self.current_token) > 2 else "unknown"
            self.advance()
            
            # Handle function calls like identifier()
            if self.current_token and self.current_token[0] == 'LPAREN':
                self.advance()  # consume '('
                args = []
                
                # Parse arguments if any
                if self.current_token and self.current_token[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    
                    while self.current_token and self.current_token[0] == 'COMMA':
                        self.advance()  # consume ','
                        args.append(self.parse_expression())
                
                self.expect('RPAREN')
                
                return {
                    "type": "FunctionCall",
                    "name": value,
                    "arguments": args,
                    "line": line
                }
            
            return {"type": "Identifier", "name": value, "line": line}
            
        else:
            line = self.current_token[2] if len(self.current_token) > 2 else "unknown"
            column = self.current_token[3] if len(self.current_token) > 3 else "unknown"
            raise SyntaxError(f"Unexpected token in expression: {self.current_token[0]} at line {line}, column {column}")