import pytest
from utils import eval_llm_output, evaluate_top_outputs_efficient 

def test_eval_llm_output_success():
    llm_output = """
    [PYTHON]
    def max_sum(my_list):
        return max([sum(x) for x in my_list])
    [/PYTHON]
    [TESTS]
    # Test case 1:
    assert max_sum([[1, 2], [3, 4]]) == 7
    # Test case 2:
    assert max_sum([[1, 2], [-3, 4]]) == 3
    # Test case 3:
    assert max_sum([[-1, -2], [-3, -4]]) == -3
    [/TESTS]
    """
    test_list = [
        'assert maximum_Sum([[1,2,3],[4,5,6],[10,11,12],[7,8,9]]) == 33',
        'assert maximum_Sum([[0,1,1],[1,1,2],[3,2,1]]) == 6',
        'assert maximum_Sum([[0,1,3],[1,2,1],[9,8,2],[0,1,0],[6,4,8]]) == 19',
        'assert maximum_Sum([[0,-1,-1],[-1,-1,-2],[-3,-2,-1]]) == -2'
    ]
    
    assert eval_llm_output(llm_output, test_list) == True

def test_eval_llm_output_failure():
    llm_output = """
    [PYTHON]
    def max_sum_wrong(my_list):
        # Incorrect implementation on purpose
        return sum([sum(x) for x in my_list])
    [/PYTHON]
    [TESTS]
    # Test case 1:
    assert max_sum_wrong([[1, 2], [3, 4]]) == 7
    # Test case 2:
    assert max_sum_wrong([[1, 2], [-3, 4]]) == 3
    # Test case 3:
    assert max_sum_wrong([[-1, -2], [-3, -4]]) == -3
    [/TESTS]
    """
    test_list = [
        'assert maximum_Sum([[1,2,3],[4,5,6],[10,11,12],[7,8,9]]) == 33',
        'assert maximum_Sum([[0,1,1],[1,1,2],[3,2,1]]) == 6',
        'assert maximum_Sum([[0,1,3],[1,2,1],[9,8,2],[0,1,0],[6,4,8]]) == 19',
        'assert maximum_Sum([[0,-1,-1],[-1,-1,-2],[-3,-2,-1]]) == -2'
    ]
    
    assert eval_llm_output(llm_output, test_list) == False

# Mock eval_llm_output to simulate different scenarios without running actual evaluations
@pytest.fixture(autouse=True)
def mock_eval_llm_output(monkeypatch):
    def mock_return(llm_output, test_list):
        # Simulate eval_llm_output behavior based on llm_output content
        return "true" in llm_output
    monkeypatch.setattr("utils.eval_llm_output", mock_return)  # Adjust the path as necessary

# Test with various top configurations and expected outcomes
@pytest.mark.parametrize("llm_output_list, top, expected", [
    (["true_result"], [1], [True]),
    (["false_result", "true_result"], [1, 2], [False, True]),
    (["false_result", "false_result", "true_result"], [1, 2, 3], [False, False, True]),
    (["true_result", "false_result", "true_result"], [1, 2, 3], [True, True, True]),
    (["false_result"] * 10 + ["true_result"], [1, 5, 10, 11], [False, False, False, True]),
])
def test_evaluate_top_outputs_efficient(llm_output_list, top, expected):
    assert evaluate_top_outputs_efficient(llm_output_list, top, ["dummy_test"]) == expected

# Test with an empty llm_output_list
def test_empty_llm_output_list():
    assert evaluate_top_outputs_efficient([], [1, 2, 3], ["dummy_test"]) == [False, False, False]

# Test with top values exceeding the llm_output_list length
def test_top_exceeds_llm_output_list_length():
    llm_output_list = ["false_result"] * 5 + ["true_result"]
    top = [5, 10, 15]  # Exceeds the llm_output_list length
    expected = [False, True, True]  # True for tops that exceed the index of the only true_result
    assert evaluate_top_outputs_efficient(llm_output_list, top, ["dummy_test"]) == expected
