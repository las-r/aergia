<p align="center">
  <img src="assets/images/name.svg" alt="Aergia" width="300" />
</p>

<p align="center">
  <a href="https://github.com/las-r/aergia/actions/workflows/test.yml">
    <img src="https://github.com/las-r/aergia/actions/workflows/test.yml/badge.svg?event=push" alt="Build Status">
  </a>
  <a href="https://github.com/las-r/aergia/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/las-r/aergia?color=lightgrey" alt="License" />
  </a>
  <a href="https://pypi.org/project/aergia-lang/">
    <img src="https://img.shields.io/pypi/dm/aergia-lang?color=orange" alt="PyPI - Downloads" />
  </a>
  <a href="https://github.com/las-r/aergia/pulse">
    <img src="https://img.shields.io/github/commit-activity/m/las-r/aergia?color=blueviolet" alt="GitHub - Pulse" />
  </a>
  <a href="https://pypi.org/project/aergia-lang/">
    <img src="https://img.shields.io/pypi/v/aergia-lang?color=blue" alt="PyPI version" />
  </a>
  <a href="https://github.com/las-r/aergia">
    <img src="https://img.shields.io/github/languages/code-size/las-r/aergia?color=success" alt="GitHub Code Size" />
  </a>
</p>

<p align="center">
  <strong>Aergia</strong> is a minimalist and lightweight interpreted programming language. 
</p>

```py
{greet :name:
    > "Hello, %name%!"
}

= lang_name "Aergia"
@greet:lang_name:
```

## Installation & Quick Start
Get up and running with `pip` in seconds:

```bash
pip install aergia-lang
aergia your_program.aer
```

## Documentation
Full documentation and syntax guides be found [here](https://las-r.github.io/aergia/).

## Tools
Aergia includes built-in tools to streamline your development workflow:

* [**Agathos**](https://las-r.github.io/aergia/packages.html#agathos): The Aergia package manager.
* **Lethes**: A native program minifier to compress your source code.
  ```bash
  aergia --lethes <filename.aer>  # Shorthand: aergia -l <filename.aer>
  ```
* **Otia**: An automatic code prettifier and formatter.
  ```bash
  aergia --otia <filename.aer>    # Shorthand: aergia -o <filename.aer>
  ```

## IDE Support
* [VS Code Extension](https://github.com/las-r/aergia/tree/main/editors/vscode)
* [Sublime Text Grammar](https://github.com/las-r/aergia/tree/main/editors/sublime)
* [Notepad++ UDL](https://github.com/las-r/aergia/tree/main/editors/npp)

## Contributors
A huge thanks to the developers helping shape Aergia! 

* [lyxal](https://github.com/lyxal)