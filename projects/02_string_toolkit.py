"""Project 2 - String toolkit.

Small, tested string utilities built from the Part 2 chapters.

Run:
    python 02_string_toolkit.py --demo
    python 02_string_toolkit.py slugify "Hello, World!"
    python 02_string_toolkit.py caesar "hello" 3
Commands: slugify, palindrome, vowels, caesar, titleclean, wordfreq
Standard library only.
"""
import re
import sys


def slugify(text):
    """'Hello, World!' -> 'hello-world'."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def is_palindrome(text):
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def count_vowels(text):
    return sum(1 for ch in text.lower() if ch in "aeiou")


def caesar(text, shift):
    """Shift letters (both cases) by `shift`; other characters are unchanged."""
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


def title_clean(text):
    return " ".join(word.capitalize() for word in text.split())


def word_frequency(text, top=3):
    counts = {}
    for word in re.findall(r"[a-z']+", text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:top]


def run_demo():
    print(slugify("  Hello, World! Python 3 rocks  "))
    print(is_palindrome("A man, a plan, a canal: Panama"), is_palindrome("Python"))
    print(count_vowels("Learning Python is Fun"))
    secret = caesar("Hello, World!", 3)
    print(secret, "->", caesar(secret, -3))
    print(title_clean("  hELLo    wORLD "))
    print(word_frequency("to be or not to be that is the question"))


def main(argv):
    if not argv or argv[0] == "--demo":
        run_demo()
        return 0
    command, args = argv[0], argv[1:]
    try:
        if command == "slugify":
            print(slugify(args[0]))
        elif command == "palindrome":
            print(is_palindrome(args[0]))
        elif command == "vowels":
            print(count_vowels(args[0]))
        elif command == "caesar":
            print(caesar(args[0], int(args[1])))
        elif command == "titleclean":
            print(title_clean(args[0]))
        elif command == "wordfreq":
            print(word_frequency(args[0]))
        else:
            print("unknown command:", command)
            return 2
    except (IndexError, ValueError):
        print("usage: see the docstring at the top of this file")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
