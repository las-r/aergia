---
layout: default
title: 7. Files
parent: Syntax
nav_order: 7
---

# 7. Files
Files in Aergia work identically to Python.

| Token | Python Equivalent | Syntax Pattern |
| --- | --- | --- |
| `@!:` | `open("file.txt", "r")` | `@!: "file.txt" "r"` |
| `<!:` | `file.read()` | `<!: file` |
| `>!:` | `file.write("some text")` | `>!: file "some text"` |
| `!!:` | `file.close()` | `!!: file` |