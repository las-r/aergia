---
layout: default
title: Packages
nav_order: 5
---

# Packages
Aergia supports package creation and management.

## Agathos
Agathos is Aergia's decentralized package management tool. It lets you:
- Install packages straight from GitHub
- Remove packages by name
- List packages with name, author, and version.

### Installing Packages
You can install packages from GitHub using the `--libget` argument, or `-lh` for shorthand. 

```bash
aergia --libget https://github.com/las-r/aergia-example-package
```

### Removing Packages
You can remove packages by name using the `--librem` argument, or `-lr` for shorthand. 

```bash
aergia --librem example_package
```

### Listing Packages
You can get a list of packages using the  `--libls` argument, or `-ll` for shorthand.

## Development
Of course, you can make your own packages!

Every package MUST have the following things:
- An `aerpkg.json`, which gives basic package info.
- And a `main.aer`.

This is how an `aerpkg.json` should look like (note that every field is MANDATORY):
```json
{
  "name": "example_package",
  "author": "las-r",
  "version": "0.0.1",
  "dependencies": [],  // Should just be a list of links to other GH repos
  "src": "src"
}
```

Each field should be pretty self explanatory. The `src` field is just the source folder for your project. The `main.aer` should be located inside of the source folder.

It's recommended to use the [Aergia Example Package](https://github.com/las-r/aergia-example-package) as a baseline for your projects.