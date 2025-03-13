import unittest
from src.lexer import Lexer
from src.parser import Parser

class TestParser(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()

    def test_parse_expression(self):
        tokens = self.lexer.tokenize("a + b")
        ast = self.parser.parse(tokens)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.type, 'BinaryExpression')
        self.assertEqual(ast.left.name, 'a')
        self.assertEqual(ast.right.name, 'b')
        self.assertEqual(ast.operator, '+')

    def test_parse_nested_expression(self):
        tokens = self.lexer.tokenize("(a + b) * c")
        ast = self.parser.parse(tokens)
        self.assertIsNotNone(ast)
        self.assertEqual(ast.type, 'BinaryExpression')
        self.assertEqual(ast.left.type, 'BinaryExpression')
        self.assertEqual(ast.right.name, 'c')

    def test_parse_invalid_expression(self):
        tokens = self.lexer.tokenize("a +")
        with self.assertRaises(Exception):
            self.parser.parse(tokens)

    def test_parse_function_declaration(self):
        tokens = self.lexer.tokenize("func:test { println(\"Hello\"); }")
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.assertIsNotNone(ast)
        self.assertEqual(ast["type"], "Program")
        self.assertEqual(len(ast["body"]), 1)
        self.assertEqual(ast["body"][0]["type"], "FunctionDeclaration")
        self.assertEqual(ast["body"][0]["name"], "test")

    def test_parse_enter_block(self):
        tokens = self.lexer.tokenize("enter { call test; }")
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.assertIsNotNone(ast)
        self.assertEqual(ast["type"], "Program")
        self.assertEqual(len(ast["body"]), 1)
        self.assertEqual(ast["body"][0]["type"], "EntryPoint")

    def test_parse_invalid_syntax(self):
        tokens = self.lexer.tokenize("func:test { println(\"Hello\") }")  # Missing semicolon
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        with self.assertRaises(Exception):
            self.parser.parse()

    def test_parse_assignment_statement(self):
        tokens = self.lexer.tokenize("assign x = 10;")
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse_statement()
        self.assertIsNotNone(ast)
        self.assertEqual(ast["type"], "AssignmentStatement")
        self.assertEqual(ast["name"], "x")
        self.assertEqual(ast["value"]["type"], "NumericLiteral")
        self.assertEqual(ast["value"]["value"], 10)

if __name__ == '__main__':
    unittest.main()