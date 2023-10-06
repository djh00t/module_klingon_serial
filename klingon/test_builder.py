import os
import ast
import openai
import logging
import re
import subprocess
import tokenize
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

IGNORE = [
    ".git/", 
    ".pytest_cache/", 
    "docs/", 
    "setup.py", 
    "klingon/test_builder.py", 
    "tests/"
]

def find_python_scripts(directory):
    logger.info(f"Finding Python scripts in directory: {directory}")
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in IGNORE]
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def filter_scripts(scripts, ignore_list):
    filtered_scripts = [script for script in scripts if not any(script.startswith(i) for i in ignore_list)]
    logger.info(f"Filtered {len(filtered_scripts)} scripts")
    return filtered_scripts

def inspect_scripts(scripts):
    logger.info(f"Inspecting {len(scripts)} scripts")
    for script in scripts:
        logger.debug(f"Inspecting script: {script}")
        try:
            with open(script) as f:
                code = f.read()
            # ignore strings enclosed in backticks
            code = re.sub(r'`.*?`', '', code, flags=re.DOTALL)
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    yield script, node.name
        except SyntaxError:
            logger.warning(f"Skipping file due to SyntaxError: {script}")


def check_existing_tests(functions):
    functions = list(functions)
    logger.info(f"Checking existing tests for {len(functions)} functions")
    for script, function in functions:
        test_file = "test_" + os.path.basename(script)
        if os.path.exists(test_file):
            with open(test_file) as f:
                if f"def test_{function}()" in f.read():
                    yield script, function, True
                else:
                    yield script, function, False
        else:
            yield script, function, False

def chunk_prompt(prompt, max_length=4090):
    tokens = prompt.split(' ')
    chunks = []
    chunk = []
    length = 0
    for token in tokens:
        if length + len(token) > max_length:
            chunks.append((' '.join(chunk), length))
            chunk = []
            length = 0
        chunk.append(token)
        length += len(token)
    if chunk:
        chunks.append((' '.join(chunk), length))
    return chunks

def generate_tests(functions):
    functions = list(functions)
    logger.info(f"Generating tests for {len(functions)} functions")
    for script, function, exists in functions:
        if not exists:
            retries = 0
            while retries < 3:
                try:
                    # code to generate test using openai
                    with open(script) as f:
                        code_to_test = f.read()
                    prompt = f"Generate pytest tests that cover 100% of the following code:\n\n```python\n{code_to_test}\n```\n\nEnsure that the tests cover all edge cases and provide meaningful assertions. Only return the testing code as a snippet. Do not include any comments."
                    prompt_chunks = chunk_prompt(prompt)
                    responses = []
                    for chunk, length in prompt_chunks:
                        max_tokens = min(length - 100, 4096)
                        response = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=chunk, max_tokens=max_tokens)
                        responses.append(response)
                    test = "\n" + response.choices[0].text.strip()
                    # convert markdown comments to Google docstring comments
                    test = '\n'.join('# ' + line[3:] if line.startswith('```') else line for line in test.split('\n'))
                    # parse the test code to extract import statements and TODO comments
                    import_lines = [line for line in test.split('\n') if line.startswith('import') or line.startswith('from')]
                    todo_lines = [line for line in test.split('\n') if 'TODO' in line]
                    other_lines = [line for line in test.split('\n') if line not in import_lines and line not in todo_lines]

                    # Add import statement for pytest if it doesn't already exist
                    if "import pytest" not in import_lines:
                        import_lines.insert(0, "import pytest")

                    # replace TODO comments with real working code
                    for todo_line in todo_lines:
                        function_name = todo_line.split(' ')[-1]
                        other_lines.append(f"def test_{function_name}():\n    assert {function_name}() == 'expected_result'")
                    # print the test code
                    print(f"Test code for function {function} in script {script}:\n{test}")
                    # save the test immediately, one file per function
                    test_file = f"tests/test_{os.path.splitext(os.path.basename(script))[0]}_{function}.py"
                    with open(test_file, "w") as f:
                        # write import statements at the top
                        f.write('\n'.join([line + '  # type: ignore' if 'netifaces2' in line or 'strtobool' in line else line for line in import_lines]))
                        f.write('\n\n')  # Add an extra newline here
                        # write the rest of the test code
                        f.write('\n'.join(other_lines))
                        f.write('\n')
                    # format and check the test file
                    format_and_check_test_file(test_file)
                    break
                except subprocess.CalledProcessError:
                    retries += 1
                    logger.warning(f"Formatting failed for {test_file}. Retrying {retries} of 3 times.")
            if retries == 3:
                logger.error(f"Failed to format {test_file} after 3 retries.")

def save_tests(tests):
    # no need to save tests here as they are saved in generate_tests
    pass

def find_imports(script):
    with open(script) as f:
        tree = ast.parse(f.read())
    return [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]

def find_missing_requirements(scripts):
    all_imports = set()
    for script in scripts:
        all_imports.update(find_imports(script))
    with open("requirements.txt") as f:
        requirements = {line.strip() for line in f if line.strip() and not line.startswith("#")}
    return all_imports - requirements

def format_and_check_test_file(test_file):
    # format the test file using black
    subprocess.run(["black", test_file], check=True)
    # check the test file using mypy
    subprocess.run(["mypy", test_file], check=True)

if __name__ == "__main__":
    logger.info("Starting test builder")
    directory = "."
    scripts = find_python_scripts(directory)
    scripts = filter_scripts(scripts, IGNORE)
    functions = inspect_scripts(scripts)
    functions = check_existing_tests(functions)
    tests = generate_tests(functions)
    save_tests(tests)
    missing_requirements = find_missing_requirements(scripts)
    if missing_requirements:
        logger.warning(f"Missing requirements: {', '.join(missing_requirements)}")
    logger.info("Finished test builder")
