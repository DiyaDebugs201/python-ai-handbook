# Chapter 30 — Python Wrap-Up and Introduction to the AI Section

> Part 6 — Python Integration and AI Foundations · Video: 10:47:48–10:52:08 · Previous: [29 map(), filter() and reduce()](29-map-filter-reduce.md) · Next: [31 LLMs, Prompting, Temperature and Hallucination](31-llms-prompting-temperature-hallucination.md)

**In this chapter:** a look back at what the Python part has given you and how the pieces fit together, a map of the AI section that follows, how Python is actually used in AI development, and the practical skill you need before calling any AI service: keeping secrets such as API keys out of your code with environment variables and a `.env` file.

**Before you start:** this chapter assumes you have worked through Parts 1 to 5, mainly strings ([Chapter 06](06-strings-basics-indexing-concatenation.md)), dictionaries ([Dictionaries](23-dictionaries.md#dictionaries)), functions ([Chapter 25](25-defining-functions-and-return-values.md)) and modules ([Chapter 03](03-builtin-functions-print-and-modules.md)). Recap: a module is a file of Python code you can `import`; a dictionary maps keys to values; a function takes inputs and returns a result. Examples were run with Python 3.13 using only the standard library.

---

## Python Wrap-Up and AI Section Introduction

**Timestamp:** [10:47:48](https://www.youtube.com/watch?v=J9BI0jGOds8&t=38868s)

**Learning objectives:**

- Summarise which Python skills the rest of the handbook relies on.
- Describe what the AI section covers and in what order.
- Explain how the notes label toy code, pseudocode and code that needs an AI service.
- Run a self-check that the Python foundations are in place.

**1. Intuition**

Learning Python first and AI second is like learning to drive before learning how a delivery company plans its routes. The first part gave you the vehicle: variables, decisions, loops, containers and functions. The second part is about a specific kind of cargo: language models, and the systems that are built around them. You will not need new Python syntax to follow it, but you will constantly *use* what you have learned.

**2. Why does it exist?**

AI systems look mysterious until you see that most of the code around a model is ordinary Python: building text, sending it somewhere, reading a dictionary that comes back, looping over results, and handling errors. A short wrap-up makes this link explicit before the vocabulary of AI begins, so that a "prompt" is seen as a string, a "response" as a dictionary, and an "agent" as a loop.

**3. Technical explanation**

*What Python gave you, and where it appears in the AI section:*

| Python skill | Where it comes back |
|---|---|
| Strings, f-strings, methods | Building prompts, cleaning and splitting text |
| Lists, tuples, sets | Batches of messages, documents, vocabularies |
| Dictionaries | Chat messages, API requests and responses, configuration |
| Loops and conditions | Processing many documents, agent loops, retries |
| Functions, arguments, `**kwargs` | Wrappers around model calls, tool functions |
| Comprehensions, `map`, `filter` | Cleaning datasets, scoring, selecting results |
| Modules and `import` | Using libraries; the standard library for the toy demos |
| Errors and debugging | Handling failed requests and bad data |

*The AI section, chapter by chapter:*

1. [Chapter 31](31-llms-prompting-temperature-hallucination.md): what a large language model is, prompting, the temperature setting, and hallucination.
2. [Chapter 32](32-context-engineering-and-tokens.md): context engineering, tokens and token costs.
3. [Chapter 33](33-vectors-and-embeddings.md): vectors and embeddings.
4. [Chapter 34](34-context-window-and-model-parameters.md): the context window and model parameters.
5. [Chapter 35](35-attention-and-transformers.md): the attention mechanism and transformers.
6. [Chapter 36](36-pretraining-fine-tuning-rlhf.md): pretraining, fine-tuning and RLHF.
7. [Chapter 37](37-retrieval-augmented-generation.md): retrieval-augmented generation.
8. [Chapter 38](38-mcp-and-ai-agents.md): the Model Context Protocol and AI agents.
9. [Chapter 39](39-multimodal-reasoning-slm-agi-asi.md): multimodal models, reasoning models, small language models, AGI and ASI.
10. [Chapter 40](40-recap-and-final-thoughts.md): recap, evaluation, limitations and responsible use.

*How the AI chapters are written.* Each AI topic separates three layers and keeps them apart:

- **Intuition**: an everyday picture of the idea, clearly marked as an analogy.
- **Mechanism**: what actually happens, described accurately but at a level suitable for a beginner.
- **Code**: small demonstrations in Python. Each one is labelled:
  - *Toy demo*: runs with the standard library only, and illustrates an idea with simplified numbers. It is *not* how a real model works.
  - *Pseudocode*: shows the shape of an operation and is not runnable.
  - *Requires an AI service*: real code that calls an online model; it needs an account and an API key, so it is shown but not run here. Output shown for these is clearly described as illustrative.

*Claims that can go out of date* (names of models, prices, limits, protocol versions) are kept to a minimum, are described in general terms, and are noted as "check the official documentation". Where a specific fact about a standard is stated (the Model Context Protocol, for example), it has been checked against the official documentation, and the page to re-check is given.

**4. Syntax**

```text
There is no new syntax in this chapter.
The labels used in the AI chapters are:
  Toy demo ................ runs here, standard library only, simplified
  Pseudocode .............. not runnable, shows the shape
  Requires an AI service .. needs an account and API key, not run here
```

This is a description of the notes' conventions, not code.

**5. Example 1 — Basic**

A short self-check that uses many Python ideas together. If you can read every line, you are ready:

```python
messages = [
    {"role": "user", "content": "  What is a list?  "},
    {"role": "assistant", "content": "An ordered, changeable collection."},
    {"role": "user", "content": "And a tuple?"},
]

def clean(text):
    return text.strip()

user_questions = [clean(m["content"]) for m in messages if m["role"] == "user"]
print(user_questions)

counts = {}
for message in messages:
    counts[message["role"]] = counts.get(message["role"], 0) + 1
print(counts)

total_words = sum(len(m["content"].split()) for m in messages)
print("total words:", total_words)
```

Output:

```text
['What is a list?', 'And a tuple?']
{'user': 2, 'assistant': 1}
total words: 11
```

Line by line:

- `messages` is a list of dictionaries: the usual shape of a conversation.
- The comprehension keeps only the user turns and cleans each one with a function.
- The loop counts messages per role, with `get` supplying a default of 0.
- `sum` with a generator expression counts all the words.

**6. Example 2 — Practical**

A complete mini program in the style used later in the handbook: small functions, one `main`, a clear flow. It builds a "prompt" (a string) and fakes the model with a stand-in function. *Toy demo: no AI is involved.*

```python
def build_prompt(question, notes):
    lines = ["Answer using only the notes below.", "", "Notes:"]
    for number, note in enumerate(notes, start=1):
        lines.append(f"{number}. {note}")
    lines += ["", f"Question: {question}"]
    return "\n".join(lines)


def fake_model(prompt):
    """A stand-in for a real model: it only reports how long the prompt is."""
    return f"[pretend answer; the prompt had {len(prompt.split())} words]"


def main():
    notes = ["Lists keep order.", "Sets keep unique items."]
    prompt = build_prompt("Which type keeps unique items?", notes)
    print(prompt)
    print("---")
    print(fake_model(prompt))


if __name__ == "__main__":
    main()
```

Output:

```text
Answer using only the notes below.

Notes:
1. Lists keep order.
2. Sets keep unique items.

Question: Which type keeps unique items?
---
[pretend answer; the prompt had 22 words]
```

Line by line:

- `build_prompt` is string work: a list of lines, `enumerate`, an f-string and `join`.
- `fake_model` takes the place of a real model call, so the program runs anywhere. In real code this one function would send the text to a service and return its reply.
- `main()` and the `__main__` guard are the pattern from [Functions: Core Concepts](25-defining-functions-and-return-values.md#functions-core-concepts).

**7. Example 3 — Edge case or common mistake**

A common wrap-up mistake is reading AI chapters as if they needed new Python. They do not, but they do need care with text and data. Typical problems are shown with ordinary Python:

```python
reply = {"choices": [{"text": "hello"}]}

print(reply["choices"][0]["text"])
for action in [lambda: reply["answer"], lambda: reply["choices"][1], lambda: reply["choices"][0]["text"] + 5]:
    try:
        action()
    except Exception as error:
        print(type(error).__name__ + ":", error)

print(reply.get("answer", "no answer key"))
```

Output:

```text
hello
KeyError: 'answer'
IndexError: list index out of range
TypeError: can only concatenate str (not "int") to str
no answer key
```

A response with a different shape from the one you expected gives `KeyError`, `IndexError` or `TypeError`. When working with services, read the real response structure first, and use `get` and checks for missing parts.

**8. Common mistakes**

- Skipping the Python foundations and then being unable to read AI code.
- Treating the toy demos as descriptions of how real models work.
- Assuming a service's response always has the shape you expect.
- Memorising model names and numbers that change, instead of learning the ideas.
- Trying to run code labelled "requires an AI service" without an account and key.

**9. Real-world and AI applications**

A real AI application is a Python program that (1) prepares text, (2) calls a model or a retrieval system, (3) checks and uses the result, and (4) handles failures. Each of these steps is something you have practised. The rest of this handbook gives names to the ideas behind step 2.

**10. Practice**

1. In your own words, list five Python features from Parts 1 to 5 that an AI application would use, and say what each would be used for.
2. Change `build_prompt` so that it adds a line `"Be brief."` before the question.
3. Write `count_roles(messages)` that returns a dictionary of role counts (use `collections.Counter` or a loop).
4. Write a function `last_user_message(messages)` that returns the content of the last message with role `"user"`, or `None`.
5. For the response in Example 3, write a function `safe_text(reply)` that returns the first choice's text, or an empty string when any part is missing.

**11. Interview questions**

- *Why learn Python before AI concepts?* Nearly all AI tooling and application code is written in Python, and the ideas (strings, dictionaries, loops, functions) are the everyday material of that code.
- *What does a typical AI application do in Python?* Prepare input text, call a model or service, check and use the result, and handle errors.
- *What is a toy demo?* A simplified program that illustrates an idea but is not how the real system works.

**12. Quick revision**

- The AI section needs no new syntax; it reuses strings, dictionaries, loops, functions and modules.
- Chapters 31 to 40 go from LLM basics to agents and responsible use.
- Code is labelled: toy demo, pseudocode, or requires an AI service.
- Facts that change quickly are kept general and should be re-checked in official documentation.

---

## How Python Is Used in AI Development

This section is supplementary: the video topic list does not name it, but it explains why the course teaches Python before AI and which tools you will meet next.

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Python Wrap-Up and AI Section Introduction](30-python-wrap-up-and-ai-intro.md#python-wrap-up-and-ai-section-introduction)).

**Learning objectives:**

- Name the main roles Python plays in AI work: glue code, data handling, model use and model building.
- Recognise the standard library families of tools without needing to install them.
- Distinguish *using* a hosted model from *building* a model.

**1. Intuition**

Python is the kitchen counter where AI ingredients are prepared and combined. The heavy cooking (the model's own calculations) happens in fast machinery written in other languages, but you stand at the counter in Python, deciding what goes in, in what order, and what to do with what comes out.

**2. Why does it exist?**

Python became the usual language for AI because it is quick to write and read, has a huge ecosystem of libraries, and can call fast code written in other languages underneath. Researchers can try an idea in a few lines, and engineers can reuse the same language to put it into a product.

**3. Technical explanation**

*Roles of Python in AI development:*

1. **Glue**: connecting services. Calling a web API, reading files, moving data from one format to another.
2. **Data handling**: loading, cleaning, transforming and splitting data, with tools such as the built-in containers, the `csv` and `json` modules, and (third-party) libraries such as NumPy and pandas for tables and arrays.
3. **Using models**: sending prompts to a hosted language model through the provider's Python library or plain HTTP, and processing the result.
4. **Building and training models**: libraries such as scikit-learn, PyTorch and TensorFlow provide the mathematical building blocks and training loops. The heavy numerical work runs in optimised code, not in plain Python loops.
5. **Applications**: web services, command-line tools and notebooks that wrap the above for users.

*Using versus building.* Most application developers *use* models that someone else trained, through an API or a downloaded model. Training a large model from scratch needs data, hardware and expertise far beyond a beginner project. The skills in this handbook serve both, but the first four chapters of the AI section and the later chapters on retrieval and agents are about *using* models well.

*Standard library and third-party packages.* The Python installation ships with a *standard library* (`json`, `os`, `re`, `math`, `collections`, `urllib`, `statistics` and more) that needs no installation. Third-party packages are installed with `pip` (see [Installation and Environment Setup](02-installation-and-environment-setup.md)). To keep every demo in this handbook runnable by anyone, the demos use only the standard library; real projects would use the packages named above, and where a package would be natural, the chapter says so without running it.

*Notebooks and scripts.* AI work is often done in notebooks (documents that mix code, output and text) for exploration, and in scripts and services for production. Both run the same Python.

*Speed.* Plain Python loops are slow for large numeric work, which is why array libraries exist: they apply an operation to a whole array at once in compiled code. You will see the same idea in [Vectors and Embeddings](33-vectors-and-embeddings.md).

**4. Syntax**

```text
import json                # standard library: always available
import os                  # standard library
# pip install requests     # third-party: install first (shown, not run here)
```

The `pip` line is a shell command shown as a comment, not run here.

**5. Example 1 — Basic**

```python
import json

response_text = '{"model": "example-model", "choices": [{"text": "Hello!"}], "usage": {"total_tokens": 12}}'
data = json.loads(response_text)
print(type(data).__name__)
print(data["choices"][0]["text"])
print(data["usage"]["total_tokens"])

request = {"model": "example-model", "messages": [{"role": "user", "content": "Hi"}]}
print(json.dumps(request))
print(json.dumps(request, indent=2))
```

Output:

```text
dict
Hello!
12
{"model": "example-model", "messages": [{"role": "user", "content": "Hi"}]}
{
  "model": "example-model",
  "messages": [
    {
      "role": "user",
      "content": "Hi"
    }
  ]
}
```

Line by line: a model service typically speaks JSON, a text format for dictionaries and lists. `json.loads` turns JSON text into Python dictionaries and lists; `json.dumps` turns Python data into JSON text. The model name and the response are invented for the demonstration: this is a *toy demo* showing the data shapes, not a real call.

**6. Example 2 — Practical**

A tiny data-preparation pipeline using only the standard library, in the shape of real AI data work: load records, clean, deduplicate, split into train and test sets. *Toy demo.*

```python
import csv
import io
import random

raw_csv = """text,label
 Great product ,positive
terrible service,negative
great product,positive
,negative
Okay I guess,neutral
Loved it,positive
"""

rows = list(csv.DictReader(io.StringIO(raw_csv)))
print(len(rows), "rows read")

cleaned = []
seen = set()
for row in rows:
    text = row["text"].strip().lower()
    if not text:
        continue
    if text in seen:
        continue
    seen.add(text)
    cleaned.append({"text": text, "label": row["label"]})
print(len(cleaned), "rows after cleaning")
for row in cleaned:
    print(row)

random.seed(0)
shuffled = cleaned[:]
random.shuffle(shuffled)
split = int(len(shuffled) * 0.8)
train, test = shuffled[:split], shuffled[split:]
print(len(train), "train,", len(test), "test")
print(sorted(row["label"] for row in cleaned))
```

Output:

```text
6 rows read
4 rows after cleaning
{'text': 'great product', 'label': 'positive'}
{'text': 'terrible service', 'label': 'negative'}
{'text': 'okay i guess', 'label': 'neutral'}
{'text': 'loved it', 'label': 'positive'}
3 train, 1 test
['negative', 'neutral', 'positive', 'positive']
```

Line by line:

- `csv.DictReader` turns each row into a dictionary; `io.StringIO` lets us read from a string as if it were a file.
- The loop cleans the text, skips empty rows with `continue`, and skips duplicates with a set. Note that `" Great product "` and `"great product"` become the same text after cleaning, so the second is dropped.
- The data is shuffled with a fixed seed (so that the run is repeatable) and split 80/20 into training and test sets, which is the standard way to check a model on data it has not seen.

**7. Example 3 — Edge case or common mistake**

Plain Python is not the tool for heavy numeric work, and a third-party package may not be installed:

```python
import time

n = 300000
values = list(range(n))

start = time.perf_counter()
total = 0
for v in values:
    total += v * v
loop_time = time.perf_counter() - start

start = time.perf_counter()
total2 = sum(v * v for v in values)
builtin_time = time.perf_counter() - start

print(total == total2)
print("loop and built-in both finished:", loop_time > 0 and builtin_time > 0)

try:
    import numpy
    print("numpy is installed, version available:", bool(numpy.__version__))
except ImportError as error:
    print("ImportError:", error)
```

Output:

```text
True
loop and built-in both finished: True
numpy is installed, version available: True
```

Both ways give the same sum; timings vary by machine and are not printed. The last line depends on your machine: NumPy was installed in the environment used to run these examples, so you may see an `ImportError` message instead. The important lessons: (1) numeric libraries exist because pure-Python loops over millions of numbers are slow compared with compiled array code, and (2) a package such as NumPy is *third-party*. If it is not installed, `import` fails with `ModuleNotFoundError` (a subtype of `ImportError`). Install it with `pip` in a virtual environment first.

**8. Common mistakes**

- Installing packages globally instead of in a virtual environment (see [Installation and Environment Setup](02-installation-and-environment-setup.md)).
- Using pure Python loops on huge numeric data when an array library would be far faster.
- Assuming that "uses Python" means the model itself is written in Python.
- Importing a package that is not installed in the environment you are running.
- Confusing using a hosted model with training one.

**9. Real-world and AI applications**

Typical Python jobs in an AI team: cleaning and labelling data, writing evaluation scripts that run a model on many test questions and score the answers, building a retrieval index over company documents, writing a service that calls a model and returns a formatted answer, and automating repeated tasks. For all of these, correct and readable Python matters more than any particular library.

**10. Practice**

1. Parse the JSON text `'{"name": "Asha", "skills": ["python", "sql"]}'` and print the second skill.
2. Convert the dictionary `{"a": 1, "b": [1, 2]}` to JSON text with `json.dumps`.
3. Extend Example 2 so that it also reports how many rows were dropped and why (empty or duplicate).
4. Write a function `train_test_split(items, test_fraction, seed)` returning two lists.
5. Explain in two sentences the difference between *using* a hosted language model and *training* one.

**11. Interview questions**

- *Why is Python so common in AI?* Readable, a large ecosystem, easy glue to fast compiled libraries.
- *What is the standard library?* The modules that come with Python and need no installation.
- *Why do array libraries exist if Python has lists?* They run numeric operations in compiled code over whole arrays, which is much faster than Python loops.
- *Why split data into training and test sets?* To measure how a model does on data it was not trained on.

**12. Quick revision**

- Python in AI: glue, data handling, using models, building models, applications.
- JSON ⇄ Python: `json.loads` and `json.dumps`.
- Use the standard library when possible; install third-party packages in a virtual environment.
- Heavy numeric work uses array libraries, not plain loops.
- Use a hosted model versus train a model are different jobs.

---

## Environment Variables, .env Files, and API Keys

This section is supplementary: the video topic list does not name it, but you cannot safely call an AI service without it.

**Timestamp:** supplementary section (not a separate video topic; it belongs with [Python Wrap-Up and AI Section Introduction](30-python-wrap-up-and-ai-intro.md#python-wrap-up-and-ai-section-introduction)).

**Learning objectives:**

- Explain what an API key is and why it must never be written into source code or committed to Git.
- Read environment variables with `os.environ` and `os.getenv`.
- Use a `.env` file and a `.env.example` template, and keep `.env` out of version control.
- Handle a missing key with a clear error, and know what to do if a key leaks.

**1. Intuition**

An API key is like the key card to a company's building that also bills the company each time you swipe it. You would not tape a copy to the front door (your public code). You keep it in your pocket (an environment variable or an untracked `.env` file), and the program reads it only when it needs to open the door.

**2. Why does it exist?**

Most AI services charge per use and identify you by an API key. Anyone who has the key can spend your money and act as you. If the key is typed into a script and the script is pushed to a public GitHub repository, automated scanners can find it within minutes. Environment variables let the *same code* run on your laptop, a test server and production with different secrets, and keep the secrets out of the code itself.

**3. Technical explanation**

- An *environment variable* is a named value that the operating system passes to every program it starts. Python reads them through `os.environ` (a dictionary-like object) or `os.getenv(name, default)`.
- `os.environ["NAME"]` raises `KeyError` if the variable is missing; `os.getenv("NAME")` returns `None` (or a default you give).
- Environment variables are always *strings*. Convert numbers and booleans yourself (`int(os.getenv("RETRIES", "3"))`).
- A *`.env` file* is a plain text file with lines `NAME=value`, kept in the project folder and **never committed**. A helper loads it into the environment when the program starts. The commonly used third-party package is `python-dotenv` (`load_dotenv()`); this handbook also shows a tiny standard-library loader so that the demo runs anywhere.
- A *`.env.example`* file is committed to the repository. It lists the *names* of the variables the project needs, with fake placeholder values and comments, so others know what to create. It must never contain a real secret.
- `.gitignore` must list `.env`, so Git never tracks it. (This handbook's `.gitignore` already does.) Adding a file to `.gitignore` after it was committed does not remove it from history.
- Good habits:
  1. Never put a key in source code, notebooks, screenshots, chat messages or error logs.
  2. Never print a key. If you must show it, show only the last few characters.
  3. Use one key per project, with the lowest permissions and a spending limit if the provider offers one.
  4. Check for the key at program start and fail with a helpful message.
  5. If a key leaks, **revoke it immediately** in the provider's dashboard and create a new one. Deleting the file or the commit is not enough, because the old value may already be copied.
- Names such as `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` or `MY_SERVICE_API_KEY` are conventions used by different providers' libraries. Check your provider's documentation for the exact name its library reads.
- In production, secrets usually come from a secrets manager or the hosting platform's settings, not a file, but the program reads them in the same way: from the environment.

**4. Syntax**

```text
import os
key = os.environ["MY_SERVICE_API_KEY"]        # KeyError if missing
key = os.getenv("MY_SERVICE_API_KEY")         # None if missing
timeout = int(os.getenv("TIMEOUT_SECONDS", "30"))

# .env  (never committed)
MY_SERVICE_API_KEY=real-secret-value

# .env.example  (committed)
MY_SERVICE_API_KEY=your-key-here
```

The `.env` lines are file contents, not Python.

**5. Example 1 — Basic**

```python
import os

os.environ["DEMO_NAME"] = "Asha"
print(os.environ["DEMO_NAME"])
print(os.getenv("DEMO_NAME"))
print(os.getenv("DEMO_MISSING"))
print(os.getenv("DEMO_MISSING", "fallback"))

os.environ["DEMO_RETRIES"] = "5"
retries = int(os.getenv("DEMO_RETRIES", "3"))
print(retries + 1, type(os.getenv("DEMO_RETRIES")).__name__)

print("DEMO_NAME" in os.environ, "DEMO_MISSING" in os.environ)
```

Output:

```text
Asha
Asha
None
fallback
6 str
True False
```

Line by line: setting `os.environ["DEMO_NAME"]` inside a program changes the environment only for that program (and the programs it starts). `os.getenv` returns `None` or your default for a missing name. Values are strings, so `"5"` has to be converted with `int`. (The names here are demo names, not real secrets.)

**6. Example 2 — Practical**

A small standard-library `.env` loader, applied to a temporary file with a fake key, followed by a safe way to read and display the key. *Toy demo: the key below is fake.*

```python
import os
import tempfile
from pathlib import Path


def load_env_file(path):
    """Read NAME=value lines into os.environ without overriding existing values."""
    loaded = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        if name not in os.environ:
            os.environ[name] = value
            loaded.append(name)
    return loaded


def mask(secret):
    if len(secret) <= 4:
        return "*" * len(secret)
    return "*" * (len(secret) - 4) + secret[-4:]


def get_api_key(name="DEMO_SERVICE_API_KEY"):
    key = os.getenv(name)
    if not key or key == "your-key-here":
        raise RuntimeError(f"Set {name} in your environment or in a .env file (see .env.example).")
    return key


with tempfile.TemporaryDirectory() as folder:
    env_path = Path(folder) / ".env"
    env_path.write_text(
        "# demo file with a FAKE key\n"
        "DEMO_SERVICE_API_KEY=fake-key-1234567890\n"
        'DEMO_MODEL_NAME="small-model"\n'
        "\n"
        "NOT A VALID LINE\n"
    )
    print("loaded:", load_env_file(env_path))

key = get_api_key()
print("key (masked):", mask(key))
print("model:", os.environ["DEMO_MODEL_NAME"])
print("masked short value:", mask("abc"))

try:
    get_api_key("DEMO_UNSET_KEY")
except RuntimeError as error:
    print("RuntimeError:", error)
```

Output:

```text
loaded: ['DEMO_SERVICE_API_KEY', 'DEMO_MODEL_NAME']
key (masked): ***************7890
model: small-model
masked short value: ***
RuntimeError: Set DEMO_UNSET_KEY in your environment or in a .env file (see .env.example).
```

Line by line:

- `load_env_file` skips blank lines, comments and lines without `=`; splits on the *first* `=` (so values may contain `=`); removes surrounding quotes; and does not override a variable that is already set in the environment (real environment settings win over the file).
- The demo writes a temporary `.env` file with a *fake* key so that no real secret is involved, loads it, and then the file is deleted along with the temporary folder.
- `mask` shows only the last four characters, which is how keys are shown in logs and dashboards.
- `get_api_key` fails early with a message that tells the user what to do, and treats the placeholder from `.env.example` as "not set".

In a real project the `.env` file sits in the project folder and the loader is `load_dotenv()` from the third-party `python-dotenv` package (installed with `pip install python-dotenv`; *not run here*):

```text
from dotenv import load_dotenv
load_dotenv()                       # reads .env in the current folder
key = os.environ["MY_SERVICE_API_KEY"]
```

This is pseudocode for a third-party package, shown without running.

**7. Example 3 — Edge case or common mistake**

```python
import os

try:
    key = os.environ["DEMO_SERVICE_KEY_THAT_IS_NOT_SET"]
except KeyError as error:
    print("KeyError:", error)

os.environ["DEMO_FLAG"] = "False"
print(bool(os.environ["DEMO_FLAG"]))
print(os.environ["DEMO_FLAG"].lower() == "true")

os.environ["DEMO_COUNT"] = "ten"
try:
    int(os.environ["DEMO_COUNT"])
except ValueError as error:
    print("ValueError:", error)

try:
    os.environ["DEMO_NUMBER"] = 5
except TypeError as error:
    print("TypeError:", error)
```

Output:

```text
KeyError: 'DEMO_SERVICE_KEY_THAT_IS_NOT_SET'
True
False
ValueError: invalid literal for int() with base 10: 'ten'
TypeError: str expected, not int
```

Reading a missing variable with `[]` raises `KeyError`. The string `"False"` is truthy (any non-empty string is), so test text such as `value.lower() == "true"`. A value that is not a number must be handled when converting. Environment values must be strings; assigning a number raises `TypeError`.

The most dangerous mistake is hard-coding a key. The code below is shown as text so that it is never run or copied (the value is an obvious fake):

```text
API_KEY = "sk-this-is-a-fake-example-key"      # WRONG: secret inside the source code
client = SomeClient(api_key=API_KEY)
```

And the right pattern, which reads the key from the environment at run time:

```python
import os


def make_client_settings():
    key = os.getenv("DEMO_SERVICE_API_KEY2")
    if key is None:
        return {"ready": False, "reason": "no key set"}
    return {"ready": True, "key_ending": key[-4:]}


print(make_client_settings())
os.environ["DEMO_SERVICE_API_KEY2"] = "fake-abcd1234"
print(make_client_settings())
```

Output:

```text
{'ready': False, 'reason': 'no key set'}
{'ready': True, 'key_ending': '1234'}
```

If a key is ever committed or pasted publicly: (1) revoke it at once in the provider's dashboard, (2) create a new key, (3) remove it from the code, and only then (4) clean up history. Removing the commit alone does not make an exposed key safe.

**8. Common mistakes**

- Typing an API key directly into a script, notebook or prompt that is saved or shared.
- Committing `.env` (check that `.gitignore` lists it *before* the first commit).
- Putting a real key into `.env.example`.
- Printing the key in logs or error messages.
- Forgetting that environment values are strings (`"False"` is truthy).
- Setting a variable in one terminal and running the program from another, so it is not found.
- Assuming that deleting a leaked key's commit makes it safe.
- Sharing one key between many projects and people.

**9. Real-world and AI applications**

Every call to a hosted model needs a key, so this pattern appears at the top of almost every AI script and service: load settings, check the key, create the client. Teams keep a committed `.env.example`, ignore the real `.env`, and use the host's secret settings in production. Leaked keys on public repositories are a well-known cause of unexpected bills, which is why providers scan for them and why revoking is the first response.

**10. Practice**

1. Read an environment variable `DEMO_USER` with a default of `"guest"`, and print it. Then set it in the program and print again.
2. Write `get_int_setting(name, default)` that returns an integer from the environment, or the default when the variable is missing or not a number.
3. Write `.env.example` content for a project that needs a key, a model name and a timeout (use placeholders only).
4. Extend `load_env_file` so that it ignores lines with an empty name.
5. Explain why `.env` must be in `.gitignore` before the first commit, and what to do if it was committed by mistake.
6. Why is `bool("False")` a bad way to read a boolean setting? Write a safe `get_bool_setting`.

**11. Interview questions**

- *What is an environment variable?* A named string value provided by the operating system to a program.
- *Why not hard-code API keys?* They would be exposed to anyone who can read the code, including in version control, and could not be changed without editing code.
- *What is the purpose of `.env.example`?* To document which variables are needed, with placeholder values, without exposing real secrets.
- *What do you do when a key leaks?* Revoke it immediately, create a new one, and then remove it from the code and history.
- *`os.environ["X"]` versus `os.getenv("X")`?* The first raises `KeyError` if missing; the second returns `None` or a default.

**12. Quick revision**

- Keys live in environment variables, loaded from an untracked `.env` file locally.
- `os.environ["X"]` (error if missing), `os.getenv("X", default)`; values are strings.
- Commit `.env.example` with placeholders; ignore `.env`.
- Never print or share a key; mask it if shown.
- A leaked key must be revoked, not just deleted.

---

## Answers to Practice Exercises

### Answers: Python Wrap-Up and AI Section Introduction

1. For example: strings (building prompts and cleaning text); dictionaries (chat messages and API responses); loops (processing many documents or running an agent); functions (wrapping a model call and writing tools); error handling with `try`/`except` (retrying failed requests); comprehensions (cleaning datasets).

2.

```python
def build_prompt(question, notes):
    lines = ["Answer using only the notes below.", "", "Notes:"]
    for number, note in enumerate(notes, start=1):
        lines.append(f"{number}. {note}")
    lines += ["", "Be brief.", f"Question: {question}"]
    return "\n".join(lines)


print(build_prompt("What is a set?", ["Sets keep unique items."]))
```

Output:

```text
Answer using only the notes below.

Notes:
1. Sets keep unique items.

Be brief.
Question: What is a set?
```

3.

```python
from collections import Counter


def count_roles(messages):
    return dict(Counter(message["role"] for message in messages))


chat = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}, {"role": "user", "content": "c"}]
print(count_roles(chat))
```

Output:

```text
{'user': 2, 'assistant': 1}
```

4.

```python
def last_user_message(messages):
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]
    return None


chat = [{"role": "user", "content": "first"}, {"role": "assistant", "content": "reply"}, {"role": "user", "content": "second"}]
print(last_user_message(chat), last_user_message([]))
```

Output:

```text
second None
```

5.

```python
def safe_text(reply):
    choices = reply.get("choices") or []
    if not choices:
        return ""
    return str(choices[0].get("text", ""))


print(repr(safe_text({"choices": [{"text": "hello"}]})))
print(repr(safe_text({})), repr(safe_text({"choices": []})), repr(safe_text({"choices": [{}]})))
```

Output:

```text
'hello'
'' '' ''
```

### Answers: How Python Is Used in AI Development

1.

```python
import json

data = json.loads('{"name": "Asha", "skills": ["python", "sql"]}')
print(data["skills"][1])
```

Output:

```text
sql
```

2.

```python
import json

print(json.dumps({"a": 1, "b": [1, 2]}))
```

Output:

```text
{"a": 1, "b": [1, 2]}
```

3.

```python
import csv
import io

raw_csv = "text,label\n Great product ,positive\ngreat product,positive\n,negative\nOkay,neutral\n"
seen = set()
kept = 0
empty = 0
duplicates = 0
for row in csv.DictReader(io.StringIO(raw_csv)):
    text = row["text"].strip().lower()
    if not text:
        empty += 1
    elif text in seen:
        duplicates += 1
    else:
        seen.add(text)
        kept += 1
print("kept", kept, "| empty", empty, "| duplicates", duplicates)
```

Output:

```text
kept 2 | empty 1 | duplicates 1
```

4.

```python
import random


def train_test_split(items, test_fraction, seed):
    shuffled = list(items)
    random.Random(seed).shuffle(shuffled)
    cut = int(len(shuffled) * (1 - test_fraction))
    return shuffled[:cut], shuffled[cut:]


train, test = train_test_split(range(10), 0.2, seed=1)
print(len(train), len(test), sorted(train + test) == list(range(10)))
```

Output:

```text
8 2 True
```

The original list is not changed (a copy is shuffled), and a seed makes the split repeatable.

5. *Using* a hosted model means sending inputs to a model that someone else has already trained and receiving its outputs, which needs only an account and a few lines of code. *Training* a model means adjusting its internal numbers using large amounts of data and computing power, which is a far larger and more specialised task.

### Answers: Environment Variables, .env Files, and API Keys

1.

```python
import os

print(os.getenv("DEMO_USER", "guest"))
os.environ["DEMO_USER"] = "Asha"
print(os.getenv("DEMO_USER", "guest"))
```

Output:

```text
guest
Asha
```

2.

```python
import os


def get_int_setting(name, default):
    try:
        return int(os.environ[name])
    except (KeyError, ValueError):
        return default


os.environ["DEMO_A"] = "7"
os.environ["DEMO_B"] = "seven"
print(get_int_setting("DEMO_A", 3), get_int_setting("DEMO_B", 3), get_int_setting("DEMO_C", 3))
```

Output:

```text
7 3 3
```

3. Content of a `.env.example` file (placeholders only; the real file is called `.env`, is never committed, and holds the real values):

```text
# Copy this file to .env and fill in real values. Never commit .env.
MY_SERVICE_API_KEY=your-key-here
MODEL_NAME=your-model-name
TIMEOUT_SECONDS=30
```

4.

```python
import os


def load_lines(lines):
    loaded = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if not name:
            continue
        os.environ.setdefault(name, value.strip())
        loaded.append(name)
    return loaded


print(load_lines(["A_KEY=1", "=orphan", "# comment", "B_KEY = two"]))
print(os.environ["B_KEY"])
```

Output:

```text
['A_KEY', 'B_KEY']
two
```

5. Git remembers every file it has ever tracked. If `.env` is committed once, its contents remain in the repository history even after the file is deleted or ignored later, and anyone with access to the repository (or a public copy) can read the old values. So `.env` must be in `.gitignore` before the first commit. If it was committed by mistake, treat every key in it as leaked: revoke and replace the keys first, then remove the file from the tracked files and, if the repository was ever shared, clean the history.

6. Any non-empty string is truthy, so `bool("False")` is `True`. Compare the text instead:

```python
import os


def get_bool_setting(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


os.environ["DEMO_DEBUG"] = "False"
print(bool(os.environ["DEMO_DEBUG"]), get_bool_setting("DEMO_DEBUG"), get_bool_setting("DEMO_MISSING_FLAG", True))
```

Output:

```text
True False True
```

---

## Chapter Summary and Key Takeaways

- The AI section reuses the Python you already know: strings for prompts, dictionaries for messages and responses, loops for processing and agents, functions for wrappers and tools.
- In this handbook, AI code is labelled as a toy demo (standard library only, simplified), pseudocode (not runnable), or requires an AI service (needs an account and key, not run here); facts that change quickly are kept general and should be checked in official documentation.
- Python is used in AI development for glue code, data handling, using hosted models and building models; heavy numeric work runs in compiled array libraries, and `json` is the usual format for exchanging data with services.
- API keys belong in environment variables, loaded from an untracked `.env` file; commit a `.env.example` with placeholders, keep `.env` in `.gitignore`, never print or share a key, and revoke any key that leaks.
- Environment values are always strings, so convert numbers and booleans explicitly, and check for required settings at program start with a clear error message.

Next: [Chapter 31 — LLMs, Prompting, Temperature and Hallucination](31-llms-prompting-temperature-hallucination.md) begins the AI concepts.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
