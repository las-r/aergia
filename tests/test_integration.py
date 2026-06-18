from aergia.lexer import tokenize
from aergia.parser import parse
from aergia.nodes import Environment

def run_aergia(code):
    """
    Simulates the interpreter pipeline: 
    Lexes, parses, and executes code in a clean environment.
    """
    env = Environment()
    tokens = tokenize(code)
    ast = parse(tokens)
    
    for node in ast:
        if node:
            node.eval(env)
    return env

def test_full_math_pipeline(capsys):
    """Verifies that math, variables, and output work together."""
    code = """
    = x 10
    = y 20
    = result +x y
    > result
    """
    env = run_aergia(code)
    
    # Check variable state
    assert env["result"] == 30
    
    # Check console output
    captured = capsys.readouterr()
    assert captured.out.strip() == "30"

def test_array_lifecycle(capsys):
    """Verifies complex array manipulation."""
    code = """
    = arr < 1 2 3 >
    +: arr 4
    = item -: arr
    > item
    """
    env = run_aergia(code)
    
    # Verify the popped item and the remaining array
    assert env["item"] == 4
    assert env["arr"] == [1, 2, 3]
    
    captured = capsys.readouterr()
    assert captured.out.strip() == "4"

def test_if_logic_flow(capsys):
    """Verifies control flow logic."""
    code = """
    = x 5
    (== x 5 > "Correct")
    """
    run_aergia(code)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Correct"
    