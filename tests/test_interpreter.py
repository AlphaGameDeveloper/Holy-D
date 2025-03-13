import unittest
import io
import sys
import time
from unittest.mock import patch
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.interpreter = Interpreter()
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_interpret_print_statement(self):
        source_code = "enter { print(\"Hello\"); }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        self.assertEqual(self.captured_output.getvalue(), "Hello")

    def test_interpret_function_call(self):
        source_code = "func:test { println(\"Function called\"); } enter { call test; }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        self.assertEqual(self.captured_output.getvalue(), "Function called\n")

    def test_interpret_string_concatenation(self):
        source_code = "enter { println(\"Hello\" + \" World\"); }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        self.assertEqual(self.captured_output.getvalue(), "Hello World\n")

    def test_interpret_simple_expression(self):
        source_code = "a = 5; b = a + 2;"
        tokens = self.lexer.tokenize(source_code)
        ast = self.parser.parse(tokens)
        result = self.interpreter.interpret(ast)
        self.assertEqual(result['b'], 7)

    def test_interpret_conditional(self):
        source_code = "if (true) { result = 10; } else { result = 20; }"
        tokens = self.lexer.tokenize(source_code)
        ast = self.parser.parse(tokens)
        result = self.interpreter.interpret(ast)
        self.assertEqual(result['result'], 10)

    def test_interpret_loop(self):
        source_code = "result = 0; for (i = 0; i < 5; i = i + 1) { result = result + i; }"
        tokens = self.lexer.tokenize(source_code)
        ast = self.parser.parse(tokens)
        result = self.interpreter.interpret(ast)
        self.assertEqual(result['result'], 10)

    @patch('time.sleep')
    def test_interpret_sleep_function(self, mock_sleep):
        source_code = "enter { call sleep(2); }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        mock_sleep.assert_called_once_with(2.0)

    @patch('sys.exit')
    def test_interpret_exit_function_default(self, mock_exit):
        source_code = "enter { call exit(); }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    def test_interpret_exit_function_with_code(self, mock_exit):
        source_code = "enter { call exit(42); }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        mock_exit.assert_called_once_with(42)

    def test_interpret_variable_assignment(self):
        source_code = "enter { assign x = 42; println(x); }"
        tokens = self.lexer.tokenize(source_code)
        self.parser.tokens = tokens
        self.parser.position = 0
        self.parser.current_token = tokens[0]
        
        ast = self.parser.parse()
        self.interpreter.interpret(ast)
        self.assertEqual(self.captured_output.getvalue(), "42\n")

if __name__ == '__main__':
    unittest.main()