import re

# aergia lexer
# made by las-r on github

# constants
TOKENPATTERN = r'"[^"]*"|==|<<|>>|<=|>=|[()\[\]{}+\-*/%^=&|!~<>:@?,.\']|[\w.]+'

# preprocessor
def preprocess(code):
    lines = code.splitlines()
    cleaned = []
    for line in lines:
        cleaned.append(line.split("#")[0])
    return " ".join(cleaned)

# tokenizer
def tokenize(code):
    tokens = re.findall(TOKENPATTERN, preprocess(code))
    return tokens