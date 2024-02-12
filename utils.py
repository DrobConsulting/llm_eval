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

def eval_llm_output(llm_output, test_list):
    try:
        # Step 1: Extract the Python function code and function name from the LLM output
        function_code = re.search(r'\[PYTHON\](.*?)\[/PYTHON\]', llm_output, re.DOTALL).group(1).strip()
        function_name = re.search(r'def (\w+)\(', function_code).group(1)
    except Exception as e:
        print('parsing failed:', e)
        return False

    try:
        # Prepare the environment to execute the code
        exec_globals = {}
        exec(function_code, exec_globals)
    except Exception as e:
        print('exec failed:', e)
        return False
    
    # Step 2: Dynamically modify the `test_list` to use the extracted function name
    modified_test_list = []
    for test in test_list:
        try:
            # Extracting the existing function name pattern from the test case
            pattern = re.search(r'assert (\w+)\(', test).group(1)
            # Replace the extracted pattern with the correct function name
            modified_test = test.replace(pattern, function_name)
            modified_test_list.append(modified_test)
        except Exception as e:
            print('Error modifying test case:', e)
            return False
    
    # Step 3: Execute the modified test cases
    try:
        for test in modified_test_list:
            exec(test, exec_globals)
    except Exception as e:
        print('test case failed:', e)
        return False
    
    # If all tests pass without an assertion error
    return True

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


