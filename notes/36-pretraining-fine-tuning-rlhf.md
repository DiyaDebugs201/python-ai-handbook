# Chapter 36 — Pretraining, Fine-Tuning and RLHF

> Part 6 — Python Integration and AI Foundations · Video: 12:04:37–12:16:08 · Previous: [35 Attention Mechanism and Transformers](35-attention-and-transformers.md) · Next: [37 Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)

**In this chapter:** how the parameters of a language model get their values: *pretraining* on large amounts of text to predict the next token, *fine-tuning* on smaller, targeted data, and *RLHF* (reinforcement learning from human feedback) to make behaviour match human preferences.

**Before you start:** you need loops, dictionaries, functions, `random`, and the ideas of parameters ([Model Parameters](34-context-window-and-model-parameters.md#model-parameters)) and next-token probabilities ([Transformers](35-attention-and-transformers.md#transformers)). Recap: parameters are numbers learned in training and fixed afterwards. All code is a *toy demo* with tiny data, standard library only. Real training uses huge datasets, specialised hardware and neural networks; the toys show the *idea* of learning from data, not how production models are built. Examples were run with Python 3.13.

---

## How LLMs Learn: Pretraining

**Timestamp:** [12:04:37](https://www.youtube.com/watch?v=J9BI0jGOds8&t=43477s)

**Learning objectives:**

- Explain pretraining as learning to predict the next token from a very large text collection.
- Describe the training loop at a high level: predict, measure error (loss), adjust parameters.
- Show gradient descent on a tiny problem in Python.
- Explain what pretraining does and does not give a model, including knowledge cutoff.

**1. Intuition**

Imagine a student who reads an enormous library but is only ever given one exercise: "Here is a passage with the next word covered. Guess it." Each wrong guess nudges the student's habits slightly. After billions of such exercises the student becomes remarkably good at continuing text, and in doing so picks up grammar, facts, styles and common reasoning patterns. Nobody told them any rules directly. (An analogy: the model does not read as a person does; its parameters are adjusted by arithmetic.)

**2. Why does it exist?**

Writing rules by hand for language is impossible: too many exceptions and too much world knowledge. Learning from examples scales, and plain text is abundant and needs no human labels, because the "answer" (the next token) is already in the text. This is called *self-supervised* learning. A single pretraining run gives a general-purpose base model that can later be adapted to many tasks.

**3. Technical explanation**

- **Data.** Large collections of text (web pages, books, code and more), cleaned, filtered and deduplicated, then tokenized (see [Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs)). What goes in strongly shapes what comes out, including its gaps and biases.
- **Objective.** For each position in a text, predict the next token given the tokens before it. The model outputs probabilities for every token in its vocabulary.
- **Loss.** A number measuring how wrong the prediction was. A common choice is *cross-entropy*: the negative logarithm of the probability the model gave to the correct token. High probability on the right token means low loss; a confident wrong guess means high loss.
- **Gradient descent.** For each parameter, work out which direction would reduce the loss (the *gradient*, found by backpropagation), then move a small step (the *learning rate*) that way. Repeat over many batches of text.
- **Scale.** Pretraining uses huge numbers of tokens, billions of parameters and large clusters of hardware for long periods, which is why it is very costly and done by few organisations.
- **Result: a base model.** It is good at continuing text. It is not yet good at following instructions or being helpful and safe, and it may continue a question with more questions. Later stages address this (see [Fine-Tuning](#fine-tuning) and [RLHF](#rlhf)).
- **Knowledge cutoff.** The model knows only what was in its training data, up to some date. It does not learn from your conversations during use (see [Model Parameters](34-context-window-and-model-parameters.md#model-parameters)). For newer or private information, supply it in the context or retrieve it (see [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)).
- **Memorisation versus generalisation.** A model should learn patterns, not just store text, but some memorisation of frequently repeated passages does happen.
- **Intuition versus mechanism.** "The model reads the library" is the intuition. The mechanism is repeated parameter updates that lower the next-token loss.

**4. Syntax**

```text
repeat many times:
    take a batch of text
    predictions = model(batch_without_next_tokens)
    loss = how_wrong(predictions, real_next_tokens)
    gradients = direction_that_reduces(loss)
    parameters = parameters - learning_rate * gradients
```

Pseudocode of the training loop; the examples below implement tiny versions.

**5. Example 1 — Basic**

*Toy demo.* "Pretraining" a bigram model: count which word follows which in a small text, then turn counts into probabilities. This is learning from data without rules, although a real model is a neural network and conditions on far more than one previous word:

```python
from collections import Counter, defaultdict

corpus = "the cat sat on the mat . the cat ate the fish . the dog sat on the rug ."
words = corpus.split()

counts = defaultdict(Counter)
for current, following in zip(words, words[1:]):
    counts[current][following] += 1

print(dict(counts["the"]))
total = sum(counts["the"].values())
print({word: round(n / total, 3) for word, n in counts["the"].items()})
print(counts["sat"].most_common(1))
```

Output:

```text
{'cat': 2, 'mat': 1, 'fish': 1, 'dog': 1, 'rug': 1}
{'cat': 0.333, 'mat': 0.167, 'fish': 0.167, 'dog': 0.167, 'rug': 0.167}
[('on', 2)]
```

Line by line: `zip(words, words[1:])` pairs each word with its successor; the counts per word are the learned "parameters". After `the` the text most often had `cat`, and `sat` was always followed by `on`. Predicting the next word means choosing from these probabilities.

**6. Example 2 — Practical**

*Toy demo.* The training loop on a single parameter. We want to learn a number `w` so that `prediction = w * x` matches data that follows `y = 3x`. The loop predicts, measures the error, and moves `w` down the gradient of the loss:

```python
data = [(1, 3), (2, 6), (3, 9), (4, 12)]  # (x, y) pairs, generated by y = 3x
w = 0.0
learning_rate = 0.02

for epoch in range(1, 41):
    loss = 0.0
    gradient = 0.0
    for x, y in data:
        error = w * x - y
        loss += error ** 2
        gradient += 2 * error * x
    loss /= len(data)
    gradient /= len(data)
    w -= learning_rate * gradient
    if epoch in (1, 2, 5, 10, 20, 40):
        print(f"epoch {epoch:>2}: w = {w:.4f}, loss = {loss:.4f}")
```

Output:

```text
epoch  1: w = 0.9000, loss = 67.5000
epoch  2: w = 1.5300, loss = 33.0750
epoch  5: w = 2.4958, loss = 3.8912
epoch 10: w = 2.9153, loss = 0.1099
epoch 20: w = 2.9976, loss = 0.0001
epoch 40: w = 3.0000, loss = 0.0000
```

Line by line:

- `error` is how far the prediction is from the truth; the loss is the mean squared error.
- `gradient` is the derivative of the loss with respect to `w` (for `error²` it is `2 × error × x`), averaged over the data.
- `w -= learning_rate * gradient` moves `w` a small step in the direction that reduces the loss.
- The printed values show the loss shrinking and `w` approaching 3. The reported loss is the value *before* that epoch's update.

A language model does the same with billions of parameters at once and with next-token cross-entropy as the loss. Here is that loss for a single prediction:

```python
import math

for probability_of_correct_token in [0.9, 0.5, 0.1, 0.01]:
    loss = -math.log(probability_of_correct_token)
    print(f"p(correct) = {probability_of_correct_token:<4} -> loss = {loss:.3f}")
```

Output:

```text
p(correct) = 0.9  -> loss = 0.105
p(correct) = 0.5  -> loss = 0.693
p(correct) = 0.1  -> loss = 2.303
p(correct) = 0.01 -> loss = 4.605
```

Confident correct predictions give a loss near zero; giving the right token a tiny probability is penalised heavily.

**7. Example 3 — Edge case or common mistake**

The learning rate matters. Too large a step overshoots and diverges:

```python
data = [(1, 3), (2, 6), (3, 9), (4, 12)]


def train(learning_rate, epochs=8):
    w = 0.0
    history = []
    for _ in range(epochs):
        gradient = sum(2 * (w * x - y) * x for x, y in data) / len(data)
        w -= learning_rate * gradient
        history.append(round(w, 2))
    return history


print("small rate:", train(0.02))
print("too large: ", train(0.2))
```

Output:

```text
small rate: [0.9, 1.53, 1.97, 2.28, 2.5, 2.65, 2.75, 2.83]
too large:  [9.0, -9.0, 27.0, -45.0, 99.0, -189.0, 387.0, -765.0]
```

With the small rate `w` moves steadily towards 3; with the large rate each step overshoots by more than the last and `w` blows up. Real training tunes the learning rate carefully.

A model learns only from its data, so gaps in the data are gaps in the model:

```python
from collections import Counter, defaultdict

corpus = "the cat sat . the cat ate ."
words = corpus.split()
counts = defaultdict(Counter)
for a, b in zip(words, words[1:]):
    counts[a][b] += 1

print(counts["cat"].most_common())
print("after 'dog':", counts["dog"].most_common())
```

Output:

```text
[('sat', 1), ('ate', 1)]
after 'dog': []
```

The model has never seen `dog`, so it has nothing to say about it. Real models generalise far better than this lookup table, but they too are weakest on topics rare or absent in their data, and cannot know events after their cutoff.

Memorising instead of generalising is another failure, visible even in a toy:

```python
training_pairs = {1: 2, 2: 4, 3: 6}
memoriser = dict(training_pairs)
rule = lambda x: 2 * x

for x in [2, 10]:
    print(x, "memoriser:", memoriser.get(x, "no idea"), "| learned rule:", rule(x))
```

Output:

```text
2 memoriser: 4 | learned rule: 4
10 memoriser: no idea | learned rule: 20
```

The memoriser is perfect on the examples it has seen and useless on new input; a model that has captured the pattern handles both. Evaluating on held-out data, not just the training data, is how this is checked.

**8. Common mistakes**

- Thinking the model looks things up in its training data at answer time: the data is not stored as documents; only parameters remain.
- Assuming the model keeps learning from your chat. It does not unless it is deliberately trained again.
- Forgetting the knowledge cutoff and trusting the model on recent events.
- Assuming the training data is unbiased or complete.
- Treating a base model as an assistant: it continues text, it does not necessarily follow instructions.
- Confusing training (changing parameters) with inference (using the fixed model).

**9. Real-world and AI applications**

Pretraining produces the base models behind assistants. Knowing it explains why models have a knowledge cutoff, why they know common topics better than rare ones, why they can echo biases in their data, and why organisations add context, retrieval or fine-tuning for specialised needs rather than pretraining their own model, which costs far too much for most teams.

**10. Practice**

1. Extend Example 1 to predict the most likely word after `on` and after `the`.
2. Train the one-parameter model on data from `y = 5x`. How many epochs does it need to get `w` within 0.01 of 5 with a rate of 0.02?
3. Compute the cross-entropy loss for a correct-token probability of 0.25.
4. Change the learning rate in Example 3 to 0.1 and 0.25. Which values converge and which diverge?
5. Explain the difference between training and inference.
6. Why does a model have a knowledge cutoff?

**11. Interview questions**

- *What is pretraining?* Training a model on a very large text collection to predict the next token, so it learns language and general knowledge from the data.
- *What is the loss?* A number measuring how wrong the prediction was; training adjusts parameters to reduce it.
- *What is gradient descent?* Repeatedly moving parameters a small step in the direction that reduces the loss.
- *Why does a model have a knowledge cutoff?* It only learned from data up to a certain date, and parameters do not change when it is used.
- *What is self-supervised learning?* Learning where the labels come from the data itself, such as the next token in a text.

**12. Quick revision**

- Pretraining: predict the next token over huge text; no human labels needed.
- Loss measures error; gradient descent lowers it; learning rate sets the step.
- Result: a base model that continues text; not yet an assistant.
- Knowledge cutoff; no learning from chats at use time.
- Gaps and biases in data become gaps and biases in the model.

---

## Fine-Tuning

**Timestamp:** [12:08:10](https://www.youtube.com/watch?v=J9BI0jGOds8&t=43690s)

**Learning objectives:**

- Explain fine-tuning as continued training of a pretrained model on a smaller, targeted dataset.
- Distinguish instruction tuning from domain fine-tuning, and fine-tuning from prompting and retrieval.
- Describe the shape of a fine-tuning dataset.
- Name the risks: overfitting, forgetting and poor-quality data.

**1. Intuition**

A pretrained model is like a graduate with a broad education. Fine-tuning is a short, focused apprenticeship: a few hundred worked examples of exactly how your company writes support replies or how a legal clause is summarised. The graduate keeps the general education but adopts the house style and routines. (An analogy.)

**2. Why does it exist?**

A base model is not specialised and does not reliably follow instructions. Full pretraining is far too expensive to repeat for each need. Starting from the pretrained weights and continuing training on a small dataset is much cheaper and often enough to teach format, tone, task behaviour or domain vocabulary.

**3. Technical explanation**

- **Definition.** Fine-tuning continues training a pretrained model's parameters (or a small added subset of them) on a smaller dataset, usually with a low learning rate.
- **Instruction tuning (supervised fine-tuning).** Training on many examples of the form *instruction → good response*, which turns a text-continuing base model into one that follows instructions and chats. Providers do this before release.
- **Domain or task fine-tuning.** Training on your own examples to specialise the style, format or task (for instance, always return a JSON structure, or write in a house tone).
- **Parameter-efficient methods.** Instead of changing all weights, methods such as *LoRA* train a small number of extra parameters, which needs less memory and storage. Details vary by tool.
- **Data format.** Typically a file of examples, each an input and the desired output, or a list of role-tagged messages. The exact format is defined by the provider or library you use.
- **When to use it, and when not to.**
  - Good for: consistent style or format, specialised behaviours, reducing prompt length, smaller models matched to a narrow task.
  - Weak for: adding facts that change often (use retrieval), or fixing hallucination by itself.
  - Try prompting and retrieval first: they are cheaper, faster to change and easier to undo.
- **Risks.** *Overfitting* (memorising the small dataset), *catastrophic forgetting* (losing general abilities), bad or inconsistent examples producing bad behaviour, and leaking private data into the model. Quality and diversity of the data matter more than quantity.
- **Evaluation.** Hold back examples that are not used for training and compare the fine-tuned model with the original on them.

**4. Syntax**

```text
{"input": "<instruction or question>", "output": "<the response you want>"}
{"input": "...", "output": "..."}
```

An illustrative record shape (often one JSON object per line); real formats differ between providers.

**5. Example 1 — Basic**

*Toy demo.* Fine-tuning the bigram idea: start from "pretrained" counts, then continue with a small domain text that is weighted more heavily, and watch the predictions shift:

```python
from collections import Counter, defaultdict

general = "the cat sat on the mat . the dog sat on the rug . the cat sat on the sofa ."
domain = "the model sat on the server . the model ran on the server ."

counts = defaultdict(Counter)


def train(text, weight=1):
    words = text.split()
    for a, b in zip(words, words[1:]):
        counts[a][b] += weight


train(general)
print("before:", counts["the"].most_common(3))
train(domain, weight=3)
print("after: ", counts["the"].most_common(3))
print("sat ->", counts["sat"].most_common(1), "(still from the general data)")
```

Output:

```text
before: [('cat', 2), ('mat', 1), ('dog', 1)]
after:  [('model', 6), ('server', 6), ('cat', 2)]
sat -> [('on', 6)] (still from the general data)
```

Line by line: the first call builds the general model; the second adds the domain text with a higher weight (a crude stand-in for more training on that data). After `the` the model now prefers `server` and `model`, while things it learned earlier and that the domain data does not contradict are kept.

**6. Example 2 — Practical**

*Toy demo.* A fine-tuning *dataset*: building and validating records, then holding out some for evaluation. This part uses only the standard library and is the preparation step done before any real fine-tuning run:

```python
import json
import random

raw = [
    ("Summarise: The meeting moved to Friday.", "Meeting moved to Friday."),
    ("Summarise: Sales rose 5 percent in March.", "March sales up 5 percent."),
    ("Summarise: The server restarts at midnight.", "Server restarts at midnight."),
    ("Summarise: Training starts on Monday.", "Training starts Monday."),
    ("Summarise: The report is due next week.", "Report due next week."),
    ("", "Empty input should be rejected."),
]

clean = [{"input": i.strip(), "output": o.strip()} for i, o in raw if i.strip() and o.strip()]
print("kept", len(clean), "of", len(raw), "records")

rng = random.Random(42)
rng.shuffle(clean)
split = int(len(clean) * 0.8)
train_set, eval_set = clean[:split], clean[split:]
print("train:", len(train_set), "eval:", len(eval_set))

lines = [json.dumps(record) for record in train_set]
print(lines[0])
```

Output:

```text
kept 5 of 6 records
train: 4 eval: 1
{"input": "Summarise: Training starts on Monday.", "output": "Training starts Monday."}
```

Line by line:

- The list comprehension drops records with an empty input or output: bad examples harm a fine-tuned model.
- The data is shuffled with a fixed seed (so the result is reproducible) and split, 80 percent for training and 20 percent held back to evaluate.
- Each record becomes one JSON line, the typical file shape. The exact fields required depend on the provider or tool you use.

*Pseudocode, requires an AI service or training library (not run here):*

```text
# names are placeholders; check your provider's documentation
file_id   = upload("train.jsonl")
job       = create_fine_tune_job(base_model="<model-name>", training_file=file_id)
wait_until(job.finished)
answer    = call_model(model=job.new_model_name, messages=[...])
```

**7. Example 3 — Edge case or common mistake**

Contradictory examples teach inconsistent behaviour. A quick check finds the same input labelled in different ways:

```python
records = [
    ("Refund request", "Escalate"),
    ("Refund request", "Close ticket"),
    ("Password reset", "Send link"),
]
seen = {}
conflicts = []
for text, label in records:
    if text in seen and seen[text] != label:
        conflicts.append((text, seen[text], label))
    seen.setdefault(text, label)
print(conflicts)
```

Output:

```text
[('Refund request', 'Escalate', 'Close ticket')]
```

Overfitting shows up as a gap between training and evaluation scores:

```python
history = [("epoch 1", 0.62, 0.60), ("epoch 3", 0.85, 0.78), ("epoch 6", 0.97, 0.74), ("epoch 9", 0.99, 0.70)]
for name, train_score, eval_score in history:
    print(f"{name}: train {train_score:.2f}, eval {eval_score:.2f}, gap {train_score - eval_score:.2f}")
best = max(history, key=lambda row: row[2])
print("best on evaluation data:", best[0])
```

Output:

```text
epoch 1: train 0.62, eval 0.60, gap 0.02
epoch 3: train 0.85, eval 0.78, gap 0.07
epoch 6: train 0.97, eval 0.74, gap 0.23
epoch 9: train 0.99, eval 0.70, gap 0.29
best on evaluation data: epoch 3
```

The scores are invented to show a typical pattern: training accuracy keeps rising while the evaluation score peaks and then falls, so the best stopping point is epoch 3 by the evaluation data, not the end of training.

Fine-tuning is the wrong tool for facts that change often:

```python
fine_tuned_knowledge = {"return window": "14 days"}  # baked in at training time
current_policy = {"return window": "30 days"}        # what is true today
print("fine-tuned says:", fine_tuned_knowledge["return window"])
print("today it is:   ", current_policy["return window"])
```

Output:

```text
fine-tuned says: 14 days
today it is:    30 days
```

Knowledge baked into the weights goes stale until the next training run; retrieval (see [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)) reads the current document instead.

**8. Common mistakes**

- Fine-tuning when better prompts or retrieval would do.
- Using fine-tuning to add frequently changing facts.
- Small, noisy, contradictory or duplicated datasets.
- Evaluating only on the training data.
- Including secrets or personal data in training examples.
- Expecting fine-tuning alone to remove hallucinations.

**9. Real-world and AI applications**

Instruction tuning turns base models into assistants. Companies fine-tune for brand voice, strict output formats, classification tasks and domain-specific language, and often fine-tune a smaller model to do one task well and cheaply. Parameter-efficient methods let teams adapt open-weight models on modest hardware.

**10. Practice**

1. Extend Example 1 with a second domain text and show how the top prediction after `the` changes.
2. Write a function that removes duplicate `(input, output)` pairs from a dataset.
3. Split a list of 50 numbered records into 80 percent training and 20 percent evaluation with a fixed seed. Print the sizes.
4. Given train and eval scores per epoch, write code that returns the epoch with the best evaluation score.
5. List two situations where fine-tuning is a good choice and two where it is not.
6. Why must secrets not appear in training data?

**11. Interview questions**

- *What is fine-tuning?* Continuing the training of a pretrained model on a smaller, targeted dataset to adapt its behaviour.
- *Fine-tuning versus prompting?* Prompting changes the input per call and is immediate; fine-tuning changes the model's parameters and needs data and a training run.
- *Fine-tuning versus RAG?* RAG supplies current facts at answer time; fine-tuning shapes style, format and behaviour.
- *What is catastrophic forgetting?* Losing earlier general abilities while training on new, narrow data.
- *What is LoRA?* A parameter-efficient method that trains a small set of added parameters instead of all the weights.

**12. Quick revision**

- Fine-tuning = more training on a small, targeted dataset.
- Instruction tuning makes assistants; domain tuning adapts style and tasks.
- Good data beats a lot of data; hold out an evaluation set.
- Try prompting and retrieval first; not for fast-changing facts.
- Risks: overfitting, forgetting, bad or private data.

---

## RLHF

**Timestamp:** [12:11:31](https://www.youtube.com/watch?v=J9BI0jGOds8&t=43891s)

**Learning objectives:**

- Explain RLHF (reinforcement learning from human feedback) and the problem it addresses.
- Describe the stages: collect comparisons, train a reward model, optimise the language model against it.
- Compute a simple reward-based choice in Python.
- Explain the limits: reward hacking, biased feedback, and related approaches.

**1. Intuition**

A chef can cook technically correct dishes, but diners prefer some over others. In RLHF, people are shown two answers to the same question and say which is better. From many such choices a "taste judge" is learned. The model is then trained to produce dishes the judge scores highly. The result is an assistant that is more helpful, polite and cautious than the base model. (An analogy.)

**2. Why does it exist?**

"A good answer" is hard to write as a rule, but easy for a person to recognise by comparison. Predicting the next token does not by itself make a model helpful, honest or safe: the internet contains rude, wrong and harmful text too. RLHF turns human judgement into a training signal that steers behaviour.

**3. Technical explanation**

*Typical stages (simplified; real pipelines differ):*

1. **Start from an instruction-tuned model** (see [Fine-Tuning](#fine-tuning)).
2. **Collect comparisons.** For many prompts, the model produces several answers and human raters rank or choose the better one, using written guidelines.
3. **Train a reward model.** A model that takes a prompt and an answer and outputs a score, trained so that preferred answers score higher than rejected ones.
4. **Optimise the language model with reinforcement learning** to produce answers the reward model scores highly, while a penalty keeps it from drifting too far from the original model (to stay fluent and avoid exploiting the reward model).
5. **Evaluate and repeat.** Check helpfulness, safety and regressions.

*Related ideas.* Methods such as *direct preference optimisation* learn from preference comparisons without a separate reward model. Some approaches use AI-generated feedback, guided by written principles, in addition to or instead of human labels. Reasoning-focused models use reinforcement learning with automatically checkable outcomes (see [Reasoning Models](39-multimodal-reasoning-slm-agi-asi.md#reasoning-models)). The details differ between organisations and are not always published.

*Benefits.* Better instruction following, tone and refusals of clearly harmful requests, and fewer rude or unhelpful outputs.

*Limits.*

- **Feedback quality.** Raters can be inconsistent or biased, and preferences differ across cultures and people.
- **Reward hacking.** The model can learn to please the reward model (for example, longer, more confident answers) rather than be correct.
- **Sycophancy.** Optimising for approval can make a model agree with users too readily.
- **Not a truth guarantee.** Preferred answers sound good to raters; hallucinations can persist (see [AI Hallucination](31-llms-prompting-temperature-hallucination.md#ai-hallucination)).
- **Cost.** Collecting quality human feedback is expensive.

**4. Syntax**

```text
reward_model(prompt, answer) -> score          # learned from human comparisons

choose answers (or train the model) so that:
    expected reward(answer) is high
    while staying close to the original model
```

Pattern only; real training uses reinforcement-learning algorithms not shown here.

**5. Example 1 — Basic**

*Toy demo.* Pairwise preferences turned into scores. Each time a person prefers one answer, the winner gains a point; the totals give a crude "reward" per answer:

```python
comparisons = [
    ("answer_A", "answer_B"),  # (preferred, rejected)
    ("answer_A", "answer_C"),
    ("answer_B", "answer_C"),
    ("answer_A", "answer_B"),
    ("answer_C", "answer_B"),
]

scores = {}
for winner, loser in comparisons:
    scores[winner] = scores.get(winner, 0) + 1
    scores[loser] = scores.get(loser, 0) - 1

print(scores)
best = max(scores, key=scores.get)
print("highest reward:", best)
```

Output:

```text
{'answer_A': 3, 'answer_B': -2, 'answer_C': -1}
highest reward: answer_A
```

Line by line: each tuple is one human choice; winners go up and losers down. The totals say `answer_A` is most preferred overall. A real reward model is a neural network that generalises to new answers, and it is trained with a probability model of preferences, not simple tallies.

**6. Example 2 — Practical**

*Toy demo.* A hand-written "reward model" scoring answers, and *best-of-n* selection: generate several candidate answers and keep the one with the highest reward. This is one simple way reward models are used, and it shows the effect without reinforcement learning:

```python
candidates = [
    "idk",
    "A list is an ordered, changeable collection of items, for example [1, 2, 3].",
    "Lists are very very very very very very very good and I am absolutely certain.",
    "A list holds items in order.",
]


def toy_reward(answer):
    words = answer.split()
    score = 0.0
    score += min(len(words), 12) * 0.2            # some detail is good, up to a point
    score += 1.0 if "for example" in answer else 0.0  # examples are liked
    score -= 0.5 * (len(words) - len(set(words)))      # repetition is penalised
    return round(score, 2)


for answer in candidates:
    print(f"{toy_reward(answer):>5}  {answer}")
print("best of 4:", max(candidates, key=toy_reward))
```

Output:

```text
  0.2  idk
  3.4  A list is an ordered, changeable collection of items, for example [1, 2, 3].
 -0.6  Lists are very very very very very very very good and I am absolutely certain.
  1.2  A list holds items in order.
best of 4: A list is an ordered, changeable collection of items, for example [1, 2, 3].
```

Line by line:

- `toy_reward` encodes three invented preferences: some detail, an example, and no repetition. A real reward model learns such preferences from comparisons instead of having them written by hand.
- Each candidate is scored; `max(..., key=toy_reward)` picks the best.
- The rambling, repetitive answer scores low despite sounding confident, the one-word answer is low for lack of detail, and the answer with an example wins.

**7. Example 3 — Edge case or common mistake**

*Reward hacking.* If the reward only measures something easy (here: length), an optimiser exploits it:

```python
def naive_reward(answer):
    return len(answer.split())


candidates = [
    "Lists are ordered collections.",
    "Lists are ordered collections that can be changed, indexed, sliced and looped over.",
    "Lists lists lists lists lists lists lists lists lists lists lists lists lists lists.",
]
best = max(candidates, key=naive_reward)
print(best)
```

Output:

```text
Lists lists lists lists lists lists lists lists lists lists lists lists lists lists.
```

The padding wins, because the reward is a proxy for quality, not quality itself. Real reward models are far more subtle, but the same kind of exploitation happens, which is why a penalty for drifting from the original model and careful evaluation are used.

Disagreeing raters give noisy signals. A simple agreement check:

```python
votes = {"pair1": ["A", "A", "A"], "pair2": ["A", "B", "B"], "pair3": ["A", "B", "A"]}
for pair, v in votes.items():
    top = max(set(v), key=v.count)
    print(pair, "majority:", top, "agreement:", round(v.count(top) / len(v), 2))
```

Output:

```text
pair1 majority: A agreement: 1.0
pair2 majority: B agreement: 0.67
pair3 majority: A agreement: 0.67
```

Pairs with low agreement carry less reliable signal. Real projects measure agreement and write guidelines to improve it.

Optimising for approval can reward flattery. A toy contrast:

```python
answers = {
    "agrees": "You are absolutely right, great idea!",
    "corrects": "That claim is incorrect: Python lists are mutable.",
}
approval_if_user_is_wrong = {"agrees": 0.9, "corrects": 0.6}   # invented human approval ratings
accuracy = {"agrees": 0.0, "corrects": 1.0}                    # invented ground truth
print("highest approval:", max(approval_if_user_is_wrong, key=approval_if_user_is_wrong.get))
print("most accurate:   ", max(accuracy, key=accuracy.get))
```

Output:

```text
highest approval: agrees
most accurate:    corrects
```

The ratings are invented to illustrate the risk: when the approval signal and accuracy disagree, optimising only for approval pushes a model towards agreeable but wrong answers. This is one reason developers add honesty-focused data and evaluations.

**8. Common mistakes**

- Thinking RLHF teaches the model facts: it mainly shapes behaviour and style.
- Believing human preference equals truth.
- Using a reward that is an easy-to-game proxy.
- Assuming the process is the same at every organisation: details are often unpublished.
- Ignoring rater disagreement and bias in the feedback data.
- Treating "aligned" as "perfectly safe".

**9. Real-world and AI applications**

Preference-based training is a main reason today's assistants are conversational, follow instructions, decline clearly harmful requests, and adopt a helpful tone. Teams building applications use the same idea on a smaller scale: collecting thumbs up and thumbs down, ranking outputs, and using scoring functions to choose among candidate answers or to evaluate changes.

**10. Practice**

1. Add two more comparisons to Example 1 so that `answer_B` becomes the highest-scoring answer.
2. Add a fourth rule to `toy_reward` that rewards answers containing the word `ordered`. Print the new ranking.
3. Write `best_of_n(candidates, reward)` that returns the highest-scoring answer and its score.
4. Make `naive_reward` harder to game by penalising repeated words, and rerun the candidates.
5. Explain in your own words why reward hacking happens.
6. Name one benefit and one limit of RLHF.

**11. Interview questions**

- *What is RLHF?* Training a model with a reward signal learned from human preference comparisons, to make it more helpful and safe.
- *What is a reward model?* A model that scores an answer, trained so that humans' preferred answers score higher.
- *What is reward hacking?* The model exploiting weaknesses of the reward signal to score highly without actually being better.
- *Does RLHF make models truthful?* Not by itself; it optimises for preferred answers, which can still be wrong.
- *What is an alternative to RLHF?* For example direct preference optimisation, or feedback guided by written principles.

**12. Quick revision**

- RLHF: human comparisons, reward model, optimise the model for high reward with a leash.
- Makes assistants more helpful, polite and cautious.
- Limits: noisy feedback, reward hacking, sycophancy, not a truth guarantee.
- Best-of-n: sample several answers, keep the top-scored one.
- Related: DPO, AI feedback, outcome-based reinforcement learning.

---

## Answers to Practice Exercises

### Answers: How LLMs Learn: Pretraining

1.

```python
from collections import Counter, defaultdict

words = "the cat sat on the mat . the cat ate the fish . the dog sat on the rug .".split()
counts = defaultdict(Counter)
for a, b in zip(words, words[1:]):
    counts[a][b] += 1
print(counts["on"].most_common(1), counts["the"].most_common(1))
```

Output:

```text
[('the', 2)] [('cat', 2)]
```

2.

```python
data = [(x, 5 * x) for x in range(1, 5)]
w, rate, epoch = 0.0, 0.02, 0
while abs(w - 5) > 0.01:
    gradient = sum(2 * (w * x - y) * x for x, y in data) / len(data)
    w -= rate * gradient
    epoch += 1
print(epoch, round(w, 4))
```

Output:

```text
18 4.9919
```

3.

```python
import math

print(round(-math.log(0.25), 3))
```

Output:

```text
1.386
```

4.

```python
data = [(1, 3), (2, 6), (3, 9), (4, 12)]
for rate in (0.1, 0.25):
    w = 0.0
    for _ in range(8):
        w -= rate * sum(2 * (w * x - y) * x for x, y in data) / len(data)
    print(rate, round(w, 3))
```

Output:

```text
0.1 2.988
0.25 -9809.571
```

A rate of 0.1 converges (w near 3); 0.25 diverges, because each step overshoots by more than the last.

5. Training changes the model's parameters using data and a loss; inference uses the fixed, finished model to produce an output for an input.

6. The parameters were set from data collected up to some date, and they do not change when the model is used, so it knows nothing about later events unless the information is supplied in the context.

### Answers: Fine-Tuning

1.

```python
from collections import Counter, defaultdict

counts = defaultdict(Counter)


def train(text, weight=1):
    words = text.split()
    for a, b in zip(words, words[1:]):
        counts[a][b] += weight


train("the cat sat on the mat . the cat sat on the sofa .")
print(counts["the"].most_common(2))
train("the model ran on the server . the model ran on the cluster .", weight=3)
print(counts["the"].most_common(2))
train("the cluster failed . the cluster restarted . the cluster ran .", weight=3)
print(counts["the"].most_common(2))
```

Output:

```text
[('cat', 2), ('mat', 1)]
[('model', 6), ('server', 3)]
[('cluster', 12), ('model', 6)]
```

2.

```python
def dedupe(pairs):
    seen = set()
    out = []
    for pair in pairs:
        if pair not in seen:
            seen.add(pair)
            out.append(pair)
    return out


print(dedupe([("a", "b"), ("a", "b"), ("c", "d")]))
```

Output:

```text
[('a', 'b'), ('c', 'd')]
```

3.

```python
import random

records = [f"record {i}" for i in range(1, 51)]
random.Random(1).shuffle(records)
cut = int(len(records) * 0.8)
print(len(records[:cut]), len(records[cut:]))
```

Output:

```text
40 10
```

4.

```python
scores = [(1, 0.60), (2, 0.71), (3, 0.78), (4, 0.74)]  # (epoch, evaluation score)
print(max(scores, key=lambda row: row[1])[0])
```

Output:

```text
3
```

5. Good: a consistent house style or output format; a narrow task where a small tuned model should replace a large prompt. Not good: facts that change often (use retrieval); a one-off task that a better prompt solves.

6. The model can memorise and later repeat parts of its training data, so secrets or personal data might leak to people who use the model.

### Answers: RLHF

1. For example, add comparisons so that `answer_B` wins more often:

```python
comparisons = [
    ("answer_A", "answer_B"), ("answer_A", "answer_C"), ("answer_B", "answer_C"),
    ("answer_A", "answer_B"), ("answer_C", "answer_B"),
    ("answer_B", "answer_A"), ("answer_B", "answer_A"), ("answer_B", "answer_A"),
    ("answer_B", "answer_C"), ("answer_B", "answer_C"),
]
scores = {}
for winner, loser in comparisons:
    scores[winner] = scores.get(winner, 0) + 1
    scores[loser] = scores.get(loser, 0) - 1
print(scores, max(scores, key=scores.get))
```

Output:

```text
{'answer_A': 0, 'answer_B': 3, 'answer_C': -3} answer_B
```

2.

```python
def toy_reward(answer):
    words = answer.split()
    score = min(len(words), 12) * 0.2
    score += 1.0 if "for example" in answer else 0.0
    score -= 0.5 * (len(words) - len(set(words)))
    score += 0.5 if "ordered" in answer else 0.0
    return round(score, 2)


candidates = ["idk", "A list is an ordered collection, for example [1, 2].", "A list holds items."]
for c in sorted(candidates, key=toy_reward, reverse=True):
    print(toy_reward(c), c)
```

Output:

```text
3.5 A list is an ordered collection, for example [1, 2].
0.8 A list holds items.
0.2 idk
```

3.

```python
def best_of_n(candidates, reward):
    best = max(candidates, key=reward)
    return best, reward(best)


print(best_of_n(["a", "bb", "ccc"], len))
```

Output:

```text
('ccc', 3)
```

4.

```python
def better_reward(answer):
    words = answer.split()
    return len(set(words))


candidates = [
    "Lists are ordered collections.",
    "Lists are ordered collections that can be changed, indexed, sliced and looped over.",
    "Lists lists lists lists lists lists lists lists lists lists lists lists lists lists.",
]
print(max(candidates, key=better_reward))
```

Output:

```text
Lists are ordered collections that can be changed, indexed, sliced and looped over.
```

Counting only distinct words removes the reward for repetition (padding with new words would still game it, so real rewards need more than this).

5. The reward is a proxy for what people actually want. An optimiser finds whatever raises the proxy most cheaply, even if that is not real quality.

6. Benefit: better instruction following and tone. Limit: it optimises for preferred answers, which are not necessarily true (reward hacking and flattery are also risks).

---

## Chapter Summary and Key Takeaways

- Pretraining adjusts parameters by gradient descent so the model predicts the next token over a huge text collection; it needs no human labels and yields a base model with a knowledge cutoff, which does not learn from your chats at use time.
- Fine-tuning continues training on a smaller targeted dataset to adapt style, format or tasks; data quality, a held-out evaluation set and avoiding overfitting matter, and it is not the tool for fast-changing facts.
- RLHF turns human comparisons into a reward model and optimises the model against it, making assistants more helpful and safe, with limits: noisy feedback, reward hacking, sycophancy, and no guarantee of truth.
- Training changes parameters; using the model (inference) does not.
- Prompting, retrieval and fine-tuning are complementary; try the cheaper, easier-to-change options first.

Next: [Chapter 37 — Retrieval-Augmented Generation](37-retrieval-augmented-generation.md) shows how to give a model current and private knowledge at answer time.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
