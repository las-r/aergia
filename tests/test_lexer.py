import pytest
from aergia.lexer import tokenize

def test_tokenize_literals_and_variables():
    tokens = tokenize('x 42 "hello world"')
    token_strings = [t[0] for t in tokens]
    
    assert token_strings == ['x', '42', '"hello world"']

def test_tokenize_ignores_comments():
    code = """
    = x 10  # assign x
    # this is a full line comment
    + x 5
    """
    tokens = tokenize(code)
    token_strings = [t[0] for t in tokens]
    
    assert '#' not in token_strings
    assert 'assign' not in token_strings
    assert token_strings == ['=', 'x', '10', '+', 'x', '5']

def test_tokenize_multichar_operators():
    # Testing Aergia's specific multi-character ops
    code = "== != <= >= && || -> =? .. +: -: ~: *:"
    tokens = tokenize(code)
    token_strings = [t[0] for t in tokens]
    
    expected = ['==', '!=', '<=', '>=', '&&', '||', '->', '=?', '..', '+:', '-:', '~:', '*:']
    assert token_strings == expected

def test_tokenize_line_and_col_tracking():
    code = "a\n  b\nc"
    tokens = tokenize(code)
    
    # Format: (token_string, line_number, column_number)
    assert tokens[0] == ('a', 1, 1)
    assert tokens[1] == ('b', 2, 3) # Line 2, column 3 due to spaces
    assert tokens[2] == ('c', 3, 1)

def test_tokenize_arrays_and_punctuation():
    code = "< 1 2 > ; @func:+arg 3 arg2:"
    tokens = tokenize(code)
    token_strings = [t[0] for t in tokens]
    
    assert token_strings == ['<', '1', '2', '>', ';', '@', 'func', ':', '+', 'arg', '3', 'arg2', ':']
    
def test_tokenize_hash_inside_string():
    """Verifies that comment symbols inside string literals are not stripped."""
    code = '= color "#FF0000"  # This is a real comment'
    tokens = tokenize(code)
    token_strings = [t[0] for t in tokens]
    
    assert '#FF0000"' in token_strings[2]
    assert 'comment' not in token_strings

def test_tokenize_numeric_bases():
    """Ensures hex and binary literal notations are isolated cleanly."""
    code = "0x1A 0b1010"
    tokens = tokenize(code)
    token_strings = [t[0] for t in tokens]
    
    assert token_strings == ['0x1A', '0b1010']

def test_tokenize_lexical_error():
    """Confirms that invalid/mismatched characters cause the tokenizer to fail immediately."""
    with pytest.raises(ValueError, match="Unexpected character"):
        tokenize("= x 10 \\")  # Stray backslash outside string causes a failure