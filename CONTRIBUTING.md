# Contributing

Thank you for helping to improve the *Python + AI — Complete Learning Handbook*. This is a learning resource, so clarity and correctness matter more than volume. Small, focused improvements are very welcome.

## Ways to help

- **Fix errors**: typos, wrong explanations, broken links or anchors, code that does not run or whose printed output does not match.
- **Improve explanations**: clearer analogies, better examples, sharper "common mistakes".
- **Update changing facts**: protocols, product features, limits and prices change. If you update a fact, cite the official source and the date you checked.
- **Add practice problems** with working solutions.
- **Report unclear passages** by opening an issue that quotes the passage and says what was confusing.

## Ground rules

1. **Independent writing.** Notes are written in the contributor's own words. Do not paste transcripts, subtitles, lyrics, or text copied from books, articles or documentation. Short quotations of official terms or error messages are fine. Do not attribute statements to the course instructor.
2. **No secrets, ever.** Never commit API keys, tokens, passwords or personal data. Use placeholders such as `your-key-here`. The file `.env` is ignored by Git; only `.env.example` is committed.
3. **Code must run.** Every Python block in `notes/`, `practice/` and `projects/` must be valid Python 3 and its shown output must be the real output. Python blocks that show broken or incomplete code, pseudocode, patterns, or anything needing an AI service must use a `text` fence, not a `python` fence, and must say what they are.
4. **Label AI code honestly.** Code that imitates AI ideas must be marked as a *toy demo*. Code that needs an AI service or an extra package must be marked as such, and must not contain real credentials.
5. **Keep the structure.** Each topic follows the template used throughout the notes (timestamp, learning objectives, intuition, why it exists, technical explanation, syntax, three examples, common mistakes, applications, practice, interview questions, quick revision). Section headings must match `SYLLABUS_MAPPING.md` so that links keep working.
6. **Be fair and careful.** Present contested topics (such as AGI timelines) as debates, not as settled facts. Avoid claims you cannot support.

## How to propose a change

1. Fork the repository and create a branch with a short descriptive name.
2. Make your change. Keep each pull request focused on one topic.
3. Run the code you touched. For a note, re-run each Python block and compare the output with what is printed.
4. Check links and anchors in the files you changed. Heading anchors follow GitHub's rules (lower case, spaces become hyphens, punctuation removed).
5. Update `PROGRESS_TRACKER.md` or `SYLLABUS_MAPPING.md` if you add or move a topic.
6. Open a pull request that says what you changed and why, and which files you ran or checked.

## Style guide

- Prefer short sentences and plain words. Define a term the first time you use it, or link to the [glossary](docs/GLOSSARY.md).
- Use everyday analogies and say where an analogy stops being accurate.
- Use `python` fences only for valid Python; show output in a separate `text` block after the word "Output:".
- Avoid output that changes between runs (random values without a seed, timings, memory addresses, unordered sets of strings).
- Keep examples small and self-contained; use only the standard library unless a section clearly says otherwise.
- Use British or American spelling consistently within a file; the existing notes use British spelling for prose.

## Code of conduct

Be kind and constructive. Assume good intent, give specific and respectful feedback, and welcome beginners. Harassment or discrimination is not acceptable.

## Licence

This repository does not include a licence file. If you plan to publish your own copy, choose a licence yourself (the README suggests options); contributions are accepted on the understanding that the repository owner decides on the licence.
