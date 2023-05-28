# CodeGenerator

🤖 Generate code snippets effortlessly with the CodeGenerator!

The CodeGenerator is a Python class that utilizes the power of pre-trained language models to generate code snippets based on different prompt styles. Whether you need to complete partial code snippets, generate function signatures, add comments or docstrings, the CodeGenerator has got you covered!

## Features

✨ Easy-to-use: Generate code snippets with just a few lines of code.

⚙️ Customizable: Control the length, temperature, and sampling techniques for code generation.

🌐 Multi-language support: Generate code in various programming languages, including Python, Java, C++, and more.

🔌 Extensible: Easily add new prompt styles to expand the capabilities of code generation.

## Usage

1. Install the required dependencies:

```shell
pip install transformers
```

2. Create an instance of the CodeGenerator class:

```python
from CodeGenerator import CodeGenerator

generator = CodeGenerator()
```

3. Choose a prompt style and generate code:

```python
input_text = "<prompt_prefix>your prompt here"
output_file = "output.py"

generator.generate_code(input_text, output_file)
```

4. Enjoy your generated code!

## Prompt Styles

The CodeGenerator supports the following prompt styles:

- "Fill in the Middle": Complete code snippets by filling in the missing parts.

- "Function Signature": Generate function signatures based on provided inputs.

- "Comment": Add comments to code snippets to describe their purpose.

- "Docstring": Generate docstrings for code snippets to provide documentation.

## Examples

Check out the `examples` directory for code samples and generated outputs for different prompt styles.

## Contributing

👍 Contributions are welcome! If you have any ideas, bug reports, or feature requests, please submit them via issues or pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
```
```

