import re

# aergia lexer
# made by las-r on github

# ruleset
LEXERRULES = [
    r'<<<', r'>>>',
    r'==', r'!=', r'<<', r'>>', r'<=', r'>=', 
    r'\+>', r'\+<', r'\*>', r'\*<', r'~>', 
    r'\+:', r'-:', r'~:', r'\*:', r'\$:', r'::', r'=:', 
    r'\&\&', r'\|\|', r'->', r'=\?', r'\.\.',
    r'"(?:[^"\\]|\\.)*"',
    r'[\(\)\[\]\{\}\+\-\*\/%\^=;\&\|\$!\~<>:@\?,.\'`]',
    r'\b[\w.]+\b'
]
TOKENPATTERN = re.compile('|'.join(LEXERRULES))

# tokenizer
def tokenize(code):
    tokens = []
    for lidx, line in enumerate(code.splitlines(), start=1):
        cleaned = line.split("#")[0]
        if not cleaned.strip():
            continue
        for match in TOKENPATTERN.finditer(cleaned):
            tokens.append((match.group(0).strip(), lidx, match.start() + 1)) 
    return tokens