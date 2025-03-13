import time
import sys

class Interpreter:
    def __init__(self, parser=None):
        self.parser = parser
        self.environment = {}  # Global scope
        self.functions = {}    # Function definitions

    def interpret(self, ast=None):
        if ast is None and self.parser:
            ast = self.parser.parse()
        
        if ast["type"] == "Program":
            # First pass: register all functions
            for node in ast["body"]:
                if node["type"] == "FunctionDeclaration":
                    self.functions[node["name"]] = node
            
            # Second pass: execute entry point if exists
            for node in ast["body"]:
                if node["type"] == "EntryPoint":
                    self.execute_statements(node["body"])
            
            return self.environment
        else:
            return self.visit_node(ast)

    def visit_node(self, node):
        method_name = f'visit_{node["type"]}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node['type']} method defined")

    def execute_statements(self, statements):
        result = None
        for statement in statements:
            result = self.visit_node(statement)
        return result

    def visit_FunctionDeclaration(self, node):
        # Function declarations are handled in the first pass
        pass

    def visit_EntryPoint(self, node):
        return self.execute_statements(node["body"])

    def visit_PrintStatement(self, node):
        value = self.visit_node(node["expression"])
        if node["newline"]:
            print(value)
        else:
            print(value, end="", flush=True)
        return None

    def visit_CallStatement(self, node):
        function_name = node["name"]
        
        # Handle built-in functions
        if function_name in ["sleep", "exit"]:
            # Evaluate arguments
            args = [self.visit_node(arg) for arg in node["arguments"]] if "arguments" in node else []
            
            if function_name == "sleep":
                if not args:
                    raise TypeError("sleep() takes exactly 1 argument (0 given)")
                time.sleep(float(args[0]))
                return None
            elif function_name == "exit":
                exit_code = 0
                if args:
                    exit_code = int(args[0])
                sys.exit(exit_code)
                return None
        
        # Handle user-defined functions
        if function_name not in self.functions:
            line = node.get("line", "unknown")
            raise NameError(f"Function '{function_name}' not defined at line {line}")
        
        function_def = self.functions[function_name]
        
        # Create a new scope for function execution
        previous_env = self.environment.copy()
        
        # Handle arguments if provided
        if "arguments" in node and node["arguments"] and len(function_def["params"]) > 0:
            # Evaluate arguments
            arg_values = [self.visit_node(arg) for arg in node["arguments"]]
            
            # Add arguments to function's environment
            for i, param_name in enumerate(function_def["params"]):
                if i < len(arg_values):
                    self.environment[param_name] = arg_values[i]
        
        # Execute function body
        result = self.execute_statements(function_def["body"])
        
        # Restore previous environment
        self.environment = previous_env
        
        return result

    def visit_FunctionCall(self, node):
        function_name = node["name"]
        
        # For built-in functions
        if function_name in ["print", "println", "sleep", "exit"]:
            args = [self.visit_node(arg) for arg in node["arguments"]]
            if function_name == "println":
                print(*args)
            elif function_name == "print":
                print(*args, end="")
            elif function_name == "sleep":
                if not args:
                    raise TypeError("sleep() takes exactly 1 argument (0 given)")
                time.sleep(float(args[0]))
            elif function_name == "exit":
                exit_code = 0
                if args:
                    exit_code = int(args[0])
                sys.exit(exit_code)
            return None
            
        # For user-defined functions
        if function_name not in self.functions:
            line = node.get("line", "unknown")
            raise NameError(f"Function '{function_name}' not defined at line {line}")
        
        function_def = self.functions[function_name]
        
        # Create a new scope for function execution
        previous_env = self.environment.copy()
        
        # Execute function body
        result = self.execute_statements(function_def["body"])
        
        # Restore previous environment
        self.environment = previous_env
        
        return result

    def visit_StringLiteral(self, node):
        return node["value"]

    def visit_NumericLiteral(self, node):
        return node["value"]

    def visit_Identifier(self, node):
        name = node["name"]
        if name in self.environment:
            return self.environment[name]
        raise NameError(f"Variable '{name}' not defined")

    def visit_BinaryExpression(self, node):
        left = self.visit_node(node["left"])
        right = self.visit_node(node["right"])
        
        if node["operator"] == "+":
            return left + right
        elif node["operator"] == "-":
            return left - right
        elif node["operator"] == "*":
            return left * right
        elif node["operator"] == "/":
            return left / right
        else:
            raise ValueError(f"Unknown operator: {node['operator']}")

    def visit_AssignmentStatement(self, node):
        """Execute an assignment statement."""
        var_name = node["name"]
        value = self.visit_node(node["value"])
        
        # Store the value in the environment
        self.environment[var_name] = value
        
        return value