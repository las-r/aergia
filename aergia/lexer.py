import re

# aergia lexer
# made by las-r on github

# lexer rules
RULES = [
    ('COMMENT', r'#.*'),
    ('STRING', r'"(?:[^"\\]|\\.)*"'), 
    ('OP_3', r'<<<|>>>|@!:|<!:|>!:|!!:'),
    ('OP_2', r'==|!=|<<|>>|<=|>=|\&\&|\|\||\+>|\+<|\*>|\*<|~>|!>|\+:|-:|~:|\*:|\$:|\^:|=:|->|=>|=\?|=,|=\.|=\'|\.\.|!!'),
    ('OP_1', r'[\(\)\[\]\{\}\+\-\*\/%\^=;\&\|\$!\~<>:@\?,.\'`]'),
    ('IDENT_NUM', r'\b\w+\.\w+\b|\b\w+\b|\.\d+'),
    ('SPACE', r'[ \t\r]+'),
    ('NEWLINE', r'\n'),
    ('MISMATCH', r'.')
]

# compile into pattern
PATTERN = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in RULES))

# tokenizer
def tokenize(code):
    tokens = []
    lidx = 1
    lstart = 0
    for match in PATTERN.finditer(code):
        kind = match.lastgroup
        if kind is not None:
            value = match.group(kind)
            col = match.start() - lstart + 1
            if kind == 'NEWLINE':
                lidx += 1
                lstart = match.end()
            elif kind == 'COMMENT' or kind == 'SPACE':
                continue
            elif kind == 'MISMATCH':
                raise ValueError(f"Unexpected character {value!r} at line {lidx}, column {col}")
            elif kind == 'STRING':
                tokens.append((value, lidx, col))
            else:
                tokens.append((value.strip(), lidx, col))
    return tokens