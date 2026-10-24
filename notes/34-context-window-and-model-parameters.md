# Chapter 34 — Context Window and Model Parameters

> Part 6 — Python Integration and AI Foundations · Video: 11:31:37–11:46:56 · Previous: [33 Vectors and Embeddings](33-vectors-and-embeddings.md) · Next: [35 Attention Mechanism and Transformers](35-attention-and-transformers.md)

**In this chapter:** the *context window* (how much text a model can consider in one call and what happens at the limit), and *model parameters* (the learned numbers inside a model, what "7 billion parameters" means, why size affects memory and cost, and how this differs from the *settings* you pass in a request).

**Before you start:** you need the token ideas from [Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs), context assembly from [Context Engineering](32-context-engineering-and-tokens.md#context-engineering), and basic arithmetic with Python. Recap: a token is a unit of text; the model reads and writes tokens. All code here is a *toy demo* using the standard library; the sizes and limits used are invented examples, not the specification of any real model.

---

## Context Window

**Timestamp:** [11:31:37](https://www.youtube.com/watch?v=J9BI0jGOds8&t=41497s)

**Learning objectives:**

- Define the context window and say what counts toward it.
- Predict what happens when a conversation or document exceeds it.
- Explain why a larger window is not an automatic fix.
- Write code that checks and trims content to fit a window.

**1. Intuition**

A context window is like the surface of a desk. Everything the model is working with (instructions, documents, the conversation, and the answer it is writing) has to lie on the desk at once. A bigger desk lets you spread out more papers, but a cluttered desk is slower to work at, costs more to rent, and some papers at the edges can get overlooked. Anything that does not fit on the desk simply is not seen. (An analogy: the model does not literally look at papers.)

**2. Why does it exist?**

The model's calculations compare tokens with other tokens in the input (see [Attention Mechanism](35-attention-and-transformers.md#attention-mechanism)), and the work and memory needed grow as the input gets longer. A model is also trained on sequences up to some length. So each model has a maximum number of tokens it can handle in one call: its context window (also called context length).

**3. Technical explanation**

- The **context window** is the maximum number of tokens the model can process in a single call. It covers the *input* (system instructions, history, documents, tool results, your question) **and** the *output* it generates, so `input tokens + output tokens <= window`.
- **Sizes** differ between models and change over time: from a few thousand tokens to hundreds of thousands or more. Look up the current figure for the model you use; the numbers in this chapter are invented.
- **Beyond the limit.** Depending on the service, a call that is too long is rejected with an error, or older content is cut off, or the answer is truncated. Chat applications often drop or summarise the oldest messages. Never assume the model "remembers" what has been cut: it has no access to it.
- **No memory between calls.** The model keeps nothing between calls. A "conversation" works because the application re-sends the history each time inside the window.
- **Bigger is not automatically better.**
  - Cost and delay rise with the number of input tokens.
  - Models can use information in a long context less reliably than information in a short one, particularly details buried in the middle, although this varies by model and improves over time.
  - Irrelevant material distracts; selection (see [Context Engineering](32-context-engineering-and-tokens.md#context-engineering)) still matters.
  - A large window is a limit, not a goal: use only what you need.
- **Strategies when content is too long.** Truncate (keep the start, the end, or the most recent part), summarise older parts, split documents into chunks and retrieve only the relevant ones (see [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)), or use a model with a larger window.
- **Window versus training data.** The window limits what the model can *see now*; its knowledge from training is separate and does not use up the window (see [How LLMs Learn: Pretraining](36-pretraining-fine-tuning-rlhf.md#how-llms-learn-pretraining)).

**4. Syntax**

```text
input_tokens + max_output_tokens <= context_window

available_for_input = context_window - tokens_reserved_for_answer
```

These are patterns, implemented in the examples.

**5. Example 1 — Basic**

*Toy demo.* Checking whether an input fits, using words as a stand-in for tokens:

```python
CONTEXT_WINDOW = 50
RESERVED_FOR_ANSWER = 15

system = "You are a helpful assistant."
history = ["Hello there.", "Hi! How can I help you today?"]
question = "Please summarise the main ideas of object oriented programming in simple words."

parts = [system] + history + [question]
used = sum(len(part.split()) for part in parts)
available = CONTEXT_WINDOW - RESERVED_FOR_ANSWER

print("input words:", used)
print("available for input:", available)
print("fits:", used <= available)
```

Output:

```text
input words: 26
available for input: 35
fits: True
```

Line by line: all parts of the input are added up, the room reserved for the answer is subtracted from the window, and the two numbers are compared. Here it fits with room to spare; adding more history would eventually break the inequality.

**6. Example 2 — Practical**

*Toy demo.* A chat history trimmer that keeps the system message and as many recent turns as fit, the strategy used by many simple chat applications:

```python
def words(text):
    return len(text.split())


def trim_to_window(system, turns, question, limit):
    used = words(system) + words(question)
    kept = []
    for role, text in reversed(turns):
        cost = words(text)
        if used + cost > limit:
            break
        kept.append((role, text))
        used += cost
    kept.reverse()
    return kept, used


turns = [
    ("user", "My name is Asha and I am learning Python."),
    ("assistant", "Nice to meet you Asha. Python is a great choice."),
    ("user", "What is a dictionary?"),
    ("assistant", "A collection of key and value pairs."),
    ("user", "Show an example."),
    ("assistant", "ages = {'Asha': 20}"),
]

for limit in [60, 30, 20]:
    kept, used = trim_to_window("Be brief.", turns, "What is my name?", limit)
    print(f"limit {limit}: kept {len(kept)} of {len(turns)} turns, used {used}")
    print("   first kept turn:", kept[0][1] if kept else None)
```

Output:

```text
limit 60: kept 6 of 6 turns, used 43
   first kept turn: My name is Asha and I am learning Python.
limit 30: kept 4 of 6 turns, used 24
   first kept turn: What is a dictionary?
limit 20: kept 3 of 6 turns, used 20
   first kept turn: A collection of key and value pairs.
```

Line by line:

- The system message and the new question are always counted, then turns are added from newest to oldest until the limit would be exceeded.
- With a small window the early turns (including the one with the user's name) are dropped, so the model *cannot* answer "What is my name?" from the history. Nothing is wrong with the model; the information is simply not in the window.
- Summarising old turns into one short line (for example "The user is Asha, learning Python") would keep important facts using few tokens.

**7. Example 3 — Edge case or common mistake**

Forgetting to reserve room for the answer:

```python
CONTEXT_WINDOW = 100
input_tokens = 98
max_output_tokens = 20

print("input fits alone:", input_tokens <= CONTEXT_WINDOW)
print("input plus output fits:", input_tokens + max_output_tokens <= CONTEXT_WINDOW)
print("room left for the answer:", CONTEXT_WINDOW - input_tokens)
```

Output:

```text
input fits alone: True
input plus output fits: False
room left for the answer: 2
```

The input alone fits, but only 2 tokens remain for the answer, so a longer answer would be cut off or rejected.

Cutting text in the middle of a word or sentence is another trap. Compare a blunt cut with one at a sentence boundary:

```python
text = "Python is popular. It is easy to read. It is used in AI. It has many libraries."
limit = 40

blunt = text[:limit]
sentences = text.split(". ")
kept, total = [], 0
for sentence in sentences:
    if total + len(sentence) + 2 > limit:
        break
    kept.append(sentence)
    total += len(sentence) + 2
clean = ". ".join(kept) + "."

print(repr(blunt))
print(repr(clean))
```

Output:

```text
'Python is popular. It is easy to read. I'
'Python is popular. It is easy to read.'
```

The blunt cut ends in the middle of a word, which can confuse the model; cutting at sentence boundaries keeps the text meaningful (the rule here is simplified: it does not handle abbreviations such as "e.g.").

Naive truncation can also remove the most important part:

```python
document = ["Intro.", "Background.", "Background 2.", "KEY RESULT: the answer is 42."]
print("keep first two:", document[:2])
print("keep last two: ", document[-2:])
```

Output:

```text
keep first two: ['Intro.', 'Background.']
keep last two:  ['Background 2.', 'KEY RESULT: the answer is 42.']
```

Keeping only the start loses the key result at the end. Decide what matters (start, end, or the most relevant chunks) rather than always cutting the tail.

**8. Common mistakes**

- Counting only the input and forgetting the output.
- Assuming the model remembers what was cut or earlier calls.
- Believing a larger window means you can skip selection and trimming.
- Cutting text mid-sentence, or cutting the most important part.
- Using a window size from memory or an old article rather than the current documentation.
- Ignoring cost and delay, which grow with input length.

**9. Real-world and AI applications**

Chat products manage the window by trimming or summarising history; document question-answering splits long files into chunks and retrieves the relevant ones; coding assistants choose which files to include; agents summarise earlier steps to keep working on long tasks. Teams measure tokens per request to stay within the limit and the budget.

**10. Practice**

1. A model has a window of 8,000 tokens. Your prompt is 6,500 tokens and you want up to 2,000 tokens of answer. Does it fit? By how much are you over or under?
2. Modify `trim_to_window` so that it also adds a note `"[earlier turns omitted]"` when anything was dropped.
3. Write `fits(parts, window, reserve)` that returns `True` if the word count of all parts plus `reserve` is at most `window`.
4. Write a function that keeps both the first and the last `n` words of a long text with `"..."` between them.
5. Why can a chat application "forget" something you told it earlier in a long conversation?
6. Give two reasons why a very large window is not always the best choice.

**11. Interview questions**

- *What is a context window?* The maximum number of tokens (input plus output) a model can handle in a single call.
- *What happens if you exceed it?* The call may be rejected, older content may be dropped, or the output may be cut off, depending on the service.
- *Does the model remember earlier conversations?* Not by itself; the application re-sends history within the window, or stores facts externally.
- *How do you handle documents longer than the window?* Chunk and retrieve, summarise, or truncate carefully; or use a larger-window model.

**12. Quick revision**

- Window = max tokens per call, input plus output.
- Beyond it: error, cut or truncated.
- No memory between calls; history is re-sent.
- Bigger window: more cost and delay, not a replacement for selection.
- Trim, summarise, or retrieve; reserve room for the answer.

---

## Model Parameters

**Timestamp:** [11:39:49](https://www.youtube.com/watch?v=J9BI0jGOds8&t=41989s)

**Learning objectives:**

- Explain what a model *parameter* (weight) is and what "7B parameters" means.
- Distinguish learned parameters from request settings such as temperature and maximum output length.
- Estimate the memory a model needs from its parameter count and numeric precision.
- Describe how parameter count relates to capability, cost and speed, and why it is not the whole story.

**1. Intuition**

Think of a huge mixing desk with billions of tiny dials. Training turns the dials, little by little, until the output sounds right; once training is finished the dial positions are fixed and *are* the model's knowledge. "Parameters" are the dials. Separately, the person using the model has a few front-panel knobs (such as temperature) that can be changed on every request without touching the dials. (An analogy: the parameters are numbers in matrices, not physical dials.)

**2. Why does it exist?**

A model has to store what it has learned somewhere. Numbers that are adjusted during training are the mechanism by which a network adapts to data. The word "parameter" is used in two ways in AI work, and confusing them causes real mix-ups, so this chapter keeps them apart.

**3. Technical explanation**

*Two meanings of "parameters".*

1. **Model parameters (weights).** The numbers inside the model that are learned during training: weights and biases in its layers. They are what the model file stores. They do not change while you use the model (unless it is trained further, see [Fine-Tuning](36-pretraining-fine-tuning-rlhf.md#fine-tuning)).
2. **Request parameters (settings).** Options you send with each call: temperature, the maximum number of output tokens, stop sequences, and similar sampling options (see [Temperature](31-llms-prompting-temperature-hallucination.md#temperature)). The exact names and ranges depend on the provider. They change *how* the fixed model generates, not what it has learned.

*Parameter count.* Models are often described by their parameter count: "7B" means about 7 billion (7 × 10⁹) learned numbers. Counts for large models range from millions to hundreds of billions or more (some are not published).

*Where parameters live.* A network is made of layers; a simple layer that maps `n_in` inputs to `n_out` outputs has `n_in × n_out` weights plus `n_out` biases. Stacking many wide layers multiplies the count quickly. In a transformer (see [Transformers](35-attention-and-transformers.md#transformers)) most parameters are in the attention and feed-forward layers and in the token embedding table (see [Vectors and Embeddings](33-vectors-and-embeddings.md)).

*Memory estimate.* Each parameter is stored as a number of a chosen precision:

- 32-bit floating point: 4 bytes per parameter
- 16-bit: 2 bytes
- 8-bit quantised: 1 byte
- 4-bit quantised: 0.5 byte

so memory for the weights is about `parameters × bytes per parameter`. Running a model also needs extra memory for the working state of the current context, so this is a lower bound. **Quantisation** means storing the weights at lower precision to save memory, often with a small loss of quality.

*Size and capability.* More parameters generally give a model more capacity to learn, but quality also depends on the amount and quality of training data, the training method and the architecture. A smaller, well-trained model can beat a larger, weaker one on a given task. Larger models cost more to run and are slower (see [Small Language Models](39-multimodal-reasoning-slm-agi-asi.md#small-language-models-slms)). Some designs (for example *mixture of experts*) have a large total parameter count but use only part of it for each token.

*Open weights.* Some models publish their parameters (open-weight models) so that you can run them yourself; with others the weights are private and you can only call them through a service.

**4. Syntax**

```text
dense layer parameters = n_in * n_out + n_out        # weights + biases

weight_memory_bytes = parameter_count * bytes_per_parameter
```

Patterns, implemented below.

**5. Example 1 — Basic**

*Toy demo.* Counting the parameters of a small network (a stack of dense layers) by formula:

```python
layer_sizes = [4, 8, 8, 2]


def dense_parameters(n_in, n_out):
    return n_in * n_out + n_out


total = 0
for n_in, n_out in zip(layer_sizes, layer_sizes[1:]):
    count = dense_parameters(n_in, n_out)
    print(f"{n_in:>2} -> {n_out:>2}: {count} parameters")
    total += count
print("total:", total)
```

Output:

```text
 4 ->  8: 40 parameters
 8 ->  8: 72 parameters
 8 ->  2: 18 parameters
total: 130
```

Line by line: `zip(layer_sizes, layer_sizes[1:])` pairs each layer with the next; each pair is a block of weights (`n_in × n_out`) plus one bias per output. A network this small has a few hundred parameters; a language model has billions, but the counting idea is the same.

**6. Example 2 — Practical**

*Toy demo.* Estimating the memory needed for the weights at different precisions. The model sizes are generic round numbers, not specific products:

```python
BYTES = {"32-bit": 4, "16-bit": 2, "8-bit": 1, "4-bit": 0.5}


def weight_gigabytes(parameters, precision):
    return parameters * BYTES[precision] / 1e9


for billions in [1, 7, 70]:
    parameters = billions * 1_000_000_000
    row = ", ".join(f"{p}: {weight_gigabytes(parameters, p):.1f} GB" for p in BYTES)
    print(f"{billions:>2}B -> {row}")
```

Output:

```text
 1B -> 32-bit: 4.0 GB, 16-bit: 2.0 GB, 8-bit: 1.0 GB, 4-bit: 0.5 GB
 7B -> 32-bit: 28.0 GB, 16-bit: 14.0 GB, 8-bit: 7.0 GB, 4-bit: 3.5 GB
70B -> 32-bit: 280.0 GB, 16-bit: 140.0 GB, 8-bit: 70.0 GB, 4-bit: 35.0 GB
```

Line by line:

- The dictionary maps each precision to bytes per parameter.
- The function multiplies the parameter count by the bytes and converts to gigabytes (using 10⁹ bytes per GB).
- The table shows why precision matters: a 7B model needs about 28 GB at 32-bit but only about 3.5 GB at 4-bit. These are lower bounds for the weights alone; the context and software need extra memory. This is why smaller or quantised models can run on ordinary hardware while the largest ones need specialised servers.

Request parameters, by contrast, are simply values you pass. *Pseudocode, requires an AI service; the names vary by provider and are placeholders:*

```text
response = call_model(
    model="<model-name>",
    messages=[...],
    temperature=0.2,        # randomness of sampling
    max_output_tokens=300,  # cap on the answer length
    stop=["\n\n"],          # optional stop sequences
)
```

**7. Example 3 — Edge case or common mistake**

Mixing up the two meanings: changing a request parameter does not change what the model knows. A toy "model" with a fixed learned table and a request setting makes the difference concrete:

```python
import random

# learned parameters: fixed once "training" is done
learned = {"sunny": 0.7, "rainy": 0.2, "snowy": 0.1}


def generate(temperature, seed):
    rng = random.Random(seed)
    if temperature == 0:
        return max(learned, key=learned.get)
    weights = [value ** (1 / temperature) for value in learned.values()]
    return rng.choices(list(learned), weights=weights)[0]


print("learned table before:", learned)
print([generate(0, seed) for seed in range(5)])
print([generate(2.0, seed) for seed in range(8)])
print("learned table after: ", learned)
```

Output:

```text
learned table before: {'sunny': 0.7, 'rainy': 0.2, 'snowy': 0.1}
['sunny', 'sunny', 'sunny', 'sunny', 'sunny']
['snowy', 'sunny', 'snowy', 'sunny', 'sunny', 'rainy', 'rainy', 'sunny']
learned table after:  {'sunny': 0.7, 'rainy': 0.2, 'snowy': 0.1}
```

With temperature 0 the same most likely word is chosen every time; with a higher temperature other words appear. Either way the learned table is untouched: settings change the sampling, not the stored knowledge.

Bigger is not automatically better, and numbers can be misleading:

```python
models = [("A", 70, 60), ("B", 7, 75)]  # name, billions of parameters, invented task score
for name, size, score in models:
    print(f"model {name}: {size}B parameters, invented score {score}, score per billion {score / size:.1f}")
best = max(models, key=lambda m: m[2])
print("best on this invented task:", best[0])
```

Output:

```text
model A: 70B parameters, invented score 60, score per billion 0.9
model B: 7B parameters, invented score 75, score per billion 10.7
best on this invented task: B
```

The scores are invented to make a point: in this made-up case the smaller model does better on the task, because parameter count is only one factor.

Memory estimates are lower bounds, and unit conventions differ:

```python
parameters = 7_000_000_000
weights_gb = parameters * 2 / 1e9
weights_gib = parameters * 2 / 2**30
print(round(weights_gb, 2), "GB (decimal)")
print(round(weights_gib, 2), "GiB (binary)")
```

Output:

```text
14.0 GB (decimal)
13.04 GiB (binary)
```

Decimal gigabytes and binary gibibytes differ by about 7 percent here; check which one a tool reports.

**8. Common mistakes**

- Using "parameters" for both learned weights and request settings without saying which.
- Assuming more parameters always means a better model.
- Treating the weights-only memory estimate as the total memory needed.
- Mixing up decimal GB and binary GiB, or ignoring precision.
- Thinking that changing temperature teaches the model something.
- Assuming the parameter count of every model is public.

**9. Real-world and AI applications**

Parameter count and precision decide whether a model fits on a laptop, a single server GPU or a cluster, and drive serving cost. Teams choose between a large hosted model and a small, possibly quantised, model they run themselves based on quality needs, latency, privacy and cost. Request parameters are tuned per task: low temperature for extraction, higher for brainstorming, and a sensible maximum output length to control cost.

**10. Practice**

1. Compute the parameter count of a network with layer sizes `[10, 20, 5]`.
2. A model has 13 billion parameters. How many gigabytes do the weights need at 16-bit and at 4-bit precision?
3. Name two request parameters and say what each changes.
4. Explain in one sentence the difference between a model's parameters and the parameters of a request.
5. Write `describe(parameters)` that returns `"7.0B"` for 7,000,000,000 and `"350.0M"` for 350,000,000.
6. Why is "weights memory" only a lower bound for what you need to run a model?

**11. Interview questions**

- *What are model parameters?* The learned numbers (weights and biases) that hold what the model learned during training.
- *What does 70B mean?* About 70 billion learned parameters.
- *How does parameter count affect cost?* More parameters need more memory and computation, which means slower and costlier serving.
- *What is quantisation?* Storing weights at lower numeric precision to reduce memory, usually with some quality trade-off.
- *Are temperature and max tokens parameters of the model?* They are request settings that control generation, not learned parameters.

**12. Quick revision**

- Parameters (weights): learned, fixed after training, hold the model's knowledge.
- Request parameters: temperature, max tokens, etc., set per call.
- Dense layer: `n_in × n_out + n_out`.
- Memory ≈ parameters × bytes per parameter (a lower bound).
- Size is not everything: data, training and design matter.

---

## Answers to Practice Exercises

### Answers: Context Window

1. The total is 6,500 + 2,000 = 8,500 tokens, which is 500 over the 8,000 window; it does not fit. Reduce the prompt to 6,000 tokens or fewer, or lower the maximum output.

```python
window, prompt, answer = 8000, 6500, 2000
print(prompt + answer, prompt + answer - window)
```

Output:

```text
8500 500
```

2.

```python
def words(text):
    return len(text.split())


def trim_with_note(system, turns, question, limit):
    note = "[earlier turns omitted]"
    used = words(system) + words(question)
    kept = []
    for role, text in reversed(turns):
        if used + words(text) > limit:
            break
        kept.append((role, text))
        used += words(text)
    kept.reverse()
    if len(kept) < len(turns) and used + words(note) <= limit:
        kept.insert(0, ("system", note))
    return kept


turns = [("user", "one two three four"), ("assistant", "five six seven"), ("user", "eight nine")]
print(trim_with_note("Be brief.", turns, "Why?", 11))
```

Output:

```text
[('system', '[earlier turns omitted]'), ('assistant', 'five six seven'), ('user', 'eight nine')]
```

3.

```python
def fits(parts, window, reserve):
    return sum(len(p.split()) for p in parts) + reserve <= window


print(fits(["a b c", "d e"], 10, 4), fits(["a b c", "d e"], 8, 4))
```

Output:

```text
True False
```

4.

```python
def head_and_tail(text, n):
    words = text.split()
    if len(words) <= 2 * n:
        return text
    return " ".join(words[:n] + ["..."] + words[-n:])


print(head_and_tail("one two three four five six seven eight nine ten", 2))
```

Output:

```text
one two ... nine ten
```

5. The application re-sends history inside the window. In a long conversation the oldest messages may be trimmed or summarised to make room, so the model no longer receives them and cannot use them.

6. For example: higher cost and slower responses as the input grows, less reliable use of details buried in very long inputs, and the fact that irrelevant material can distract the model.

### Answers: Model Parameters

1.

```python
sizes = [10, 20, 5]
total = sum(a * b + b for a, b in zip(sizes, sizes[1:]))
print(total)
```

Output:

```text
325
```

2.

```python
parameters = 13_000_000_000
print(parameters * 2 / 1e9, "GB at 16-bit")
print(parameters * 0.5 / 1e9, "GB at 4-bit")
```

Output:

```text
26.0 GB at 16-bit
6.5 GB at 4-bit
```

3. For example: `temperature` changes how random the sampling is; `max_output_tokens` caps the length of the answer.

4. A model's parameters are the learned weights stored in the model; the parameters of a request are the settings sent with each call to control generation.

5.

```python
def describe(parameters):
    if parameters >= 1e9:
        return f"{parameters / 1e9:.1f}B"
    return f"{parameters / 1e6:.1f}M"


print(describe(7_000_000_000), describe(350_000_000))
```

Output:

```text
7.0B 350.0M
```

6. Running a model also needs memory for the working state of the current context and for the software around it, so the weights alone are a minimum.

---

## Chapter Summary and Key Takeaways

- The context window is the maximum number of tokens in one call, covering input and output; beyond it content is rejected, cut or dropped, and the model cannot use what it does not receive.
- Models keep no memory between calls: the application re-sends history, trims or summarises it, or retrieves relevant pieces.
- A bigger window costs more and is slower, and does not replace choosing what goes in.
- Model parameters are the learned weights fixed after training; "7B" means about seven billion of them; request parameters such as temperature are separate settings.
- Memory for weights is roughly parameters times bytes per parameter (a lower bound); quantisation saves memory; size is only one factor in quality.

Next: [Chapter 35 — Attention Mechanism and Transformers](35-attention-and-transformers.md) explains how a model relates the tokens in its window to each other.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
