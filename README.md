# knuth_fisher_yates_shuffle_tools

A small library for unbiased in-place shuffling of a mutable sequence using the Fisher-Yates algorithm with a pluggable random source.

## Usage

```python
from knuth_fisher_yates_shuffle_tools import shuffle

items = [1, 2, 3, 4, 5]
shuffle(items)
print(items)  # a random permutation of the original list
```

To make the shuffle deterministic, pass a callable that takes an integer `n` and returns an integer in `[0, n)`:

```python
from knuth_fisher_yates_shuffle_tools import shuffle

items = [1, 2, 3]
shuffle(items, rand=lambda n: 0)
print(items)  # [2, 3, 1]
```

## Why this library exists

The standard library's `random.shuffle` is convenient but not testable without monkey-patching. This library exposes the random source as an explicit parameter, making it trivial to write deterministic tests for code that relies on shuffling. The trade-off is a slightly more verbose call site when you want the default behaviour; you must pass `rand=None` or omit the argument.

## Edge cases

- The sequence must be mutable. Passing a tuple or string raises `TypeError`.
- The random source must return an integer within `[0, n)`. If it returns an out-of-range value, `shuffle` raises `ValueError`.
- An empty sequence or a single-element sequence is left unchanged.
