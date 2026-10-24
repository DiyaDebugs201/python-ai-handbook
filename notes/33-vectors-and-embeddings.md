# Chapter 33 — Vectors and Embeddings

> Part 6 — Python Integration and AI Foundations · Video: 11:26:22–11:31:37 · Previous: [32 Context Engineering and Tokens](32-context-engineering-and-tokens.md) · Next: [34 Context Window and Model Parameters](34-context-window-and-model-parameters.md)

**In this chapter:** how a list of numbers (a *vector*) can represent the meaning of a word, sentence or document; what an *embedding* is; how *similarity* between vectors is measured; and how this makes meaning-based search possible.

**Before you start:** you need lists, tuples, loops, functions and comprehensions ([Chapter 18](18-lists-fundamentals.md), [Chapter 25](25-defining-functions-and-return-values.md)), `math` basics, and the token idea from [Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs). Recap: models read token IDs, but IDs are just labels; they do not say which tokens are similar in meaning. All code is a *toy demo* with small, hand-made vectors using only the standard library. Real embeddings come from a trained model (an AI service or a library) and have hundreds or thousands of dimensions. Examples were run with Python 3.13.

---

## Vectors and Embeddings

**Timestamp:** [11:26:22](https://www.youtube.com/watch?v=J9BI0jGOds8&t=41182s)

**Learning objectives:**

- Define a vector, a dimension and an embedding.
- Explain why meaning is represented as a position in space, and what "close" means.
- Compute dot product, length and cosine similarity in Python.
- Describe how embeddings are used for semantic search, and their limits.

**1. Intuition**

Imagine a map of a city where every shop is placed so that similar shops are near each other: bakeries together, bookshops together. A shop's address is two numbers (how far east, how far north). To find shops like a given bakery you look at its neighbours. An embedding does the same for text, except the "map" has hundreds or thousands of directions instead of two, and the model learns where to put each text so that texts with similar meaning end up close together. (This is an analogy: the real directions are not human-readable like "east" or "sweetness".)

**2. Why does it exist?**

Computers compare text by exact characters, so "car" and "automobile" look completely different, and a search for "how do I get my money back" misses a page titled "Refund policy". Meaning is needed, not spelling. Turning text into numbers that reflect meaning lets a program measure "how related are these?" with arithmetic, which is fast and works at scale. This is the basis of semantic search and of retrieval for [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md).

**3. Technical explanation**

- A **vector** is an ordered list of numbers, for example `[0.2, -1.5, 3.0]`. The number of entries is its **dimension**. A vector can be seen as an arrow or a point in space.
- An **embedding** is a vector produced by a model to represent a piece of text (or an image, audio and so on). It is learned during training so that items with similar meaning have vectors that are close together.
- **Embedding model versus language model.** Embedding models are separate models (or parts of models) that output one vector per input; a chat model generates text. Inside a language model, tokens also have learned vectors (token embeddings) that are the first step of its calculation (see [Attention Mechanism and Transformers](35-attention-and-transformers.md)).
- **Measuring closeness.**
  - *Dot product*: multiply matching entries and add them up.
  - *Length* (norm): the square root of the dot product of a vector with itself.
  - *Cosine similarity*: dot product divided by the product of the lengths. It measures the angle between the vectors, from -1 (opposite) through 0 (unrelated direction) to 1 (same direction), and ignores the length. It is the most common measure for text embeddings.
  - *Euclidean distance*: the straight-line distance between the points. Smaller means closer.
- **Semantic search.** Embed every document once and store the vectors; embed the query; return the documents whose vectors are most similar to the query vector. Large collections use a *vector database* or index that finds nearest neighbours quickly (often approximately).
- **Limits.** Embeddings capture similarity, not truth. Quality depends on the embedding model and language; vectors from different models are not comparable with each other; you must use the same model for documents and queries; text that is similar but opposite in meaning ("the flight was on time" versus "the flight was late") may still be close; and very long texts must be split into chunks first.
- **Intuition versus mechanism.** The intuition is "a map of meaning". The mechanism is a trained neural network that outputs numbers; no one assigns the dimensions by hand.

**4. Syntax**

```text
dot(a, b)    = a[0]*b[0] + a[1]*b[1] + ...
length(a)    = sqrt(dot(a, a))
cosine(a, b) = dot(a, b) / (length(a) * length(b))
```

These are formulas (pattern), implemented in the examples below.

**5. Example 1 — Basic**

*Toy demo.* Vectors as lists, with dot product, length and cosine similarity:

```python
import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def length(a):
    return math.sqrt(dot(a, a))


def cosine(a, b):
    return dot(a, b) / (length(a) * length(b))


a = [1, 2, 3]
b = [2, 4, 6]
c = [3, 0, -1]
print(dot(a, b), length(a))
print(round(cosine(a, b), 4))
print(round(cosine(a, c), 4))
print(round(cosine(a, [-1, -2, -3]), 4))
```

Output:

```text
28 3.7416573867739413
1.0
0.0
-1.0
```

Line by line:

- `zip` pairs matching entries; the generator multiplies them and `sum` adds them: this is the dot product.
- `b` is `a` doubled, so it points in exactly the same direction: cosine similarity 1.0, even though it is longer.
- `c` points in a different direction, giving a value near zero.
- The negated vector points the opposite way: -1.0.

**6. Example 2 — Practical**

*Toy demo.* Tiny hand-made "embeddings" with three invented dimensions (roughly: animal-ness, vehicle-ness, food-ness). Real embeddings are learned and have no such labels; the numbers here are made up to show the idea. Semantic search is then a ranking by cosine similarity:

```python
import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cosine(a, b):
    return dot(a, b) / (math.sqrt(dot(a, a)) * math.sqrt(dot(b, b)))


# invented dimensions: [animal, vehicle, food]
embeddings = {
    "cat": [0.9, 0.0, 0.1],
    "dog": [0.8, 0.1, 0.1],
    "car": [0.0, 0.9, 0.0],
    "truck": [0.1, 0.8, 0.0],
    "bread": [0.0, 0.0, 0.9],
    "pizza": [0.1, 0.0, 0.8],
}


def most_similar(word, top=3):
    scores = [(other, cosine(embeddings[word], vector)) for other, vector in embeddings.items() if other != word]
    scores.sort(key=lambda pair: pair[1], reverse=True)
    return [(other, round(score, 3)) for other, score in scores[:top]]


print(most_similar("cat"))
print(most_similar("car"))
print(most_similar("pizza", top=2))
```

Output:

```text
[('dog', 0.992), ('pizza', 0.233), ('truck', 0.123)]
[('truck', 0.992), ('dog', 0.123), ('cat', 0.0)]
[('bread', 0.992), ('dog', 0.244)]
```

Line by line:

- Each word maps to a vector of the same dimension; vectors can only be compared when they have the same length.
- `most_similar` scores every other word against the chosen one, sorts from highest to lowest cosine similarity and returns the top results.
- The nearest neighbour of `cat` is `dog`, of `car` is `truck`, and of `pizza` is `bread`, simply because their numbers point in similar directions.

Now a small document search, using the same idea. Documents are embedded in advance (the vectors are invented), and the query is embedded in the same space:

```python
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


# invented dimensions: [money, shipping, account]
documents = {
    "Refund policy": [0.9, 0.1, 0.2],
    "Delivery times": [0.1, 0.9, 0.0],
    "Reset your password": [0.0, 0.1, 0.9],
}
query_vector = [0.8, 0.1, 0.1]  # pretend: embedding of "how do I get my money back?"

ranked = sorted(documents, key=lambda title: cosine(query_vector, documents[title]), reverse=True)
for title in ranked:
    print(f"{cosine(query_vector, documents[title]):.3f}  {title}")
```

Output:

```text
0.995  Refund policy
0.231  Delivery times
0.136  Reset your password
```

The refund page ranks first although the query shares no words with its title. In a real system the vectors would come from an embedding model, not from hand-written numbers.

**7. Example 3 — Edge case or common mistake**

Mismatched dimensions raise no error with `zip`, but silently give wrong answers:

```python
import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


a = [1, 2, 3]
b = [1, 2]
print(dot(a, b))
print(len(a) == len(b))
```

Output:

```text
5
False
```

`zip` stops at the shorter list, so the third entry of `a` was ignored without any warning. Checking the lengths first avoids this:

```python
def safe_dot(a, b):
    if len(a) != len(b):
        raise ValueError(f"dimension mismatch: {len(a)} versus {len(b)}")
    return sum(x * y for x, y in zip(a, b))


try:
    safe_dot([1, 2, 3], [1, 2])
except ValueError as error:
    print("error:", error)
```

Output:

```text
error: dimension mismatch: 3 versus 2
```

A zero vector has no direction, so cosine similarity divides by zero:

```python
import math

zero = [0, 0, 0]
other = [1, 2, 3]
try:
    print(sum(x * y for x, y in zip(zero, other)) / (math.sqrt(0) * math.sqrt(14)))
except ZeroDivisionError as error:
    print("ZeroDivisionError:", error)
```

Output:

```text
ZeroDivisionError: float division by zero
```

Real code should handle that case (for example, return 0.0 when either length is zero).

Dot product and cosine can rank differently, because the dot product depends on length:

```python
import math

query = [1, 0]
short_close = [1, 0.1]
long_far = [5, 5]

dot = lambda a, b: sum(x * y for x, y in zip(a, b))
cos = lambda a, b: dot(a, b) / (math.sqrt(dot(a, a)) * math.sqrt(dot(b, b)))

print("dot:   ", dot(query, short_close), dot(query, long_far))
print("cosine:", round(cos(query, short_close), 3), round(cos(query, long_far), 3))
```

Output:

```text
dot:    1.0 5
cosine: 0.995 0.707
```

By dot product the long vector wins, by cosine similarity the short vector pointing almost the same way wins. Which one to use depends on the embedding model: many return vectors of length 1, for which both rankings agree. Check your provider's documentation.

Similar wording does not guarantee similar meaning. A toy bag-of-words vector (counts of words) shows the problem:

```python
import math
from collections import Counter


def bag(text):
    return Counter(text.lower().replace(".", "").split())


def cosine_bags(a, b):
    words = set(a) | set(b)
    dot = sum(a[w] * b[w] for w in words)
    return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))


one = bag("The flight was on time.")
two = bag("The flight was not on time.")
three = bag("Our plane landed punctually.")
print(round(cosine_bags(one, two), 3))
print(round(cosine_bags(one, three), 3))
```

Output:

```text
0.913
0.0
```

Counting words rates the contradictory sentence as very similar and the paraphrase (same meaning, different words) as unrelated. Learned embeddings handle paraphrases far better, but can still be fooled by negation, which is one reason retrieval results need checking.

*Requires an AI service or library (not run here):*

```text
# pseudocode; the function name and model name are placeholders
vector = embed(model="<embedding-model>", text="How do I get a refund?")
print(len(vector))   # the dimension, fixed by the model
```

**8. Common mistakes**

- Comparing vectors from different embedding models, or embedding documents and queries with different models.
- Comparing vectors of different dimensions.
- Dividing by a zero length.
- Assuming that close vectors mean the same or true meaning.
- Embedding very long documents without splitting them into chunks.
- Mixing up dot product and cosine similarity when vectors are not normalised.
- Re-embedding unchanged documents on every query instead of storing the vectors.

**9. Real-world and AI applications**

Semantic search, "similar items" recommendations, duplicate detection, clustering support tickets, classification with few examples, and above all the retrieval step of [RAG](37-retrieval-augmented-generation.md). Vector databases and libraries store embeddings and find nearest neighbours efficiently. The mini-project `projects/07_toy_rag_retriever.py` builds a small retriever using simple word-count vectors and cosine similarity (not learned embeddings).

**10. Practice**

1. Compute the dot product and length of `[3, 4]` by hand, then check with the functions from Example 1.
2. Find the cosine similarity of `[1, 0]` and `[0, 1]`. What does the result mean?
3. Add `"banana": [0.0, 0.0, 0.8]` to the toy embeddings and print its most similar words.
4. Write `normalize(v)` that returns the vector divided by its length. What is the length of the result?
5. Write `top_k(query_vector, documents, k)` that returns the k titles with highest cosine similarity.
6. Make `cosine` return `0.0` instead of failing when a vector has zero length.
7. In your own words, why must queries and documents use the same embedding model?

**11. Interview questions**

- *What is an embedding?* A vector produced by a trained model that represents text (or other data) so that similar meanings are close together.
- *Why cosine similarity?* It compares direction and ignores vector length, which suits text embeddings.
- *What is semantic search?* Finding documents by closeness of meaning (vector similarity) instead of exact keyword matches.
- *What is a vector database for?* Storing embeddings and finding the nearest ones to a query vector quickly.
- *What are the limits of embeddings?* They reflect similarity, not truth; negation and fine distinctions can be missed; they depend on the model and need chunking for long text.

**12. Quick revision**

- Vector = list of numbers; dimension = its length.
- Embedding = learned vector for a text, close for similar meaning.
- Cosine = dot / (length × length), from -1 to 1.
- Same model, same dimension, for queries and documents.
- Semantic search = embed, compare, rank; check results.

---

## Answers to Practice Exercises

### Answers: Vectors and Embeddings

1. By hand: dot = 3×3 + 4×4 = 25, length = √25 = 5.

```python
import math

v = [3, 4]
d = sum(x * y for x, y in zip(v, v))
print(d, math.sqrt(d))
```

Output:

```text
25 5.0
```

2.

```python
import math

a, b = [1, 0], [0, 1]
dot = sum(x * y for x, y in zip(a, b))
print(dot / (math.sqrt(1) * math.sqrt(1)))
```

Output:

```text
0.0
```

The result 0 means the vectors are at a right angle: no similarity in direction.

3.

```python
import math

embeddings = {
    "cat": [0.9, 0.0, 0.1],
    "dog": [0.8, 0.1, 0.1],
    "car": [0.0, 0.9, 0.0],
    "bread": [0.0, 0.0, 0.9],
    "pizza": [0.1, 0.0, 0.8],
    "banana": [0.0, 0.0, 0.8],
}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


scores = sorted(
    ((w, round(cosine(embeddings["banana"], v), 3)) for w, v in embeddings.items() if w != "banana"),
    key=lambda pair: pair[1],
    reverse=True,
)
print(scores[:3])
```

Output:

```text
[('bread', 1.0), ('pizza', 0.992), ('dog', 0.123)]
```

4.

```python
import math


def normalize(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


unit = normalize([3, 4])
print(unit, math.sqrt(sum(x * x for x in unit)))
```

Output:

```text
[0.6, 0.8] 1.0
```

The result always has length 1 (apart from tiny rounding effects).

5.

```python
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def top_k(query_vector, documents, k):
    ranked = sorted(documents, key=lambda title: cosine(query_vector, documents[title]), reverse=True)
    return ranked[:k]


docs = {"A": [1, 0], "B": [0.9, 0.1], "C": [0, 1]}
print(top_k([1, 0.05], docs, 2))
```

Output:

```text
['A', 'B']
```

6.

```python
import math


def safe_cosine(a, b):
    la = math.sqrt(sum(x * x for x in a))
    lb = math.sqrt(sum(y * y for y in b))
    if la == 0 or lb == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (la * lb)


print(safe_cosine([0, 0], [1, 2]), safe_cosine([1, 2], [2, 4]))
```

Output:

```text
0.0 0.9999999999999998
```

7. Every embedding model builds its own "map" with its own directions and dimensions. A position in one model's space means nothing in another's, so vectors are only comparable when produced by the same model.

---

## Chapter Summary and Key Takeaways

- A vector is a list of numbers; an embedding is a learned vector that represents the meaning of text so that similar meanings are close together.
- Closeness is measured with arithmetic: dot product, length, cosine similarity (direction, from -1 to 1) or distance.
- Semantic search embeds documents and a query with the same model, then ranks documents by similarity; it powers the retrieval step of RAG.
- Embeddings measure similarity, not truth: negation and subtle differences can be missed, and vectors from different models cannot be compared.
- Check dimensions, handle zero vectors, and split long texts into chunks.

Next: [Chapter 34 — Context Window and Model Parameters](34-context-window-and-model-parameters.md) covers how much a model can read at once and what "parameters" means.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
