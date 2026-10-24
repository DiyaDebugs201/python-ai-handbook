# Glossary

Short definitions of the terms used in this handbook, in alphabetical order, each with a pointer to the chapter that explains it. Definitions are deliberately brief; follow the link for the full explanation and examples. AI terms are used in their common, general sense, and fast-moving topics should be checked against current official documentation.

[A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [V](#v) · [W](#w)

## A

- **Agent (AI agent)** — a system in which a model chooses actions, such as tool calls, step by step toward a goal, observing results as it goes. See [Chapter 38](../notes/38-mcp-and-ai-agents.md).
- **AGI (artificial general intelligence)** — a hypothetical AI with broad, flexible, roughly human-level ability; there is no single agreed definition. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Argument** — a value passed to a function when it is called. See [Chapter 26](../notes/26-function-arguments.md).
- **ASI (artificial superintelligence)** — a hypothetical AI far beyond the best humans in almost all intellectual areas. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Assignment** — binding a name to a value with `=`. See [Chapter 12](../notes/12-relational-logical-assignment-operators.md).
- **Attention** — a mechanism that gives each token weights over other tokens and blends their information. See [Chapter 35](../notes/35-attention-and-transformers.md).

## B

- **Base model** — a model after pretraining only; it continues text but is not yet tuned to follow instructions. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).
- **Boolean** — a value that is `True` or `False`. See [Chapter 05](../notes/05-numeric-types-and-booleans.md).
- **Bug** — a mistake in a program that makes it behave incorrectly. See [Chapter 04](../notes/04-errors-and-identifiers.md).

## C

- **Chunking** — splitting documents into passages for retrieval. See [Chapter 37](../notes/37-retrieval-augmented-generation.md).
- **Comprehension (list comprehension)** — a compact expression that builds a list from an iterable. See [Chapter 20](../notes/20-list-comprehension.md).
- **Conditional** — code that runs only if a condition is true (`if`, `elif`, `else`). See [Chapter 14](../notes/14-conditional-statements.md).
- **Context** — everything a model receives in one call: instructions, history, documents, tool results and the request. See [Chapter 32](../notes/32-context-engineering-and-tokens.md).
- **Context engineering** — designing what goes into the model's input, and in what form and order. See [Chapter 32](../notes/32-context-engineering-and-tokens.md).
- **Context window** — the maximum number of tokens (input plus output) a model can handle in one call. See [Chapter 34](../notes/34-context-window-and-model-parameters.md).
- **Cosine similarity** — a measure of the angle between two vectors, from -1 to 1; used to compare embeddings. See [Chapter 33](../notes/33-vectors-and-embeddings.md).

## D

- **Dictionary (`dict`)** — a collection of key-value pairs. See [Chapter 23](../notes/23-dictionaries.md).
- **Distillation** — training a small model to imitate a larger one. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Dot product** — the sum of the products of matching entries of two vectors. See [Chapter 33](../notes/33-vectors-and-embeddings.md).

## E

- **Embedding** — a vector produced by a trained model to represent text or other data so that similar meanings are close together. See [Chapter 33](../notes/33-vectors-and-embeddings.md).
- **Environment variable** — a named setting stored outside the program, often used for secrets such as API keys. See [Chapter 30](../notes/30-python-wrap-up-and-ai-intro.md).
- **Evaluation** — measuring how well a system performs on a test set. See [Chapter 40](../notes/40-recap-and-final-thoughts.md).
- **Exception** — an error raised while a program runs. See [Chapter 04](../notes/04-errors-and-identifiers.md).

## F

- **f-string** — a string literal prefixed with `f` that evaluates expressions inside braces. See [Chapter 09](../notes/09-string-formatting-and-f-strings.md).
- **Fine-tuning** — continuing the training of a pretrained model on a smaller, targeted dataset. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).
- **First-class function** — a function that can be stored in a variable, passed as an argument and returned. See [Chapter 28](../notes/28-first-class-functions-and-lambda.md).
- **Float** — a number with a fractional part. See [Chapter 05](../notes/05-numeric-types-and-booleans.md).
- **Function** — a named, reusable block of code. See [Chapter 25](../notes/25-defining-functions-and-return-values.md).

## G

- **Gradient descent** — repeatedly adjusting parameters a small step in the direction that reduces the loss. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).
- **Grounding** — tying an answer to supplied sources so claims can be checked. See [Chapter 37](../notes/37-retrieval-augmented-generation.md).

## H

- **Hallucination** — fluent output that is unsupported or false. See [Chapter 31](../notes/31-llms-prompting-temperature-hallucination.md).
- **Host (MCP host)** — the AI application that manages MCP client connections. See [Chapter 38](../notes/38-mcp-and-ai-agents.md).

## I

- **Identifier** — the name given to a variable, function or other object. See [Chapter 04](../notes/04-errors-and-identifiers.md).
- **Immutable** — cannot be changed after creation (for example `str`, `tuple`). See [Chapter 24](../notes/24-mutability-iteration-and-pitfalls.md).
- **Index** — the position of an item in a sequence, starting at 0. See [Chapter 06](../notes/06-strings-basics-indexing-concatenation.md).
- **Inference** — using a trained model to produce outputs, as opposed to training it. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).
- **Integer (`int`)** — a whole number. See [Chapter 05](../notes/05-numeric-types-and-booleans.md).

## K

- **Keyword argument** — an argument passed by name, such as `f(x=1)`. See [Chapter 26](../notes/26-function-arguments.md).
- **Knowledge cutoff** — the date after which a model has no training data. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).

## L

- **Lambda** — a small anonymous function written with `lambda`. See [Chapter 28](../notes/28-first-class-functions-and-lambda.md).
- **List** — an ordered, changeable collection. See [Chapter 18](../notes/18-lists-fundamentals.md).
- **LLM (large language model)** — a neural network trained on large amounts of text to predict the next token. See [Chapter 31](../notes/31-llms-prompting-temperature-hallucination.md).
- **Loop** — code that repeats (`for`, `while`). See [Chapter 16](../notes/16-while-loop-and-loop-control.md) and [Chapter 17](../notes/17-for-loop-range-and-nested-loops.md).
- **Loss** — a number measuring how wrong a prediction was; training tries to reduce it. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).

## M

- **MCP (Model Context Protocol)** — an open protocol for connecting AI applications to tools and data sources. See [Chapter 38](../notes/38-mcp-and-ai-agents.md).
- **Method** — a function attached to an object, called with dot notation. See [Chapter 10](../notes/10-ord-chr-and-string-methods.md).
- **Modality** — a type of data such as text, image or audio. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Module** — a Python file whose names can be imported. See [Chapter 03](../notes/03-builtin-functions-print-and-modules.md).
- **Multimodal** — handling more than one modality. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Mutable** — can be changed after creation (for example `list`, `dict`, `set`). See [Chapter 24](../notes/24-mutability-iteration-and-pitfalls.md).

## N

- **Namespace / scope** — the region of a program where a name is visible. See [Chapter 27](../notes/27-variable-scope.md).
- **Next-token prediction** — the training objective of most language models. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).

## O

- **Operator** — a symbol such as `+` or `==` that acts on values. See [Chapter 11](../notes/11-arithmetic-operators.md).
- **Overfitting** — learning the training data too closely and generalising poorly. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).

## P

- **Parameter (function)** — a name in a function definition that receives an argument. See [Chapter 26](../notes/26-function-arguments.md).
- **Parameter (model)** — a learned number (weight or bias) inside a model. See [Chapter 34](../notes/34-context-window-and-model-parameters.md).
- **Pretraining** — the first, large-scale stage of training a language model on text. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).
- **Prompt** — the text and messages sent to a model. See [Chapter 31](../notes/31-llms-prompting-temperature-hallucination.md).
- **Prompt injection** — instructions hidden in data that try to steer a model. See [Chapter 37](../notes/37-retrieval-augmented-generation.md).

## Q

- **Quantisation** — storing model weights at lower numeric precision to save memory. See [Chapter 34](../notes/34-context-window-and-model-parameters.md).

## R

- **RAG (retrieval-augmented generation)** — retrieving relevant passages and placing them in the prompt so the model answers from them. See [Chapter 37](../notes/37-retrieval-augmented-generation.md).
- **Reasoning model** — a model set up to generate intermediate steps before the final answer. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Return value** — what a function gives back with `return`. See [Chapter 25](../notes/25-defining-functions-and-return-values.md).
- **RLHF (reinforcement learning from human feedback)** — tuning a model using a reward learned from human preference comparisons. See [Chapter 36](../notes/36-pretraining-fine-tuning-rlhf.md).

## S

- **Self-attention** — attention where queries, keys and values come from the same sequence. See [Chapter 35](../notes/35-attention-and-transformers.md).
- **Set** — an unordered collection of unique items. See [Chapter 22](../notes/22-sets.md).
- **Slicing** — extracting part of a sequence with `[start:stop:step]`. See [Chapter 07](../notes/07-string-slicing.md).
- **SLM (small language model)** — a compact language model, cheaper and faster but less broadly capable. See [Chapter 39](../notes/39-multimodal-reasoning-slm-agi-asi.md).
- **Softmax** — a function that turns scores into probabilities adding up to 1. See [Chapter 31](../notes/31-llms-prompting-temperature-hallucination.md).
- **String (`str`)** — a sequence of characters. See [Chapter 06](../notes/06-strings-basics-indexing-concatenation.md).
- **Syntax error** — code that breaks the rules of the language. See [Chapter 04](../notes/04-errors-and-identifiers.md).

## T

- **Temperature** — a setting controlling how random token sampling is. See [Chapter 31](../notes/31-llms-prompting-temperature-hallucination.md).
- **Token** — a unit of text from a model's vocabulary. See [Chapter 32](../notes/32-context-engineering-and-tokens.md).
- **Tokenizer** — the component that converts text to token IDs and back. See [Chapter 32](../notes/32-context-engineering-and-tokens.md).
- **Tool (model tool)** — a function the model can ask an application to run. See [Chapter 38](../notes/38-mcp-and-ai-agents.md).
- **Transformer** — a neural network architecture of stacked attention and feed-forward blocks. See [Chapter 35](../notes/35-attention-and-transformers.md).
- **Tuple** — an ordered, unchangeable collection. See [Chapter 21](../notes/21-tuples.md).
- **Type conversion (casting)** — changing a value from one type to another. See [Chapter 08](../notes/08-type-conversion.md).

## V

- **Variable** — a name bound to a value. See [Chapter 04](../notes/04-errors-and-identifiers.md).
- **Vector** — an ordered list of numbers. See [Chapter 33](../notes/33-vectors-and-embeddings.md).
- **Vector database** — a store that finds the nearest vectors to a query vector quickly. See [Chapter 33](../notes/33-vectors-and-embeddings.md).

## W

- **Weights** — the learned numbers in a model, also called parameters. See [Chapter 34](../notes/34-context-window-and-model-parameters.md).

Back to the [README](../README.md).
