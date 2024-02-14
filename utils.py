"""
Author: Michael Drob
Contact: https://www.linkedin.com/in/michael-drob/
License: Apache 2.0

This program is free software: you can redistribute it and/or modify
it under the terms of the Apache License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Apache License for more details.

You should have received a copy of the Apache License
along with this program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.
"""

import re
from tqdm.asyncio import tqdm
import multiprocessing
from queue import Empty
from multiprocessing import Queue

def eval_llm_output(llm_output, test_list, timeout=5):  # timeout in seconds
    def execute_tests(exec_globals, modified_test_list, result_queue):
        try:
            for test in modified_test_list:
                exec(test, exec_globals)
        except Exception as e:
            print('test case failed:', e)
            result_queue.put(False)
            return
        result_queue.put(True)
    
    try:
        # Extract the Python function code and function name
        function_code = re.search(r'\[PYTHON\](.*?)\[/PYTHON\]', llm_output, re.DOTALL).group(1).strip()
        function_name = re.search(r'def (\w+)\(', function_code).group(1)
    except Exception as e:
        print('parsing failed:', e)
        return False

    try:
        # Prepare the environment
        exec_globals = {}
        exec(function_code, exec_globals)
    except Exception as e:
        print('exec failed:', e)
        return False
    
    modified_test_list = []
    for test in test_list:
        try:
            pattern = re.search(r'assert (\w+)\(', test).group(1)
            modified_test = test.replace(pattern, function_name)
            modified_test_list.append(modified_test)
        except Exception as e:
            print('Error modifying test case:', e)
            return False

    result_queue = Queue()
    #The reason to use multiprocessing is to avoid timeouts from endless loops returned by the llm
    process = multiprocessing.Process(target=execute_tests, args=(exec_globals, modified_test_list, result_queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        print('Execution timed out')
        return False

    try:
        result = result_queue.get_nowait()
        return result
    except Empty:
        print('No result received from test execution process.')
        return False

def eval_llm_top_k(llm_outputs, test_list, k):
    """
    Evaluates LLM outputs against a set of test cases up to a specified number of attempts (k thresholds).
    
    This function iterates through a list of LLM outputs, applying each to a given list of test cases
    using the eval_llm_output function, until a successful evaluation is found or the list is exhausted.
    Success within the bounds of each threshold in 'k' is tracked and reported.

    Args:
        llm_outputs (list of str): A list of strings, each representing an LLM output that includes
                                   Python code to be tested.
        test_list (list of str): A list of test case strings that are to be executed against the LLM output.
                                 Each test case should be a Python assert statement.
        k (list of int): A list of integers in increasing order, each representing a threshold for the
                         number of attempts to find a successful LLM output. The function returns a list
                         of booleans indicating success within each threshold.

    Returns:
        list of bool: A list of boolean values the same length as 'k'. Each element represents whether
                      a successful LLM output was found in fewer than or equal to the corresponding number
                      of attempts. For example, if 'k' is [10, 100] and the seventh LLM output is the first
                      to pass all tests, the function returns [True, True]. If no successful LLM output is
                      found within the attempts, or if the successful attempt is beyond a 'k' threshold, the
                      corresponding value is False.

    Note: This function depends on the eval_llm_output function to evaluate each LLM output. Ensure that
          eval_llm_output is correctly defined and accessible within the same scope.
    """
    # Initialize a list to keep track of successes within the k thresholds
    results = [False] * len(k)
    # Counter for attempts
    attempts = 0

    # Loop through each llm_output
    for llm_output in llm_outputs:
        attempts += 1
        # Try evaluating the current llm_output
        if eval_llm_output(llm_output, test_list):
            # If eval_llm_output returns True, update results based on attempts
            for i, threshold in enumerate(k):
                if attempts <= threshold:
                    results[i] = True
            # Since we found a successful attempt, no need to continue
            break
        # If we've tried as many times as the largest number in k, stop trying
        if attempts >= max(k):
            break
    
    # Return the results list, indicating success within each threshold
    return results

async def generate_solutions_async(task, tests, MODELS, client, k=10, model_index=0, use_adapter=False, adapter_id=None):
    solutions = []
    model = MODELS[model_index]  # Select the model configuration based on the provided index
    generate_params = model["parameters"]  # Get generation parameters from the model configuration

    # Prepare the prompt using the model's chatPromptTemplate if necessary
    if model.get("preprompt"):
        prompt = model["preprompt"] + task + tests
    prompt_template = model["chatPromptTemplate"].format(task=task, tests=tests)
    
    for _ in range(k):  # Assuming each call generates one solution
        if use_adapter and adapter_id:
            generate_params["adapter_id"] = adapter_id
        else:
            generate_params.pop("adapter_id", None)  # Remove adapter_id if it exists

        # Generate the solution asynchronously
        response = await client.generate(prompt_template, **generate_params)
        solutions.append(response.generated_text)

    return solutions

def generate_solutions(task, tests, k=10, model_index=0, use_adapter=False, adapter_id=None):
    solutions = []
    model = MODELS[model_index]  # Select the model configuration based on the provided index
    generate_params = model["parameters"]  # Get generation parameters from the model configuration
    
    # Prepare the prompt using the model's chatPromptTemplate if necessary
    if model["preprompt"]:
        prompt = model["preprompt"] + task + tests
    prompt_template = model["chatPromptTemplate"].format(task=task, tests=tests)
    
    for _ in range(k):  # Assuming each call generates one solution
        if use_adapter and adapter_id:
            generate_params["adapter_id"] = adapter_id
        else:
            generate_params.pop("adapter_id", None)  # Remove adapter_id if it exists
        
        # Generate the solution
        response = client.generate(prompt_template, **generate_params)
        solutions.append(response.generated_text)
    return solutions

async def generate_and_evaluate_problems_async(dataset, MODELS, client):
    pass_at_1 = 0

    async for i, problem in tqdm(enumerate(dataset['test']), desc="Processing Problems", total=len(dataset['test'])):
        task = problem['text']
        test_cases = problem['test_list']

        async def retry_solutions(task, test_cases, attempts=3):
            for attempt in range(attempts):
                try:
                    solutions = await generate_solutions_async(task, str(test_cases), MODELS, client, k=1)
                    return solutions
                except Exception as e:
                    print(f'Attempt {attempt + 1} failed with error:', e)
                    if attempt == attempts - 1:
                        raise

        try:
            solutions = await retry_solutions(task, test_cases)
            print(f"evaluating problem {i}")
            print("task: ", task)
            print("solutions: ", solutions)

            if eval_llm_top_k(solutions, test_cases, [1])[0]:
                pass_at_1 += 1
                print('passed')
            else:
                print('failed')

            print(f'running average {pass_at_1/(i+1)}, {pass_at_1} correct, {i+1} total')
            print()
        except Exception as e:
            print('Could not process the problem due to an error:', e)


