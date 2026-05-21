# Aergia
**Aergia** is a minimalist yet still usable programming language, depending on your definition of usable.

## Installation
### Global Installation (pip)
```bash
pip install git+https://github.com/las-r/aergia.git
```

### Local Installation (in a directory)
Copy `/aergia` to your working directory.

## Usage
```bash
aergia <filename.aer>
```
Alternatively (for local installations):
```bash
python -m aergia <filename.aer>
```

## Updating
### ≥v1.5.0
```
aergia --ghupdate
```

### <v1.5.0
```
pip install --upgrade git+https://github.com/las-r/aergia.git
```

## Syntax Documentation
Syntax Documentation can be found [here](https://las-r.github.io/aergia/).

## Tools
Aergia is provied with a few basic tools to aid in development:
- **Lethes**:\
A basic program minifier.\
Usage:  `aergia --lethes <filename.aer>`

- **Otia** (unreleased, wip):\
A basic program linter.\
Usage:  `aergia --otia <filename.aer>`