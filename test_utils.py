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

import pytest
from utils import eval_llm_output, eval_llm_top_k 

def test_eval_llm_output_success():
    llm_output = """
    [PYTHON]
    def max_sum(my_list):
        return max([sum(x) for x in my_list])
    [/PYTHON]
    """
    test_list = [
        'assert max_sum([[1, 2, 3], [4, 5, 6], [10, 11, 12], [7, 8, 9]]) == 33',
        'assert max_sum([[0, 1, 1], [1, 1, 2], [3, 2, 1]]) == 6',
        'assert max_sum([[0, 1, 3], [1, 2, 1], [9, 8, 2], [0, 1, 0], [6, 4, 8]]) == 19',
        'assert max_sum([[0, -1, -1], [-1, -1, -2], [-3, -2, -1]]) == -2'
    ]
    
    assert eval_llm_output(llm_output, test_list) == True

def test_eval_llm_output_failure():
    llm_output = """
    [PYTHON]
    def max_sum_wrong(my_list):
        # Incorrect implementation on purpose
        return sum([sum(x) for x in my_list])
    [/PYTHON]
    """
    test_list = [
        'assert max_sum_wrong([[1, 2, 3], [4, 5, 6], [10, 11, 12], [7, 8, 9]]) == 33',
        'assert max_sum_wrong([[0, 1, 1], [1, 1, 2], [3, 2, 1]]) == 6',
        'assert max_sum_wrong([[0, 1, 3], [1, 2, 1], [9, 8, 2], [0, 1, 0], [6, 4, 8]]) == 19',
        'assert max_sum_wrong([[0, -1, -1], [-1, -1, -2], [-3, -2, -1]]) == -2'
    ]
    
    assert eval_llm_output(llm_output, test_list) == False

def test_eval_llm_output_sphere_volume_success():
    llm_output = """
    [PYTHON]
    def get_sphere_volume(radius):
        import math
        return (4/3) * math.pi * radius**3
    [/PYTHON]
    """
    test_list = [
        'assert get_sphere_volume(10) == 4188.790204786391',
        'assert get_sphere_volume(25) == 65449.84694978735',
        'assert get_sphere_volume(20) == 33510.32163829113'
    ]
    
    assert eval_llm_output(llm_output, test_list) == True

def test_eval_llm_output_sphere_volume_failure():
    llm_output = """
    [PYTHON]
    def get_sphere_volume_incorrect(radius):
        # Incorrect implementation on purpose
        return 2 * radius**3
    [/PYTHON]
    """
    test_list = [
        'assert get_sphere_volume_incorrect(10) == 4188.790204786391',
        'assert get_sphere_volume_incorrect(25) == 65449.84694978735',
        'assert get_sphere_volume_incorrect(20) == 33510.32163829113'
    ]
    
    assert eval_llm_output(llm_output, test_list) == False

@pytest.fixture
def mock_eval_function(monkeypatch):
    def mock_eval_llm_output(llm_output, test_list):
        return "success" in llm_output

    monkeypatch.setattr("utils.eval_llm_output", mock_eval_llm_output)

def test_eval_llm_top_k_all_success(mock_eval_function):
    llm_outputs = ["fail", "fail", "success"]
    test_list = []  # Test list is irrelevant for this mock
    k = [3, 4, 5]
    expected = [True, True, True]
    actual = eval_llm_top_k(llm_outputs, test_list, k)
    assert actual == expected

def test_eval_llm_top_k_partial_success(mock_eval_function):
    llm_outputs = ["fail"] * 5 + ["success"]
    test_list = []  # Test list is irrelevant for this mock
    k = [5, 6, 10]
    expected = [False, True, True]
    actual = eval_llm_top_k(llm_outputs, test_list, k)
    assert actual == expected

def test_eval_llm_top_k_no_success(mock_eval_function):
    llm_outputs = ["fail"] * 10
    test_list = []  # Test list is irrelevant for this mock
    k = [5, 8]
    expected = [False, False]
    actual = eval_llm_top_k(llm_outputs, test_list, k)
    assert actual == expected

def test_eval_llm_top_k_empty_outputs(mock_eval_function):
    llm_outputs = []
    test_list = []
    k = [1, 2]
    expected = [False, False]
    actual = eval_llm_top_k(llm_outputs, test_list, k)
    assert actual == expected


