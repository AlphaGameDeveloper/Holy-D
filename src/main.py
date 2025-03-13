import sys
import os
import traceback
import json
import pathlib
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import argparse

def save_ast(ast, file_path):
    """Save the abstract syntax tree to a cache directory in the same folder as the script file, similar to __pycache__."""
    # Get the directory where the script file is located
    script_dir = os.path.dirname(os.path.abspath(file_path))
    hd_cache_dir = os.path.join(script_dir, "_holy_d_cache")
    
    # Create the cache directory if it doesn't exist
    os.makedirs(hd_cache_dir, exist_ok=True)
    
    # Use the base filename without its extension for the AST file
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    ast_file_path = os.path.join(hd_cache_dir, f"{base_filename}.hdast")
    
    try:
        with open(ast_file_path, 'w') as ast_file:
            json.dump(ast, ast_file, indent=2)
        print(f"AST saved to {ast_file_path}")
        return True
    except Exception as e:
        print(f"Error saving AST: {str(e)}")
        return False

def run_file(file_path):
    """Run a Holy-D script file"""
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()
        
        # Save the AST to a file
        save_ast(ast, file_path)
        
        # Run the interpreter
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        
        return result
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return None
            
def run_repl():
    """Run the Holy-D REPL (Read-Eval-Print Loop)"""
    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()
    
    print("Holy-D REPL (type 'exit' to quit, 'save' to save and execute)")
    count = 1
    ast = None
    
    while True:
        try:
            source_code = input('> ')
            if source_code.lower() in ['exit', 'quit']:
                break
            elif source_code.lower() == 'save' and ast is not None:
                save_ast(ast, f"repl_session_{count}.hd")
                count += 1
                continue
                
            tokens = lexer.tokenize(source_code)
            ast = parser.parse(tokens)
            result = interpreter.interpret(ast)
            
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {str(e)}")
            ast = None

def print_version():
    """Print version information"""
    print("Holy-D Language Interpreter v0.1.0")

def main():
    """Main entry point for the Holy-D language CLI using argparse"""
    parser = argparse.ArgumentParser(description="Holy-D Language Interpreter")
    parser.add_argument("script", nargs="?", help="Holy-D script file to run")
    parser.add_argument("--version", action="store_true", help="Show version information and exit")
    args = parser.parse_args()

    if args.version:
        print_version()
    elif args.script:
        run_file(args.script)
    else:
        run_repl()

if __name__ == "__main__":
    main()
