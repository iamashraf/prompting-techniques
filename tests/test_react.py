from prompting_techniques.techniques.react import calculate, extract_action


def test_calculate_adds_correctly():
    assert calculate("850000 + 1200000") == "2050000"


def test_calculate_strips_thousands_separators():
    assert calculate("850,000 + 1,200,000") == "2050000"


def test_calculate_rejects_names_and_calls():
    assert calculate("__import__('os').system('echo hi')").startswith("Error")


def test_calculate_rejects_exponentiation():
    assert calculate("9**9").startswith("Error")


def test_calculate_rejects_expressions_over_the_length_cap():
    assert calculate("1+" * 150 + "1").startswith("Error")


def test_extract_action_returns_expression_and_truncated_response():
    response = "Thought: I should add these.\nAction: calculate[1 + 2]\nObservation: 3 (hallucinated)"

    result = extract_action(response)

    assert result is not None
    expression, truncated = result
    assert expression == "1 + 2"
    assert truncated == "Thought: I should add these.\nAction: calculate[1 + 2]"
    assert "Observation" not in truncated


def test_extract_action_returns_none_when_there_is_no_action():
    assert extract_action("Final Answer: here is the report") is None
