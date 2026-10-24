"""Project 7 - Toy RAG retriever.

A miniature retrieval-augmented pipeline: chunk documents, vectorize them with
simple word counts (NOT learned embeddings), retrieve the best chunks with cosine
similarity, and assemble a prompt. The model call is a fake stand-in so the
program runs offline and prints the same output every time. Nothing here calls
an AI service.

Run:
    python 07_toy_rag_retriever.py --demo
    python 07_toy_rag_retriever.py "How long do refunds take?"
Standard library only.
"""
import math
import re
import sys
from collections import Counter

STOP_WORDS = frozenset({"a", "an", "the", "is", "are", "of", "to", "for", "in", "on", "i", "my", "do", "does",
                        "how", "can", "what", "with", "and", "long", "take", "takes"})

DOCUMENTS = {
    "refunds.txt": "Refunds are available within 30 days of purchase with a receipt. Gift cards cannot be refunded. "
                   "Approved refunds are paid back within five working days.",
    "shipping.txt": "Standard shipping takes five working days. Express shipping takes two working days. "
                    "Shipping to remote areas can take up to ten working days.",
    "accounts.txt": "Reset your password from the account settings page. Two step sign in can be enabled in settings.",
}


def chunk_text(source, text, max_words=14, overlap=3):
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        chunks.append({"source": source, "text": " ".join(words[start:start + max_words])})
        if start + max_words >= len(words):
            break
        start += max_words - overlap
    return chunks


def vectorize(text):
    return Counter(w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP_WORDS)


def cosine(a, b):
    dot = sum(a[w] * b[w] for w in a if w in b)
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def build_index(documents):
    chunks = [c for source, text in documents.items() for c in chunk_text(source, text)]
    return [(chunk, vectorize(chunk["text"])) for chunk in chunks]


def retrieve(index, question, k=2, min_score=0.15):
    q = vectorize(question)
    scored = sorted(((cosine(q, vec), chunk) for chunk, vec in index), key=lambda pair: pair[0], reverse=True)
    return [(round(score, 3), chunk) for score, chunk in scored[:k] if score >= min_score]


def build_prompt(question, hits):
    sources = "\n".join(f"[{i}] ({chunk['source']}) {chunk['text']}" for i, (_, chunk) in enumerate(hits, 1))
    return ("Answer using only the numbered sources and cite them like [1]. If they do not contain the answer, say so.\n\n"
            f"Sources:\n{sources}\n\nQuestion: {question}")


def fake_model(prompt):
    """Stand-in for a language model: echoes the first source line, or says it does not know."""
    lines = [line for line in prompt.splitlines() if line.startswith("[1]")]
    return lines[0] if lines else "I could not find that in the documents."


def answer(index, question):
    hits = retrieve(index, question)
    return hits, build_prompt(question, hits), fake_model(build_prompt(question, hits))


def run_demo():
    index = build_index(DOCUMENTS)
    print("chunks indexed:", len(index))
    for question in ["Can I get a refund on a gift card?", "How long does express shipping take?", "Who won the football match?"]:
        hits, prompt, reply = answer(index, question)
        print("\nQ:", question)
        print("retrieved:", [(score, chunk["source"]) for score, chunk in hits])
        print("A:", reply)
    print("\n--- prompt sent for the last answerable question ---")
    print(build_prompt("How long does express shipping take?", retrieve(index, "How long does express shipping take?")))


def main(argv):
    if not argv or argv[0] == "--demo":
        run_demo()
        return 0
    index = build_index(DOCUMENTS)
    hits, prompt, reply = answer(index, " ".join(argv))
    print(prompt)
    print("\nFake model reply:", reply)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
