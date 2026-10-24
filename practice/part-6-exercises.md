# Part 6 — Extra Practice: Python Integration and AI Foundations

> [Practice index](README.md) · [Solutions for this part](solutions/part-6-solutions.md)

These 12 problems go beyond the exercises inside the chapters. Try each one on your own before opening the solutions. Run your code, compare with your prediction, and only then check the solution. Related chapters:

- [Chapter 30 — Python Wrap-Up and Introduction to the AI Section](../notes/30-python-wrap-up-and-ai-intro.md)
- [Chapter 31 — LLMs, Prompting, Temperature and Hallucination](../notes/31-llms-prompting-temperature-hallucination.md)
- [Chapter 32 — Context Engineering and Tokens](../notes/32-context-engineering-and-tokens.md)
- [Chapter 33 — Vectors and Embeddings](../notes/33-vectors-and-embeddings.md)
- [Chapter 34 — Context Window and Model Parameters](../notes/34-context-window-and-model-parameters.md)
- [Chapter 35 — Attention Mechanism and Transformers](../notes/35-attention-and-transformers.md)
- [Chapter 36 — Pretraining, Fine-Tuning and RLHF](../notes/36-pretraining-fine-tuning-rlhf.md)
- [Chapter 37 — Retrieval-Augmented Generation](../notes/37-retrieval-augmented-generation.md)
- [Chapter 38 — Model Context Protocol and AI Agents](../notes/38-mcp-and-ai-agents.md)
- [Chapter 39 — Multimodal AI, Reasoning Models, SLMs, AGI and ASI](../notes/39-multimodal-reasoning-slm-agi-asi.md)
- [Chapter 40 — Recap and Final Thoughts](../notes/40-recap-and-final-thoughts.md)

Tips: write a few lines at a time and run often; if you are stuck for more than ten minutes read only the hint again, then the solution's explanation; afterwards rewrite the solution from memory.

## P6.1 — Read a setting from the environment

Read the environment variable `HANDBOOK_DEMO_VALUE` using a default of `"not set"`. Then set it inside the program with `os.environ` and read it again. (Never put real secrets in code.)

*Hint:* `os.environ.get(name, default)`.

## P6.2 — Rough token estimator

Write `estimate_tokens(text)` that returns the larger of 1 and `round(len(text) / 4)`, and `estimate_words_tokens(text)` that uses `round(len(text.split()) / 0.75)`. Compare them on a sentence and on `"3.14159265358979"`. They are only estimates, not a real tokenizer.

*Hint:* Two rules of thumb for English.

## P6.3 — Nearest neighbour by cosine similarity

Given `docs = {"cat": [0.9, 0.1], "dog": [0.8, 0.2], "car": [0.1, 0.9]}` and a query vector `[0.85, 0.15]`, print the documents ranked by cosine similarity with their scores to 3 decimals.

*Hint:* dot / (length * length).

## P6.4 — Softmax with temperature

Write `softmax(scores, temperature)` and print the probabilities (3 decimals) of scores `[2.0, 1.0, 0.1]` at temperatures 0.5, 1 and 2. Describe in a comment what happens as temperature rises.

*Hint:* Divide scores by the temperature before exponentiating.

## P6.5 — Prompt template with validation

Write `build_prompt(template, **fields)` that fills a template such as `"Summarise in {n} bullets: {text}"` and raises a clear `ValueError` naming any missing field.

*Hint:* `string.Formatter().parse` or `str.format` with a `KeyError` handler.

## P6.6 — Trim history to a budget

Write `trim(messages, budget)` that keeps the most recent messages whose total word count is at most `budget`, in original order. Test with 4 short messages and budget 7.

*Hint:* Walk the list backwards.

## P6.7 — Chunk with overlap

Write `chunks(words, size, overlap)` that splits a list of words into chunks of `size` words, each starting `size - overlap` words after the previous one. Test on the words `a` to `j` with size 4 and overlap 1.

*Hint:* A step of `size - overlap`.

## P6.8 — Top-k retrieval by overlap

Given four short documents and a question, return the 2 documents sharing the most words with the question (ignore case).

*Hint:* `set` intersection and `sorted(..., key=...)`.

## P6.9 — Spot unsupported numbers

Given an answer and its source text, list the numbers in the answer that do not appear in the source (a simple hallucination check).

*Hint:* `re.findall(r"\d+", text)`.

## P6.10 — Cost calculator

Write `call_cost(input_tokens, output_tokens, input_price, output_price)` with prices per million tokens (use invented prices 2.0 and 8.0), and print the cost of 1,000 calls with 1,500 input and 300 output tokens each.

*Hint:* Divide by 1,000,000.

## P6.11 — Tool registry with errors

Create a dictionary of tools `{"add": ..., "upper": ...}` and a function `run(name, **arguments)` that returns a result, or a clear error string for an unknown tool or bad arguments, without crashing.

*Hint:* `try` / `except TypeError` for wrong arguments.

## P6.12 — Evaluate a classifier

Compute the accuracy of the simple function `is_positive(text)` (true if the text contains `good` or `great`) on five labelled examples and list the failures.

*Hint:* Keep a list of `(text, expected)` pairs.

---

Solutions: [part-6-solutions.md](solutions/part-6-solutions.md) · Back to the [practice index](README.md).
