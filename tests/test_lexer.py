import unittest
from src.lexer import Lexer

class TestLexer(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def test_tokenize_single_token(self):
        result = self.lexer.tokenize("let x = 10;")
        expected = [
            ('LET', 'let'),
            ('IDENTIFIER', 'x'),
            ('ASSIGN', '='),
            ('NUMBER', '10'),
            ('SEMICOLON', ';')
        ]
        self.assertEqual(result, expected)

    def test_tokenize_multiple_tokens(self):
        result = self.lexer.tokenize("if (x > 5) { return x; }")
        expected = [
            ('IF', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'x'),
            ('GT', '>'),
            ('NUMBER', '5'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('RETURN', 'return'),
            ('IDENTIFIER', 'x'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
        self.assertEqual(result, expected)

    def test_tokenize_invalid_input(self):
        with self.assertRaises(ValueError):
            self.lexer.tokenize("let x = ;")

    def test_tokenize_function_declaration(self):
        result = self.lexer.tokenize("func:test { println(\"Hello\"); }")
        expected = [
            ('FUNC', 'func'),
            ('COLON', ':'),
            ('IDENTIFIER', 'test'),
            ('LBRACE', '{'),
            ('PRINTLN', 'println'),
            ('LPAREN', '('),
            ('STRING', 'Hello'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
        self.assertEqual(result, expected)

    def test_tokenize_enter_block(self):
        result = self.lexer.tokenize("enter { call test; }")
        expected = [
            ('ENTER', 'enter'),
            ('LBRACE', '{'),
            ('CALL', 'call'),
            ('IDENTIFIER', 'test'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}')
        ]
        self.assertEqual(result, expected)

    def test_tokenize_comments(self):
        result = self.lexer.tokenize("// This is a comment\nprint(\"Hello\");")
        expected = [
            ('PRINT', 'print'),
            ('LPAREN', '('),
            ('STRING', 'Hello'),
            ('RPAREN', ')'),
            ('SEMICOLON', ';')
        ]
        self.assertEqual(result, expected)

    def test_tokenize_assignment(self):
        result = self.lexer.tokenize("assign x = 10;")
        expected = [
            ('ASSIGN', 'assign'),
            ('IDENTIFIER', 'x'),
            ('ASSIGN', '='),
            ('NUMBER', 10),
            ('SEMICOLON', ';')
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()