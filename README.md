> [!WARNING]
> This branch is for the Aergia v2 rewrite and is a major WIP.

Aergia is a minimalist and lightweight interpreted programming language. 
```py
= greet {:name:
    > ++"Hello, " name "!"
}

= lang "Aergia"
@greet:lang:
```

## Philosophies
1. Every feature must justify its existence.
2. All built-in features must be represented using non-alphanumeric characters.
3. Every feature must follow uniform syntactic and semantic rules.
4. Every feature must be composable with every other feature.