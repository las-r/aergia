import os
import re
from ..lexer import tokenize

# aergia minifier
# by las-r

# minify function
def minify(code):
    tokens = tokenize(code)
    if not tokens:
        return ""
    minified = [tokens[0][0]]
    for i in range(1, len(tokens)):
        prev = minified[-1]
        cur = tokens[i][0]
        if (prev.isalnum() or '_' in prev or '.' in prev) and (cur.isalnum() or '_' in cur or '.' in cur):
            minified.append(" ")
            minified.append(cur)
            continue
        combined = prev + cur
        testtokens = tokenize(combined)
        if len(testtokens) != 2 or testtokens[0][0] != prev:
            minified.append(" ")
        minified.append(cur)
    return "".join(minified)

# minify file function
def minifyf(filepath):
    bpath, ext = os.path.splitext(filepath)
    mpath = f"{bpath}.min{ext}"
    with open(filepath, 'r', encoding='utf-8') as f:
        ocode = f.read()
    mcode = minify(ocode)
    with open(mpath, 'w', encoding='utf-8') as f:
        f.write(mcode)
    print(f"Lethes has consumed {os.path.basename(filepath)} -> Created {os.path.basename(mpath)}")
    return mpath