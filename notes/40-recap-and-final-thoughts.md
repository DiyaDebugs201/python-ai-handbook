# Chapter 40 — Recap and Final Thoughts

> Part 6 — Python Integration and AI Foundations · Video: 12:56:47–end · Previous: [39 Multimodal AI, Reasoning Models, SLMs, AGI and ASI](39-multimodal-reasoning-slm-agi-asi.md) · Next: back to the [README](../README.md)

**In this chapter:** a recap of how the Python skills and the AI concepts of this handbook connect, a short set of final thoughts with next steps, and a supplementary section on *evaluation, limitations and responsible use*, which every real AI project needs.

**Before you start:** this chapter reviews the whole handbook, especially [Chapter 30](30-python-wrap-up-and-ai-intro.md) through [Chapter 39](39-multimodal-reasoning-slm-agi-asi.md). All code is a *toy demo* (standard library, tiny invented data) or *pseudocode*; nothing calls a real AI service. Examples were run with Python 3.13.

---

## Recap: How It All Connects

**Timestamp:** [12:56:47](https://www.youtube.com/watch?v=J9BI0jGOds8&t=46607s)

**Learning objectives:**

- Trace a question through a typical AI application from text to answer.
- Map each AI concept in Part 6 to the Python skills it relies on.
- Assemble a miniature end-to-end pipeline in Python.
- Identify where each kind of failure can enter.

**1. Intuition**

Think of a restaurant. The *kitchen* (the model) has been trained for years (pretraining, fine-tuning, feedback). The *waiter* (your Python program) takes the order, fetches the right ingredients from the pantry (retrieval), tells the kitchen exactly what to make (prompt and context), carries the dish out, and checks it before it reaches the table. Customers only notice the meal, but most of the quality comes from the waiter's care, the pantry's organisation and the checks. (An analogy.)

**2. Why does it exist?**

The earlier chapters covered the parts one at a time. Real applications combine them, and failures happen at the joints: wrong context, wrong retrieval, unchecked output. A recap shows the whole pipeline so that each part has a place.

**3. Technical explanation**

*The pipeline, with chapter references.*

1. **Your Python program** receives the user's request, reads settings and keys from the environment (see [Environment Variables, .env Files, and API Keys](30-python-wrap-up-and-ai-intro.md#environment-variables-env-files-and-api-keys)) and handles errors. This is where functions, dictionaries, loops, string handling and `try`/`except` from Parts 1 to 5 are used.
2. **Context engineering** decides what goes into the input: instructions, history, retrieved facts, tool results (see [Context Engineering](32-context-engineering-and-tokens.md#context-engineering)), within the budget set by **tokens** and the **context window** (see [Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs) and [Context Window](34-context-window-and-model-parameters.md#context-window)).
3. **Retrieval** (RAG) finds relevant passages using **embeddings** and similarity (see [Vectors and Embeddings](33-vectors-and-embeddings.md) and [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md#retrieval-augmented-generation-rag)).
4. **Prompting** and settings such as **temperature** shape the request (see [Prompting](31-llms-prompting-temperature-hallucination.md#prompting) and [Temperature](31-llms-prompting-temperature-hallucination.md#temperature)).
5. **The model** (a transformer with fixed learned parameters; see [Transformers](35-attention-and-transformers.md#transformers) and [Model Parameters](34-context-window-and-model-parameters.md#model-parameters)) produces probabilities for the next token, one token at a time. Its abilities came from **pretraining**, **fine-tuning** and **RLHF** (see [Chapter 36](36-pretraining-fine-tuning-rlhf.md)).
6. **Tools and agents** let the model request actions that your code carries out, for example via MCP (see [Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md)).
7. **Checks** on the output: grounding against sources, format validation, safety filters, and human review where stakes are high (see [AI Hallucination](31-llms-prompting-temperature-hallucination.md#ai-hallucination)).
8. **Logging and evaluation** record what happened and measure quality over time (see the supplementary section below).

*Where failures enter.* Missing or wrong context; poor retrieval; ambiguous prompts; outdated knowledge; hallucination; tool misuse or injected instructions; cost and latency growth; leaked secrets. For each there is a Python-level control: validation, limits, logging, tests.

*Choosing a model setup.* Use a smaller or cheaper model when the task is simple ([Small Language Models](39-multimodal-reasoning-slm-agi-asi.md#small-language-models-slms)), a reasoning model when it needs multi-step working ([Reasoning Models](39-multimodal-reasoning-slm-agi-asi.md#reasoning-models)), and a multimodal one when inputs are not text ([Multimodal AI](39-multimodal-reasoning-slm-agi-asi.md#multimodal-ai)). Add retrieval for changing facts, fine-tuning for style and format, and an agent loop only when the task needs the model to choose steps.

**4. Syntax**

```text
request -> validate -> build context (instructions + retrieved facts + history, under a token budget)
        -> call model (settings) -> parse -> check (grounding, format, safety)
        -> answer + sources -> log
```

A pipeline outline, not code.

**5. Example 1 — Basic**

*Toy demo.* A table linking each concept to the Python skill it leans on, as a dictionary you can query:

```python
connections = {
    "tokens": "strings, len(), splitting text",
    "embeddings": "lists, loops, math (dot product)",
    "retrieval": "dictionaries, sorting with key=",
    "context assembly": "functions, slicing, comprehensions",
    "tool calls": "dictionaries, functions as values, exceptions",
    "agents": "while/for loops, conditionals, state in lists",
    "api keys": "os.environ, never hard-coded",
}

for concept, skill in connections.items():
    print(f"{concept:<17} <- {skill}")
print(len(connections), "concepts")
```

Output:

```text
tokens            <- strings, len(), splitting text
embeddings        <- lists, loops, math (dot product)
retrieval         <- dictionaries, sorting with key=
context assembly  <- functions, slicing, comprehensions
tool calls        <- dictionaries, functions as values, exceptions
agents            <- while/for loops, conditionals, state in lists
api keys          <- os.environ, never hard-coded
7 concepts
```

Line by line: a dictionary maps each concept to the Python skills used to implement it, and a loop prints it neatly using a format specifier (`:<17` left-aligns in 17 columns). The point is practical: the AI topics you met are built from the Python you already know.

**6. Example 2 — Practical**

*Toy demo.* An end-to-end miniature that strings together ideas from Part 6: a token estimate, retrieval by word overlap, prompt assembly under a budget, a **fake model** (a function standing in for a real service, so output is deterministic), and a grounding check on the answer. Nothing here is a real AI call.

```python
import re
from collections import Counter

DOCUMENTS = [
    {"source": "refunds.txt", "text": "Refunds are available within 30 days of purchase with a receipt."},
    {"source": "refunds.txt", "text": "Gift cards cannot be refunded."},
    {"source": "shipping.txt", "text": "Standard shipping takes five working days."},
]
STOP = {"a", "an", "the", "is", "are", "of", "to", "for", "in", "on", "i", "my", "do", "how", "can", "what", "with", "and", "long", "does"}


def words(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


def estimate_tokens(text):
    return max(1, round(len(text) / 4))          # rough estimate, not a real tokenizer


def retrieve(question, k=2):
    q = Counter(words(question))
    scored = sorted(((sum(q[w] for w in words(d["text"])), d) for d in DOCUMENTS), key=lambda p: p[0], reverse=True)
    return [d for score, d in scored[:k] if score > 0]


def build_prompt(question, docs, budget_tokens=120):
    header = "Answer only from the sources. If they do not contain the answer, say you do not know.\n"
    parts, used = [], estimate_tokens(header) + estimate_tokens(question)
    for i, d in enumerate(docs, 1):
        line = f"[{i}] {d['text']}"
        if used + estimate_tokens(line) > budget_tokens:
            break
        parts.append(line)
        used += estimate_tokens(line)
    return header + "\n".join(parts) + f"\nQuestion: {question}", used


def fake_model(prompt):
    """Stand-in for a language model: returns the first source line, or 'I do not know'."""
    sources = [l for l in prompt.splitlines() if l.startswith("[")]
    return sources[0].split("] ", 1)[1] if sources else "I do not know."


def grounded(answer, docs):
    return answer == "I do not know." or any(answer == d["text"] for d in docs)


for question in ["How long does shipping take?", "Who won the match?"]:
    docs = retrieve(question)
    prompt, tokens = build_prompt(question, docs)
    answer = fake_model(prompt)
    print(f"Q: {question}")
    print(f"   retrieved {len(docs)} source(s), prompt about {tokens} tokens")
    print(f"   A: {answer} | grounded: {grounded(answer, docs)}")
```

Output:

```text
Q: How long does shipping take?
   retrieved 1 source(s), prompt about 41 tokens
   A: Standard shipping takes five working days. | grounded: True
Q: Who won the match?
   retrieved 0 source(s), prompt about 26 tokens
   A: I do not know. | grounded: True
```

Line by line:

- `retrieve` scores each document by shared words and keeps the best with a positive score; a question with no overlap gets none.
- `build_prompt` adds instructions, then sources while they fit the token budget (see [Context Engineering](32-context-engineering-and-tokens.md#context-engineering)).
- `fake_model` replaces the real model call. A real call would send `prompt` to an AI service and return generated text.
- `grounded` checks that the answer is supported by the retrieved sources, or is an honest "I do not know".
- With no relevant source, the pipeline says it does not know rather than guessing, the behaviour you want from a well-designed system.

**7. Example 3 — Edge case or common mistake**

A pipeline hides problems if you only look at the final answer. Logging each stage makes failures diagnosable:

```python
def stage_log(question, docs, prompt_tokens, answer):
    return {"question": question, "docs": len(docs), "prompt_tokens": prompt_tokens, "answer": answer}


record = stage_log("Who won the match?", [], 31, "I do not know.")
print(record)
problems = []
if record["docs"] == 0:
    problems.append("no sources retrieved: check retrieval or whether the knowledge exists")
if record["prompt_tokens"] > 100:
    problems.append("prompt large: consider trimming")
print(problems or "no problems detected")
```

Output:

```text
{'question': 'Who won the match?', 'docs': 0, 'prompt_tokens': 31, 'answer': 'I do not know.'}
['no sources retrieved: check retrieval or whether the knowledge exists']
```

Another frequent error is calling a real service from a test without safeguards. Keep the model call behind a function so tests can substitute a fake:

```python
def answer_question(question, model):
    return model(f"Question: {question}")


print(answer_question("2 + 2?", model=lambda prompt: "fake: 4"))
```

Output:

```text
fake: 4
```

Passing the model as an argument (a first-class function, see [First-Class Functions](28-first-class-functions-and-lambda.md)) lets you test the surrounding logic without cost, delay or randomness.

**8. Common mistakes**

- Treating the model as the whole system and neglecting retrieval, context, validation and logging.
- Debugging only the final answer, not each stage.
- Calling real services in every test.
- Mixing instructions with untrusted data.
- Skipping budgets for tokens, time and money.
- Assuming one design (a big model, an agent) fits every task.

**9. Real-world and AI applications**

Support assistants, search over company documents, coding helpers, data analysis assistants and workflow automation all follow this outline. The differences lie in the sources, the tools, the checks and the level of human oversight.

**10. Practice**

1. Add two more concepts to the `connections` dictionary and print them in alphabetical order.
2. Add a third document to `DOCUMENTS` and ask a question that it answers. Show the output.
3. Change `budget_tokens` in `build_prompt` to 30. What happens to the number of sources included?
4. Write a `fake_model` variant that always answers "I do not know." and show that `grounded` accepts it.
5. Draw (in text) the pipeline for an application you would like to build, labelling each stage with a chapter from this handbook.
6. List three things you would log for every request in a production system.

**11. Interview questions**

- *Walk me through an LLM application end to end.* Request, validation, context building (with retrieval and budgets), model call with settings, output parsing, checks, answer with sources, logging.
- *Where do hallucinations come from, and how do you reduce them?* From generating plausible text without support; reduce with retrieval, instructions to use only sources, verification, and an honest "I do not know" path.
- *How do you test an LLM application?* Keep the model behind an interface, test the surrounding logic with fakes, and evaluate real model behaviour on a fixed test set.

**12. Quick revision**

- Python is the glue: input, context, retrieval, calls, checks, logs.
- The model is one component with fixed knowledge and probabilistic output.
- Control cost with tokens and budgets; control quality with retrieval and checks.
- Log each stage; test with fakes.
- Choose the simplest design that works.

---

## Final Thoughts

**Timestamp:** [12:59:03](https://www.youtube.com/watch?v=J9BI0jGOds8&t=46743s)

**Learning objectives:**

- Summarise what you have learned and what the handbook did not cover.
- Choose concrete next steps for practice and projects.
- Build a simple personal learning plan in Python.
- Keep good habits: verify, measure, stay current.

**1. Intuition**

You have just finished an introductory course, the equivalent of learning the alphabet, basic grammar and a few hundred words of a language. You can read and write simple sentences, and you understand how the language is structured. Fluency comes from using it, in projects you care about. (An analogy.)

**2. Why does it exist?**

A syllabus ends, but skills fade without use, and the AI field changes quickly. A short closing section turns the course into a plan: what to practise, what to read next, and which habits keep you reliable as tools change.

**3. Technical explanation**

*What you now have.*

- **Python basics**: values and types, strings, operators, conditionals, loops, lists, tuples, sets, dictionaries, functions and scope, lambdas and `map`/`filter`/`reduce`.
- **AI concepts**: how LLMs work at a high level (tokens, embeddings, attention, transformers), how they are trained, how to use them well (prompting, context, retrieval, tools, agents) and where they fail.

*What this handbook does not cover.* Object-oriented programming, file handling, modules and packages in depth, error handling in depth, virtual environments and dependency management, testing frameworks, data libraries such as NumPy and pandas, calling real AI services from code, building neural networks, deployment, and security in depth. These are natural next steps.

*Suggested next steps.*

1. **Finish the practice**: work through `practice/` and the `projects/` folder, extending each project with a feature of your own.
2. **Learn the next Python layer**: files, exceptions, classes, modules and packages, virtual environments, `pytest`.
3. **Work with data**: NumPy, pandas, simple plots.
4. **Call a real service**: pick a provider, read its current documentation, keep the key in an environment variable, and build a small tool such as a document question-answerer with your own retrieval.
5. **Build and evaluate one small project end to end**, with tests and a written evaluation.
6. **Read primary sources**: official documentation for the tools you use, and original papers when you want depth. Check dates: advice in this area ages fast.

*Habits that last.* Verify before trusting (code and model output). Keep secrets out of code. Measure instead of guessing. Write small, testable functions. Keep notes of what you learned in your own words. Share your work and ask for review.

*A note about this handbook.* It is an independently written study aid based on a public course outline. Check facts that matter against official sources, especially anything marked as changing quickly, such as protocols, product features, prices and limits.

**4. Syntax**

There is no new syntax; the closing tool is a plan you can write as data:

```text
goal -> milestones -> weekly tasks -> review
```

**5. Example 1 — Basic**

*Toy demo.* A learning plan as a list of dictionaries, with a count of what is done:

```python
plan = [
    {"task": "Finish Part 1 exercises", "done": True},
    {"task": "Build the contact book project", "done": True},
    {"task": "Learn files and exceptions", "done": False},
    {"task": "Call a real AI service from Python", "done": False},
]

done = sum(item["done"] for item in plan)
print(f"{done}/{len(plan)} done ({done / len(plan):.0%})")
for item in plan:
    mark = "x" if item["done"] else " "
    print(f"[{mark}] {item['task']}")
```

Output:

```text
2/4 done (50%)
[x] Finish Part 1 exercises
[x] Build the contact book project
[ ] Learn files and exceptions
[ ] Call a real AI service from Python
```

Line by line: `sum` over booleans counts the `True` values (`True` is `1`), the percentage uses an f-string format, and each task is printed as a checklist line.

**6. Example 2 — Practical**

*Toy demo.* A tiny spaced-review scheduler. Topics you finished get a next-review day that grows after each successful review, a simple version of spaced repetition:

```python
from datetime import date, timedelta

today = date(2026, 1, 1)           # fixed date so the output is reproducible
intervals = [1, 3, 7, 14, 30]      # days until the next review after each successful review


def schedule(topic, reviews_done, start=today):
    index = min(reviews_done, len(intervals) - 1)
    return topic, start + timedelta(days=intervals[index])


topics = {"tokens": 0, "embeddings": 1, "rag": 2, "agents": 5}
for topic, count in topics.items():
    name, due = schedule(topic, count)
    print(f"{name:<11} reviewed {count}x -> next review on {due.isoformat()}")
```

Output:

```text
tokens      reviewed 0x -> next review on 2026-01-02
embeddings  reviewed 1x -> next review on 2026-01-04
rag         reviewed 2x -> next review on 2026-01-08
agents      reviewed 5x -> next review on 2026-01-31
```

Line by line: `intervals` grows with each successful review; `min(...)` caps the index so topics reviewed many times reuse the last interval; `timedelta` adds days to a `date`. The date is fixed here so that the output never changes; in real use you would start from `date.today()`.

**7. Example 3 — Edge case or common mistake**

A plan with no deadlines or measurable outcome is just a wish. A check that flags vague tasks:

```python
tasks = ["Learn AI", "Build a CLI note-taker with tests by Sunday", "Get better at Python"]


def looks_measurable(task):
    markers = ["build", "finish", "write", "complete", "by "]
    return any(marker in task.lower() for marker in markers)


for task in tasks:
    print(f"{'ok ' if looks_measurable(task) else 'vague'}  {task}")
```

Output:

```text
vague  Learn AI
ok   Build a CLI note-taker with tests by Sunday
vague  Get better at Python
```

The check is crude (it only looks for certain words), but the habit it points to is real: make each task something you can finish and verify.

Another common mistake is copying code or model output you do not understand. A habit that helps: explain it back in your own words and change one thing to see what happens.

```python
def explain_back(code_snippet):
    return f"Before using this, I should be able to say what each of its {len(code_snippet.splitlines())} lines does."


print(explain_back("total = 0\nfor n in [1, 2, 3]:\n    total += n"))
```

Output:

```text
Before using this, I should be able to say what each of its 3 lines does.
```

**8. Common mistakes**

- Moving on to advanced topics before the basics are solid.
- Only watching or reading, without writing code.
- Never finishing a project.
- Copying AI-generated code without understanding or testing it.
- Chasing every new tool instead of building depth.
- Trusting outdated tutorials on fast-moving topics.

**9. Real-world and AI applications**

The same path (basics, small projects, data skills, a real service, evaluation) is how most people move from beginner to useful practitioner. Portfolio projects with a README, tests and an honest evaluation show more than certificates alone.

**10. Practice**

1. Write your own learning plan as a list of dictionaries with at least five tasks, each with a deadline string, and print the ones not yet done.
2. Extend the review scheduler so that a failed review resets `reviews_done` to 0.
3. Pick one project from `projects/` and write down three features you would add.
4. List five topics from this handbook you would explain to a friend, and for each write one sentence.
5. Write a short list of official sources you will check for each fast-moving topic (protocols, prices, limits).

**11. Interview questions**

- *What would you do next to become productive with AI in Python?* Learn files, errors, classes and packages; learn data libraries; call a real service with keys in environment variables; build and evaluate a small project.
- *How do you keep up with a fast-changing field?* Rely on official documentation and primary sources, date-stamp what you learn, and build small projects to test claims.
- *How do you show your skills?* With working, tested projects, a clear README and an honest evaluation of strengths and weaknesses.

**12. Quick revision**

- You have the Python basics and the AI mental model.
- Next: files, exceptions, classes, packages, data libraries, a real service, evaluation.
- Build small, finish, test, write it up.
- Verify facts that change.
- Keep secrets out of code.

---

## Evaluation, Limitations, and Responsible Use

This section is supplementary: the video topic list does not name it, but evaluation and responsible use are part of building any AI application and tie the earlier chapters together.

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Final Thoughts](40-recap-and-final-thoughts.md#final-thoughts)).

**Learning objectives:**

- Build a small evaluation set and compute simple metrics.
- Write regression checks so that changes do not silently reduce quality.
- Recognise key limitations and risks of AI systems.
- Apply basic responsible-use practices: privacy, transparency, human oversight.

**1. Intuition**

Before a new medicine is sold it is tested on a defined group, with a clear measure of success and a check for side effects. An AI feature should be treated the same way: decide what "good" means, test on examples you did not tune it for, and keep testing after every change. (An analogy.)

**2. Why does it exist?**

Model output varies, can look right while being wrong, and changes when prompts, models or data change. Without measurement you cannot tell whether a change helped. And because these systems affect people, you must consider privacy, fairness, safety and honesty.

**3. Technical explanation**

*Evaluation basics.*

- **Test set**: a fixed list of inputs with the expected outcome or a way to judge it. Keep it separate from examples you used while designing prompts or training, so it measures real ability.
- **Metrics**: for classification, *accuracy* (share correct), and *precision* and *recall* when classes are unbalanced or errors have different costs. For free-form text, compare against references, use rule-based checks (format, required facts, forbidden content), human review, or a second model as judge (which has its own errors and biases and should itself be checked against human judgement).
- **Groundedness**: for RAG, check that claims are supported by the retrieved sources, and that retrieval returned the needed passages.
- **Regression tests**: re-run the test set after each change to prompts, models or code; compare against the previous results.
- **Variance**: because outputs can vary, run important checks more than once and look at the distribution, not just one run.
- **Cost and latency** are metrics too.

*Limitations to keep in mind.*

- **Hallucination** and confident errors (see [AI Hallucination](31-llms-prompting-temperature-hallucination.md#ai-hallucination)).
- **Knowledge cutoff** and no learning from your conversations by default.
- **Bias** from training data and feedback, which can produce unfair or stereotyped outputs.
- **Sensitivity** to wording and to the order of information in the context.
- **Reasoning limits**: fluent steps can be wrong.
- **Prompt injection** and misuse of tools.
- **Privacy**: prompts and documents may be stored or processed by a service; models can reproduce memorised text.
- **Environmental and financial cost** of training and running large models.

*Responsible-use practices.*

- **Data minimisation**: send only the data needed; remove or mask personal information where possible; read the provider's data-handling terms.
- **Transparency**: tell users when they interact with AI and when content is machine-generated; cite sources.
- **Human oversight**: keep a person in the loop for decisions that affect people's rights, health, money or safety; do not automate those decisions on model output alone.
- **Access control and least privilege** for tools and data.
- **Fairness checks**: test with varied inputs and groups; monitor for different error rates.
- **Security**: protect keys, validate inputs and outputs, limit actions.
- **Incident handling**: log, monitor, and have a way to correct or switch off a feature.
- **Respect licences and consent** for data and content, and follow applicable laws and your organisation's policies. This handbook does not give legal advice.

**4. Syntax**

```text
for example in test_set:
    output = system(example.input)
    record whether output meets example.expectation
report metrics; compare with the previous run
```

A pattern, implemented below.

**5. Example 1 — Basic**

*Toy demo.* Accuracy on a small labelled test set, using a deliberately simple keyword classifier as the "system":

```python
def classify(text):
    positive = {"great", "good", "love", "excellent"}
    negative = {"bad", "terrible", "hate", "poor"}
    words = set(text.lower().replace("!", "").replace(".", "").split())
    score = len(words & positive) - len(words & negative)
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"


test_set = [
    ("I love this product", "positive"),
    ("Terrible service.", "negative"),
    ("It arrived on Tuesday", "neutral"),
    ("Not good at all", "negative"),
    ("Excellent value!", "positive"),
]

correct = 0
for text, expected in test_set:
    got = classify(text)
    ok = got == expected
    correct += ok
    print(f"{'PASS' if ok else 'FAIL'}  expected={expected:<9} got={got:<9} | {text}")
print(f"accuracy: {correct}/{len(test_set)} = {correct / len(test_set):.0%}")
```

Output:

```text
PASS  expected=positive  got=positive  | I love this product
PASS  expected=negative  got=negative  | Terrible service.
PASS  expected=neutral   got=neutral   | It arrived on Tuesday
FAIL  expected=negative  got=positive  | Not good at all
PASS  expected=positive  got=positive  | Excellent value!
accuracy: 4/5 = 80%
```

Line by line: `classify` is a stand-in for any system; each test case has an expected label; the loop compares and counts. The failing case ("Not good at all") shows what a test set is for: it exposes a weakness (negation) that is easy to miss when you only try cases you expect to work.

**6. Example 2 — Practical**

*Toy demo.* Precision and recall for one class, and a regression check that compares two versions of a system on the same test set:

```python
def precision_recall(results, positive_label):
    tp = sum(1 for expected, got in results if got == positive_label and expected == positive_label)
    fp = sum(1 for expected, got in results if got == positive_label and expected != positive_label)
    fn = sum(1 for expected, got in results if got != positive_label and expected == positive_label)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return round(precision, 2), round(recall, 2)


expected = ["spam", "spam", "spam", "ham", "ham", "ham", "ham", "spam"]
version_a = ["spam", "ham", "ham", "ham", "ham", "ham", "ham", "spam"]    # cautious
version_b = ["spam", "spam", "spam", "spam", "spam", "ham", "ham", "spam"]  # eager

for name, predictions in [("A", version_a), ("B", version_b)]:
    results = list(zip(expected, predictions))
    accuracy = sum(e == g for e, g in results) / len(results)
    precision, recall = precision_recall(results, "spam")
    print(f"version {name}: accuracy {accuracy:.0%}, precision {precision}, recall {recall}")

previous_accuracy = 0.75
current_accuracy = sum(e == g for e, g in zip(expected, version_b)) / len(expected)
print("regression!" if current_accuracy < previous_accuracy else "no regression", f"({current_accuracy:.2f} vs {previous_accuracy:.2f})")
```

Output:

```text
version A: accuracy 75%, precision 1.0, recall 0.5
version B: accuracy 75%, precision 0.67, recall 1.0
no regression (0.75 vs 0.75)
```

Line by line:

- *Precision* is the share of items predicted `spam` that really are spam; *recall* is the share of real spam that was found. Version A is cautious (high precision, low recall) and B is eager (the reverse).
- Which is better depends on the cost of each error. Missing spam may be acceptable; blocking a real message may not be.
- The last lines compare against a stored previous score to flag a regression automatically.

**7. Example 3 — Edge case or common mistake**

Testing on the examples you tuned on gives an inflated score. Keep a held-out set:

```python
import random

examples = [f"case {i}" for i in range(20)]
rng = random.Random(0)
rng.shuffle(examples)
tuning, held_out = examples[:14], examples[14:]
print(len(tuning), "for tuning,", len(held_out), "held out")
print("overlap:", set(tuning) & set(held_out))
```

Output:

```text
14 for tuning, 6 held out
overlap: set()
```

Another trap is evaluating privacy last. A simple masking step removes obvious personal data before text leaves your system:

```python
import re


def mask_pii(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL]", text)
    text = re.sub(r"\b\d{10}\b", "[PHONE]", text)
    return text


print(mask_pii("Contact asha@example.com or 9876543210 about the order."))
print(mask_pii("Call me at 98765 43210"))
```

Output:

```text
Contact [EMAIL] or [PHONE] about the order.
Call me at 98765 43210
```

The first line is masked; the second is not, because the number is written with a space. Pattern-based masking is incomplete (it misses names, addresses and other formats), so treat it as one layer, minimise what you send, and use proper data-protection tools and policies for sensitive data.

Averages can hide unfairness. Check results by group:

```python
results = [("group A", True)] * 18 + [("group A", False)] * 2 + [("group B", True)] * 12 + [("group B", False)] * 8
overall = sum(ok for _, ok in results) / len(results)
print(f"overall accuracy: {overall:.0%}")
for group in ["group A", "group B"]:
    subset = [ok for g, ok in results if g == group]
    print(f"{group}: {sum(subset) / len(subset):.0%} ({len(subset)} cases)")
```

Output:

```text
overall accuracy: 75%
group A: 90% (20 cases)
group B: 60% (20 cases)
```

The invented numbers show an overall score of 75 percent that conceals a 90 versus 60 percent gap between groups, which an overall average would never reveal.

**8. Common mistakes**

- No test set, or evaluating only on cases used for tuning.
- Looking at accuracy only when error costs differ.
- Trusting a single run of a variable system.
- Using a model as judge without checking the judge.
- Ignoring subgroups, cost and latency.
- Treating pattern-based privacy masking as complete.
- Deploying without human oversight for high-stakes decisions.

**9. Real-world and AI applications**

Teams keep evaluation sets for each feature, run them automatically on every change, track groundedness for RAG answers, review samples by hand, and monitor production for drift. Responsible-use policies cover data handling, disclosure to users, human review and incident response.

**10. Practice**

1. Add three more test cases to Example 1, including one that uses negation, and report the new accuracy.
2. Fix `classify` so that "Not good at all" returns `negative`, for example by treating `not` as flipping the next word. Rerun the tests.
3. Compute precision and recall for the `ham` class in Example 2.
4. Write `check_regression(old, new, tolerance)` that returns `True` if the new score is not worse than the old by more than the tolerance.
5. Extend `mask_pii` to handle phone numbers written as `98765 43210`. What other formats would it still miss?
6. List five responsible-use practices you would apply to a document question-answering tool for a company.

**11. Interview questions**

- *How do you evaluate an LLM application?* With a fixed, held-out test set, metrics suited to the task (accuracy, precision and recall, groundedness, human review), repeated runs, and regression checks on every change.
- *What is the difference between precision and recall?* Precision is the share of predicted positives that are correct; recall is the share of actual positives that were found.
- *What are the main limitations of LLMs?* Hallucination, knowledge cutoff, bias, sensitivity to wording, reasoning errors, prompt injection and privacy risks.
- *What is responsible use?* Minimising data, being transparent, keeping human oversight for important decisions, protecting security, and checking fairness.

**12. Quick revision**

- Test set + metrics + held-out data + regression checks.
- Precision vs recall; look at subgroups.
- Limits: hallucination, cutoff, bias, injection, privacy.
- Responsible use: minimise data, disclose, oversight, least privilege.
- Re-evaluate after every change.

---

## Answers to Practice Exercises

### Answers: Recap: How It All Connects

1.

```python
connections = {"tokens": "strings", "retrieval": "dictionaries"}
connections["context assembly"] = "functions and slicing"
connections["agents"] = "loops and conditionals"
for concept in sorted(connections):
    print(concept, "<-", connections[concept])
```

Output:

```text
agents <- loops and conditionals
context assembly <- functions and slicing
retrieval <- dictionaries
tokens <- strings
```

2. Add a document and ask a question it answers; this checks the retrieval path:

```python
DOCS = ["Gift cards cannot be refunded.", "Opening hours are nine to five."]
question = "What are the opening hours?"
words = lambda t: set(t.lower().replace("?", "").replace(".", "").split())
best = max(DOCS, key=lambda d: len(words(d) & words(question)))
print(best)
```

Output:

```text
Opening hours are nine to five.
```

3. A smaller budget means fewer sources fit, so fewer documents are included (possibly none beyond the header and question). The prompt remains within budget but may lack the information needed.

```python
def estimate_tokens(text):
    return max(1, round(len(text) / 4))


for budget in (120, 30):
    used = estimate_tokens("Answer only from the sources.\n") + estimate_tokens("Question?")
    included = 0
    for line in ["[1] " + "Refunds are available within 30 days of purchase with a receipt.", "[2] Gift cards cannot be refunded."]:
        if used + estimate_tokens(line) <= budget:
            used += estimate_tokens(line)
            included += 1
    print(budget, included)
```

Output:

```text
120 2
30 1
```

4.

```python
def always_unknown(prompt):
    return "I do not know."


def grounded(answer, docs):
    return answer == "I do not know." or answer in docs


print(grounded(always_unknown("anything"), []))
```

Output:

```text
True
```

5. For example: `user question -> validate (Ch 4) -> retrieve passages (Ch 33, 37) -> build prompt under token budget (Ch 32, 34) -> call model with low temperature (Ch 31, 35) -> check grounding (Ch 31) -> answer with sources -> log (Ch 40)`.

6. For example: the question (or a hash if it is sensitive), which sources were retrieved, the prompt size in tokens, the model name and settings, latency, cost, and any error or check failure.

### Answers: Final Thoughts

1.

```python
plan = [
    {"task": "Finish Part 1 practice", "deadline": "2026-11-01", "done": True},
    {"task": "Build contact book project", "deadline": "2026-11-10", "done": False},
    {"task": "Learn files and exceptions", "deadline": "2026-11-20", "done": False},
    {"task": "Learn classes", "deadline": "2026-12-01", "done": False},
    {"task": "Call a real AI service", "deadline": "2026-12-15", "done": False},
]
for item in plan:
    if not item["done"]:
        print(item["deadline"], item["task"])
```

Output:

```text
2026-11-10 Build contact book project
2026-11-20 Learn files and exceptions
2026-12-01 Learn classes
2026-12-15 Call a real AI service
```

2.

```python
intervals = [1, 3, 7, 14, 30]


def next_interval(reviews_done, success):
    if not success:
        reviews_done = 0
    index = min(reviews_done, len(intervals) - 1)
    return reviews_done, intervals[index]


print(next_interval(3, True), next_interval(3, False))
```

Output:

```text
(3, 14) (0, 1)
```

3. For example, for the contact book: search by partial name, save and load from a file, and detect duplicate numbers.

4. Open exercise; a good test is whether the friend could do something new after your explanation.

5. For example: for protocols, the official specification site; for prices and limits, the provider's pricing and documentation pages; for Python itself, docs.python.org.

### Answers: Evaluation, Limitations, and Responsible Use

1.

```python
def classify(text):
    positive = {"great", "good", "love", "excellent"}
    negative = {"bad", "terrible", "hate", "poor"}
    words = set(text.lower().replace("!", "").replace(".", "").split())
    score = len(words & positive) - len(words & negative)
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"


tests = [
    ("I love this product", "positive"), ("Terrible service.", "negative"),
    ("It arrived on Tuesday", "neutral"), ("Not good at all", "negative"),
    ("Excellent value!", "positive"),
    ("Not bad", "positive"), ("Never good", "negative"), ("Great, but slow", "positive"),
]
correct = sum(classify(t) == e for t, e in tests)
print(f"{correct}/{len(tests)}")
```

Output:

```text
4/8
```

2.

```python
def classify(text):
    positive = {"great", "good", "love", "excellent"}
    negative = {"bad", "terrible", "hate", "poor"}
    words = text.lower().replace("!", "").replace(".", "").split()
    score = 0
    for i, word in enumerate(words):
        sign = 1 if word in positive else -1 if word in negative else 0
        if sign and i > 0 and words[i - 1] in {"not", "never"}:
            sign = -sign
        score += sign
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"


for text in ["Not good at all", "I love this product", "Not bad"]:
    print(text, "->", classify(text))
```

Output:

```text
Not good at all -> negative
I love this product -> positive
Not bad -> positive
```

3.

```python
expected = ["spam", "spam", "spam", "ham", "ham", "ham", "ham", "spam"]
version_a = ["spam", "ham", "ham", "ham", "ham", "ham", "ham", "spam"]
tp = sum(e == "ham" and g == "ham" for e, g in zip(expected, version_a))
fp = sum(e != "ham" and g == "ham" for e, g in zip(expected, version_a))
fn = sum(e == "ham" and g != "ham" for e, g in zip(expected, version_a))
print(round(tp / (tp + fp), 2), round(tp / (tp + fn), 2))
```

Output:

```text
0.67 1.0
```

4.

```python
def check_regression(old, new, tolerance=0.0):
    return new >= old - tolerance


print(check_regression(0.80, 0.78, 0.05), check_regression(0.80, 0.70, 0.05))
```

Output:

```text
True False
```

5.

```python
import re


def mask_pii(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL]", text)
    text = re.sub(r"\b\d{5}\s?\d{5}\b", "[PHONE]", text)
    return text


print(mask_pii("Call me at 98765 43210 or 9876543210"))
```

Output:

```text
Call me at [PHONE] or [PHONE]
```

It would still miss numbers with country codes or dashes, names, street addresses, ID numbers and anything written in words.

6. For example: send only the needed text and mask personal data; check the provider's data-handling terms; apply access control so users only retrieve documents they may see; tell users answers are AI-generated and cite sources; keep a human review path and log requests for audit.

---

## Chapter Summary and Key Takeaways

- A typical AI application is a Python pipeline: request, validation, context assembly under a token budget, retrieval, model call with settings, output checks, answer with sources and logging; the model is one component among several.
- Failures enter at the joints (context, retrieval, prompts, tools, unchecked output), and each has a Python-level control: validation, limits, logging and tests.
- Keep the model call behind a function so the rest of the system can be tested with fakes.
- The course gives you Python fundamentals and an AI mental model; the next steps are files, exceptions, classes, packages, data libraries, calling a real service, and finishing evaluated projects.
- Evaluate with a held-out test set, suitable metrics, subgroup checks and regression tests; practise responsible use through data minimisation, transparency, human oversight and security; verify fast-changing facts against official sources.

You have reached the end of the handbook. Return to the [README](../README.md) for the practice exercises, projects and revision checklist.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
