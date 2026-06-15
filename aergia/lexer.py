import re

# aergia lexer
# made by las-r on github

# ruleset
LEXERRULES = [
    # 3 char
    r'<<<', r'>>>',
    
    # 2 char
    r'==', r'!=', r'<<', r'>>', r'<=', r'>=', 
    r'\+>', r'\*>', r'\*<', r'~>', 
    r'\+:', r'-:', r'~:', r'\*:', r'\$:', r'::', r'=:', 
    r'\&\&', r'\|\|', r'->', r'=\?', r'\.\.',
    
    # strings
    r'"(?:[^"\\]|\\.)*"',
    
    # 1 char
    r'[\(\)\[\]\{\}\+\-\*\/%\^=;\&\|\$!\~<>:@\?,.\'`]',
    
    # everything else
    r'\b[\w.]+\b'
]
TOKENPATTERN = re.compile('|'.join(LEXERRULES))

# tokenizer
def tokenize(code):
    lines = code.splitlines()
    tokens = []
    for lidx, line in enumerate(lines, start=1):
        cleaned = line.split("#")[0]
        if not cleaned.strip():
            continue
        for match in TOKENPATTERN.finditer(cleaned):
            tokentext = match.group(0).strip()
            cidx = match.start() + 1
            tokens.append((tokentext, lidx, cidx)) 
    return tokens