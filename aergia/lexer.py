import re

# aergia lexer
# made by las-r on github

# constants
TOKENPATTERN = r'<<<|>>>|==|!=|<<|>>|<=|>=|\+>|\*>|\*<|~>|\+:|-:|~:|\*:|\$:|::|=:|\&\&|\|\||->|"(?:[^"\\]|\\.)*"|[\(\)\[\]\{\}\+\-\*\/%\^=;\&\|\$!\~<>:@\?,.\'`]|\b[\w.]+\b'

def tokenize(code):
    lines = code.splitlines()
    tokens = []
    for lidx, line in enumerate(lines, start=1):
        cleaned = line.split("#")[0]
        if not cleaned.strip():
            continue
        for match in re.finditer(TOKENPATTERN, cleaned):
            token_text = match.group(0)
            cidx = match.start() + 1
            tokens.append((token_text, lidx, cidx))
    return tokens