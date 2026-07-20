import pytest
from aergia.lexer import tokenize
from aergia.parser import parse
from aergia.nodes import AergiaRuntimeError, Environment

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

def test_unary_type_casting(capsys):
    """Exercises type mutations using standard unary conversions."""
    code = """
    = numeric_str "123"
    = actual_int =. numeric_str
    = actual_float =' numeric_str
    = back_to_str =, actual_int
    
    > +actual_int 7
    > +actual_float 0.5
    """
    run_aergia(code)
    captured = capsys.readouterr()
    assert captured.out.strip().split() == ["130", "123.5"]

def test_lexical_scoping_and_closures():
    """Guarantees child lexical scopes protect local boundaries from dirtying up parent environments."""
    code = """
    = global_var 100
    {local_scope
        = global_var 42
        = shadow_var 999
    }
    @local_scope
    """
    env = run_aergia(code)
    assert env["global_var"] == 42  # Explicit re-assignment changes parent value
    assert "shadow_var" not in env  # Enclosed local scope definitions must drop out

def test_recursive_function_execution(capsys):
    """Runs a classic recursive implementation to confirm standard stack execution patterns."""
    code = """
    {fib :n:
        (<= n 1
            ? n
        ) -> (
            ? +@fib:-n 1: @fib:-n 2:
        )
    }
    = result @fib:6:
    > result
    """
    env = run_aergia(code)
    assert env["result"] == 8
    captured = capsys.readouterr()
    assert captured.out.strip() == "8"

def test_named_function_call_via_variable(capsys):
    """Regression: CallNode used to dispatch on self.target instead of the
    resolved func, so any call through a VariableNode (i.e. every normal
    named call) raised 'Function call target must be callable.'"""
    code = """
    {double :n:
        ? *n 2
    }
    > @double:21:
    """
    run_aergia(code)
    captured = capsys.readouterr()
    assert captured.out.strip() == "42"

def test_named_function_implicit_return():
    """Regression: named functions without an explicit '?' used to
    fall through and return None instead of the last evaluated expr."""
    code = """
    {addone :n:
        +n 1
    }
    = r @addone:4:
    """
    env = run_aergia(code)
    assert env["r"] == 5

def test_logical_not_returns_int():
    """Regression: '!' used operator.not_ which yields python bool
    (True/False) instead of the documented 0/1 int."""
    code = "= r ! 0"
    env = run_aergia(code)
    assert env["r"] == 1
    assert type(env["r"]) is int

def test_runtime_error_traceback():
    """Asserts that runtime environment faults trigger proper diagnostics."""
    code = """
    = a 10
    = b 0
    = broken /a b
    """
    with pytest.raises(AergiaRuntimeError, match="division by zero"):
        run_aergia(code)