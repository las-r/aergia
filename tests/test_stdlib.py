import io
import sys
import pytest
from pathlib import Path
from aergia.lexer import tokenize
from aergia.parser import parse
from aergia.nodes import Environment

STDDIR = Path(__file__).parent / "aergia" / "std"

def run_aergia(code, inp=""):
    """Same helper as test_integration.py, but wired up so imports of
    std_*.aer resolve against the real stdlib folder."""
    env = Environment({"__dir__": STDDIR, "__stdlib__": STDDIR})
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        tokens = tokenize(code)
        ast = parse(tokens)
        for node in ast:
            if node:
                node.eval(env)
    finally:
        sys.stdin = old
    return env

# ── std_str.aer ────────────────────────────────────────────────────────────

def test_str_ltrim_keeps_first_char():
    """Regression: ltrim used to drop the first non-space char"""
    env = run_aergia('+< "std_str.aer" str\n= r @str.ltrim:"  hi  ":\n')
    assert env["r"] == "hi  "

def test_str_rtrim_unreverses():
    """Regression: rtrim reversed the string but never reversed back"""
    env = run_aergia('+< "std_str.aer" str\n= r @str.rtrim:"  hi  ":\n')
    assert env["r"] == "  hi"

def test_str_trim_both_sides():
    env = run_aergia('+< "std_str.aer" str\n= r @str.trim:"  hi  ":\n')
    assert env["r"] == "hi"

def test_str_reverse_uses_correct_join():
    """Regression: reverse called the nonexistent 'str_join' name"""
    env = run_aergia('+< "std_str.aer" str\n= r @str.reverse:"abc":\n')
    assert env["r"] == "cba"

def test_str_has_substring():
    env = run_aergia('+< "std_str.aer" str\n= r @str.has:"hello world" "wor":\n')
    assert env["r"] == 1

def test_str_split_empty_delim():
    """Regression: split with del="" used string-concat assignment on
    an array instead of pushing, and used to leave a stray trailing entry"""
    env = run_aergia('+< "std_str.aer" str\n= r @str.split:"abc" "":\n')
    assert env["r"] == ["a", "b", "c"]

def test_str_join_split_roundtrip():
    env = run_aergia('+< "std_str.aer" str\n= parts @str.split:"a-b-c" "-":\n= r @str.join:parts "-":\n')
    assert env["r"] == "a-b-c"

# ── std_type.aer ─────────────────────────────────────────────────────────

def test_type_is_float_true_for_fraction():
    """Regression: is_float always returned 0, the cast result was
    computed then thrown away instead of being compared"""
    env = run_aergia('+< "std_type.aer" t\n= r @t.is_float:5.5:\n')
    assert env["r"] == 1

def test_type_is_float_false_for_int():
    env = run_aergia('+< "std_type.aer" t\n= r @t.is_float:5:\n')
    assert env["r"] == 0

def test_type_is_arr():
    """Regression: missing '?' meant this relied on the implicit-return
    fix in CallNode to work at all"""
    env = run_aergia('+< "std_type.aer" t\n= r @t.is_arr:< 1 2 3 >:\n')
    assert env["r"] == 1

def test_type_is_arr_false_for_str():
    env = run_aergia('+< "std_type.aer" t\n= r @t.is_arr:"hi":\n')
    assert env["r"] == 0

def test_type_is_empty():
    env = run_aergia('+< "std_type.aer" t\n= r @t.is_empty:< >:\n')
    assert env["r"] == 1

# ── std_arr.aer ────────────────────────────────────────────────────────────

def test_arr_sortby():
    """Regression: '@f:: out j:' parsed as a 0-arg call because a bare ':'
    closes the arg list before the nested index expression can be parsed"""
    env = run_aergia('+< "std_arr.aer" arr\n= r @arr.sortby:< 5 3 1 4 2 > {:x: x}:\n')
    assert env["r"] == [1, 2, 3, 4, 5]

def test_arr_sort():
    env = run_aergia('+< "std_arr.aer" arr\n= r @arr.sort:< 5 3 1 4 2 >:\n')
    assert env["r"] == [1, 2, 3, 4, 5]