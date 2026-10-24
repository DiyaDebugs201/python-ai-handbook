# Part 6 — Solutions: Python Integration and AI Foundations

> [Practice index](../README.md) · [Problems for this part](../part-6-exercises.md)

Every program below was run with Python 3.13 and the output shown is the real output. Your own solution may differ and still be correct: compare behaviour, not wording.

## P6.1 — Read a setting from the environment

Read the environment variable `HANDBOOK_DEMO_VALUE` using a default of `"not set"`. Then set it inside the program with `os.environ` and read it again. (Never put real secrets in code.)

```python
import os

print(os.environ.get("HANDBOOK_DEMO_VALUE", "not set"))
os.environ["HANDBOOK_DEMO_VALUE"] = "demo"
print(os.environ.get("HANDBOOK_DEMO_VALUE", "not set"))
```

Output:

```text
not set
demo
```

`get` avoids a `KeyError` when the variable is missing. Real keys are set outside the program, never written into source code.

## P6.2 — Rough token estimator

Write `estimate_tokens(text)` that returns the larger of 1 and `round(len(text) / 4)`, and `estimate_words_tokens(text)` that uses `round(len(text.split()) / 0.75)`. Compare them on a sentence and on `"3.14159265358979"`. They are only estimates, not a real tokenizer.

```python
def estimate_tokens(text):
    return max(1, round(len(text) / 4))


def estimate_words_tokens(text):
    return round(len(text.split()) / 0.75)


for text in ["The quick brown fox jumps over the lazy dog.", "3.14159265358979"]:
    print(estimate_tokens(text), estimate_words_tokens(text))
```

Output:

```text
11 12
4 1
```

The two rules agree roughly on ordinary English but disagree on a long digit string, which one 'word' but many characters. Real tokenizers differ again.

## P6.3 — Nearest neighbour by cosine similarity

Given `docs = {"cat": [0.9, 0.1], "dog": [0.8, 0.2], "car": [0.1, 0.9]}` and a query vector `[0.85, 0.15]`, print the documents ranked by cosine similarity with their scores to 3 decimals.

```python
import math

docs = {"cat": [0.9, 0.1], "dog": [0.8, 0.2], "car": [0.1, 0.9]}
query = [0.85, 0.15]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


for name in sorted(docs, key=lambda n: cosine(query, docs[n]), reverse=True):
    print(name, round(cosine(query, docs[name]), 3))
```

Output:

```text
cat 0.998
dog 0.998
car 0.281
```

Sorting by similarity gives a tiny semantic search; the invented vectors put `cat` and `dog` close to the query.

## P6.4 — Softmax with temperature

Write `softmax(scores, temperature)` and print the probabilities (3 decimals) of scores `[2.0, 1.0, 0.1]` at temperatures 0.5, 1 and 2. Describe in a comment what happens as temperature rises.

```python
import math


def softmax(scores, temperature=1.0):
    exps = [math.exp(s / temperature) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


for t in (0.5, 1, 2):
    print(t, [round(p, 3) for p in softmax([2.0, 1.0, 0.1], t)])
# Higher temperature flattens the distribution, so less likely options get more probability.
```

Output:

```text
0.5 [0.864, 0.117, 0.019]
1 [0.659, 0.242, 0.099]
2 [0.502, 0.304, 0.194]
```

Dividing by a small temperature exaggerates differences between scores; a large one flattens them.

## P6.5 — Prompt template with validation

Write `build_prompt(template, **fields)` that fills a template such as `"Summarise in {n} bullets: {text}"` and raises a clear `ValueError` naming any missing field.

```python
def build_prompt(template, **fields):
    try:
        return template.format(**fields)
    except KeyError as missing:
        raise ValueError(f"missing field: {missing.args[0]}") from None


template = "Summarise in {n} bullets: {text}"
print(build_prompt(template, n=3, text="Python is popular."))
try:
    build_prompt(template, n=3)
except ValueError as error:
    print("ValueError:", error)
```

Output:

```text
Summarise in 3 bullets: Python is popular.
ValueError: missing field: text
```

`format` raises `KeyError` for a missing placeholder; converting it to a `ValueError` gives a clearer message for callers.

## P6.6 — Trim history to a budget

Write `trim(messages, budget)` that keeps the most recent messages whose total word count is at most `budget`, in original order. Test with 4 short messages and budget 7.

```python
def trim(messages, budget):
    kept, used = [], 0
    for message in reversed(messages):
        cost = len(message.split())
        if used + cost > budget:
            break
        kept.append(message)
        used += cost
    return list(reversed(kept))


history = ["hello there", "how are you today", "fine thanks", "what is a list"]
print(trim(history, 7))
```

Output:

```text
['fine thanks', 'what is a list']
```

Recent messages usually matter most, so the walk goes from newest to oldest and stops at the first one that does not fit.

## P6.7 — Chunk with overlap

Write `chunks(words, size, overlap)` that splits a list of words into chunks of `size` words, each starting `size - overlap` words after the previous one. Test on the words `a` to `j` with size 4 and overlap 1.

```python
def chunks(words, size, overlap):
    step = size - overlap
    result = []
    for start in range(0, len(words), step):
        result.append(words[start:start + size])
        if start + size >= len(words):
            break
    return result


for chunk in chunks(list("abcdefghij"), 4, 1):
    print(chunk)
```

Output:

```text
['a', 'b', 'c', 'd']
['d', 'e', 'f', 'g']
['g', 'h', 'i', 'j']
```

Overlap repeats boundary words in neighbouring chunks so that a fact is less likely to be cut off from its context.

## P6.8 — Top-k retrieval by overlap

Given four short documents and a question, return the 2 documents sharing the most words with the question (ignore case).

```python
docs = [
    "Refunds are available within 30 days",
    "Shipping takes five working days",
    "Gift cards cannot be refunded",
    "Our office is closed on holidays",
]
question = "how many days for refunds"
q = set(question.lower().split())
ranked = sorted(docs, key=lambda d: len(q & set(d.lower().split())), reverse=True)
print(ranked[:2])
```

Output:

```text
['Refunds are available within 30 days', 'Shipping takes five working days']
```

Word overlap is a crude relevance score, but it shows the retrieve-then-rank pattern used in RAG.

## P6.9 — Spot unsupported numbers

Given an answer and its source text, list the numbers in the answer that do not appear in the source (a simple hallucination check).

```python
import re

source = "The course has 40 chapters and 96 topics."
answer = "The course has 40 chapters, 96 topics and 7 projects."
source_numbers = set(re.findall(r"\d+", source))
unsupported = [n for n in re.findall(r"\d+", answer) if n not in source_numbers]
print(unsupported)
```

Output:

```text
['7']
```

Numbers are easy to check mechanically; anything not in the source is flagged for review. This does not catch every kind of unsupported claim.

## P6.10 — Cost calculator

Write `call_cost(input_tokens, output_tokens, input_price, output_price)` with prices per million tokens (use invented prices 2.0 and 8.0), and print the cost of 1,000 calls with 1,500 input and 300 output tokens each.

```python
def call_cost(input_tokens, output_tokens, input_price, output_price):
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000


one = call_cost(1500, 300, 2.0, 8.0)
print(round(one, 6), round(one * 1000, 2))
```

Output:

```text
0.0054 5.4
```

Input and output are priced separately; the prices here are invented, so check a real provider's price list.

## P6.11 — Tool registry with errors

Create a dictionary of tools `{"add": ..., "upper": ...}` and a function `run(name, **arguments)` that returns a result, or a clear error string for an unknown tool or bad arguments, without crashing.

```python
tools = {"add": lambda a, b: a + b, "upper": lambda text: text.upper()}


def run(name, **arguments):
    if name not in tools:
        return f"error: unknown tool {name}"
    try:
        return tools[name](**arguments)
    except TypeError as error:
        return f"error: {error}"


print(run("add", a=2, b=3))
print(run("upper", text="hi"))
print(run("delete"))
print(run("add", a=1))
```

Output:

```text
5
HI
error: unknown tool delete
error: <lambda>() missing 1 required positional argument: 'b'
```

Returning errors as data (instead of crashing) is what lets an agent loop report a failure back to the model and continue.

## P6.12 — Evaluate a classifier

Compute the accuracy of the simple function `is_positive(text)` (true if the text contains `good` or `great`) on five labelled examples and list the failures.

```python
def is_positive(text):
    return any(word in text.lower() for word in ("good", "great"))


tests = [
    ("A great film", True),
    ("Good value", True),
    ("Not good at all", False),
    ("Terrible", False),
    ("It was fine", True),
]
failures = [(t, e) for t, e in tests if is_positive(t) != e]
print(f"accuracy: {(len(tests) - len(failures)) / len(tests):.0%}")
print(failures)
```

Output:

```text
accuracy: 60%
[('Not good at all', False), ('It was fine', True)]
```

Listing failures, not just the score, shows what to fix (negation and unknown words here).

---

Back to the [problems](../part-6-exercises.md) or the [practice index](../README.md).
