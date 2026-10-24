# Projects

Seven small programs that put the handbook's ideas to work. Every project uses **only the Python standard library**, has a `--demo` mode that prints the same output every time, and keeps its logic in functions so you can import and test them.

Run any project from this folder:

```text
python 01_environment_check.py --demo
```

(Use `python3` instead of `python` if that is how Python is started on your computer.)

| # | Project | Skills used | Chapters |
|---|---|---|---|
| 1 | [`01_environment_check.py`](01_environment_check.py) | modules, version tuples, dictionaries, environment variables (values are never printed) | [01](../notes/01-introduction-to-programming-and-python.md)–[04](../notes/04-errors-and-identifiers.md), [30](../notes/30-python-wrap-up-and-ai-intro.md) |
| 2 | [`02_string_toolkit.py`](02_string_toolkit.py) | slicing, `ord`/`chr`, string methods, regular expressions | [06](../notes/06-strings-basics-indexing-concatenation.md)–[10](../notes/10-ord-chr-and-string-methods.md) |
| 3 | [`03_number_guessing_game.py`](03_number_guessing_game.py) | loops, conditionals, `random` with a seed, separating logic from input/output | [14](../notes/14-conditional-statements.md)–[17](../notes/17-for-loop-range-and-nested-loops.md) |
| 4 | [`04_contact_book.py`](04_contact_book.py) | dictionaries, validation, JSON files, a menu loop | [18](../notes/18-lists-fundamentals.md)–[24](../notes/24-mutability-iteration-and-pitfalls.md) |
| 5 | [`05_functional_text_pipeline.py`](05_functional_text_pipeline.py) | lambda, `map`, `filter`, `reduce`, function composition | [28](../notes/28-first-class-functions-and-lambda.md), [29](../notes/29-map-filter-reduce.md) |
| 6 | [`06_token_estimator.py`](06_token_estimator.py) | token and cost arithmetic, `argparse`; **a rough estimator, not a real tokenizer** | [32](../notes/32-context-engineering-and-tokens.md), [34](../notes/34-context-window-and-model-parameters.md) |
| 7 | [`07_toy_rag_retriever.py`](07_toy_rag_retriever.py) | chunking, word-count vectors, cosine similarity, prompt assembly; **toy retrieval with a fake model, no AI service** | [33](../notes/33-vectors-and-embeddings.md), [37](../notes/37-retrieval-augmented-generation.md) |

## Ideas for extending each project

1. **Environment check**: add a check for a free-disk-space minimum, or read the list of variable names from a file.
2. **String toolkit**: add `is_anagram(a, b)` and a `--help` message listing the commands.
3. **Guessing game**: let the player choose the range and keep a high-score table in a JSON file.
4. **Contact book**: export to CSV with the `csv` module; reject duplicate phone numbers.
5. **Text pipeline**: add a bigram counter and a `--stop-words FILE` option.
6. **Token estimator**: read the text from a file and warn when the estimate exceeds a limit you pass in.
7. **Toy RAG retriever**: add a `--show-chunks` option, load documents from a folder of `.txt` files, and write an evaluation of five questions with the expected source file for each (see [Evaluation, Limitations, and Responsible Use](../notes/40-recap-and-final-thoughts.md#evaluation-limitations-and-responsible-use)).

## Safety notes

- No project needs an API key, a network connection or any package outside the standard library. If you extend one to call a real service, keep the key in an environment variable (see `.env.example` in the repository root) and never commit it.
- Project 4 can write a `contacts.json` file in the folder you run it from. It is listed in `.gitignore` so it is not committed by accident; still, do not store real personal data in a toy project.

Back to the [README](../README.md).
