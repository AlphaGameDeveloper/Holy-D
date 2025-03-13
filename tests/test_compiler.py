import unittest
from src.compiler import Compiler
from src.parser import Parser
from src.lexer import Lexer

class TestCompiler(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.compiler = Compiler()

    def test_compile_simple_expression(self):
        source_code = "let x = 5;"
        tokens = self.lexer.tokenize(source_code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = b'\x05'  # Example expected bytecode
        self.assertEqual(bytecode, expected_bytecode)

    def test_compile_function_definition(self):
        source_code = "func add(a, b) { return a + b; }"
        tokens = self.lexer.tokenize(source_code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = b'\x01\x02'  # Example expected bytecode for function
        self.assertEqual(bytecode, expected_bytecode)

    def test_compile_if_statement(self):
        source_code = "if (x > 0) { return true; }"
        tokens = self.lexer.tokenize(source_code)
        ast = self.parser.parse(tokens)
        bytecode = self.compiler.compile(ast)
        expected_bytecode = b'\x03'  # Example expected bytecode for if statement
        self.assertEqual(bytecode, expected_bytecode)

if __name__ == '__main__':
    unittest.main()