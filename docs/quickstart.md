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
cd aergia
pip install -e .
```

## Usage
```bash
aergia <filename.aer>
# Alternatively (for local installations):
python3 -m aergia <filename.aer>
```

## Updating
### PyPI
```bash
pip install --upgrade aergia-lang
```

### GitHub
```bash
aergia --ghupdate
# Or using pip:
pip install --upgrade git+https://github.com/las-r/aergia.git
```