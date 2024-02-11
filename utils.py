import re

def eval_llm_output(llm_output, test_list):
    try:
        # Step 1: Extract the Python function code and function name from the LLM output
        function_code = re.search(r'\[PYTHON\](.*?)\[/PYTHON\]', llm_output, re.DOTALL).group(1).strip()
        function_name = re.search(r'def (\w+)\(', function_code).group(1)
    except Exception as e:
        print('parsing failed:', e)
        return False
    
    # Prepare the environment to execute the code
    exec_globals = {}
    exec(function_code, exec_globals)
    
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

def evaluate_top_outputs_efficient(llm_output_list, top, test_list):
    """
    Efficiently evaluates the top x elements from llm_output_list using eval_llm_output and checks if any
    of the evaluations up to the top x positions are true, without redundant evaluations.
    
    Parameters:
    - llm_output_list: List of LLM outputs.
    - top: List of integers, each indicating up to which position to check for a true evaluation.
    - test_list: The test cases to be used with eval_llm_output.
    
    Returns:
    - A list of booleans, each corresponding to whether any of the top x elements evaluated to true.
    """
    results = [False] * len(top)  # Initialize result list with False
    eval_results = []  # Track evaluation results to avoid re-evaluation
    
    # Sort top to handle in ascending order; this ensures efficiency in traversal
    sorted_top_indices = sorted((val, idx) for idx, val in enumerate(top))
    max_top = sorted_top_indices[-1][0]  # Get the maximum top value for early stopping
    
    current_true_found = False
    for i, llm_output in enumerate(llm_output_list):
        if i >= max_top:
            break  # Stop if we've evaluated up to the maximum top value
        
        # Evaluate current llm_output only if not already evaluated
        eval_result = eval_llm_output(llm_output, test_list)
        eval_results.append(eval_result)
        
        if eval_result:
            current_true_found = True  # Mark true found for this and subsequent top values
        
        # Update the results list based on current evaluation
        for top_val, top_idx in sorted_top_indices:
            if i < top_val:
                results[top_idx] = results[top_idx] or current_true_found
        
        if current_true_found:
            # If a true result is found, all subsequent tops are updated, break early if possible
            if all(results[idx] for _, idx in sorted_top_indices if i < _):
                break
    
    return results