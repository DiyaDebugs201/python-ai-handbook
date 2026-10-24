# Chapter 32 — Context Engineering and Tokens

> Part 6 — Python Integration and AI Foundations · Video: 11:12:19–11:26:22 · Previous: [31 LLMs, Prompting, Temperature and Hallucination](31-llms-prompting-temperature-hallucination.md) · Next: [33 Vectors and Embeddings](33-vectors-and-embeddings.md)

**In this chapter:** what *context engineering* means (deciding everything that goes into the model's input, beyond a single prompt), and what *tokens* are: the pieces a model reads and writes, how text is split into them, how to estimate how many a text uses, and how token counts turn into cost, speed and limits.

**Before you start:** you need strings and string methods ([Chapter 06](06-strings-basics-indexing-concatenation.md), [Chapter 10](10-ord-chr-and-string-methods.md)), dictionaries ([Dictionaries](23-dictionaries.md#dictionaries)), loops and functions, and the prompt basics from [Prompting](31-llms-prompting-temperature-hallucination.md#prompting). Recap: a prompt is the text sent to a model; a chat is a list of role-tagged messages; the model generates its answer one token at a time. All demos are labelled *toy demo* (standard library, simplified, **not** a real tokenizer or real prices) or *pseudocode*. Examples were run with Python 3.13.

---

## Context Engineering

**Timestamp:** [11:12:19](https://www.youtube.com/watch?v=J9BI0jGOds8&t=40339s)

**Learning objectives:**

- Define the *context* of a model call and list what it can contain.
- Explain how context engineering differs from writing a single good prompt.
- Describe the main techniques: selecting, ordering, summarising, trimming, and giving tools and memory.
- Write simple Python that assembles a context under a size budget.

**1. Intuition**

A model is like a consultant who walks into a meeting with no memory of any previous meeting. Everything they know about *your* situation is what is on the table in front of them right now: the brief, the relevant documents, the notes from the last session, the question. A good project manager decides what goes on that table: enough to do the job, nothing distracting, the most important papers on top. That job is context engineering. (This is an analogy: the model really does start every call with only what is in its input.)

**2. Why does it exist?**

A model can use only the information in its context for that call (plus whatever it learned in training). Real applications need it to use *your* data, the *current* conversation and the *results of tools*, and the space for all of this is limited and costs money (see [Context Window](34-context-window-and-model-parameters.md#context-window)). A good prompt is not enough when the answer depends on dozens of possible documents, a long history and tool outputs: someone has to choose and arrange them. Poor choices give wrong, slow or expensive answers, however clever the model.

**3. Technical explanation**

*Context* is everything the model receives in one call:

- the **system instructions** (role, rules, style),
- the **conversation history** so far,
- **retrieved documents or data** (see [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)),
- **tool definitions and tool results** (see [Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md)),
- **examples** (few-shot),
- **memory** the application has stored from earlier sessions, and
- the **current user request**.

*Prompt engineering versus context engineering.* Prompt engineering focuses on the wording of the instructions. Context engineering is wider: it is the design of the whole information flow into the model, with the question "what is the smallest set of the right information that lets the model do this task well?"

*Core techniques:*

1. **Select**: include only what is relevant (retrieve the few best documents rather than all of them).
2. **Order and structure**: put instructions and key facts where they are most likely to be used, label sections clearly, and separate data from instructions. (Models can handle information in the middle of a very long context less reliably than information at the start or end, although this varies between models.)
3. **Compress**: summarise old conversation turns or long documents; remove boilerplate and duplicates.
4. **Trim**: drop the least important material when over budget, with a clear priority order.
5. **Offload**: keep big data outside the context (files, databases, search) and let the model fetch what it needs through tools.
6. **Isolate**: give sub-tasks to separate model calls with their own small contexts, and pass back only results.
7. **Remember**: store facts from earlier sessions outside the model and bring back the relevant ones.
8. **Measure**: count tokens, test how answer quality changes when the context changes, and watch cost and delay.

*Failure modes:* too little context (the model guesses), too much (cost, slowness, distraction), conflicting or outdated information, irrelevant documents, a long history full of an old mistake, and tool outputs that flood the window. All of these are controllable in code.

**4. Syntax**

```text
Pseudocode: assembling a context under a budget

context = []
context += system_instructions            # always included
context += most_relevant(documents, k)    # selected
context += recent(history, n)             # trimmed history
context += summary_of(older_history)      # compressed
context += user_request                   # always included
while tokens(context) > budget:
    drop the least important piece
```

This is pseudocode, not runnable code.

**5. Example 1 — Basic**

*Toy demo.* A context is just a list of labelled parts, and its "size" is the sum of the sizes of the parts. Here the size is measured in words as a rough stand-in for tokens:

```python
context = {
    "system": "You are a concise assistant for Python beginners.",
    "history": [
        ("user", "What is a list?"),
        ("assistant", "An ordered, changeable collection of items."),
    ],
    "documents": ["Lists are written with square brackets.", "Tuples cannot be changed."],
    "request": "Show me how to add an item to a list.",
}


def size(text):
    return len(text.split())


parts = {
    "system": size(context["system"]),
    "history": sum(size(text) for _, text in context["history"]),
    "documents": sum(size(doc) for doc in context["documents"]),
    "request": size(context["request"]),
}
print(parts)
print("total words:", sum(parts.values()))

biggest = max(parts, key=parts.get)
print("largest part:", biggest)
```

Output:

```text
{'system': 8, 'history': 10, 'documents': 10, 'request': 10}
total words: 38
largest part: history
```

Line by line: the context is a dictionary with the different kinds of material; the sizes are added up per part so that you can see where the space goes. In a real system the size would be counted in tokens, and the largest part is the first place to look when a call is too big or too expensive.

**6. Example 2 — Practical**

*Toy demo.* Building a context under a budget with priorities: always keep the system message and the request; add the most relevant documents; keep as much recent history as will fit; and summarise or drop the rest.

```python
def words(text):
    return len(text.split())


def relevance(document, request):
    request_words = set(request.lower().replace("?", "").split())
    return len(request_words & set(document.lower().replace(".", "").split()))


def build_context(system, history, documents, request, budget):
    used = words(system) + words(request)
    chosen_docs = []
    ranked = sorted(documents, key=lambda d: relevance(d, request), reverse=True)
    for doc in ranked:
        if relevance(doc, request) == 0:
            continue
        if used + words(doc) <= budget:
            chosen_docs.append(doc)
            used += words(doc)

    kept_history = []
    for role, text in reversed(history):
        if used + words(text) <= budget:
            kept_history.insert(0, (role, text))
            used += words(text)
        else:
            break
    dropped = len(history) - len(kept_history)
    return chosen_docs, kept_history, dropped, used


history = [
    ("user", "Hi there, I am new to programming and want to learn."),
    ("assistant", "Welcome! Python is a friendly first language."),
    ("user", "What is a list?"),
    ("assistant", "An ordered, changeable collection of items."),
]
documents = [
    "A list is written with square brackets and can be changed with append.",
    "The weather in spring is mild.",
    "A tuple is written with round brackets and cannot be changed.",
]

for budget in [60, 30, 18]:
    docs, kept, dropped, used = build_context(
        "You are a Python tutor.", history, documents, "How do I add to a list?", budget
    )
    print(f"budget {budget:>2}: used {used:>2} words, {len(docs)} docs, {len(kept)} history turns kept, {dropped} dropped")
```

Output:

```text
budget 60: used 53 words, 2 docs, 3 history turns kept, 1 dropped
budget 30: used 25 words, 1 docs, 0 history turns kept, 4 dropped
budget 18: used 18 words, 0 docs, 1 history turns kept, 3 dropped
```

Line by line:

- The system message and the request are always counted first, because the model cannot work without them.
- Documents are ranked by a crude relevance score (shared words with the request) and added while there is room; documents with no overlap are skipped altogether (the weather note).
- History is added from the *newest* turn backwards, because recent turns usually matter most, and stops at the first one that does not fit.
- A smaller budget forces more to be dropped. A real system would also have the choice to *summarise* the dropped turns instead of discarding them.

**7. Example 3 — Edge case or common mistake**

*Toy demo.* Putting everything in the context is not free, and low-quality context can hurt. Compare a focused context with a "dump everything" context:

```python
documents = [
    "Refunds are available within 30 days of purchase with a receipt.",
    "The office is closed on public holidays.",
    "Shipping to remote areas takes up to ten working days.",
    "Gift cards cannot be refunded.",
    "Our logo uses two shades of blue.",
]
question = "Can I get a refund after 30 days?"


def overlap(document, question):
    clean = lambda text: set(text.lower().replace("?", "").replace(".", "").split())
    return len(clean(document) & clean(question))


focused = [d for d in documents if overlap(d, question) >= 2]
print("focused:", focused)
print("words: focused", sum(len(d.split()) for d in focused), "vs everything", sum(len(d.split()) for d in documents))
```

Output:

```text
focused: ['Refunds are available within 30 days of purchase with a receipt.']
words: focused 11 vs everything 40
```

The focused context is smaller and holds the relevant facts. The crude word-overlap rule here is only a stand-in: real systems score relevance with embeddings (see [Vectors and Embeddings](33-vectors-and-embeddings.md)). Overlap rules can also miss relevant documents and keep irrelevant ones:

```python
question = "Can I return my purchase?"
print(overlap("Refunds are available within 30 days of purchase.", question))
print(overlap("Can I park my car here?", question))
```

Output:

```text
1
3
```

The document about refunds shares only the word `purchase` with the question, while an unrelated sentence about parking scores as high because it shares the words `can`, `i` and `my`. This is why simple keyword rules are weak, and why better relevance measures (stop-word removal, embeddings) are used.

An outdated or contradictory piece of context is another hazard:

```python
notes = [
    ("2023-01-10", "Return window is 14 days."),
    ("2024-06-01", "Return window is 30 days."),
]
latest = max(notes, key=lambda note: note[0])
print("use:", latest[1])
print("all notes would contradict:", [text for _, text in notes])
```

Output:

```text
use: Return window is 30 days.
all notes would contradict: ['Return window is 14 days.', 'Return window is 30 days.']
```

If both versions are sent, the model sees two conflicting rules. Context engineering includes removing or marking outdated material.

**8. Common mistakes**

- Sending everything "just in case".
- Sending too little, so the model has to guess.
- Leaving old, conflicting or irrelevant material in the context.
- Letting a long history, or a very large tool output, crowd out the instructions.
- Never counting tokens or measuring cost.
- Mixing instructions and untrusted data without markers.
- Assuming that a larger context window removes the need to choose what goes in.

**9. Real-world and AI applications**

Every serious LLM application is, in effect, a context-assembly program: a support assistant that adds the customer's account details and the three most relevant help articles; a coding assistant that includes the open file and related definitions but not the whole repository; an agent that summarises its earlier steps to leave room for new tool results. Quality, cost and speed are all improved by good context decisions more often than by changing the model.

**10. Practice**

1. List five kinds of information that can be part of a model's context.
2. In your own words, what is the difference between prompt engineering and context engineering?
3. Modify `build_context` so that, when history turns do not fit, it adds a single line `"[earlier conversation omitted]"` and counts it.
4. Write a function that removes duplicate documents (ignoring case and extra spaces) before they are added to the context.
5. Given a list of `(timestamp, text)` notes, write a function that returns only the latest note for each topic (use a dictionary keyed by topic).
6. Name three problems that can come from a context that is too large.

**11. Interview questions**

- *What is context engineering?* Designing what information goes into the model's input, and in what form and order, for each call.
- *How does it differ from prompt engineering?* Prompt engineering is about instruction wording; context engineering covers the whole input: history, retrieved data, tools, memory and budget.
- *Why not put everything in the context?* It costs more, slows the response, can exceed the limit, and irrelevant or conflicting information can reduce answer quality.
- *Name some techniques.* Selecting, ordering, summarising, trimming, offloading to tools, isolating sub-tasks, and memory.

**12. Quick revision**

- Context = everything the model receives in a call: instructions, history, documents, tools, examples, memory, request.
- The model knows your situation only through the context.
- Select, order, compress, trim, offload, isolate, remember, measure.
- Too little: guessing. Too much: cost, delay, distraction.
- Count tokens and test changes.

---

## Tokens and Token Costs

**Timestamp:** [11:17:22](https://www.youtube.com/watch?v=J9BI0jGOds8&t=40642s)

**Learning objectives:**

- Explain what a token is and why models use tokens instead of whole words or single letters.
- Describe how a tokenizer works at a high level (subword merging) and why different tokenizers give different counts.
- Estimate token counts with rules of thumb, and know why they are only estimates.
- Calculate the cost of a call from input and output tokens, and understand the other things tokens limit.

**1. Intuition**

Think of text being cut into Scrabble-style tiles. Common words are one tile (`the`, `and`), rarer words are split into several tiles (`un` + `believ` + `able`), and unusual strings (a long number, a made-up name, text in a less common language) need many small tiles. The model reads and writes tile by tile, and billing is by the number of tiles. This is an analogy: the actual tiles come from a vocabulary learned from data, and they are not neat syllables.

**2. Why does it exist?**

A model works with numbers, so text has to be converted. Using single characters makes sequences very long; using whole words needs an enormous vocabulary and cannot handle new or misspelled words. Subword tokens are a compromise: a vocabulary of tens of thousands of pieces that can build any text, keep common words short, and handle unseen words by splitting them into known pieces.

**3. Technical explanation**

*What a token is.* A **token** is a unit of text from the model's fixed vocabulary: a whole common word, part of a word, a punctuation mark, or even a single byte or character for unusual input. Each token has an integer ID. The model never sees letters; it sees a sequence of IDs.

*Tokenizers.*

- A **tokenizer** converts text to token IDs and back. Many tokenizers are built with *byte-pair encoding* (BPE) or a similar algorithm: start from small units (bytes or characters), repeatedly find the most frequent adjacent pair in a large text sample, merge it into a new token, and stop when the vocabulary reaches the chosen size.
- Different model families use different tokenizers and vocabularies, so the **same text has different token counts for different models**. Always count with the tokenizer (or the token-counting tool) of the model you use; providers report the token usage of each call in the response.
- Spaces, capital letters and punctuation matter: `"Hello"`, `" Hello"` and `"hello"` can be different tokens.

*Rules of thumb for estimates* (very rough, for ordinary English text; they differ by tokenizer and language):

- about 4 characters per token, or
- about 3 tokens for every 2 English words (so roughly 0.75 words per token).
- Code, numbers, URLs, emoji and many non-English languages often need *more* tokens per character.

*What tokens limit and cost:*

1. **Cost.** Providers typically charge per token, with separate prices for *input* tokens (everything you send, including history, documents and instructions) and *output* tokens (what the model generates), usually quoted per million tokens. Output tokens commonly cost more than input tokens. Some services offer discounts for cached repeated input. *The prices in this handbook's examples are invented; always check your provider's current price list.*
2. **Context window.** The input and output together must fit within the model's limit (see [Context Window](34-context-window-and-model-parameters.md#context-window)).
3. **Speed.** Generation is token by token, so longer outputs take longer, and more input tokens take longer to process.
4. **Rate limits.** Services often limit tokens per minute.
5. **Output limit.** The `max tokens` setting caps the length of the answer.

*Cost of a call* = (input tokens × input price) + (output tokens × output price), where prices are per token (the per-million price divided by 1,000,000). In a chat the history is re-sent on every turn, so total input grows with the length of the conversation, and the cost of a whole conversation grows faster than linearly.

**4. Syntax**

```text
cost = input_tokens  * input_price_per_million  / 1_000_000
     + output_tokens * output_price_per_million / 1_000_000

estimate_tokens(text) ~ len(text) / 4          # rough rule of thumb
```

Python's `_` in numbers is a digit separator (`1_000_000` equals 1000000). The formula is a pattern; the prices are inputs you supply.

**5. Example 1 — Basic**

*Toy demo.* A very simple tokenizer that splits text into words and punctuation. It is *not* how real tokenizers work (they use subwords), but it shows text becoming a list of tokens with integer IDs:

```python
import re

text = "Python is fun, isn't it?"
tokens = re.findall(r"\w+|[^\w\s]", text)
print(tokens)
print(len(tokens), "tokens")

vocabulary = {}
ids = []
for token in tokens:
    if token not in vocabulary:
        vocabulary[token] = len(vocabulary)
    ids.append(vocabulary[token])
print(ids)
print(vocabulary)

reverse = {number: token for token, number in vocabulary.items()}
print([reverse[i] for i in ids])

print(len(text), "characters,", len(text) / 4, "tokens by the 4-characters rule")
```

Output:

```text
['Python', 'is', 'fun', ',', 'isn', "'", 't', 'it', '?']
9 tokens
[0, 1, 2, 3, 4, 5, 6, 7, 8]
{'Python': 0, 'is': 1, 'fun': 2, ',': 3, 'isn': 4, "'": 5, 't': 6, 'it': 7, '?': 8}
['Python', 'is', 'fun', ',', 'isn', "'", 't', 'it', '?']
24 characters, 6.0 tokens by the 4-characters rule
```

Line by line:

- The regular expression keeps runs of letters and digits together (`\w+`) and treats each punctuation mark as its own token.
- Each new token gets the next unused integer as its ID. The text becomes a list of IDs, which is what a model actually receives.
- The reverse dictionary turns IDs back into tokens (decoding).
- The rough rule of "4 characters per token" gives an estimate that differs from the toy's count: both are only approximations of a real tokenizer.

**6. Example 2 — Practical**

*Toy demo.* A tiny byte-pair-encoding trainer on a small text, to show how subword tokens come from merging frequent pairs. It is a teaching sketch, not a production tokenizer:

```python
from collections import Counter

corpus = "low low low low lower lower newest newest newest widest widest"
words = [list(word) + ["_"] for word in corpus.split()]


def pair_counts(words):
    counts = Counter()
    for word in words:
        for a, b in zip(word, word[1:]):
            counts[(a, b)] += 1
    return counts


def merge(words, pair):
    merged = []
    for word in words:
        new_word = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and (word[i], word[i + 1]) == pair:
                new_word.append(word[i] + word[i + 1])
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        merged.append(new_word)
    return merged


for step in range(1, 7):
    counts = pair_counts(words)
    best = max(counts, key=lambda pair: (counts[pair], pair))
    words = merge(words, best)
    print(f"merge {step}: {best} (seen {counts[best]} times)")

print(words[0], words[4], words[6], words[9])
```

Output:

```text
merge 1: ('o', 'w') (seen 6 times)
merge 2: ('l', 'ow') (seen 6 times)
merge 3: ('t', '_') (seen 5 times)
merge 4: ('s', 't_') (seen 5 times)
merge 5: ('e', 'st_') (seen 5 times)
merge 6: ('low', '_') (seen 4 times)
['low_'] ['low', 'e', 'r', '_'] ['n', 'e', 'w', 'est_'] ['w', 'i', 'd', 'est_']
```

Line by line:

- Each word starts as separate characters plus an end-of-word marker `_`.
- At every step the most frequent adjacent pair is found and merged into a new, longer token. After a few merges, common sequences become single tokens (here `ow`, then `low`, and the word ending `est_`).
- The final lines show how some words are now represented by a few tokens. A real tokenizer does this on gigabytes of text, with merges stopping at a vocabulary of tens of thousands of tokens, and usually works on bytes so that any text can be represented.

Estimating cost from counts. *Toy demo with invented prices (per million tokens).*

```python
INPUT_PRICE_PER_MILLION = 2.00
OUTPUT_PRICE_PER_MILLION = 8.00


def estimate_tokens(text):
    return max(1, round(len(text) / 4))


def call_cost(input_tokens, output_tokens):
    return (input_tokens * INPUT_PRICE_PER_MILLION + output_tokens * OUTPUT_PRICE_PER_MILLION) / 1_000_000


prompt = "Summarise the following article in three bullet points. " + "word " * 1500
print(estimate_tokens(prompt), "estimated input tokens")
cost = call_cost(estimate_tokens(prompt), 200)
print(f"one call: {cost:.6f} currency units")
print(f"10,000 such calls: {cost * 10_000:.2f}")

history_tokens = 0
total_input = 0
turn_tokens = 150
for turn in range(1, 11):
    history_tokens += turn_tokens
    total_input += history_tokens
print("input tokens re-sent over a 10-turn chat:", total_input, "vs", 10 * turn_tokens, "new tokens typed")
```

Output:

```text
1889 estimated input tokens
one call: 0.005378 currency units
10,000 such calls: 53.78
input tokens re-sent over a 10-turn chat: 8250 vs 1500 new tokens typed
```

Line by line:

- `estimate_tokens` applies the 4-characters rule, and `call_cost` applies the pricing formula. The price numbers are invented placeholders; real prices differ by model and change over time.
- A single call is cheap, but multiplying by many calls shows why token use matters in production.
- In a chat the history is sent again every turn: after 10 turns of 150 tokens each, the total input processed is 8,250 tokens even though only 1,500 tokens were typed. Growth is quadratic in the number of turns, which is why long conversations get expensive and why summarising old turns helps.

**7. Example 3 — Edge case or common mistake**

Character counts, word counts and token counts are different things, and estimates can be wrong:

```python
samples = {
    "english": "The quick brown fox jumps over the lazy dog.",
    "code": "for i in range(10): total += i * i",
    "numbers": "3.14159265358979323846264338327950288",
    "url": "https://example.org/a/very/long/path?query=value&other=1",
    "emoji": "I love Python 🐍🐍🐍",
}
for name, text in samples.items():
    chars = len(text)
    words = len(text.split())
    print(f"{name:<8} chars={chars:>2} words={words:>2} estimate(chars/4)={chars / 4:>5.1f}")
```

Output:

```text
english  chars=44 words= 9 estimate(chars/4)= 11.0
code     chars=34 words= 9 estimate(chars/4)=  8.5
numbers  chars=37 words= 1 estimate(chars/4)=  9.2
url      chars=56 words= 1 estimate(chars/4)= 14.0
emoji    chars=17 words= 4 estimate(chars/4)=  4.2
```

The estimates look fine for plain English, but numbers, URLs, code and emoji usually need more tokens than `chars / 4` suggests (for example, many tokenizers split long digit strings into groups of a few digits, and emoji can take several tokens each), and the word count says nothing about it. Use the model's own tokenizer for real budgets.

Counting characters is not counting bytes either:

```python
text = "naïve café 🐍"
print(len(text), len(text.encode("utf-8")))
print([len(ch.encode("utf-8")) for ch in text])
```

Output:

```text
12 17
[1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 4]
```

Some characters take several bytes in UTF-8. Many tokenizers work on bytes, which is one reason that text in some languages needs more tokens.

The same text, split differently, gives different counts:

```python
import re

text = "Tokenization isn't magic."
by_words = text.split()
by_regex = re.findall(r"\w+|[^\w\s]", text)
by_chars = list(text)
print(len(by_words), by_words)
print(len(by_regex), by_regex)
print(len(by_chars))
```

Output:

```text
3 ['Tokenization', "isn't", 'magic.']
6 ['Tokenization', 'isn', "'", 't', 'magic', '.']
25
```

Whitespace splitting gives 3 pieces, the regex 6, and characters 25. A real subword tokenizer gives yet another count, which is why the same text costs differently on different models.

Forgetting the output tokens, or the re-sent history, makes budgets too low:

```python
input_price, output_price = 2.0, 8.0
input_tokens, output_tokens = 1000, 1000
input_only = input_tokens * input_price / 1_000_000
both = (input_tokens * input_price + output_tokens * output_price) / 1_000_000
print(f"input only: {input_only:.4f}, input and output: {both:.4f}, ratio {both / input_only:.1f}x")
```

Output:

```text
input only: 0.0020, input and output: 0.0100, ratio 5.0x
```

With these invented prices, output tokens being four times as expensive means a call with equal input and output costs five times what the input alone would suggest.

A budget check before sending avoids hitting a limit:

```python
CONTEXT_LIMIT = 8000
RESERVED_FOR_ANSWER = 1000


def fits(input_tokens):
    return input_tokens + RESERVED_FOR_ANSWER <= CONTEXT_LIMIT


print(fits(5000), fits(7500))
```

Output:

```text
True False
```

The limit (invented here) covers input *and* output, so room must be left for the answer.

*Pseudocode, requires a real tokenizer and a package install (not run here):*

```text
# pip install <tokenizer-package-for-your-model>
tokenizer = load_tokenizer("<model-name>")
token_ids = tokenizer.encode(text)
print(len(token_ids))
```

Providers also report the exact token usage of every call in their responses, and many offer a token-counting tool. Check the documentation of your provider for the current way to count.

**8. Common mistakes**

- Treating words, characters and tokens as the same.
- Using one model's token count for another model.
- Forgetting that output tokens (and often higher prices) count too.
- Forgetting that chat history is re-sent each turn and grows the cost.
- Relying on `chars / 4` for code, numbers, other languages or emoji.
- Not leaving room in the context window for the answer.
- Using hard-coded prices that become out of date.

**9. Real-world and AI applications**

Token counting is used to keep prompts under the limit, to estimate and monitor spending, to split long documents into chunks that fit (see [Retrieval-Augmented Generation](37-retrieval-augmented-generation.md)), to decide when to summarise a conversation, and to compare the cost of different designs. Teams log the tokens used per request and set alerts on unusual spikes. The mini-project `projects/06_token_estimator.py` in this handbook builds a small estimator and cost calculator.

**10. Practice**

1. Use the regex tokenizer on a sentence of your own, and print the tokens and the count. Compare with the `chars / 4` estimate.
2. In the BPE toy, change the corpus and print the first six merges. Which pairs merge first and why?
3. With input price 3.00 and output price 15.00 per million tokens (invented), compute the cost of a call with 12,000 input and 800 output tokens.
4. A chat adds 200 tokens per turn. How many input tokens are processed in total over 8 turns if the whole history is sent each time?
5. Write `chunk_by_tokens(text, max_tokens)` that splits a text into chunks of at most `max_tokens` words (use words as the stand-in for tokens).
6. Explain why the same text can have different token counts on two different models.
7. Give three reasons why you should care about token usage in a production application.

**11. Interview questions**

- *What is a token?* A unit from the model's vocabulary: a word, part of a word, punctuation, or a few bytes; the model reads and writes sequences of token IDs.
- *Why do models use subword tokens?* They keep the vocabulary manageable while still being able to represent any text, including new words.
- *How are LLM calls priced?* Usually per token, with separate (typically higher) prices for output tokens than for input tokens.
- *Why is a long conversation expensive?* The history is sent as input again on every turn.
- *Is a token a word?* No; in English a token is on average a bit less than a word, and the ratio varies with the text and tokenizer.

**12. Quick revision**

- Token: a vocabulary unit; models see token IDs, not letters.
- Tokenizers (often BPE) differ between models: always count with the right one.
- Rough English estimate: ~4 characters or ~0.75 words per token; code, numbers and other languages need more.
- Cost = input tokens × input price + output tokens × output price (per-million prices).
- Tokens limit cost, speed, rate and the context window (input plus output).

---

## Answers to Practice Exercises

### Answers: Context Engineering

1. For example: system instructions, conversation history, retrieved documents, tool definitions, tool results, examples, memory notes, and the user's current request.

2. Prompt engineering is about wording the instructions well. Context engineering is wider: it decides *everything* that goes into the model's input (history, documents, tool results, memory) and how much of it, in what order and form, within a limited budget.

3.

```python
def words(text):
    return len(text.split())


def trim_history(history, budget_left):
    kept = []
    used = 0
    for role, text in reversed(history):
        if used + words(text) <= budget_left:
            kept.insert(0, (role, text))
            used += words(text)
        else:
            break
    if len(kept) < len(history):
        note = "[earlier conversation omitted]"
        if used + words(note) <= budget_left:
            kept.insert(0, ("system", note))
    return kept


history = [("user", "one two three four"), ("assistant", "five six seven"), ("user", "eight nine")]
print(trim_history(history, 8))
```

Output:

```text
[('system', '[earlier conversation omitted]'), ('assistant', 'five six seven'), ('user', 'eight nine')]
```

4.

```python
def dedupe(documents):
    seen = set()
    unique = []
    for doc in documents:
        key = " ".join(doc.lower().split())
        if key not in seen:
            seen.add(key)
            unique.append(doc)
    return unique


print(dedupe(["Refunds in 30 days.", "refunds  in 30 DAYS.", "Shipping takes a week."]))
```

Output:

```text
['Refunds in 30 days.', 'Shipping takes a week.']
```

5.

```python
def latest_per_topic(notes):
    latest = {}
    for timestamp, topic, text in notes:
        if topic not in latest or timestamp > latest[topic][0]:
            latest[topic] = (timestamp, text)
    return {topic: text for topic, (timestamp, text) in latest.items()}


notes = [
    ("2023-01-10", "returns", "14 days"),
    ("2024-06-01", "returns", "30 days"),
    ("2024-02-01", "shipping", "5 days"),
]
print(latest_per_topic(notes))
```

Output:

```text
{'returns': '30 days', 'shipping': '5 days'}
```

6. For example: higher cost, slower responses, and the risk of exceeding the window; also irrelevant or conflicting material can distract the model and lower the quality of its answer.

### Answers: Tokens and Token Costs

1.

```python
import re

sentence = "Tokens aren't words, are they?"
tokens = re.findall(r"\w+|[^\w\s]", sentence)
print(tokens, len(tokens))
print(len(sentence) / 4)
```

Output:

```text
['Tokens', 'aren', "'", 't', 'words', ',', 'are', 'they', '?'] 9
7.5
```

2.

```python
from collections import Counter

corpus = "banana bandana band"
words = [list(word) + ["_"] for word in corpus.split()]
counts = Counter()
for word in words:
    for pair in zip(word, word[1:]):
        counts[pair] += 1
print(counts.most_common(4))
```

Output:

```text
[(('a', 'n'), 5), (('b', 'a'), 3), (('n', 'a'), 3), (('a', '_'), 2)]
```

The most frequent adjacent pair (`a`+`n`, seen 5 times) merges first, followed by `b`+`a` and `n`+`a` (3 times each), because merging the most frequent pair gives the largest saving in sequence length.

3.

```python
cost = (12000 * 3.00 + 800 * 15.00) / 1_000_000
print(round(cost, 4))
```

Output:

```text
0.048
```

4.

```python
per_turn = 200
total = sum(per_turn * turn for turn in range(1, 9))
print(total, "tokens processed, versus", per_turn * 8, "typed")
```

Output:

```text
7200 tokens processed, versus 1600 typed
```

5.

```python
def chunk_by_tokens(text, max_tokens):
    words = text.split()
    return [" ".join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]


for chunk in chunk_by_tokens("one two three four five six seven", 3):
    print(repr(chunk))
```

Output:

```text
'one two three'
'four five six'
'seven'
```

6. Each model family has its own tokenizer, trained on different text and with a different vocabulary and merge rules. A word that is one token in one vocabulary can be two or three in another, so the counts differ.

7. For example: cost (spending grows with tokens), speed (more tokens take longer), the limit of the context window, and rate limits.

---

## Chapter Summary and Key Takeaways

- The context is everything the model receives in a call; context engineering is the design of that information (instructions, history, retrieved data, tool results, examples, memory) under a limited and costly budget.
- Good context is selected, ordered, compressed and trimmed, and measured; too little makes the model guess, too much costs more, slows the call and can distract it.
- A token is a unit from the model's vocabulary (often a subword); models read and write token IDs, and different models use different tokenizers, so counts differ.
- Rules of thumb (about 4 characters or 0.75 words per token for English) are only estimates, and code, numbers, URLs, emoji and many languages need more tokens.
- Cost is input tokens times the input price plus output tokens times the output price; output usually costs more, chat history is re-sent every turn, and the context window must fit both input and output.

Next: [Chapter 33 — Vectors and Embeddings](33-vectors-and-embeddings.md) shows how text becomes numbers that capture meaning.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
