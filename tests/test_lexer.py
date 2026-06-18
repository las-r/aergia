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