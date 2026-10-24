# Chapter 35 — Attention Mechanism and Transformers

> Part 6 — Python Integration and AI Foundations · Video: 11:46:56–12:04:37 · Previous: [34 Context Window and Model Parameters](34-context-window-and-model-parameters.md) · Next: [36 Pretraining, Fine-Tuning and RLHF](36-pretraining-fine-tuning-rlhf.md)

**In this chapter:** how a model decides which other tokens matter when it processes a token (*attention*), and how stacking attention with other layers gives the *transformer*, the design behind most current language models.

**Before you start:** you need lists, loops and functions, `math`, the softmax idea from [Temperature](31-llms-prompting-temperature-hallucination.md#temperature), and vectors and cosine/dot product from [Vectors and Embeddings](33-vectors-and-embeddings.md). Recap: a token becomes a vector; the dot product of two vectors is larger when they point the same way. The code here is a *toy demo* with tiny, hand-made numbers and standard library only. It shows the arithmetic idea; real models learn their numbers, use many dimensions and many attention heads, and run on specialised hardware. Examples were run with Python 3.13.

---

## Attention Mechanism

**Timestamp:** [11:46:56](https://www.youtube.com/watch?v=J9BI0jGOds8&t=42416s)

**Learning objectives:**

- Explain in plain language what attention does and why it is needed.
- Describe queries, keys and values and the steps: score, softmax, weighted sum.
- Compute a small attention example in Python.
- Explain causal masking and why long inputs make attention expensive.

**1. Intuition**

Read the sentence "The trophy did not fit in the suitcase because it was too big." To understand *it*, your mind looks back at the other words and gives the most weight to "trophy". Attention lets a model do something like this: when processing a word, it gives each other word a weight for how relevant it is, and blends the information in proportion to those weights. (An analogy: the model does not "read" like a person; it computes weights with arithmetic.)

**2. Why does it exist?**

Meaning depends on context: "bank" in "river bank" and "bank loan", or pronouns pointing to earlier nouns. Older sequence models passed information along one step at a time and tended to lose distant details, and they were slow to train because each step waited for the previous one. Attention lets every token look directly at every other token in one step, which handles long-range relations better and is easy to run in parallel.

**3. Technical explanation**

*Mechanism (one attention head).* Every token's vector is turned, by learned weight matrices, into three vectors:

- a **query** (what this token is looking for),
- a **key** (what this token offers to be matched against),
- a **value** (the information it contributes).

For one token:

1. **Score**: take the dot product of its query with the key of every token (including itself). Higher means more relevant. The scores are usually divided by the square root of the key dimension to keep them in a stable range.
2. **Softmax**: turn the scores into weights that are positive and add up to 1 (see [Temperature](31-llms-prompting-temperature-hallucination.md#temperature)).
3. **Weighted sum**: add up the value vectors, each multiplied by its weight. The result is the token's new, context-aware vector.

*Details.*

- **Multi-head attention** runs several heads in parallel, each with its own learned matrices, so that different heads can pick up different kinds of relations. Their outputs are combined.
- **Self-attention** means queries, keys and values all come from the same sequence.
- **Causal mask.** A text generator may only look at earlier tokens, not future ones (otherwise it could copy the answer). The scores for later positions are blocked before the softmax so their weights become 0.
- **Position.** Attention by itself ignores word order, so the model also adds information about each token's position to the vectors.
- **Cost.** Each token is compared with every other token, so the work grows with the square of the input length. This is a main reason why long context is expensive (see [Context Window](34-context-window-and-model-parameters.md#context-window)); many systems reuse stored keys and values from earlier tokens to avoid recomputing them during generation.
- **Intuition versus mechanism.** The weights are not human explanations of the model's reasoning; they are intermediate numbers. Looking at them can be informative but is not a reliable account of why the model answered as it did.

**4. Syntax**

```text
scores   = (Q . K^T) / sqrt(d)
weights  = softmax(scores)          # each row sums to 1
output   = weights . V
```

Here `Q`, `K`, `V` are the query, key and value vectors and `d` is the key dimension. This is a formula pattern, implemented below.

**5. Example 1 — Basic**

*Toy demo.* Attention for one token, with hand-made two-dimensional vectors:

```python
import math


def softmax(scores):
    exps = [math.exp(s) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


query = [1.0, 0.0]
keys = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1]]
values = [[10, 0], [0, 10], [8, 2]]
d = len(query)

scores = [dot(query, key) / math.sqrt(d) for key in keys]
weights = softmax(scores)
output = [sum(w * v[i] for w, v in zip(weights, values)) for i in range(2)]

print("scores: ", [round(s, 3) for s in scores])
print("weights:", [round(w, 3) for w in weights], "sum =", round(sum(weights), 3))
print("output: ", [round(x, 2) for x in output])
```

Output:

```text
scores:  [0.707, 0.0, 0.636]
weights: [0.412, 0.203, 0.384] sum = 1.0
output:  [7.2, 2.8]
```

Line by line:

- The query is compared with every key by dot product; keys 1 and 3 point close to the query, key 2 does not.
- `softmax` turns the three scores into weights adding up to 1. Keys 1 and 3 get large weights, key 2 a small one.
- The output is the weighted blend of the value vectors, so it lies between the values and leans towards those of the most relevant tokens.

**6. Example 2 — Practical**

*Toy demo.* A whole tiny sequence, with a causal mask. Each token has a made-up vector; to keep the example short the same vectors are used as queries, keys and values (real models use separate learned projections):

```python
import math

tokens = ["the", "cat", "sat"]
vectors = [[0.1, 0.1], [1.0, 0.2], [0.8, 0.9]]


def softmax(scores):
    exps = [math.exp(s) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def attention(vectors, causal):
    d = len(vectors[0])
    result = []
    for i, query in enumerate(vectors):
        scores = []
        for j, key in enumerate(vectors):
            score = sum(q * k for q, k in zip(query, key)) / math.sqrt(d)
            if causal and j > i:
                score = float("-inf")
            scores.append(score)
        weights = softmax(scores)
        mixed = [sum(w * v[k] for w, v in zip(weights, vectors)) for k in range(d)]
        result.append((weights, mixed))
    return result


for causal in (False, True):
    print("causal mask:" if causal else "no mask:")
    for token, (weights, mixed) in zip(tokens, attention(vectors, causal)):
        print(f"  {token:<4} weights={[round(w, 2) for w in weights]} -> {[round(x, 2) for x in mixed]}")
```

Output:

```text
no mask:
  the  weights=[0.31, 0.34, 0.35] -> [0.65, 0.41]
  cat  weights=[0.21, 0.4, 0.39] -> [0.73, 0.45]
  sat  weights=[0.19, 0.34, 0.47] -> [0.73, 0.51]
causal mask:
  the  weights=[1.0, 0.0, 0.0] -> [0.1, 0.1]
  cat  weights=[0.34, 0.66, 0.0] -> [0.69, 0.17]
  sat  weights=[0.19, 0.34, 0.47] -> [0.73, 0.51]
```

Line by line:

- For each position `i` the code scores its query against every key `j`, then softmaxes and mixes the vectors.
- With `causal=True`, scores for later positions `j > i` are set to minus infinity; `exp(-inf)` is 0, so those positions get weight exactly 0. The first token can only attend to itself, the last token to all three.
- Without the mask every token sees every other token, which is how models that read a whole text at once can work; text generators use the causal version.

**7. Example 3 — Edge case or common mistake**

Forgetting the scaling factor can make the weights too extreme when vectors have many dimensions:

```python
import math
import random


def softmax(scores):
    biggest = max(scores)
    exps = [math.exp(s - biggest) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


rng = random.Random(0)
d = 256
query = [rng.gauss(0, 1) for _ in range(d)]
keys = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(4)]
raw = [sum(q * k for q, k in zip(query, key)) for key in keys]
scaled = [score / math.sqrt(d) for score in raw]

print("without scaling:", [round(w, 3) for w in softmax(raw)])
print("with scaling:   ", [round(w, 3) for w in softmax(scaled)])
```

Output:

```text
without scaling: [0.0, 0.0, 0.718, 0.282]
with scaling:    [0.027, 0.191, 0.402, 0.379]
```

Dot products grow with the number of dimensions, so without scaling the softmax becomes extreme: here two keys take all the weight (0.718 and 0.282) and the other two get essentially 0, which makes learning hard. Dividing by `sqrt(d)` keeps the weights more balanced. The vectors here are random, only to show the numerical effect.

A numerically careful softmax subtracts the largest score first (as above). Without it, large scores overflow:

```python
import math

scores = [1000, 1001]
try:
    math.exp(scores[0])
except OverflowError as error:
    print("OverflowError:", error)

biggest = max(scores)
exps = [math.exp(s - biggest) for s in scores]
print([round(e / sum(exps), 3) for e in exps])
```

Output:

```text
OverflowError: math range error
[0.269, 0.731]
```

Subtracting the maximum does not change the result of softmax, but it keeps the numbers small.

Attention weights always add up to 1, so a token cannot "attend more" in total, only distribute attention differently, and a long input spreads weight thinly. The cost, too, grows quickly:

```python
for n in [1_000, 10_000, 100_000]:
    print(f"{n:>7} tokens -> {n * n:>14,} pairwise comparisons per head per layer")
```

Output:

```text
   1000 tokens ->      1,000,000 pairwise comparisons per head per layer
  10000 tokens ->    100,000,000 pairwise comparisons per head per layer
 100000 tokens -> 10,000,000,000 pairwise comparisons per head per layer
```

Ten times as many tokens means a hundred times as many comparisons. Real systems use optimised implementations and other tricks, but the pressure is why long context costs more.

**8. Common mistakes**

- Thinking attention is the model "understanding" like a person, or that attention weights fully explain its answers.
- Forgetting the scaling, or computing softmax without subtracting the maximum.
- Confusing queries, keys and values: queries and keys decide *how much*, values supply *what*.
- Forgetting the causal mask for text generation.
- Ignoring position information.
- Assuming that cost grows linearly with input length.

**9. Real-world and AI applications**

Attention is the core operation of language models, translation, summarisation and many image and audio models. It is why a model can resolve a pronoun, follow a reference to something said much earlier, and use an instruction at the start of a prompt when writing the end of an answer. Engineers who understand its quadratic cost make better decisions about context length, chunking and caching.

**10. Practice**

1. In Example 1, change the query to `[0.0, 1.0]`. Predict which value gets the largest weight, then run it.
2. Compute `softmax([0, 0, 0])` by hand and by code. What does it tell you?
3. Write `attend(query, keys, values)` that returns the weights and the output, and test it with two keys.
4. Add a line to Example 2 that prints which earlier token the last token attends to most.
5. Explain in your own words why a text generator needs a causal mask.
6. If an input grows from 2,000 to 8,000 tokens, by what factor do the pairwise comparisons grow?

**11. Interview questions**

- *What does attention do?* For each token it computes weights over the other tokens and blends their information accordingly.
- *What are queries, keys and values?* Learned projections of each token: the query asks, keys are matched against it, and values carry the content that is combined.
- *Why is it divided by the square root of the dimension?* To keep dot products from growing with the dimension, which would make the softmax too extreme.
- *Why is attention expensive for long inputs?* Every token is compared with every other token, so work grows with the square of the length.
- *What is multi-head attention?* Several attention computations in parallel with separate learned projections, combined at the end.

**12. Quick revision**

- Attention: weights over tokens, then a weighted sum of values.
- Score = query · key / √d; softmax; weighted sum.
- Causal mask blocks future tokens for generation.
- Multi-head: several attentions in parallel.
- Cost grows with the square of the length.

---

## Transformers

**Timestamp:** [11:52:46](https://www.youtube.com/watch?v=J9BI0jGOds8&t=42766s)

**Learning objectives:**

- Describe a transformer as a stack of repeated blocks and name the parts of a block.
- Explain how a transformer turns tokens into a next-token prediction.
- Explain why transformers became dominant (parallel training, long-range relations, scale).
- Relate the transformer to parameters, context window and generation.

**1. Intuition**

Picture a team passing a document through a series of review rounds. In each round, every reader looks at the whole text (attention), then each reader refines their own understanding privately (a feed-forward step). After dozens of rounds, the last note is turned into a guess for the next word. A transformer repeats this two-step block many times. (An analogy; the real "readers" are matrix calculations.)

**2. Why does it exist?**

Earlier designs processed text one token at a time, which made training slow and long-range context weak. The transformer, introduced in the 2017 paper "Attention Is All You Need", replaced step-by-step processing with attention over the whole sequence, which can be calculated in parallel on modern hardware. That made it practical to train on far more data with far more parameters, and capability grew with scale.

**3. Technical explanation**

*Pipeline for a text generator (decoder-style transformer):*

1. **Tokenize**: split text into tokens and map them to IDs (see [Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs)).
2. **Embed**: look up a vector for each token ID (see [Vectors and Embeddings](33-vectors-and-embeddings.md)) and add position information.
3. **Blocks**: pass the vectors through a stack of identical-in-structure blocks. Each block has:
   - **(masked, multi-head) self-attention**, to mix in information from earlier tokens;
   - a **feed-forward network** applied to each position separately, which transforms the vector (much of the model's stored knowledge is thought to sit in these layers, but this is an active research question);
   - **residual connections** (the input is added back to the output of each sub-layer) and **normalisation**, which keep training stable.
4. **Output layer**: the final vector of the last position is turned into a score for every token in the vocabulary, and softmax gives probabilities for the next token.
5. **Choose the next token** by sampling or taking the most likely, controlled by settings such as temperature (see [Temperature](31-llms-prompting-temperature-hallucination.md#temperature)).
6. **Repeat**: append the chosen token and run again, until a stop token or the output limit.

*Variants.* Encoder-style models read a whole text and produce representations (used for embeddings and classification); decoder-style models generate text token by token (most chat models); encoder-decoder models do both (often used for translation). Transformers are also used for images, audio and combinations (see [Multimodal AI](39-multimodal-reasoning-slm-agi-asi.md#multimodal-ai)).

*Why it connects everything in this part.* The number of blocks and the width of the vectors determine the **parameter count** (see [Model Parameters](34-context-window-and-model-parameters.md#model-parameters)); the length of sequence attention can handle is the **context window**; the one-token-at-a-time loop is why generation speed and cost depend on **output tokens**; and the learned weights come from **pretraining** (see [How LLMs Learn: Pretraining](36-pretraining-fine-tuning-rlhf.md#how-llms-learn-pretraining)).

*Limits.* The transformer predicts likely tokens from patterns in data; it does not by itself guarantee truth (see [AI Hallucination](31-llms-prompting-temperature-hallucination.md#ai-hallucination)), and its cost grows with long inputs. Researchers also study alternative architectures.

**4. Syntax**

```text
x = embed(tokens) + positions
for block in blocks:
    x = x + attention(norm(x))        # mix information between tokens
    x = x + feed_forward(norm(x))     # transform each token's vector
logits = output_layer(x[last])
probabilities = softmax(logits)
```

This is a pseudocode sketch of one common arrangement, not runnable code.

**5. Example 1 — Basic**

*Toy demo.* The generation loop around a model, using a made-up next-token function in place of the transformer. It shows the repeated "predict one token, append, repeat" structure:

```python
def fake_model(tokens):
    """Stand-in for a transformer: returns the next token for a few known prefixes."""
    table = {
        ("the",): "cat",
        ("the", "cat"): "sat",
        ("the", "cat", "sat"): "down",
        ("the", "cat", "sat", "down"): "<end>",
    }
    return table.get(tuple(tokens), "<end>")


tokens = ["the"]
for step in range(10):
    next_token = fake_model(tokens)
    print(f"step {step}: {tokens} -> {next_token}")
    if next_token == "<end>":
        break
    tokens.append(next_token)
print(" ".join(tokens))
```

Output:

```text
step 0: ['the'] -> cat
step 1: ['the', 'cat'] -> sat
step 2: ['the', 'cat', 'sat'] -> down
step 3: ['the', 'cat', 'sat', 'down'] -> <end>
the cat sat down
```

Line by line: each pass gives the whole current sequence to the "model", which returns one token; the token is appended and the loop repeats, until a stop token or the step limit (the analogue of the maximum output length). A real transformer replaces `fake_model` with the pipeline above.

**6. Example 2 — Practical**

*Toy demo.* One tiny transformer-style block on hand-made vectors: attention, then a feed-forward step, each with a residual connection (no normalisation, no learned weights; the "weights" are fixed numbers chosen for the demonstration):

```python
import math


def softmax(scores):
    biggest = max(scores)  # subtracting the maximum keeps exp() from overflowing
    exps = [math.exp(s - biggest) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def self_attention(vectors):
    d = len(vectors[0])
    out = []
    for i, q in enumerate(vectors):
        scores = [
            (sum(a * b for a, b in zip(q, k)) / math.sqrt(d)) if j <= i else float("-inf")
            for j, k in enumerate(vectors)
        ]
        w = softmax(scores)
        out.append([sum(wi * v[c] for wi, v in zip(w, vectors)) for c in range(d)])
    return out


def feed_forward(vector):
    # fixed toy transformation: scale, then keep only positive parts (a simple "ReLU")
    return [max(0.0, 2 * x - 0.5) for x in vector]


def block(vectors):
    attended = self_attention(vectors)
    after_attention = [[x + a for x, a in zip(v, att)] for v, att in zip(vectors, attended)]  # residual
    return [[x + f for x, f in zip(v, feed_forward(v))] for v in after_attention]  # residual


x = [[0.1, 0.1], [1.0, 0.2], [0.8, 0.9]]
for layer in range(1, 4):
    x = block(x)
    print(f"after block {layer}:", [[round(v, 2) for v in vec] for vec in x])
```

Output:

```text
after block 1: [[0.2, 0.2], [4.57, 0.6], [4.1, 3.73]]
after block 2: [[0.7, 0.7], [26.95, 3.08], [24.12, 21.89]]
after block 3: [[3.7, 3.7], [161.17, 18.0], [144.2, 130.82]]
```

Line by line:

- `self_attention` is the masked attention from the previous section (its `softmax` subtracts the largest score first, for the numerical reason shown in the attention section's edge cases; without it this toy overflows by the third block, because the vectors keep growing).
- `feed_forward` transforms each position independently.
- `block` adds each sub-layer's output back to its input (the residual connection) so information can pass through unchanged as well as transformed.
- Applying `block` repeatedly stacks blocks: the vectors change each time (in this toy they also grow, because the residual connections keep adding to them and nothing normalises them). A real model has dozens of blocks with learned weights, so that after the last block the final position's vector carries what is needed to predict the next token.

Turning the final vector into next-token probabilities, again with made-up numbers:

```python
import math

vocabulary = ["down", "up", "away", "<end>"]
logits = [2.0, 0.5, 0.1, -1.0]
exps = [math.exp(x) for x in logits]
probabilities = [e / sum(exps) for e in exps]
for word, p in zip(vocabulary, probabilities):
    print(f"{word:<6} {p:.3f}")
print("most likely:", vocabulary[probabilities.index(max(probabilities))])
```

Output:

```text
down   0.703
up     0.157
away   0.105
<end>  0.035
most likely: down
```

**7. Example 3 — Edge case or common mistake**

The generation loop needs a stop condition, otherwise it runs until the length limit:

```python
def looping_model(tokens):
    return "la"


tokens = ["sing:"]
limit = 6
while len(tokens) < limit:
    tokens.append(looping_model(tokens))
print(tokens)
print("stopped by the limit, not by an end token")
```

Output:

```text
['sing:', 'la', 'la', 'la', 'la', 'la']
stopped by the limit, not by an end token
```

Real models are trained to emit an end token, and applications also set a maximum number of output tokens. Repetition loops can still occur, which is one reason for that limit.

Each new token requires another pass, so output length matters for time:

```python
prompt_tokens = 500
for output_tokens in [10, 100, 1000]:
    passes = output_tokens
    print(f"{output_tokens:>4} output tokens -> {passes} generation steps, {prompt_tokens + output_tokens} tokens in context at the end")
```

Output:

```text
  10 output tokens -> 10 generation steps, 510 tokens in context at the end
 100 output tokens -> 100 generation steps, 600 tokens in context at the end
1000 output tokens -> 1000 generation steps, 1500 tokens in context at the end
```

Reading the prompt can be done largely in parallel, but writing the answer is sequential, so long answers are slower than long prompts of the same size.

A common misunderstanding is that the model "looks up" facts. The toy below contrasts a lookup table with generating from probabilities:

```python
import random

facts = {"capital of France": "Paris"}
print("lookup:", facts.get("capital of France"), "| missing key:", facts.get("capital of Atlantis"))

next_word_probabilities = {"Paris": 0.9, "Lyon": 0.07, "Rome": 0.03}
rng = random.Random(3)
print("sampled:", [rng.choices(list(next_word_probabilities), weights=next_word_probabilities.values())[0] for _ in range(10)])
```

Output:

```text
lookup: Paris | missing key: None
sampled: ['Paris', 'Paris', 'Paris', 'Paris', 'Paris', 'Paris', 'Paris', 'Paris', 'Paris', 'Paris']
```

A lookup returns `None` for a missing key, while a probability-based generator always produces *something*, which can be wrong when the data does not support it. This is the mechanism behind hallucination (see [AI Hallucination](31-llms-prompting-temperature-hallucination.md#ai-hallucination)). The probabilities here are invented, and with this seed all ten samples happen to be `Paris`; a different seed or a flatter distribution would show other words.

*Requires a library and downloaded model (not run here):*

```text
# pseudocode; loading real transformer models needs a package and model files
model = load_model("<model-name>")
text = model.generate("Once upon a time", max_new_tokens=20)
```

**8. Common mistakes**

- Thinking the model retrieves stored sentences instead of computing probabilities for the next token.
- Forgetting that generation repeats one token at a time (cost and delay grow with output length).
- Confusing the transformer (architecture) with a trained model (architecture plus learned weights).
- Treating "transformer" and "LLM" as identical: transformers are also used for images and audio, and LLMs are one use.
- Believing that all internal details (such as where facts are stored) are settled.
- Omitting a stop condition in generation loops.

**9. Real-world and AI applications**

Chat assistants, code completion, translation, summarisation, search embeddings, image and speech models all use transformer variants. Knowing the pipeline helps in practice: you understand why prompts are tokenized, why the window is limited, why output costs more than input, why answers stream out word by word, and why changing the model size changes both quality and price.

**10. Practice**

1. List the steps of the transformer pipeline from text to the next token.
2. In `fake_model`, add a branch so that `("the", "dog")` leads to `"ran"` and test the loop with `tokens = ["the", "dog"]`.
3. Change `feed_forward` in Example 2 to `max(0.0, x)` and print the result after two blocks.
4. Write `pick_next(vocabulary, logits)` that returns the most likely token using softmax.
5. Explain why output tokens take more time than the same number of input tokens.
6. What is a residual connection, and why might it help stacking many blocks?

**11. Interview questions**

- *What is a transformer?* A neural network architecture built from stacked blocks of self-attention and feed-forward layers, introduced in 2017, now the basis of most LLMs.
- *Why did it replace earlier sequence models?* It processes a whole sequence in parallel and relates distant tokens directly, so it trains faster on more data and scales better.
- *How does a transformer generate text?* It predicts a probability for each possible next token, picks one, appends it and repeats.
- *What is the difference between encoder and decoder models?* Encoders produce representations of a whole input; decoders generate tokens one at a time using only earlier tokens.
- *Where do the parameters live?* Mainly in the attention projections, the feed-forward layers and the token embedding table.

**12. Quick revision**

- Pipeline: tokenize, embed (plus position), blocks, output scores, softmax, pick, repeat.
- Block: masked self-attention + feed-forward, with residuals and normalisation.
- Parallel training and long-range attention made scale practical.
- Generation is sequential, so output tokens cost time.
- Probabilities, not lookups: fluent but possibly wrong.

---

## Answers to Practice Exercises

### Answers: Attention Mechanism

1. The query `[0.0, 1.0]` matches key 2 best, so value 2 gets the largest weight.

```python
import math

query = [0.0, 1.0]
keys = [[1.0, 0.0], [0.0, 1.0], [0.9, 0.1]]
scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(2) for key in keys]
exps = [math.exp(s) for s in scores]
print([round(e / sum(exps), 3) for e in exps])
```

Output:

```text
[0.244, 0.494, 0.262]
```

2. By hand: all three exponentials equal 1, so each weight is 1/3.

```python
import math

exps = [math.exp(0)] * 3
print([e / sum(exps) for e in exps])
```

Output:

```text
[0.3333333333333333, 0.3333333333333333, 0.3333333333333333]
```

Equal scores give equal weights: no token is preferred.

3.

```python
import math


def attend(query, keys, values):
    d = len(query)
    scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(d) for key in keys]
    exps = [math.exp(s) for s in scores]
    weights = [e / sum(exps) for e in exps]
    output = [sum(w * v[i] for w, v in zip(weights, values)) for i in range(len(values[0]))]
    return weights, output


weights, output = attend([1, 0], [[1, 0], [0, 1]], [[5, 0], [0, 5]])
print([round(w, 3) for w in weights], [round(o, 3) for o in output])
```

Output:

```text
[0.67, 0.33] [3.349, 1.651]
```

4.

```python
weights = [0.2, 0.3, 0.5]
tokens = ["the", "cat", "sat"]
earlier = list(zip(tokens, weights))[:-1]
print(max(earlier, key=lambda pair: pair[1])[0])
```

Output:

```text
cat
```

Here `weights` is a sample weight list for the last token (made-up numbers); in Example 2 you would use the weights returned for the last position, ignoring its own entry.

5. When generating, the next token is not yet known. If a position could look at later tokens during training, it could simply copy the answer instead of learning to predict it, and at generation time those tokens do not exist. The causal mask blocks them.

6. 8,000 / 2,000 = 4 times as many tokens, so 4² = 16 times as many comparisons.

### Answers: Transformers

1. Tokenize; embed and add positions; pass through the stack of blocks (self-attention, feed-forward, residuals and normalisation); output scores for each vocabulary token; softmax to probabilities; choose a token; append and repeat.

2.

```python
def fake_model(tokens):
    table = {
        ("the",): "cat",
        ("the", "dog"): "ran",
        ("the", "cat"): "sat",
    }
    return table.get(tuple(tokens), "<end>")


tokens = ["the", "dog"]
while True:
    nxt = fake_model(tokens)
    if nxt == "<end>":
        break
    tokens.append(nxt)
print(tokens)
```

Output:

```text
['the', 'dog', 'ran']
```

3.

```python
import math


def softmax(scores):
    exps = [math.exp(s) for s in scores]
    return [e / sum(exps) for e in exps]


def self_attention(vectors):
    d = len(vectors[0])
    out = []
    for i, q in enumerate(vectors):
        scores = [(sum(a * b for a, b in zip(q, k)) / math.sqrt(d)) if j <= i else float("-inf") for j, k in enumerate(vectors)]
        w = softmax(scores)
        out.append([sum(wi * v[c] for wi, v in zip(w, vectors)) for c in range(d)])
    return out


def feed_forward(vector):
    return [max(0.0, x) for x in vector]


def block(vectors):
    attended = self_attention(vectors)
    mid = [[x + a for x, a in zip(v, att)] for v, att in zip(vectors, attended)]
    return [[x + f for x, f in zip(v, feed_forward(v))] for v in mid]


x = [[0.1, 0.1], [1.0, 0.2], [0.8, 0.9]]
for _ in range(2):
    x = block(x)
print([[round(v, 2) for v in vec] for vec in x])
```

Output:

```text
[[1.6, 1.6], [13.53, 2.93], [12.29, 11.16]]
```

4.

```python
import math


def pick_next(vocabulary, logits):
    exps = [math.exp(x) for x in logits]
    probabilities = [e / sum(exps) for e in exps]
    return vocabulary[probabilities.index(max(probabilities))]


print(pick_next(["a", "b", "c"], [0.1, 2.0, 1.0]))
```

Output:

```text
b
```

5. Input tokens can be processed largely in parallel in one pass, but each output token depends on the previous one, so the model must run one pass per generated token, in sequence.

6. A residual connection adds a layer's input to its output. This lets information (and, during training, learning signals) pass through unchanged, so many blocks can be stacked without the original signal being lost.

---

## Chapter Summary and Key Takeaways

- Attention gives every token weights over the other tokens (score from query and key, softmax, weighted sum of values), so context can shape each token's representation.
- Multi-head attention runs several in parallel; a causal mask stops generators from looking ahead; cost grows with the square of the input length.
- A transformer stacks blocks of self-attention and feed-forward layers with residual connections; its output is a probability for each possible next token.
- Text is generated by repeating one pass per token, which is why output length costs time and why a stop condition is needed.
- A transformer computes probable continuations rather than looking up facts, which explains both its fluency and its hallucinations.

Next: [Chapter 36 — Pretraining, Fine-Tuning and RLHF](36-pretraining-fine-tuning-rlhf.md) explains how the weights get their values.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
