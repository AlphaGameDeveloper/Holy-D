class Syntax:
    # Define the syntax rules and grammar for the Holy-D language
    KEYWORDS = {'func', 'enter', 'call', 'print', 'println', 'if', 'else', 'while', 'for', 'return'}
    OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
    DELIMITERS = {';', ',', '(', ')', '{', '}', ':'}

    @staticmethod
    def is_keyword(token):
        return token in Syntax.KEYWORDS

    @staticmethod
    def is_operator(token):
        return token in Syntax.OPERATORS

    @staticmethod
    def is_delimiter(token):
        return token in Syntax.DELIMITERS

    @staticmethod
    def is_identifier(token):
        if not token:
            return False
        if token[0].isdigit():
            return False
        return all(c.isalnum() or c == '_' for c in token) and not Syntax.is_keyword(token)

    @staticmethod
    def is_literal(token):
        # A simple check for literals (numbers and strings)
        if not token:
            return False
        if token.isdigit():
            return True
        if len(token) >= 2 and token.startswith('"') and token.endswith('"'):
            return True
        return False

    @staticmethod
    def validate_syntax(tokens):
        # Basic syntax validation logic
        if not tokens:
            return True
            
        # Check for unmatched braces, parentheses, etc.
        stack = []
        for token_type, value in tokens:
            if token_type == 'LPAREN':
                stack.append('(')
            elif token_type == 'RPAREN':
                if not stack or stack.pop() != '(':
                    return False
            elif token_type == 'LBRACE':
                stack.append('{')
            elif token_type == 'RBRACE':
                if not stack or stack.pop() != '{':
                    return False
        
        # If stack is not empty, we have unmatched opening brackets
        return len(stack) == 0