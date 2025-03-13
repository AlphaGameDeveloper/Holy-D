# Holy-D Language

Holy-D is a burning trash fire of a programming language

## Features

- **Curly-braces Syntax**: Familiar syntax for developers coming from languages like C, C++, and Java.
- **Expandable**: The architecture allows for future enhancements and additions to the language features.
- **Lexer, Parser, Interpreter, and Compiler**: A complete toolchain for processing and executing Holy-D code.

## Built-in Functions

Holy-D provides several built-in functions to facilitate common operations:

- `print(message)`: Display text without a newline
- `println(message)`: Display text with a newline
- `sleep(seconds)`: Pause execution for the specified number of seconds
- `exit([code])`: Exit the program with an optional exit code (default is 0)

## Installation

To get started with Holy-D, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/holy-d.git
cd holy-d
pip install -r requirements.txt
```

## Usage

After installation, you can start writing your Holy-D programs. Here’s a simple example:

```holy-d
enter {
    println("Hello, World!");
}
```

To run your Holy-D code, use the interpreter:

```bash
python src/main.py your_program.hd
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.