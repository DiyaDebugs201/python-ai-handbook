# Chapter 39 — Multimodal AI, Reasoning Models, SLMs, AGI and ASI

> Part 6 — Python Integration and AI Foundations · Video: 12:45:49–12:56:47 · Previous: [38 Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md) · Next: [40 Recap and Final Thoughts](40-recap-and-final-thoughts.md)

**In this chapter:** four widening ideas: *multimodal AI* (models that handle more than text), *reasoning models* (models that spend extra computation on intermediate steps before answering), *small language models* (compact models and when they are the better choice), and *AGI versus ASI* (terms for hypothetical future levels of AI capability).

**Before you start:** you need lists, dictionaries, functions, `collections.Counter`, and the ideas of tokens ([Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs)), embeddings ([Vectors and Embeddings](33-vectors-and-embeddings.md)), parameters ([Model Parameters](34-context-window-and-model-parameters.md#model-parameters)) and the transformer ([Transformers](35-attention-and-transformers.md#transformers)). All code is a *toy demo* (standard library, tiny data, invented numbers) or *pseudocode*. This area changes quickly: names of products and benchmark results are deliberately not given, and the descriptions here are general ones that should be checked against current sources. Examples were run with Python 3.13.

---

## Multimodal AI

**Timestamp:** [12:45:49](https://www.youtube.com/watch?v=J9BI0jGOds8&t=45949s)

**Learning objectives:**

- Define *modality* and *multimodal model*, with examples of input and output modalities.
- Explain at a high level how images and audio become sequences of vectors a transformer can use.
- Show an image as numbers and cut it into patches in Python.
- State common uses and limits.

**1. Intuition**

People understand the world through several senses at once: you read a menu, see a photo of the dish, and hear the waiter. A text-only model is like someone who has only ever read descriptions. A multimodal model can take in other kinds of input (pictures, sound, sometimes video) and relate them to words: "what is in this photo?", "read this chart", "describe this audio". (An analogy: the model does not see or hear; it processes numbers derived from pixels or sound.)

**2. Why does it exist?**

Much real information is not text: screenshots, scanned forms, charts, diagrams, photos, voice. Converting everything to text first loses information (layout, colour, tone of voice). Models that accept these inputs directly can answer questions about them and combine them with text instructions.

**3. Technical explanation**

- **Modality**: a type of data: text, image, audio, video, and others (such as tables or sensor data). A **multimodal** model handles more than one, as input, output, or both. Many systems accept images and text and produce text; others generate images, speech or video.
- **Turning non-text into vectors.** A transformer works on sequences of vectors (see [Transformers](35-attention-and-transformers.md#transformers)). For images, a common approach is to cut the image into small square **patches**, turn each patch into a vector with a learned layer, and treat the sequence of patch vectors somewhat like tokens. Audio is turned into a sequence of short-time features and processed similarly. Details differ between models.
- **Shared space.** Some models learn embeddings so that an image and a caption that describe the same thing end up close together in one vector space (see [Vectors and Embeddings](33-vectors-and-embeddings.md)). That enables search for images by text description.
- **Combining modalities.** The vectors from the image encoder and the text tokens can be placed into one sequence, and attention can relate words to image patches.
- **Cost.** Images and audio use many tokens' worth of the context window and cost accordingly; check how your provider counts them (see [Context Window](34-context-window-and-model-parameters.md#context-window)).
- **Limits.** Models can misread small text, charts and spatial relations; count objects wrongly; and **hallucinate** details that are not in the image. They may reflect biases in training data. Do not rely on them alone for high-stakes decisions, and be careful with images containing personal or sensitive information.

**4. Syntax**

*Pseudocode, requires an AI service (the message shape varies by provider; names are placeholders):*

```text
messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "What does this chart show?"},
        {"type": "image", "data": "<image bytes or a link, per provider's rules>"},
    ]}
]
answer = call_model(model="<multimodal-model-name>", messages=messages)
```

**5. Example 1 — Basic**

*Toy demo.* An image is a grid of numbers. A tiny 4×4 greyscale "image" (0 is black, 255 is white), printed and summarised:

```python
image = [
    [0, 0, 255, 255],
    [0, 0, 255, 255],
    [255, 255, 0, 0],
    [255, 255, 0, 0],
]

for row in image:
    print(" ".join(f"{pixel:>3}" for pixel in row))

pixels = [p for row in image for p in row]
print("pixels:", len(pixels), "| average brightness:", sum(pixels) / len(pixels))
print("height x width:", len(image), "x", len(image[0]))
```

Output:

```text
  0   0 255 255
  0   0 255 255
255 255   0   0
255 255   0   0
pixels: 16 | average brightness: 127.5
height x width: 4 x 4
```

Line by line: the image is a list of rows, each row a list of pixel values. The comprehension flattens the grid so the average can be computed. A real photo has colour channels (typically three numbers per pixel) and millions of pixels, but it is still numbers.

**6. Example 2 — Practical**

*Toy demo.* Cutting the image into patches and turning each patch into a small vector: the first step of how an image becomes a sequence for a transformer. Here the "vector" for a patch is just its average brightness and its darkest value; in a real model a learned layer produces a long vector:

```python
image = [
    [0, 0, 255, 255, 10, 10],
    [0, 0, 255, 255, 10, 10],
    [255, 255, 0, 0, 200, 200],
    [255, 255, 0, 0, 200, 200],
]
PATCH = 2


def patches(image, size):
    result = []
    for top in range(0, len(image), size):
        for left in range(0, len(image[0]), size):
            block = [row[left:left + size] for row in image[top:top + size]]
            result.append(block)
    return result


def describe(block):
    flat = [p for row in block for p in row]
    return [sum(flat) / len(flat), min(flat)]


sequence = [describe(block) for block in patches(image, PATCH)]
print(len(sequence), "patches")
for index, vector in enumerate(sequence):
    print(index, vector)
```

Output:

```text
6 patches
0 [0.0, 0]
1 [255.0, 255]
2 [10.0, 10]
3 [255.0, 255]
4 [0.0, 0]
5 [200.0, 200]
```

Line by line:

- Two nested `range` loops step across the image in blocks of `PATCH` rows and columns; slicing extracts each block.
- `describe` turns a block into a small vector.
- The result is a *sequence* of vectors, left to right and top to bottom, which can sit next to text tokens in one sequence. A 4×6 image with 2×2 patches gives 6 patches.

**7. Example 3 — Edge case or common mistake**

Image sizes that do not divide evenly into patches need padding or cropping, otherwise edge pixels are silently lost:

```python
image = [[1, 2, 3, 4, 5]] * 3  # 3 rows, 5 columns
size = 2
rows_used = (len(image) // size) * size
cols_used = (len(image[0]) // size) * size
print("image:", len(image), "x", len(image[0]))
print("covered by whole patches:", rows_used, "x", cols_used)
print("pixels dropped:", len(image) * len(image[0]) - rows_used * cols_used)
```

Output:

```text
image: 3 x 5
covered by whole patches: 2 x 4
pixels dropped: 7
```

If a pipeline only keeps whole patches, a 3×5 image loses 7 of its 15 pixels. Real systems resize or pad to avoid this; resizing a large image too aggressively also loses fine detail, which is why small text in screenshots is sometimes misread.

Image size matters for cost. If a provider charged by patches (illustrative only: real providers use their own rules):

```python
def patch_count(width, height, patch=16):
    return -(-width // patch) * -(-height // patch)  # ceiling division


for width, height in [(224, 224), (1024, 768), (4000, 3000)]:
    print(f"{width}x{height}: {patch_count(width, height)} patches")
```

Output:

```text
224x224: 196 patches
1024x768: 3072 patches
4000x3000: 47000 patches
```

A large photo can mean thousands of patches, so images can use a large part of the context window; many services resize large images before processing.

Checking that the model's description matches the data is a good habit; a toy check of a claim against data:

```python
chart_values = {"Mon": 12, "Tue": 18, "Wed": 9}
claim = "Tuesday had the highest value"
highest = max(chart_values, key=chart_values.get)
print(claim, "->", "supported" if highest == "Tue" else "not supported", f"(max is {highest})")
```

Output:

```text
Tuesday had the highest value -> supported (max is Tue)
```

When you have the underlying data, verify what a model says about a chart against it.

**8. Common mistakes**

- Assuming the model "sees" an image like a person, and trusting every detail it states.
- Sending huge images without considering token cost and resizing.
- Expecting precise counting, measuring or small-text reading to always work.
- Uploading images with private or sensitive information without considering where they go.
- Forgetting that outputs can also be non-text and that input and output modalities differ per model.

**9. Real-world and AI applications**

Document and receipt reading, chart and screenshot question answering, accessibility (image descriptions, speech to text), visual search, voice assistants, video summarisation, image and speech generation, robotics and vehicles combining camera and other sensors. The capability varies a lot between models, so test on your own examples.

**10. Practice**

1. Write a function that returns the brightest pixel value and its `(row, column)` position in the toy image.
2. Change `PATCH` to 1 in Example 2. How many patches are there, and what does each vector contain?
3. Write `flip_horizontal(image)` that mirrors the image left to right.
4. Compute `patch_count(512, 512, 32)`.
5. Why can an image use many tokens of the context window?
6. Name two risks of relying on a multimodal model's description of an image.

**11. Interview questions**

- *What is a multimodal model?* One that processes more than one type of data, such as text and images or audio.
- *How can a transformer process an image?* By cutting it into patches, converting each patch into a vector, and treating the sequence like tokens, often together with text tokens.
- *What is a shared embedding space for images and text?* A space where an image and a text that describe the same thing are close together, enabling text-to-image search.
- *What are the limits?* Misreading fine detail, counting and spatial errors, hallucinated details, bias and privacy concerns.

**12. Quick revision**

- Modality = type of data; multimodal = more than one.
- Images are numbers; patches become vectors in a sequence.
- Shared embedding spaces connect images and text.
- Images cost tokens; resize sensibly.
- Verify details; mind privacy.

---

## Reasoning Models

**Timestamp:** [12:48:15](https://www.youtube.com/watch?v=J9BI0jGOds8&t=46095s)

**Learning objectives:**

- Explain what distinguishes a reasoning model from a standard model.
- Describe why intermediate steps can improve answers, and the cost trade-off.
- Implement step-by-step checking and majority voting in toy Python.
- Know when a reasoning model is worth using, and its limits.

**1. Intuition**

Compare a quick guess with showing your working. Asked "what is 17 × 24?", someone who blurts an answer may be wrong; someone who writes "17 × 20 = 340, 17 × 4 = 68, total 408" is more likely to be right, and can check the steps. A reasoning model is trained and set up to spend extra generated text (or hidden computation) on working through intermediate steps before committing to a final answer. (An analogy: the model is not "thinking" like a person; it generates more tokens that help it reach a better final answer.)

**2. Why does it exist?**

A model produces one token at a time and has a fixed amount of computation per token. For multi-step problems (maths, logic, planning, code) a direct answer must "jump" to the result in one go. Generating intermediate steps gives the model more computation and a written scratchpad to build on. Prompting techniques such as asking the model to reason step by step showed gains, and some models are now trained specifically, often with reinforcement learning on tasks whose answers can be checked automatically, to produce useful reasoning before answering (see [RLHF](36-pretraining-fine-tuning-rlhf.md#rlhf)).

**3. Technical explanation**

- **What differs.** A *standard* model aims to answer directly (it can still reason if prompted). A *reasoning model* is trained or configured to generate a longer chain of intermediate steps first. Some products show a summary of that reasoning, some hide it; some let you set how much effort to allow. Names and controls vary by provider.
- **Test-time compute.** Spending more computation at answer time (longer reasoning, several attempts) rather than only at training time. Quality can improve with more of it, with diminishing returns.
- **Techniques related to it.**
  - *Chain of thought*: asking for or generating step-by-step working.
  - *Self-consistency*: produce several independent answers and take the most common one (majority vote).
  - *Verification*: check the answer with code, a calculator, tests or a second pass.
  - *Search over alternatives*: try several solution paths and keep the best.
- **Costs.** More tokens means higher cost and longer delay, and reasoning tokens usually count as output tokens even when not displayed (see [Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs)). Check your provider's billing rules.
- **When to use.** Harder multi-step problems: maths, coding, planning, analysis with many constraints. For simple lookups, rewriting or classification a standard model is usually faster and cheaper.
- **Limits.**
  - Reasoning text is not guaranteed to be a faithful account of how the answer was produced.
  - A fluent chain of reasoning can still contain errors and arrive at a wrong answer (see [AI Hallucination](31-llms-prompting-temperature-hallucination.md#ai-hallucination)).
  - Models can "overthink" simple questions.
  - Gains are largest on tasks with checkable answers; they are less clear for open-ended judgement.
- **Intuition versus mechanism.** The intuition is "showing working". The mechanism is more generated tokens, learned to be useful, feeding back into the context for later tokens.

**4. Syntax**

*Pseudocode, requires an AI service (parameter names vary by provider and are placeholders):*

```text
answer = call_model(
    model="<reasoning-model-name>",
    messages=[...],
    reasoning_effort="<low|medium|high, if the provider offers such a setting>",
    max_output_tokens=...,    # reasoning tokens usually count toward this
)
```

**5. Example 1 — Basic**

*Toy demo.* Direct answer versus working through steps, with a deliberately simple "solver". The direct guess is a made-up shortcut that is often wrong; the step-by-step method uses place values:

```python
def quick_guess(a, b):
    return round(a * b, -1)  # a rough shortcut: wrong in many cases


def step_by_step(a, b):
    steps = []
    total = 0
    for place, digit in enumerate(reversed(str(b))):
        part = a * int(digit) * 10 ** place
        steps.append(f"{a} x {digit} x {10 ** place} = {part}")
        total += part
    steps.append(f"total = {total}")
    return total, steps


answer, steps = step_by_step(17, 24)
print("quick guess:", quick_guess(17, 24))
print("\n".join(steps))
print("correct:", answer == 17 * 24)
```

Output:

```text
quick guess: 410
17 x 4 x 1 = 68
17 x 2 x 10 = 340
total = 408
correct: True
```

Line by line: the shortcut rounds the true product, so it is close but not exact. The step-by-step version multiplies by each digit of `b` at its place value and adds the parts, recording each step; every step is small and checkable, which is the advantage of showing working.

**6. Example 2 — Practical**

*Toy demo.* Self-consistency (majority vote) over several noisy attempts. A "model" that answers correctly only 60 percent of the time is simulated with a seeded random generator, and voting over more attempts improves the result:

```python
import random
from collections import Counter

TRUE_ANSWER = 408


def noisy_attempt(rng, p_correct=0.6):
    if rng.random() < p_correct:
        return TRUE_ANSWER
    return rng.choice([398, 418, 404, 412, 340])  # plausible wrong answers


def majority(rng, attempts):
    votes = Counter(noisy_attempt(rng) for _ in range(attempts))
    return votes.most_common(1)[0][0]


rng = random.Random(7)
trials = 2000
for attempts in [1, 5, 15]:
    correct = sum(majority(rng, attempts) == TRUE_ANSWER for _ in range(trials))
    print(f"{attempts:>2} attempts per question: {correct / trials:.1%} correct")
```

Output:

```text
 1 attempts per question: 61.4% correct
 5 attempts per question: 86.2% correct
15 attempts per question: 99.0% correct
```

Line by line:

- `noisy_attempt` returns the right answer with probability 0.6 and otherwise one of several different wrong answers.
- `majority` collects the answers and returns the most common.
- Because the wrong answers are spread out while the right one repeats, the vote is correct much more often than a single attempt. This only works if errors are somewhat independent and scattered; if the model is wrong in the same way each time, voting does not help. It also multiplies the cost by the number of attempts.

Verification with code is another strong tool: do not trust a stated result when it can be checked.

```python
def check_claim(a, b, claimed):
    actual = a * b
    return actual == claimed, actual


for claimed in [408, 418]:
    ok, actual = check_claim(17, 24, claimed)
    print(f"17 x 24 = {claimed}? {'verified' if ok else 'wrong, actual ' + str(actual)}")
```

Output:

```text
17 x 24 = 408? verified
17 x 24 = 418? wrong, actual 408
```

**7. Example 3 — Edge case or common mistake**

Plausible but wrong steps. This toy "reasoning" has a flawed middle step but still ends in a confident answer, and a verifier catches it:

```python
steps = [
    "17 x 20 = 340",
    "17 x 4 = 78",      # wrong step: should be 68
    "340 + 78 = 418",
]
claimed_final = 418


def verify_step(step):
    expression, result = step.split("=")
    left = eval(expression.replace("x", "*"), {"__builtins__": {}})  # toy only: input is controlled here
    return left == int(result)


for step in steps:
    print(step, "->", "ok" if verify_step(step) else "ERROR")
print("final answer correct:", claimed_final == 17 * 24)
```

Output:

```text
17 x 20 = 340 -> ok
17 x 4 = 78 -> ERROR
340 + 78 = 418 -> ok
final answer correct: False
```

The chain reads smoothly, but the second step is wrong, so the final answer is too. Fluency is not correctness. (The `eval` here works on a trusted, fixed string; never use `eval` on text from users or models in real code, because it can run arbitrary code. Use a proper expression parser or a calculator tool instead.)

Costs: extra reasoning tokens add up.

```python
input_tokens = 500
for label, output_tokens in [("direct", 100), ("with reasoning", 2500)]:
    cost = (input_tokens * 2.0 + output_tokens * 8.0) / 1_000_000   # invented prices per million tokens
    print(f"{label:<15} {output_tokens:>5} output tokens -> {cost:.4f}")
```

Output:

```text
direct            100 output tokens -> 0.0018
with reasoning   2500 output tokens -> 0.0210
```

With these invented numbers, reasoning makes a call roughly twelve times as expensive. That can be well worth it for a hard problem, and wasteful for a simple one.

**8. Common mistakes**

- Using a reasoning model for tasks that do not need it (slower and costlier).
- Believing visible reasoning is a faithful explanation of the model's process.
- Trusting a confident chain of steps without verifying the result.
- Forgetting that hidden reasoning tokens may still be billed and count toward limits.
- Expecting voting to fix systematic errors.
- Using `eval` on model or user text.

**9. Real-world and AI applications**

Mathematics and science problems, code generation and debugging with test feedback, multi-constraint planning, data analysis where the model can run code to check itself, and agents (see [AI Agents](38-mcp-and-ai-agents.md#ai-agents)) that need to plan across steps. In practice, teams route easy requests to cheaper models and hard ones to reasoning models, and add automatic verification wherever answers are checkable.

**10. Practice**

1. Extend `step_by_step` to work for any two positive integers and verify it against `*` for 10 random pairs (seeded).
2. In Example 2, change `p_correct` to 0.4. Does voting still help? Why or why not?
3. Write `verify_chain(steps)` that returns the index of the first wrong step (or `None`) for steps like `"3 + 4 = 7"`, using a safe approach without `eval` (hint: split on spaces and handle `+`).
4. Compute the cost ratio between a call with 100 output tokens and one with 3,000, at the same input size and prices.
5. Give an example of a task where a reasoning model is a good choice and one where it is not.
6. Why is visible reasoning not a guarantee of a correct answer?

**11. Interview questions**

- *What is a reasoning model?* A model trained or configured to generate intermediate reasoning steps before the final answer, spending more computation at answer time.
- *Why does it help?* Intermediate steps give the model more computation and a scratchpad for multi-step problems, especially ones with checkable answers.
- *What are the trade-offs?* Higher cost and latency, and no guarantee of correctness or of faithful explanations.
- *What is self-consistency?* Sampling several answers and choosing the most common one.
- *How do you check reasoning?* Verify results with code, tests, calculators or sources, not by how convincing the steps sound.

**12. Quick revision**

- Reasoning = extra intermediate steps before answering; more test-time compute.
- Helps multi-step, checkable tasks; costs more tokens and time.
- Self-consistency (vote) and verification improve reliability.
- Fluent steps can still be wrong.
- Route: simple tasks to cheaper models.

---

## Small Language Models (SLMs)

**Timestamp:** [12:52:07](https://www.youtube.com/watch?v=J9BI0jGOds8&t=46327s)

**Learning objectives:**

- Define a small language model and explain why "small" is relative.
- List advantages (cost, speed, privacy, on-device use) and limits.
- Estimate memory for small versus large models.
- Design simple routing between a small and a large model.

**1. Intuition**

A pocket dictionary versus a full encyclopedia set. For most everyday lookups the pocket dictionary is quicker, cheaper and fits in your bag; for rare or complex topics you need the big set. A small language model is the pocket version: far fewer parameters, much cheaper to run, good at focused tasks, but with less breadth and depth. (An analogy.)

**2. Why does it exist?**

Large models are costly to serve, slow, need large hardware, and usually run in someone else's data centre. Many applications need something cheaper, faster, private, or working offline. Better training data and methods, and techniques that transfer knowledge from big models into small ones, have made compact models good enough for many tasks.

**3. Technical explanation**

- **Definition.** There is no official threshold. "Small" usually means from a few hundred million to a few billion parameters (as opposed to tens or hundreds of billions), and the boundary moves as technology improves. A "small" model today may exceed what a "large" model could do years ago.
- **Advantages.**
  - *Cost and speed*: fewer parameters means less computation per token (see [Model Parameters](34-context-window-and-model-parameters.md#model-parameters)).
  - *Deployment*: can run on a laptop, phone or modest server; with quantisation even less memory.
  - *Privacy and control*: data can stay on the device or in your own environment, and you can run open-weight models yourself.
  - *Specialisation*: fine-tuning a small model on a narrow task (see [Fine-Tuning](36-pretraining-fine-tuning-rlhf.md#fine-tuning)) can match a much larger general model on that task.
  - *Latency*: responses start sooner.
- **Techniques that produce them.** Training on carefully selected data; *distillation* (training a small "student" to imitate a larger "teacher"); quantisation; pruning.
- **Limits.** Less world knowledge, weaker on long, complex or open-ended reasoning, smaller effective use of long context, more sensitive to prompt wording, and generally more prone to errors on hard questions. Quality varies enormously between models, so evaluate on your own tasks.
- **Patterns.** Use a small model for classification, extraction, routing, summarising short texts and simple chat; use a larger model for hard cases; combine them with a *router* or with *cascades* (try small first, escalate if unsure). Small models also commonly serve as the *embedding* or *guardrail* components in larger systems (see [Vectors and Embeddings](33-vectors-and-embeddings.md)).

**4. Syntax**

*Pseudocode, requires a library and downloaded model (names are placeholders):*

```text
model = load_model("<small-model-name>", precision="4-bit")   # runs locally if hardware allows
text = model.generate("Classify the sentiment: ...", max_new_tokens=5)
```

**5. Example 1 — Basic**

*Toy demo.* Memory needed for models of different sizes at different precisions (weights only, lower bound; see [Model Parameters](34-context-window-and-model-parameters.md#model-parameters)), and whether they fit a device. Sizes and the device memory are generic round numbers:

```python
BYTES = {"16-bit": 2, "4-bit": 0.5}
devices = {"phone (8 GB free)": 8, "laptop (16 GB free)": 16, "server GPU (80 GB)": 80}
models = {"small 3B": 3e9, "medium 13B": 13e9, "large 70B": 70e9}

for model_name, parameters in models.items():
    for precision, bytes_per in BYTES.items():
        gb = parameters * bytes_per / 1e9
        fits = [device for device, memory in devices.items() if gb <= memory * 0.8]  # leave 20% for other needs
        print(f"{model_name:<11} {precision:<7} {gb:>6.1f} GB  fits: {', '.join(fits) if fits else 'none'}")
```

Output:

```text
small 3B    16-bit     6.0 GB  fits: phone (8 GB free), laptop (16 GB free), server GPU (80 GB)
small 3B    4-bit      1.5 GB  fits: phone (8 GB free), laptop (16 GB free), server GPU (80 GB)
medium 13B  16-bit    26.0 GB  fits: server GPU (80 GB)
medium 13B  4-bit      6.5 GB  fits: laptop (16 GB free), server GPU (80 GB)
large 70B   16-bit   140.0 GB  fits: none
large 70B   4-bit     35.0 GB  fits: server GPU (80 GB)
```

Line by line: for each model and precision the weight memory is computed, then compared with each device, allowing only 80 percent of memory for the weights (the rest is needed for context and software). The small model fits a phone-class device (with more headroom when quantised); the large one needs a server even at 4-bit. These figures are a lower bound and illustrative only.

**6. Example 2 — Practical**

*Toy demo.* A **router**: send easy requests to a "small model" and hard ones to a "large model". Both models are fake functions, and "difficulty" is estimated by crude rules; real routers use a classifier model, confidence scores or both:

```python
def small_model(question):
    return f"[small] short answer to: {question}"


def large_model(question):
    return f"[large] detailed answer to: {question}"


HARD_WORDS = {"prove", "derive", "compare", "analyse", "analyze", "plan", "debug"}


def is_hard(question):
    words = set(question.lower().replace("?", "").split())
    return len(words) > 12 or bool(words & HARD_WORDS)


def route(question):
    return large_model(question) if is_hard(question) else small_model(question)


questions = [
    "What is the capital of France?",
    "Compare transformers and recurrent networks for long documents.",
    "Convert 5 km to miles",
]
calls = {"small": 0, "large": 0}
for q in questions:
    answer = route(q)
    calls["large" if answer.startswith("[large]") else "small"] += 1
    print(answer)
print(calls)
```

Output:

```text
[small] short answer to: What is the capital of France?
[large] detailed answer to: Compare transformers and recurrent networks for long documents.
[small] short answer to: Convert 5 km to miles
{'small': 2, 'large': 1}
```

Line by line: `is_hard` flags long questions or ones with certain verbs; `route` picks the model; the counts show the traffic split. If most traffic is easy, most calls use the cheaper model, which lowers cost. The weak point is the router itself: a wrong decision sends a hard question to a model that cannot answer it, so real systems also let the small model signal low confidence and escalate (a *cascade*).

**7. Example 3 — Edge case or common mistake**

Routing by keywords misclassifies. A short question can be hard and a long one easy:

```python
HARD_WORDS = {"prove", "derive", "compare", "analyse", "analyze", "plan", "debug"}


def is_hard(question):
    words = set(question.lower().replace("?", "").split())
    return len(words) > 12 or bool(words & HARD_WORDS)


tests = {
    "Is P equal to NP?": True,                                                                       # short but very hard
    "Please tell me the name of the capital city of the country called France if you know it?": False,  # long but easy
}
for question, truly_hard in tests.items():
    print(f"router says hard={is_hard(question)}, truth hard={truly_hard} | {question[:45]}")
```

Output:

```text
router says hard=False, truth hard=True | Is P equal to NP?
router says hard=True, truth hard=False | Please tell me the name of the capital city o
```

Both are misrouted. Measure the router on real examples before trusting it.

A cost comparison (invented prices) shows why routing is attractive, and also its limit:

```python
small_cost, large_cost = 0.2, 3.0   # invented cost per 1,000 requests, same units
requests = 1000
for share_easy in [0.9, 0.5, 0.1]:
    routed = requests * (share_easy * small_cost + (1 - share_easy) * large_cost) / 1000
    print(f"{share_easy:.0%} easy: routed cost {routed:.2f} vs all-large {requests * large_cost / 1000:.2f}")
```

Output:

```text
90% easy: routed cost 0.48 vs all-large 3.00
50% easy: routed cost 1.60 vs all-large 3.00
10% easy: routed cost 2.72 vs all-large 3.00
```

The saving depends on the share of easy requests, and on the router being right; it also ignores the cost of the quality lost when a hard question goes to the small model.

Small models are not automatically private: running one locally keeps data on your device, but using a hosted small model sends data to a service. Check where the model actually runs.

**8. Common mistakes**

- Equating "small" with "bad", or "large" with "always better".
- Choosing a model by parameter count instead of testing on your own task.
- Ignoring quality loss from heavy quantisation.
- Using a small model for tasks needing deep reasoning or broad knowledge without checking.
- Poorly tested routing rules.
- Assuming that "small" means "runs anywhere": memory for context and software also counts.

**9. Real-world and AI applications**

On-device assistants and keyboards, offline tools, classification and extraction at scale, privacy-sensitive settings, embedded devices, and cost-sensitive services using cascades. Teams often fine-tune a small model for a narrow task and keep a large model for hard cases.

**10. Practice**

1. Add a `"medium 13B"` row at 8-bit precision (1 byte per parameter) to Example 1 and see which devices can hold it.
2. Add a rule to `is_hard` for questions containing the word `explain`. Rerun the tests.
3. Write `cascade(question, small, large, confidence_of_small, threshold)` that returns the small model's answer if its confidence is at least the threshold, else the large model's.
4. With costs 0.2 and 3.0 per 1,000 requests, what share of easy traffic gives the same cost as using the large model only? (Hint: it is a trick question; think about what happens when the small share is zero.)
5. Give two reasons to choose a small model and two reasons to choose a large one.
6. What is distillation?

**11. Interview questions**

- *What is a small language model?* A compact model, typically up to a few billion parameters, that is cheaper and faster to run, often on-device, but less broadly capable than large models; the threshold is not formal.
- *When would you choose one?* For cost, latency, privacy, offline use and narrow tasks, especially after fine-tuning.
- *What is distillation?* Training a small student model to imitate a larger teacher model.
- *What is a cascade or router?* A design that sends easy requests to a cheap model and escalates hard or low-confidence ones to a larger model.

**12. Quick revision**

- SLM: few parameters, cheap, fast, can run locally.
- Quantisation and distillation help shrink models.
- Strong on narrow tasks (especially fine-tuned); weaker on breadth and hard reasoning.
- Route or cascade; measure the router.
- Test on your task, not on size.

---

## AGI versus ASI

**Timestamp:** [12:54:10](https://www.youtube.com/watch?v=J9BI0jGOds8&t=46450s)

**Learning objectives:**

- Distinguish narrow AI, AGI and ASI as commonly defined.
- Explain why there is no single agreed definition or test of AGI.
- Describe the main views in the debate fairly, without predicting dates.
- Separate today's systems and their limits from hypothetical future ones.

**1. Intuition**

Think of a calculator, a skilled doctor and a hypothetical being who could out-think every human at everything. A calculator beats you at arithmetic but can do nothing else. A doctor is flexible across many medical problems and can learn new ones. The third is a thought experiment. In AI discussions these roughly line up with *narrow AI*, *AGI* and *ASI*. (An analogy.)

**2. Why does it exist?**

These terms are used to talk about where AI research might lead and what risks and benefits could follow. They matter for planning, policy and public understanding, but they are used loosely, and headlines often blur facts about today's systems with speculation about tomorrow's.

**3. Technical explanation**

- **Narrow AI (ANI).** Systems built or trained for specific tasks or a limited range of tasks. Everything that exists today is usually placed in this category by researchers, though modern language models are much more general than older narrow systems, which is part of why the boundary is debated.
- **AGI (artificial general intelligence).** A hypothetical AI that can learn and perform a wide range of intellectual tasks at roughly the level of a capable human, and transfer skills to new situations. **There is no single agreed definition.** Some definitions stress matching human performance on most economically valuable work, others stress flexible learning and generalisation, others use particular tests or benchmarks. Because definitions differ, claims such as "AGI has been achieved" or "AGI is N years away" depend heavily on which definition is used.
- **ASI (artificial superintelligence).** A hypothetical AI that greatly surpasses the best humans across virtually all intellectual domains. It is a concept for discussion, not an existing technology.
- **Where today's systems stand (general picture).** Current models can perform impressively across many tasks, yet show well-documented limits: hallucination, inconsistent reasoning, weak long-term planning and memory without scaffolding, dependence on training data, and no reliable self-knowledge of what they do not know. Whether scaling and refining current approaches leads to AGI, or whether new ideas are needed, is an open question on which researchers disagree.
- **Views in the debate (as characterised, not endorsed).**
  - Some researchers expect rapid progress and take near-term AGI seriously.
  - Others think current methods have fundamental limits and that AGI is far off, or that the concept is too vague to be useful.
  - Others focus on present-day issues (bias, misuse, jobs, privacy, concentration of power, energy use) rather than hypothetical future systems.
  - Many people working on safety argue that risks should be studied before capabilities arrive; others argue that over-focusing on speculative risks distracts from real current harms. Reasonable experts disagree on timelines, risks and priorities.
- **Why it matters to a practitioner.** Treat claims about AGI and ASI with care: ask for the definition, the evidence and the source. Build with the capabilities and limits that exist today, and apply safety and evaluation practices (see [Recap and Final Thoughts](40-recap-and-final-thoughts.md#evaluation-limitations-and-responsible-use)).

**4. Syntax**

A comparison table (not code):

```text
Level         Scope                                         Status
Narrow AI     specific task(s)                              exists today
AGI           broad human-level ability, transfers skills   hypothetical; definitions differ
ASI           far beyond the best humans, almost all areas  hypothetical
```

**5. Example 1 — Basic**

*Toy demo.* Classification only means something once you fix a definition. A rule-based "classifier" of a system's profile, to show how the label depends on the criteria you choose. The systems and scores are invented:

```python
systems = {
    "calculator": {"tasks_covered": 0.01, "vs_human_level": 5.0},
    "chess engine": {"tasks_covered": 0.01, "vs_human_level": 3.0},
    "general assistant (invented)": {"tasks_covered": 0.40, "vs_human_level": 0.7},
    "hypothetical A": {"tasks_covered": 0.95, "vs_human_level": 1.0},
    "hypothetical B": {"tasks_covered": 0.98, "vs_human_level": 3.0},
}


def label(profile, breadth=0.9, human_level=1.0, far_beyond=2.0):
    if profile["tasks_covered"] >= breadth and profile["vs_human_level"] >= far_beyond:
        return "ASI-like"
    if profile["tasks_covered"] >= breadth and profile["vs_human_level"] >= human_level:
        return "AGI-like"
    return "narrow"


for name, profile in systems.items():
    print(f"{name:<30} -> {label(profile)}")
```

Output:

```text
calculator                     -> narrow
chess engine                   -> narrow
general assistant (invented)   -> narrow
hypothetical A                 -> AGI-like
hypothetical B                 -> ASI-like
```

Line by line: each invented system has a *breadth* (share of tasks covered) and a *level* relative to humans (1.0 = human level). The labels follow from three chosen thresholds. Nothing here measures real systems; the point is that the labels are produced by the definition.

**6. Example 2 — Practical**

*Toy demo.* Changing the definition changes the verdict:

```python
systems = {
    "general assistant (invented)": {"tasks_covered": 0.40, "vs_human_level": 0.7},
    "hypothetical A": {"tasks_covered": 0.95, "vs_human_level": 1.0},
}


def label(profile, breadth, human_level):
    return "AGI-like" if profile["tasks_covered"] >= breadth and profile["vs_human_level"] >= human_level else "narrow"


definitions = {
    "strict (90% of tasks at human level)": (0.90, 1.0),
    "looser (30% of tasks at 0.6 of human level)": (0.30, 0.6),
}
for definition, (breadth, level) in definitions.items():
    print(definition)
    for name, profile in systems.items():
        print(f"   {name:<30} {label(profile, breadth, level)}")
```

Output:

```text
strict (90% of tasks at human level)
   general assistant (invented)   narrow
   hypothetical A                 AGI-like
looser (30% of tasks at 0.6 of human level)
   general assistant (invented)   AGI-like
   hypothetical A                 AGI-like
```

The same invented system is "narrow" under one definition and "AGI-like" under another. This is why debates about whether AGI "has arrived" often talk past each other: they are using different definitions.

**7. Example 3 — Edge case or common mistake**

Mixing up *capability on a benchmark* with *general intelligence*. A system that scores high on a test may do so by memorising or by exploiting the test's format:

```python
tests = {"benchmark A": 0.97, "benchmark B": 0.95, "new unseen task": 0.40}
seen_in_training = {"benchmark A", "benchmark B"}   # imagine the test data leaked into training
for name, score in tests.items():
    note = "(may reflect memorisation)" if name in seen_in_training else "(unseen)"
    print(f"{name:<16} {score:.0%} {note}")
```

Output:

```text
benchmark A      97% (may reflect memorisation)
benchmark B      95% (may reflect memorisation)
new unseen task  40% (unseen)
```

The numbers are invented to illustrate the idea: scores on data that leaked into training can overstate real ability, which is why performance on genuinely new tasks matters.

Another common error is treating forecasts as facts:

```python
claims = [
    ("AGI will arrive by a specific year", "forecast: uncertain, experts disagree"),
    ("Models hallucinate", "observed, widely documented"),
    ("ASI will necessarily be dangerous", "speculation: debated"),
    ("Current models do not learn from your chat after training", "technical fact for standard deployments"),
]
for claim, status in claims:
    print(f"{claim:<62} -> {status}")
```

Output:

```text
AGI will arrive by a specific year                             -> forecast: uncertain, experts disagree
Models hallucinate                                             -> observed, widely documented
ASI will necessarily be dangerous                              -> speculation: debated
Current models do not learn from your chat after training      -> technical fact for standard deployments
```

Separating observed facts, technical facts, forecasts and speculation is a useful habit when reading about AI. The classifications in the table are a judgement for this handbook's purposes; look for the evidence behind any specific claim.

**8. Common mistakes**

- Using "AGI" without saying which definition.
- Treating AGI or ASI as existing products, or a particular date as established.
- Equating a high benchmark score with general intelligence.
- Assuming that consciousness, intent or human-like understanding follow from fluent output.
- Dismissing either the long-term safety debate or current, concrete harms.
- Letting speculation replace practical engineering: evaluate the systems you actually have.

**9. Real-world and AI applications**

These terms appear in company mission statements, regulation and policy debates, safety research, investment discussion and news. A practitioner uses them to read such material critically, to ask what is being claimed and on what evidence, and to keep focus on measurable capabilities, limits and risks of deployed systems.

**10. Practice**

1. Modify Example 1 so that a system with `tasks_covered` of 0.85 and level 1.2 is labelled. Which label does it get with the default thresholds, and with `breadth=0.8`?
2. Write a function that, given a list of system profiles and two definitions, returns which systems change label between them.
3. In your own words, explain why "AGI is here" and "AGI is far away" can both be said by informed people.
4. Explain the difference between narrow AI, AGI and ASI in one sentence each.
5. Pick a recent AI headline you have seen and sort its claims into observed fact, technical fact, forecast and speculation.
6. Why might a high benchmark score overstate a model's ability?

**11. Interview questions**

- *What is AGI?* A hypothetical AI able to learn and perform a wide range of intellectual tasks at about human level and to transfer skills to new situations; there is no single accepted definition.
- *What is ASI?* A hypothetical AI that greatly exceeds the best humans across virtually all intellectual domains.
- *Do AGI or ASI exist today?* No agreed AGI or ASI exists; today's systems are usually described as narrow, though increasingly general.
- *Why is AGI hard to define or test?* Intelligence is multi-dimensional, definitions differ, and benchmarks can be gamed or leaked into training data.
- *How should an engineer treat AGI claims?* With attention to the definition, the evidence and the source, and with focus on the real capabilities and limits of current systems.

**12. Quick revision**

- Narrow AI: specific tasks, exists. AGI: broad human-level, hypothetical. ASI: far beyond humans, hypothetical.
- No agreed definition: the label depends on the criteria.
- Benchmarks can mislead; unseen tasks matter.
- Experts disagree on timelines and risks.
- Separate fact, forecast and speculation.

---

## Answers to Practice Exercises

### Answers: Multimodal AI

1.

```python
image = [[0, 0, 255, 255], [0, 0, 255, 255], [255, 255, 0, 0], [255, 255, 0, 0]]
best = max(((value, (r, c)) for r, row in enumerate(image) for c, value in enumerate(row)))
print(best)
```

Output:

```text
(255, (3, 1))
```

`max` on tuples compares the pixel value first and, for ties, the position, so it returns the last-largest position by tuple order.

2.

```python
image = [[0, 0, 255, 255, 10, 10], [0, 0, 255, 255, 10, 10], [255, 255, 0, 0, 200, 200], [255, 255, 0, 0, 200, 200]]
count = sum(len(row) for row in image)
print(count, "patches of one pixel; each vector holds [average, min] of a single value")
```

Output:

```text
24 patches of one pixel; each vector holds [average, min] of a single value
```

With `PATCH = 1` there is one patch per pixel (24), and each vector is just `[value, value]`, so nothing is summarised.

3.

```python
def flip_horizontal(image):
    return [list(reversed(row)) for row in image]


print(flip_horizontal([[1, 2, 3], [4, 5, 6]]))
```

Output:

```text
[[3, 2, 1], [6, 5, 4]]
```

4.

```python
width = height = 512
patch = 32
print((width // patch) * (height // patch))
```

Output:

```text
256
```

5. Every patch becomes at least one token-like element, so a large image becomes hundreds or thousands of elements that occupy the context window and are charged for.

6. For example: the model may invent details that are not in the image, and it can misread small text or counts; also, sensitive content in the image may be processed or retained by a service.

### Answers: Reasoning Models

1.

```python
import random


def step_by_step(a, b):
    total = 0
    for place, digit in enumerate(reversed(str(b))):
        total += a * int(digit) * 10 ** place
    return total


rng = random.Random(0)
pairs = [(rng.randint(1, 99), rng.randint(1, 99)) for _ in range(10)]
print(all(step_by_step(a, b) == a * b for a, b in pairs))
```

Output:

```text
True
```

2.

```python
import random
from collections import Counter

rng = random.Random(7)
TRUE = 408


def attempt(p):
    return TRUE if rng.random() < p else rng.choice([398, 418, 404, 412, 340])


def majority(p, n):
    return Counter(attempt(p) for _ in range(n)).most_common(1)[0][0]


trials = 2000
for n in [1, 15]:
    print(n, sum(majority(0.4, n) == TRUE for _ in range(trials)) / trials)
```

Output:

```text
1 0.4065
15 0.8335
```

Voting still helps here because the right answer (40 percent) is more common than any single wrong one (12 percent each). It would not help if one wrong answer were more common than the correct one.

3.

```python
def verify_chain(steps):
    for index, step in enumerate(steps):
        left, right = step.split("=")
        a, op, b = left.split()
        value = int(a) + int(b) if op == "+" else int(a) - int(b)
        if value != int(right):
            return index
    return None


print(verify_chain(["3 + 4 = 7", "7 - 2 = 6", "6 + 1 = 7"]))
print(verify_chain(["3 + 4 = 7"]))
```

Output:

```text
1
None
```

4.

```python
print(3000 / 100)
```

Output:

```text
30.0
```

The output side of the call is 30 times larger. The total cost ratio is a bit smaller than 30, because the input part is unchanged.

5. Good: a multi-step maths or code-debugging problem with checkable results. Not good: rewriting a sentence, simple classification, or looking up a fixed fact.

6. The text of the reasoning is generated like any other text and may contain wrong steps or not reflect what actually produced the answer; only checking the result establishes correctness.

### Answers: Small Language Models (SLMs)

1.

```python
BYTES = {"8-bit": 1}
devices = {"phone (8 GB free)": 8, "laptop (16 GB free)": 16, "server GPU (80 GB)": 80}
gb = 13e9 * BYTES["8-bit"] / 1e9
print(gb, [d for d, m in devices.items() if gb <= m * 0.8])
```

Output:

```text
13.0 ['server GPU (80 GB)']
```

2.

```python
HARD_WORDS = {"prove", "derive", "compare", "analyse", "analyze", "plan", "debug", "explain"}


def is_hard(question):
    words = set(question.lower().replace("?", "").split())
    return len(words) > 12 or bool(words & HARD_WORDS)


print(is_hard("Explain recursion"), is_hard("What is 2 + 2?"))
```

Output:

```text
True False
```

3.

```python
def cascade(question, small, large, confidence_of_small, threshold):
    answer, confidence = small(question), confidence_of_small(question)
    return answer if confidence >= threshold else large(question)


small = lambda q: "small answer"
large = lambda q: "large answer"
print(cascade("easy", small, large, lambda q: 0.9, 0.7))
print(cascade("hard", small, large, lambda q: 0.3, 0.7))
```

Output:

```text
small answer
large answer
```

4. The trick: with no easy traffic every request goes to the large model, so the cost equals the large-only cost; at any share of easy traffic above zero routing is cheaper in this model, so there is no break-even share greater than 0. In reality the router's own cost and misrouting would create one.

5. Small: lower cost and latency; data can stay on the device. Large: better on hard, open-ended or knowledge-heavy tasks; fewer errors on complex reasoning.

6. Distillation trains a small student model to imitate the outputs of a larger teacher model, so that it keeps much of the quality at a fraction of the size.

### Answers: AGI versus ASI

1.

```python
def label(profile, breadth=0.9, human_level=1.0, far_beyond=2.0):
    if profile["tasks_covered"] >= breadth and profile["vs_human_level"] >= far_beyond:
        return "ASI-like"
    if profile["tasks_covered"] >= breadth and profile["vs_human_level"] >= human_level:
        return "AGI-like"
    return "narrow"


profile = {"tasks_covered": 0.85, "vs_human_level": 1.2}
print(label(profile), label(profile, breadth=0.8))
```

Output:

```text
narrow AGI-like
```

2.

```python
def label(profile, breadth, level):
    return "AGI-like" if profile["tasks_covered"] >= breadth and profile["vs_human_level"] >= level else "narrow"


def changed(systems, def_a, def_b):
    return [name for name, p in systems.items() if label(p, *def_a) != label(p, *def_b)]


systems = {"x": {"tasks_covered": 0.5, "vs_human_level": 0.8}, "y": {"tasks_covered": 0.95, "vs_human_level": 1.1}}
print(changed(systems, (0.9, 1.0), (0.4, 0.5)))
```

Output:

```text
['x']
```

3. Because the term has no single definition: someone using a loose definition (broad competence on many tasks) may say it is nearly here, while someone using a strict definition (human-level on almost everything, with robust learning and reliability) may say it is far off. Both can be sincere and informed.

4. Narrow AI is built for specific tasks and exists today; AGI is a hypothetical AI with broad, flexible, roughly human-level ability; ASI is a hypothetical AI far beyond the best humans in almost all intellectual areas.

5. Open exercise: for each claim in the headline, ask whether it is something observed and measured (fact), a known property of how systems work (technical fact), a prediction (forecast) or an argument about what might happen (speculation).

6. The test data may have leaked into the training data, the model may exploit the format of the test, or the benchmark may cover only a narrow slice of real tasks; performance on genuinely new tasks can then be much lower.

---

## Chapter Summary and Key Takeaways

- Multimodal models handle more than text: non-text data is converted into sequences of vectors (for example image patches) that a transformer can process, at a token cost, with limits such as misreading and hallucinated details.
- Reasoning models spend extra computation on intermediate steps before answering, which helps multi-step tasks with checkable answers but costs more and does not guarantee correct or faithful reasoning; verification and voting help.
- Small language models trade breadth for cost, speed, privacy and on-device use; fine-tuning, distillation and quantisation make them effective, and routing or cascades combine them with larger models.
- AGI and ASI are hypothetical levels of capability with no single agreed definition, so claims depend on the definition; separate observed facts from forecasts and speculation, and judge systems by evidence on real tasks.
- In every case: test on your own task, verify outputs, and mind cost and privacy.

Next: [Chapter 40 — Recap and Final Thoughts](40-recap-and-final-thoughts.md) ties the whole Python + AI journey together.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
