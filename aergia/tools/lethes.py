import os
from ..lexer import tokenize

# aergia minifier
# by las-r

# minify function
def minify(code):
    tokens = tokenize(code)
    minifiedtokens = []
    for i, token in enumerate(tokens):
        if i > 0:
            prevtoken = tokens[i - 1]
            if prevtoken.isalnum() and token.isalnum():
                minifiedtokens.append(" ")
        minifiedtokens.append(token)
    return "".join(minifiedtokens)

# minify file function
def minifyf(filepath):
    bpath, ext = os.path.splitext(filepath)
    mpath = f"{bpath}.l{ext}"
    with open(filepath, 'r', encoding='utf-8') as f:
        ocode = f.read()
    mcode = minify(ocode)
    with open(mpath, 'w', encoding='utf-8') as f:
        f.write(mcode)
    print(f"Lethes has consumed {os.path.basename(filepath)} -> Created {os.path.basename(mpath)}")
    return mpath