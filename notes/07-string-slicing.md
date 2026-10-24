# Chapter 07 — String Slicing

> Part 2 — Data Types and Strings · Video: 1:33:40–2:01:13 · Previous: [06 Strings: Basics, Indexing, Concatenation and Repetition](06-strings-basics-indexing-concatenation.md) · Next: [08 Type Conversion](08-type-conversion.md)

**In this chapter:** how to copy a piece of a string with `[start:stop]`, what the default values do, how negative positions work in slices, how a step value lets you skip characters or walk backwards, what happens when positions are out of range, and how `slice` objects work.

**Before you start:** you need positive and negative indexing from [String Indexing](06-strings-basics-indexing-concatenation.md#string-indexing) and [Negative Indexing](06-strings-basics-indexing-concatenation.md#negative-indexing). Recap: the first character of a string is at index `0`, the last is at `len(text) - 1`, and the last is also at `-1`. A string is immutable, which means it cannot be changed after it is created, so every operation on it makes a new string (see [String Basics](06-strings-basics-indexing-concatenation.md#string-basics)). Examples were run with Python 3.13; slicing behaves the same in all Python 3 versions.

---

## String Slicing

**Timestamp:** [1:33:40](https://www.youtube.com/watch?v=J9BI0jGOds8&t=5620s)

**Learning objectives:**

- Explain that a slice `text[start:stop]` includes `start` and excludes `stop`.
- Predict the result when `start` or `stop` is left out or negative.
- Explain why slicing never raises `IndexError` for out-of-range positions, unlike indexing.
- Use slices to extract parts of real text such as codes, extensions and prefixes.

**1. Intuition**

Indexing takes one character out of a string. Slicing takes a stretch. Picture the characters as a row of numbered seats, and picture the numbers as sitting on the left edge of each seat, with one more number at the very end. A slice `text[2:5]` cuts the row at the edge numbered 2 and again at the edge numbered 5, and hands you what is between the cuts. That is why the stop position is not included: it is the cut, not a seat.

```text
 index:    0   1   2   3   4   5
 text:   | P | y | t | h | o | n |
 cuts:   0   1   2   3   4   5   6
```

With cuts numbered like this, `text[2:5]` gives `tho`, and the length of the slice is simply `5 - 2 = 3`.

**2. Why does it exist?**

Programs constantly need part of a text: the first three letters of a code, the file extension, the last four digits of a number, the first 200 characters of a long document. Without slicing you would write loops that pick characters one by one and join them. A slice does the same job in one short, readable expression.

**3. Technical explanation**

A slice is written with a colon inside the square brackets: `text[start:stop]`.

- `start` is the index where the slice begins. The character at `start` is included.
- `stop` is the index where the slice ends. The character at `stop` is not included.
- The result is a new string containing the characters at positions `start`, `start + 1`, ..., `stop - 1`. The original string is unchanged.
- If `start` is left out, it defaults to the beginning (position 0). If `stop` is left out, it defaults to the end of the string. `text[:]` is a full copy.
- Negative numbers count from the end, as in indexing: `-1` is the last character, so `text[-3:]` is the last three characters.
- Positions beyond the ends are clipped to the ends. Slicing never raises `IndexError`. If `start` is at or after `stop` (with the default forward step), the result is an empty string `""`.

Why does the stop position behave this way? "Half-open" ranges (including the start, excluding the stop) have useful properties: `text[:n] + text[n:]` is always the whole text, and `text[a:b]` has length `b - a` when both are in range. The same convention is used by `range()` (see [The range() Function](17-for-loop-range-and-nested-loops.md#the-range-function)).

**4. Syntax**

```text
text[start:stop]
text[:stop]
text[start:]
text[:]
```

This is a pattern, not runnable code.

- `start` and `stop` are integers (positive, negative or zero) or may be omitted.
- The colon is what makes it a slice. `text[2]` is an index and returns one character; `text[2:3]` is a slice and returns a string of length one.
- Slices of a `str` always produce a `str`.

**5. Example 1 — Basic**

```python
text = "Python Programming"

print(text[0:6])
print(text[7:18])
print(text[:6])
print(text[7:])
print(text[:])
print(text[-11:])
print(text[-11:-8])
print(text[:6] + text[6:] == text)
```

Output:

```text
Python
Programming
Python
Programming
Python Programming
Programming
Pro
True
```

Line by line:

- `text[0:6]` takes positions 0 to 5, which spell `Python`. Position 6 is the space and is not included.
- `text[7:18]` takes from `P` of `Programming` to the end. The text has 18 characters, so the stop 18 is the position just after the last character.
- `text[:6]` and `text[7:]` use the default start and the default stop and give the same pieces as before.
- `text[:]` copies the whole string.
- `text[-11:]` starts 11 characters from the end and runs to the end.
- `text[-11:-8]` starts 11 from the end and stops before the 8th from the end, giving three characters.
- The last line shows that cutting at position 6 and joining the two halves always rebuilds the original.

**6. Example 2 — Practical**

Pulling pieces out of fixed-format data. A product code has the pattern `COUNTRY-YEAR-SERIAL`, for example `IN-2025-00417`, and a file name ends with an extension.

```python
product_code = "IN-2025-00417"
country = product_code[:2]
year = product_code[3:7]
serial = product_code[8:]

print(country)
print(year)
print(serial)
print(int(year) + 1)

file_name = "report_final.pdf"
extension = file_name[-3:]
base_name = file_name[:-4]
print(extension)
print(base_name)

phone = "9876543210"
masked = "******" + phone[-4:]
print(masked)
```

Output:

```text
IN
2025
00417
2026
pdf
report_final
******3210
```

Line by line:

- `product_code[:2]` is the first two characters: `IN`.
- `product_code[3:7]` skips `IN-` (positions 0, 1, 2) and takes four characters: the year. A slice of digits is still a string, so `int(year)` is needed for arithmetic (see [Explicit Type Casting](08-type-conversion.md#explicit-type-casting)).
- `product_code[8:]` starts after the second hyphen and runs to the end.
- `file_name[-3:]` is the last three characters. `file_name[:-4]` is everything except the last four characters (the dot and the extension).
- `"******" + phone[-4:]` hides all but the last four digits, a common privacy practice. The number here is made up.

These position-based slices work only when the format is fixed. For variable-width data, use `split()` or `find()` (see [String Methods](10-ord-chr-and-string-methods.md#string-methods)).

**7. Example 3 — Edge case or common mistake**

Out-of-range slices are forgiving, but off-by-one mistakes are silent:

```python
word = "Python"

print(word[2:100])
print(word[10:20])
print(word[4:2])
print(word[-100:3])
print(repr(word[3:3]))
print(word[:3] + word[3:])
```

Output:

```text
thon


Pyt
''
Python
```

Indexing the same positions would be an error:

```python
word = "Python"
print(word[10])
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(word[10])
          ~~~~^^^^
IndexError: string index out of range
```

What happened:

- `word[2:100]`: the stop is clipped to the end of the string, so you get `thon`.
- `word[10:20]`: both positions are beyond the end, so the result is the empty string (the line looks empty in the output).
- `word[4:2]`: the start is after the stop, which gives an empty string, not an error.
- `word[-100:3]`: a very negative start is clipped to the beginning.
- `word[3:3]`: the start equals the stop, so nothing lies between the cuts; `repr()` shows `''`.
- `word[10]`: indexing a single position that does not exist raises `IndexError`.

The classic mistake is expecting the stop to be included. If you want the first three characters, write `word[:3]` (not `word[:2]`). A good check is the length rule: `len(word[a:b])` equals `b - a` when both positions are inside the string.

**8. Common mistakes**

- Expecting `text[0:3]` to include the character at index 3. It stops before it.
- Using an index where a slice is needed: `text[2]` gives one character, not `text[2:]`.
- Expecting an `IndexError` from an out-of-range slice. Slices clip instead, which can hide a wrong position.
- Trying to assign to a slice of a string (`text[0:2] = "ab"`). Strings are immutable; build a new string with `"ab" + text[2:]`.
- Forgetting that the slice of digits is still text, not a number.
- Using slicing on variable-width data such as names or emails, where the positions change from row to row.

**9. Real-world and AI applications**

Slicing is used to take file extensions, prefixes, fixed-width records and the last few characters of identifiers. In text-based AI work, slices are used to truncate a long text to a maximum number of characters before sending it to a model, to preview the first few hundred characters of a document, and to cut a text into pieces of a fixed size. Be careful: a model's limit is counted in tokens, not characters, so a character slice is only an approximate safeguard (see [Context Engineering, Tokens and Token Costs](32-context-engineering-and-tokens.md#tokens-and-token-costs)). The same slice syntax works on lists, tuples and NumPy arrays, so the idea carries straight into data work.

**10. Practice**

1. For `s = "programming"`, write slices that give `pro`, `gram`, `ming` and `programming` (a full copy).
2. For `email = "diya@example.com"`, use `find("@")` to get the part before `@` and the part after it using slices.
3. Write code that takes any string `text` and returns its first half and second half (for odd lengths, put the extra character in the second half). Test on `"abcdef"` and `"abcde"`.
4. Predict the output of `"abcdef"[2:-1]`, `"abcdef"[-4:-1]` and `"abcdef"[3:1]` before you run them.
5. Why does `word[:n] + word[n:]` equal `word` for every integer `n`, including `n = 100` and `n = -100`? Test your answer.

**11. Interview questions**

- *Is the stop index of a slice inclusive?* No. The slice includes `start` and excludes `stop`.
- *What does `text[:]` do?* It returns a new string with the same content (for strings, CPython may return the same object, since strings are immutable).
- *Why does `"abc"[10:]` not raise an error, but `"abc"[10]` does?* Slices clip positions to the valid range; indexing needs one valid position.
- *What does `text[-3:]` return?* The last three characters (or the whole string if it is shorter).

**12. Quick revision**

- `text[start:stop]` includes `start`, excludes `stop`; length is `stop - start` inside the range.
- Omitted `start` means the beginning; omitted `stop` means the end.
- Negative positions count from the end.
- Out-of-range positions are clipped; empty results are `""`, not errors.
- Slicing returns a new string; strings cannot be changed in place.

---

## Slicing with a Step Value

**Timestamp:** [1:50:14](https://www.youtube.com/watch?v=J9BI0jGOds8&t=6614s)

**Learning objectives:**

- Use the full form `text[start:stop:step]`.
- Predict which characters a positive or negative step selects.
- Reverse a string with `[::-1]` and explain how the defaults change when the step is negative.
- Use `slice` objects and explain that `step` can never be zero.

**1. Intuition**

The step is the stride of your walk along the row of characters. A step of 1 visits every seat. A step of 2 visits every second seat. A negative step walks backwards: you start at the right and move left. Walking backwards through the whole row is the way to reverse it.

**2. Why does it exist?**

Taking every other character, every third item, or reversing a sequence are very common jobs. A third number in the slice makes each of them a short expression, without a loop.

**3. Technical explanation**

The full form is `text[start:stop:step]`.

- The step tells Python how far to move after each selected character. The default step is 1.
- With a positive step, Python starts at `start` and moves right, selecting positions `start`, `start + step`, `start + 2 * step`, and so on, while the position is less than `stop`.
- With a negative step, Python starts at `start` and moves left, while the position is greater than `stop`. The stop position is still excluded.
- The defaults depend on the sign of the step. For a positive step: `start` defaults to the beginning and `stop` to the end. For a negative step: `start` defaults to the last character and `stop` to "before the first character". That is why `text[::-1]` walks the entire string backwards.
- A step of `0` is not allowed and raises `ValueError: slice step cannot be zero`.
- With a negative step, you normally write `start` greater than `stop`. If `start` is smaller than `stop`, the result is empty.

A `slice` object captures these three numbers. `slice(start, stop, step)` creates one, and `text[slice(1, 4)]` equals `text[1:4]`. Its method `indices(length)` shows how Python turns defaults and negative numbers into concrete positions for a sequence of a given length.

**4. Syntax**

```text
text[start:stop:step]
text[::step]
text[::-1]
slice(start, stop, step)
```

This is a pattern, not runnable code. Any of `start`, `stop` and `step` can be omitted (but a colon must remain where a value is omitted, if a later value is given).

**5. Example 1 — Basic**

```python
text = "0123456789"

print(text[::2])
print(text[1::2])
print(text[2:8:3])
print(text[::-1])
print(text[::-2])
print(text[8:2:-2])
print(text[-1:-6:-1])
```

Output:

```text
02468
13579
25
9876543210
97531
864
98765
```

Line by line:

- `text[::2]` takes positions 0, 2, 4, 6, 8: every second character from the start.
- `text[1::2]` starts at position 1, giving 1, 3, 5, 7, 9.
- `text[2:8:3]` takes positions 2 and 5 (the next would be 8, which equals `stop` and is excluded).
- `text[::-1]` reverses the string.
- `text[::-2]` walks backwards in steps of two: 9, 7, 5, 3, 1.
- `text[8:2:-2]` starts at position 8 and moves left until it would reach position 2 (excluded): 8, 6, 4.
- `text[-1:-6:-1]` starts at the last character and takes five characters going backwards: 9, 8, 7, 6, 5.

**6. Example 2 — Practical**

A palindrome check (a word that reads the same in both directions), a date reformatter that uses reversal, and taking alternating letters:

```python
def is_palindrome(word):
    cleaned = word.lower()
    return cleaned == cleaned[::-1]


print(is_palindrome("Level"))
print(is_palindrome("Python"))
print(is_palindrome("Racecar"))

date_iso = "2025-03-14"
year = date_iso[:4]
month = date_iso[5:7]
day = date_iso[8:]
print(day + "/" + month + "/" + year)

message = "HWeolrllod"
print(message[::2])
print(message[1::2])
```

Output:

```text
True
False
True
14/03/2025
Hello
World
```

Line by line:

- `cleaned[::-1]` is the reversed string; a palindrome equals its own reverse. `lower()` makes the comparison ignore capital letters (see [String Methods](10-ord-chr-and-string-methods.md#string-methods)).
- The date slices cut the year, month and day out of a fixed-format text and join them in another order.
- The last two lines un-interleave a message hidden by weaving two words, `Hello` and `World`, letter by letter: even positions give one word and odd positions give the other.

The same slices apply to any sequence. Slicing a list with a step works exactly the same way:

```python
numbers = [10, 20, 30, 40, 50, 60]

print(numbers[::2])
print(numbers[::-1])
print(numbers[1:5])
```

Output:

```text
[10, 30, 50]
[60, 50, 40, 30, 20, 10]
[20, 30, 40, 50]
```

(Lists are covered in [Lists in Python](18-lists-fundamentals.md#lists-in-python).)

**7. Example 3 — Edge case or common mistake**

The step of zero, a step that points in the wrong direction, and what slice objects reveal:

```python
text = "abcdef"
print(text[::0])
```

Output:

```text
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    print(text[::0])
          ~~~~^^^^^
ValueError: slice step cannot be zero
```

```python
text = "abcdef"

print(repr(text[1:5:-1]))
print(text[5:1:-1])
print(repr(text[2:5:-1]))
```

Output:

```text
''
fedc
''
```

```python
print(slice(None, None, -1).indices(6))
print(slice(None, None, 1).indices(6))
print(slice(-3, None).indices(6))
print("abcdef"[slice(1, 4)])
```

Output:

```text
(5, -1, -1)
(0, 6, 1)
(3, 6, 1)
bcd
```

What happened:

- A step of 0 would never move, so Python rejects it.
- `text[1:5:-1]` walks left from position 1 but the stop (5) is to the right: nothing lies in that direction, so the result is empty. To walk left, put the larger position first, as in `text[5:1:-1]`, which gives `fedc`.
- `indices(6)` converts the defaults for a six-character string into real numbers. For a backward slice, the default start is 5 and the default stop is -1, which means "before position 0". Writing that `-1` yourself would instead mean "the last character", which is why `text[5:-1:-1]` is empty and why you leave the stop out when you want to reach the beginning.

**8. Common mistakes**

- Reversing with the wrong start and stop: `text[0:len(text):-1]` is empty, because the direction and the bounds disagree. Use `text[::-1]`.
- Writing `text[5:-1:-1]` to reach the beginning; `-1` means the last character, so nothing is selected. Omit the stop instead.
- Expecting the stop to be included when walking backwards. It is still excluded.
- Using a step of 0.
- Forgetting that `[::2]` selects positions 0, 2, 4 (the first, third, fifth characters), which can feel off by one when counting from 1.
- Applying `[::-1]` to reverse words in a sentence. It reverses characters; to reverse words, split and reverse the list.

**9. Real-world and AI applications**

Reversal and striding appear in text puzzles, checksum digits and decoding schemes. In data and AI work, `array[::2]` takes every second sample to downsample a signal, `array[::-1]` flips a sequence or an image axis, and `batch[:, ::-1]` style slices appear in NumPy and PyTorch code. Understanding string slicing makes those expressions easy to read. In text processing, `text[::-1]` is a quick way to test a function that is expected to be symmetric.

**10. Practice**

1. For `s = "abcdefghij"`, write slices for: every second character starting at `a`; every second character starting at `b`; the last four characters in reverse order.
2. Write `is_palindrome` so that it ignores spaces and capital letters, and test it on `"A man a plan a canal Panama"` (hint: remove spaces with `replace`).
3. Predict `"abcdef"[4:0:-2]` and `"abcdef"[::-3]` before running.
4. Use a slice to reverse the order of the digits of the number 12345 (hint: convert to a string, slice, convert back).
5. Explain why `"hello"[0:5:-1]` is empty and what to write to get `olleh`.

**11. Interview questions**

- *How do you reverse a string in Python?* `text[::-1]`. Strings have no `reverse()` method, because they are immutable; `reversed(text)` gives an iterator of characters.
- *What does the third number in a slice mean?* The step: the distance between selected positions; negative means moving backwards.
- *What are the default `start` and `stop` for a negative step?* The last character and "before the first character".
- *What is a `slice` object?* A value that stores `start`, `stop` and `step`, so that a slice can be named, stored and reused.

**12. Quick revision**

- `text[start:stop:step]`; the default step is 1; a step of 0 raises `ValueError`.
- Positive step walks right, negative step walks left; the stop is always excluded.
- `text[::-1]` reverses; `text[::2]` takes every second character.
- For backward slices put the larger position first, or omit both ends.
- `slice(a, b, c)` creates a reusable slice; `.indices(length)` shows the real positions.

---

## Answers to Practice Exercises

### Answers: String Slicing

1.

```python
s = "programming"

print(s[:3])
print(s[3:7])
print(s[-4:])
print(s[:])
```

Output:

```text
pro
gram
ming
programming
```

2.

```python
email = "diya@example.com"
at = email.find("@")

print(email[:at])
print(email[at + 1:])
```

Output:

```text
diya
example.com
```

`find("@")` returns the position of `@` (4). The user name is everything before it (`[:at]`). The domain starts one character after it (`[at + 1:]`), because the `@` itself is skipped.

3.

```python
def halves(text):
    middle = len(text) // 2
    return text[:middle], text[middle:]


print(halves("abcdef"))
print(halves("abcde"))
```

Output:

```text
('abc', 'def')
('ab', 'cde')
```

`len(text) // 2` is whole-number division (see [Arithmetic Operators](11-arithmetic-operators.md#arithmetic-operators)). For five characters the middle is 2, so the first half has two characters and the second half has three.

4. `"abcdef"[2:-1]` is `cde` (position 2 up to, but not including, the last character). `"abcdef"[-4:-1]` is `cde` (positions 2, 3, 4). `"abcdef"[3:1]` is empty because the start is after the stop.

```python
print("abcdef"[2:-1])
print("abcdef"[-4:-1])
print(repr("abcdef"[3:1]))
```

Output:

```text
cde
cde
''
```

5. Cutting at any position and rejoining the two parts gives the original, because every position is clipped into the range 0 to `len(word)`. With `n = 100`, `word[:100]` is the whole word and `word[100:]` is empty. With `n = -100`, `word[:-100]` is empty and `word[-100:]` is the whole word.

```python
word = "Python"

for n in [0, 3, 6, 100, -100, -2]:
    print(n, word[:n] + word[n:] == word)
```

Output:

```text
0 True
3 True
6 True
100 True
-100 True
-2 True
```

(The `for` loop is explained in [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop); here it just repeats the test for each value of `n`.)

### Answers: Slicing with a Step Value

1.

```python
s = "abcdefghij"

print(s[::2])
print(s[1::2])
print(s[-1:-5:-1])
```

Output:

```text
acegi
bdfhj
jihg
```

`s[::2]` starts at `a`; `s[1::2]` starts at `b`; `s[-1:-5:-1]` takes four characters going backwards from the end. `s[:-5:-1]` and `s[::-1][:4]` give the same result.

2.

```python
def is_palindrome(sentence):
    cleaned = sentence.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


print(is_palindrome("A man a plan a canal Panama"))
print(is_palindrome("Hello World"))
```

Output:

```text
True
False
```

3. `"abcdef"[4:0:-2]` starts at position 4 (`e`) and moves left in steps of 2 to position 2 (`c`); the next would be position 0, which is the excluded stop, so the result is `ec`. `"abcdef"[::-3]` starts at the last character (`f`) and takes every third character going left: `fc`.

```python
print("abcdef"[4:0:-2])
print("abcdef"[::-3])
```

Output:

```text
ec
fc
```

4.

```python
number = 12345
reversed_number = int(str(number)[::-1])
print(reversed_number)
```

Output:

```text
54321
```

5. With a negative step, the default and the explicit bounds must point left. `"hello"[0:5:-1]` starts at position 0 and tries to move left, but the stop (5) lies to the right, so the result is empty. Write `"hello"[::-1]`, or `"hello"[4::-1]`, to get `olleh`.

```python
print(repr("hello"[0:5:-1]))
print("hello"[::-1])
print("hello"[4::-1])
```

Output:

```text
''
olleh
olleh
```

---

## Chapter Summary and Key Takeaways

- `text[start:stop]` copies positions `start` to `stop - 1`; leaving a bound out means "from the beginning" or "to the end".
- Negative positions count from the end; out-of-range slice positions are clipped, so slices return `""` rather than raising `IndexError`.
- `text[start:stop:step]` selects every `step`-th position; a negative step walks backwards and changes the defaults, which is why `text[::-1]` reverses a string.
- A step of 0 raises `ValueError`; a step that points away from the stop gives an empty result.
- `slice(start, stop, step)` objects and `.indices(length)` show how Python interprets a slice.
- Slices create new strings and cannot be used to change a string in place.

Next: [Chapter 08 — Type Conversion](08-type-conversion.md) shows how Python converts between numbers, strings and booleans, automatically and on request.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
