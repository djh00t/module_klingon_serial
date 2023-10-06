import os
import ast
import openai
import logging
import re
import subprocess
import tokenize
from io import BytesIO
import pdb

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

IGNORE = [
    "./.git/", 
    "./.pytest_cache/", 
    "./docs/", 
    "./setup.py", 
    "./klingon/test_builder.py",
    "./klingon/openai_billing.py", 
    "./tests/"
]

def find_python_scripts(directory):
    """
    Find all Python scripts in a given directory.

    Args:
        directory (str): The directory to search for Python scripts.

    Yields:
        str: The path to a Python script.
    """
    logger.info(f"Finding Python scripts in directory: {directory}")
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in IGNORE]
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def filter_scripts(scripts, ignore_list):
    """
    Filter out scripts that should be ignored.

    Args:
        scripts (list): The list of scripts to filter.
        ignore_list (list): The list of scripts to ignore.

    Returns:
        list: The filtered list of scripts.
    """
    filtered_scripts = [script for script in scripts if not any(script.startswith(i) for i in ignore_list)]
    logger.info(f"Filtered {len(filtered_scripts)} scripts")
    return filtered_scripts


def inspect_scripts(scripts):
    """
    Inspect Python scripts to find functions.

    Args:
        scripts (list): The list of scripts to inspect.

    Yields:
        tuple: A tuple containing the path to a script and the name of a function.
    """
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
    """
    Check if tests already exist for a list of functions.

    Args:
        functions (list): The list of functions to check for tests.

    Yields:
        tuple: A tuple containing the path to a script, the name of a function, and a boolean indicating whether a test exists.
    """
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

def chunk_prompt(prompt, max_length=2500):
    """
    Chunk a prompt into smaller pieces.

    Args:
        prompt (str): The prompt to chunk.
        max_length (int, optional): The maximum length of a chunk. Defaults to 2500.

    Returns:
        list: A list of chunks.
    """
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
    """
    Generate tests for a list of functions.

    Args:
        functions (list): The list of functions to generate tests for.

    Yields:
        str: The generated test code.
    """
    functions = list(functions)
    logger.info(f"Generating tests for {len(functions)} functions")
    for script, function, exists in functions:
        if not exists:
            retries = 0
            while retries < 3:
                try:
                    # code to generate test using openai
                    with open(script) as f:
                        code = f.read()
                    tree = ast.parse(code)
                    function_node = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == function)
                    function_code = ast.unparse(function_node)
                    prompt = f"Generate pytest tests that cover 100% of the following function:\n\n```python\n{function_code}\n```\n\nEnsure that the tests cover edge cases and provide meaningful assertions. Only return the testing code as a snippet. All comments should be prefixed with '# '."
                    prompt_chunks = chunk_prompt(prompt)
                    responses = []
                    for chunk, length in prompt_chunks:
                        max_tokens = min(length - 100, 4096)
                        response = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=chunk, max_tokens=max_tokens, timeout=30)
                        responses.append(response)
                    while True:
                        test = "\n" + response.choices[0].text.strip()
                        # convert markdown comments to Google docstring comments
                        test = '\n'.join('# ' + line[3:] if line.startswith('```') else line for line in test.split('\n'))
                        # parse the test code to extract import statements and TODO comments
                        import_lines = [line for line in test.split('\n') if (line.startswith('import') or line.startswith('from')) and not line.startswith('from app import')]
                        try:
                            # try to parse the test code to check if it's valid Python code
                            ast.parse(test)
                            # if the parsing succeeds, break the loop
                            break
                        except SyntaxError:
                            # if the parsing fails, regenerate the test code
                            continue
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
                    directory_name = os.path.dirname(script).replace('./', '').replace('/', '.')
                    module_name = os.path.splitext(os.path.basename(script))[0]
                    test_file = f"tests/test_{module_name}_{function}.py"
                    with open(test_file, "w") as f:
                        # write import statement for the function being tested
                        module_path = os.path.dirname(script).replace('./', '').replace('/', '.')
                        f.write(f"from {module_path}.{module_name} import {function}\n")
                        # write other import statements
                        f.write('\n'.join([line.replace("from distutils.util import strtobool", "from klingon.strtobool import strtobool") + '  # type: ignore' if 'strtobool' in line else line for line in import_lines]))
                        f.write('\n\n')  # Add an extra newline here
                        # write the rest of the test code
                        f.write('\n'.join(other_lines))
                        f.write('\n')
                    # format and check the test file
                    format_and_check_test_file(test_file)
                    # run the test file using pytest
                    pytest_result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
                    if pytest_result.returncode != 0:
                        # if pytest fails, send the result and the test code to the OpenAI API to debug
                        debug_prompt = f"Debug the following pytest failure:\n\n{pytest_result.stdout}\n\nThe test code is:\n\n```python\n{test}\n``` Only respond with a code snippet solution, no comments."
                        #debug_response = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=debug_prompt, max_tokens=200, timeout=30)
                        debug_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are the worlds best python unit test writer."}, {"role": "user", "content": debug_prompt}], max_tokens=200)
                        print(f"Debugging advice from OpenAI:\n\n{debug_response.choices[0].text.strip()}")
                        retries += 1
                        if retries == 3:
                            logger.error(f"Failed to fix test for function {function} in script {script} after 3 retries. Skipping this test.")
                            break
                    else:
                        break
                except subprocess.CalledProcessError:
                    logger.warning(f"Retry attempt {retries+1} for {script}")
                    retries += 1
                    logger.warning(f"Formatting failed for {test_file}. Retrying {retries} of 3 times.")
            if retries == 3:
                logger.error(f"Failed to format {test_file} after 3 retries.")

def save_tests(tests):
    """
    Save generated tests.

    Args:
        tests (list): The list of generated tests to save.
    """
    # no need to save tests here as they are saved in generate_tests
    pass

def find_imports(script):
    """
    Find all import statements in a script.

    Args:
        script (str): The path to the script.

    Returns:
        list: A list of imported modules.
    """
    with open(script) as f:
        tree = ast.parse(f.read())
    return [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]

def find_missing_requirements(scripts):
    """
    Find all modules that are imported in scripts but not listed in requirements.txt.

    Args:
        scripts (list): The list of scripts to check.

    Returns:
        set: A set of missing requirements.
    """
    all_imports = set()
    for script in scripts:
        all_imports.update(find_imports(script))
    with open("requirements.txt") as f:
        requirements = {line.strip() for line in f if line.strip() and not line.startswith("#")}
    return all_imports - requirements

def format_and_check_test_file(test_file):
    """
    Format and check a test file.

    Args:
        test_file (str): The path to the test file.
    """
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
