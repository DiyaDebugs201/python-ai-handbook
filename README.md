# Python + AI — Complete Learning Handbook

A structured, practical study guide that takes you from first principles of Python to the core ideas behind modern AI applications. It is built around the topic list of a 13-hour Python + AI video and expands each topic into a full lesson with explanations, working code, expected output, common mistakes, exercises and interview questions.

> **Status:** complete. All 40 chapters, the practice problems with solutions, the 7 projects, the glossary and the revision checklist are included. Code examples were run with Python 3.13. See [PROGRESS_TRACKER.md](PROGRESS_TRACKER.md) for per-chapter validation details.

## Overview

- 40 chapters in 6 parts, covering all 96 topics of the source syllabus.
- Every chapter follows a consistent lesson structure (intuition, why it exists, technical detail, syntax, three examples, mistakes, applications, practice, interview questions, revision).
- Every chapter ends with answers to its own practice exercises, and the [`practice/`](practice/README.md) folder adds extra problems for each part, with solutions kept in a separate folder so you can attempt them first.
- Seven standard-library mini-projects in [`projects/`](projects/README.md) apply the ideas to small programs.
- The AI part separates intuition from actual mechanism, and labels toy code, conceptual pseudocode, and code that needs external libraries or API credentials.

## Prerequisites

- A computer science background is assumed. You do not need prior Python experience.
- A computer that can install a current Python 3 release (see [python.org/downloads](https://www.python.org/downloads/)).
- Comfort opening a terminal or command prompt.
- No `requirements.txt` is needed: every example, practice solution and project uses only the Python standard library. The few snippets that would need a third-party package or an AI service are shown as pseudocode and say so.
- For the optional AI demos that call external services: an account and API key for the relevant provider. Chapter 30 explains how to store keys safely with environment variables and `.env` files, and this repository's `.gitignore` already excludes `.env`.

## Learning roadmap

| Step | Part | Chapters | After this step you can |
|------|------|----------|-------------------------|
| 1 | Python Fundamentals | 01–04 | Set up Python, run code, read error messages and name things correctly. |
| 2 | Data Types and Strings | 05–10 | Work with numbers, text, type conversion and formatted output. |
| 3 | Operators and Control Flow | 11–17 | Write programs that make decisions and repeat work. |
| 4 | Python Data Structures | 18–24 | Store and manipulate collections with lists, tuples, sets and dictionaries. |
| 5 | Functions and Functional Programming | 25–29 | Write reusable functions and use functional tools such as lambda, map, filter and reduce. |
| 6 | Python Integration and AI Foundations | 30–40 | Explain how LLM-based applications work: tokens, embeddings, attention, RAG, MCP and agents. |

Study in chapter order. After each chapter, do its exercises; after each part, try the part's extra problems in [`practice/`](practice/README.md) and the matching project in [`projects/`](projects/README.md).

## Table of contents

### Part 1 — Python Fundamentals

- [01 · Introduction to Programming and Python](notes/01-introduction-to-programming-and-python.md) — video 00:00–11:10
- [02 · Installation and Environment Setup](notes/02-installation-and-environment-setup.md) — video 14:22–20:31
- [03 · Built-in Functions, print() and Modules](notes/03-builtin-functions-print-and-modules.md) — video 29:18–35:42
- [04 · Errors and Identifiers](notes/04-errors-and-identifiers.md) — video 38:20–43:59

### Part 2 — Data Types and Strings

- [05 · Numeric Types and Booleans](notes/05-numeric-types-and-booleans.md) — video 51:57–1:06:20
- [06 · Strings: Basics, Indexing, Concatenation and Repetition](notes/06-strings-basics-indexing-concatenation.md) — video 1:12:28–1:27:35
- [07 · String Slicing](notes/07-string-slicing.md) — video 1:33:40–1:50:14
- [08 · Type Conversion](notes/08-type-conversion.md) — video 2:01:13–2:07:12
- [09 · String Formatting and f-Strings](notes/09-string-formatting-and-f-strings.md) — video 3:13:46–3:25:07
- [10 · ord(), chr() and String Methods](notes/10-ord-chr-and-string-methods.md) — video 8:19:30–8:26:41

### Part 3 — Operators and Control Flow

- [11 · Operators Overview and Arithmetic Operators](notes/11-arithmetic-operators.md) — video 2:15:50–2:17:59
- [12 · Relational, Logical and Assignment Operators](notes/12-relational-logical-assignment-operators.md) — video 2:26:08–2:53:03
- [13 · Identity Operators and Operator Precedence](notes/13-identity-operators-and-precedence.md) — video 2:58:11–3:06:08
- [14 · Conditional Statements](notes/14-conditional-statements.md) — video 3:28:43–3:56:24
- [15 · Conditionals: Practice Problems](notes/15-conditionals-practice.md) — video 4:04:18
- [16 · while Loops and Loop Control](notes/16-while-loop-and-loop-control.md) — video 4:19:50–4:45:36
- [17 · for Loops, range() and Nested Loops](notes/17-for-loop-range-and-nested-loops.md) — video 4:48:36–5:20:55

### Part 4 — Python Data Structures

- [18 · Data Structures Introduction and Lists](notes/18-lists-fundamentals.md) — video 5:33:56–5:54:24
- [19 · List Functions, Methods and Copying](notes/19-list-functions-methods-and-copying.md) — video 6:01:49–6:28:20
- [20 · List Comprehension](notes/20-list-comprehension.md) — video 6:33:38
- [21 · Tuples](notes/21-tuples.md) — video 6:48:42
- [22 · Sets and Set Operations](notes/22-sets.md) — video 7:18:01–7:28:17
- [23 · Dictionaries](notes/23-dictionaries.md) — video 7:48:58–8:02:44
- [24 · Mutability, Iteration and Common Data-Structure Pitfalls](notes/24-mutability-iteration-and-pitfalls.md) — video supplementary

### Part 5 — Functions and Functional Programming

- [25 · Defining Functions and Return Values](notes/25-defining-functions-and-return-values.md) — video 8:41:36–8:59:32
- [26 · Function Arguments](notes/26-function-arguments.md) — video 9:10:11–9:33:05
- [27 · Variable Scope](notes/27-variable-scope.md) — video 9:40:20
- [28 · First-Class Functions and Lambda](notes/28-first-class-functions-and-lambda.md) — video 9:56:08–10:22:04
- [29 · map(), filter() and reduce()](notes/29-map-filter-reduce.md) — video 10:32:38–10:43:06

### Part 6 — Python Integration and AI Foundations

- [30 · Python Wrap-Up and AI Section Introduction](notes/30-python-wrap-up-and-ai-intro.md) — video 10:47:48
- [31 · LLMs, Prompting, Temperature and Hallucination](notes/31-llms-prompting-temperature-hallucination.md) — video 10:52:08–11:07:43
- [32 · Context Engineering, Tokens and Token Costs](notes/32-context-engineering-and-tokens.md) — video 11:12:19–11:17:22
- [33 · Vectors and Embeddings](notes/33-vectors-and-embeddings.md) — video 11:26:22
- [34 · Context Window and Model Parameters](notes/34-context-window-and-model-parameters.md) — video 11:31:37–11:39:49
- [35 · Attention Mechanism and Transformers](notes/35-attention-and-transformers.md) — video 11:46:56–11:52:46
- [36 · Pretraining, Fine-Tuning and RLHF](notes/36-pretraining-fine-tuning-rlhf.md) — video 12:04:37–12:11:31
- [37 · Retrieval-Augmented Generation (RAG)](notes/37-retrieval-augmented-generation.md) — video 12:16:08
- [38 · Model Context Protocol and AI Agents](notes/38-mcp-and-ai-agents.md) — video 12:26:47–12:38:47
- [39 · Multimodal AI, Reasoning Models, SLMs, AGI and ASI](notes/39-multimodal-reasoning-slm-agi-asi.md) — video 12:45:49–12:54:10
- [40 · Recap and Final Thoughts](notes/40-recap-and-final-thoughts.md) — video 12:56:47–12:59:03

Topic-by-topic detail, including video timestamps, is in [SYLLABUS_MAPPING.md](SYLLABUS_MAPPING.md).

## Repository layout

```text
python-ai-handbook/
├── README.md
├── SYLLABUS_MAPPING.md
├── PROGRESS_TRACKER.md
├── CONTRIBUTING.md
├── .env.example   placeholders only; copy to .env and never commit .env
├── .gitignore
├── docs/        blueprint, glossary, revision checklist
├── notes/       the 40 numbered chapters
├── practice/    exercises, with solutions in practice/solutions/
└── projects/    seven mini-projects (standard library only)
```

The full annotated tree is in [docs/BLUEPRINT.md](docs/BLUEPRINT.md).

## How to study a chapter

1. Read the learning objectives and intuition first.
2. Type out and run every example yourself, then compare with the expected output shown.
3. Deliberately trigger the errors shown in the edge-case example and read the messages.
4. Attempt the exercises without looking at the solutions.
5. Use the quick-revision section and [docs/REVISION_CHECKLIST.md](docs/REVISION_CHECKLIST.md) for later review.

## Navigation

- [Syllabus-to-notes mapping and coverage checklist](SYLLABUS_MAPPING.md)
- [Progress tracker](PROGRESS_TRACKER.md)
- [Repository blueprint and publishing checklist](docs/BLUEPRINT.md)
- [Glossary](docs/GLOSSARY.md)
- [Revision checklist](docs/REVISION_CHECKLIST.md)
- [Contributing](CONTRIBUTING.md)

## Source and attribution

This handbook is based on the topic list and timestamps of the [source video](https://www.youtube.com/watch?v=J9BI0jGOds8). It is an independently written study resource, not a transcript, and it is not affiliated with the video's creator. Explanations, examples and exercises are written for this project.

## A note on accuracy

Python fundamentals change slowly, but AI tooling, APIs, protocol specifications and model names change quickly. Where a claim depends on something that changes, the chapter links to official documentation. Check those sources for the latest details before relying on them.

## License

No license has been selected for this repository yet. Until one is added, default copyright applies and others have no explicit permission to reuse the contents.

Options to consider before publishing:

- **MIT or Apache-2.0** for the code examples. Both are widely used and permissive.
- **CC BY 4.0** for the written notes, if you want others to share and adapt them with credit.
- A single license for everything, if you prefer simplicity. MIT is the usual choice for that.

Choose one, add a `LICENSE` file at the repository root, and update this section. Because the notes are based on another creator's syllabus, consider whether you are comfortable with the attribution wording above.
