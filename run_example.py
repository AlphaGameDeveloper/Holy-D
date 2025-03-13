import sys
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
import traceback

def run_example(filename='example.hd'):
    try:
        with open(filename, 'r') as file:
            source_code = file.read()
        
        print(f"Running {filename}:")
        print("-" * 40)
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print("Tokenization successful!")
        
        parser = Parser(tokens)
        ast = parser.parse()
        print("Parsing successful!")
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        print("-" * 40)
        print("Program executed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_example(sys.argv[1])
    else:
        run_example()
