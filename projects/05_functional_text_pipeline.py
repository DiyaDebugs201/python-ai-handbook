"""Project 5 - Functional text pipeline.

Builds a text-analysis pipeline from small functions, using lambda, map, filter,
reduce and function composition (Part 5).

Run:
    python 05_functional_text_pipeline.py --demo
    python 05_functional_text_pipeline.py "some text to analyse"
Standard library only.
"""
import re
import sys
from functools import reduce

STOP_WORDS = frozenset({"a", "an", "and", "the", "is", "are", "of", "to", "in", "it", "that", "for"})


def compose(*functions):
    """compose(f, g, h)(x) == h(g(f(x))): functions run left to right."""
    return lambda value: reduce(lambda acc, fn: fn(acc), functions, value)


tokenize = lambda text: re.findall(r"[a-z']+", text.lower())
remove_stop_words = lambda words: list(filter(lambda w: w not in STOP_WORDS, words))
stem_plural = lambda words: list(map(lambda w: w[:-1] if len(w) > 3 and w.endswith("s") else w, words))


def count_words(words):
    return reduce(lambda counts, w: {**counts, w: counts.get(w, 0) + 1}, words, {})


def top_n(counts, n=3):
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


analyse = compose(tokenize, remove_stop_words, stem_plural, count_words, top_n)


def run_demo():
    text = "The cat and the dogs chase the cats. A dog is a friend of the cat, and dogs are loyal."
    print(tokenize(text)[:6])
    print(remove_stop_words(tokenize(text))[:6])
    print(analyse(text))
    print(compose(str.strip, str.upper, len)("  hello "))


def main(argv):
    if not argv or argv[0] == "--demo":
        run_demo()
    else:
        print(analyse(" ".join(argv)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
