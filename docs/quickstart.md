---
layout: default
title: Quickstart Guide
nav_order: 2
---

# Quickstart
A guide to getting Aergia up and running on your machine.

## Installation
### PyPI (stable)
Install the latest stable release. This might not have all the bleeding-edge features.
```bash
pip install aergia-lang
```

### GitHub (nightly)
Install the latest development version right from the repo.
```bash
pip install git+https://github.com/las-r/aergia.git
```

### Local / Source (dev)
If you want to modify the interpreter or contribute to development, clone the repo and install in editable mode.
```bash
git clone https://github.com/las-r/aergia.git
pip install -e aergia
```

## Usage
### 1. Create a file
Create a new named `test.aer` (or whatever you feel like) and add some code. For example:
```py
> "Hello, Aergia!"
```

### 2. Run the interpreter
```bash
aergia test.aer
# alternatively (for local installations):
python3 -m aergia test.aer
```

## Updating
### PyPI
```bash
pip install --upgrade aergia-lang
```

### GitHub
```bash
aergia --ghupdate
# or using pip:
pip install --upgrade git+https://github.com/las-r/aergia.git
```