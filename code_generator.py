import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
import traceback

load_dotenv()


class CodeGenerator:
    def __init__(self, checkpoint="bigcode/tiny_starcoder_py", device="cuda"):
        self.checkpoint = checkpoint
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.model = AutoModelForCausalLM.from_pretrained(self.checkpoint).to(self.device)

        self.prompt_methods = {
            "Fill in the Middle": self._generate_fill_in_the_middle,
            "Function Signature": self._generate_function_signature,
            "Comment": self._generate_comment,
            "Docstring": self._generate_docstring,
        }

    def generate(
        self,
        input_text: str,
        max_new_tokens: int,
        temperature: float = 0.8,
        top_k: int = 100,
        top_p: float = 0.9,
        repetition_penalty: float = 1.0
    ) -> str:
        inputs = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)

        try:
            outputs = self.model.generate(
                inputs,
                pad_token_id=self.tokenizer.eos_token_id,
                max_length=max_new_tokens + inputs.shape[-1],
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=repetition_penalty
            )
            generated_code = self.tokenizer.decode(outputs[0])
        except Exception as e:
            error_message = f"Code generation failed with error: {str(e)}"
            traceback.print_exc()  # Print the full traceback for debugging
            raise ValueError(error_message) from e

        return generated_code

    def generate_code(self, input_text: str, output_file: str) -> None:
        input_text = input_text.strip()

        # Calculate the number of tokens in the input text
        num_tokens_input = len(self.tokenizer(input_text)["input_ids"])

        # Calculate the maximum number of tokens to generate, capped at 8000 tokens
        max_new_tokens = min(num_tokens_input + 8000, 8000)

        prompt_type = self._extract_prompt_type(input_text)

        generated_code = self.prompt_methods[prompt_type](input_text, max_new_tokens)

        # Write the generated code to the output file
        with open(output_file, "w") as file:
            file.write(generated_code)


    def _extract_prompt_type(self, input_text: str) -> str:
        stripped_input_text = input_text.strip()
        for prompt_type in self.prompt_methods:
            stripped_prompt_type = prompt_type.strip()
            if stripped_input_text.startswith(stripped_prompt_type):
                return prompt_type
        return "Fill in the Middle"  # Default to "Fill in the Middle" if no prompt type is found



    def _generate_fill_in_the_middle(self, input_text: str, num_tokens: int) -> str:
        return self.generate(input_text, max_new_tokens=num_tokens)

    def _generate_function_signature(self, input_text: str, num_tokens: int) -> str:
        signature = input_text[4:].strip()
        try:
            return self.generate(f"def {signature}:", max_new_tokens=num_tokens)
        except Exception as e:
            error_message = f"Failed to generate code with function signature '{signature}': {str(e)}"
            traceback.print_exc()  # Print the full traceback for debugging
            raise ValueError(error_message) from e

    def _generate_comment(self, input_text: str, num_tokens: int) -> str:
        comment = input_text[2:].strip()
        try:
            return self.generate(f"# {comment}\n", max_new_tokens=num_tokens)
        except Exception as e:
            error_message = f"Failed to generate code with comment '{comment}': {str(e)}"
            traceback.print_exc()  # Print the full traceback for debugging
            raise ValueError(error_message) from e

    def _generate_docstring(self, input_text: str, num_tokens: int) -> str:
        docstring = input_text[3:-3].strip()
        try:
            return self.generate(f"\"\"\" {docstring} \"\"\"\n", max_new_tokens=num_tokens)
        except Exception as e:
            error_message = f"Failed to generate code with docstring '{docstring}': {str(e)}"
            traceback.print_exc()  # Print the full traceback for debugging
            raise ValueError(error_message) from e


# Example usage
generator = CodeGenerator()

# Example 1: Generating code for "Fill in the Middle" prompt style
input_text = "<fim_prefix>Initialize a list with 10 elements"
output_file = "output1.py"
generator.generate_code(input_text, output_file)

# Example 2: Generating code for "Function Signature" prompt style
input_text = "def multiply(a, b):"
output_file = "output2.py"
generator.generate_code(input_text, output_file)

# Example 3: Generating code for "Comment" prompt style
input_text = "# This function calculates the factorial of a number"
output_file = "output3.py"
generator.generate_code(input_text, output_file)

# Example 4: Generating code for "Docstring" prompt style
input_text = '"""This function performs matrix multiplication"""'
output_file = "output4.py"
generator.generate_code(input_text, output_file)
