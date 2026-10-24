# Chapter 16 — while Loops and Loop Control

> Part 3 — Operators and Control Flow · Video: 4:19:50–4:48:36 · Previous: [15 Conditionals: Practice Problems](15-conditionals-practice.md) · Next: [17 for Loops, range() and Nested Loops](17-for-loop-range-and-nested-loops.md)

**In this chapter:** how to repeat a block of code while a condition is true with `while`, how to stop a loop early with `break`, skip to the next round with `continue`, and leave a block empty on purpose with `pass`; plus infinite loops, how to avoid them, and the `else` clause of a loop.

**Before you start:** you need conditions and indentation from [Conditional Statements](14-conditional-statements.md), and augmented assignment such as `count += 1` from [Assignment Operators](12-relational-logical-assignment-operators.md#assignment-operators). Recap: a condition is an expression that Python treats as true or false; the code that belongs to a statement is indented under it; `x += 1` adds 1 to `x`. Examples were run with Python 3.13. Programs that wait for typed input are shown with scripted values instead, so that the output is always the same.

---

## The while Loop

**Timestamp:** [4:19:50](https://www.youtube.com/watch?v=J9BI0jGOds8&t=15590s)

**Learning objectives:**

- Explain what a loop is and when a `while` loop is the right choice.
- Write a `while` loop with a loop variable that is initialised, tested and updated.
- Recognise and avoid infinite loops, and stop one that is running.
- Use `while True` with `break`, and the `else` clause of a loop.

**1. Intuition**

A loop repeats work. A `while` loop is "keep doing this *while* something is still true": while the kettle has not boiled, keep waiting; while the queue is not empty, serve the next person. You do not know in advance how many rounds it will take. You only know the condition that decides when to stop.

**2. Why does it exist?**

Programs often repeat actions: read lines until a file ends, retry until a request succeeds, keep asking until the user gives a valid answer, keep improving an estimate until it is accurate enough. Writing the same lines again and again is impossible when the number of repetitions is not known. A loop lets one block of code run many times.

**3. Technical explanation**

A `while` statement works like this:

1. Python evaluates the condition.
2. If it is true, the body (the indented block) runs once, and Python goes back to step 1.
3. If it is false, the loop ends, and the program continues after the block.

The condition is tested *before* each round, so if it is false the first time, the body never runs.

A well-formed `while` loop has three parts that involve the *loop variable* (the value the condition looks at):

- **Initialise** it before the loop (`count = 0`).
- **Test** it in the condition (`while count < 5`).
- **Update** it inside the body (`count += 1`) so that the condition eventually becomes false.

If the update is missing or wrong, the condition stays true forever. That is an *infinite loop*: the program never ends and the terminal appears frozen. Stop it with Ctrl+C (which raises `KeyboardInterrupt`). Some infinite loops are intentional, such as a server waiting for requests: `while True:` with a `break` somewhere inside, or a signal to stop.

*The loop's `else` clause.* A `while` loop may have an `else` block. It runs when the condition becomes false in the normal way, and it is skipped if the loop was left with `break` (see the next section). Because the word is easy to misread, many programmers rarely use it.

*Choosing a loop.* Use `while` when you repeat until a condition changes and do not know the count. When you want to visit every item of a collection or repeat a known number of times, a `for` loop is the better tool (see [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop)).

**4. Syntax**

```text
initialise_loop_variable
while condition:
    body_statements
    update_loop_variable
else:
    statements_run_if_the_loop_was_not_ended_by_break
```

This is a pattern, not runnable code. The colon after the condition is required. The body is indented. The `else` part is optional.

**5. Example 1 — Basic**

```python
count = 1
while count <= 5:
    print("Round", count)
    count += 1
print("Loop finished, count is", count)

total = 0
number = 1
while number <= 100:
    total += number
    number += 1
print("Sum of 1 to 100:", total)

n = 10
while n > 0:
    n -= 3
    print(n, end=" ")
print()
```

Output:

```text
Round 1
Round 2
Round 3
Round 4
Round 5
Loop finished, count is 6
Sum of 1 to 100: 5050
7 4 1 -2 
```

Line by line:

- The first loop starts with `count = 1`, tests `count <= 5`, prints, and adds 1. After the fifth round `count` is 6, the condition is false, and the loop ends. The value of `count` after the loop is 6, not 5.
- The second loop adds the numbers from 1 to 100 into `total`, the accumulator pattern from [Assignment Operators](12-relational-logical-assignment-operators.md#assignment-operators).
- The third loop counts down in steps of 3. The loop condition `n > 0` is checked only at the start of each round, so the last value printed (`-2`) is already below 0.

**6. Example 2 — Practical**

A loop that depends on a condition and not on a fixed count: digit sums, the Collatz sequence, savings growth, and input validation with scripted "typed" answers.

```python
number = 4729
digit_sum = 0
while number > 0:
    digit_sum += number % 10
    number //= 10
print("Digit sum:", digit_sum)

value = 6
steps = 0
while value != 1:
    if value % 2 == 0:
        value //= 2
    else:
        value = 3 * value + 1
    steps += 1
print("Collatz steps for 6:", steps)

balance = 1000
years = 0
while balance < 2000:
    balance *= 1.07
    years += 1
print("Years to double at 7%:", years, round(balance, 2))

typed = ["abc", "-5", "250", "42"]
attempt = 0
age = None
while age is None or not 0 <= age <= 120:
    text = typed[attempt]
    attempt += 1
    if text.lstrip("-").isdigit():
        age = int(text)
        if not 0 <= age <= 120:
            print(f"{text!r} is out of range")
    else:
        print(f"{text!r} is not a number")
print("Accepted age:", age)
```

Output:

```text
Digit sum: 22
Collatz steps for 6: 8
Years to double at 7%: 11 2104.85
'abc' is not a number
'-5' is out of range
'250' is out of range
Accepted age: 42
```

Line by line:

- `number % 10` is the last digit and `number //= 10` removes it (see [Arithmetic Operators](11-arithmetic-operators.md#arithmetic-operators)). The loop ends when no digits are left.
- The Collatz loop has no obvious count: it runs until the value reaches 1. (It is believed, but not proven, to stop for every starting number.)
- The compound-interest loop keeps going until the balance is high enough. The number of years is the answer, so a `while` loop is natural.
- The validation loop repeats until the answer is a number in range. In a real program the line `text = typed[attempt]` would be `text = input("Age: ")`; scripted values make the output predictable. `lstrip("-")` allows a leading minus sign before `isdigit()` is tested.

**7. Example 3 — Edge case or common mistake**

An infinite loop is the classic mistake. This is a loop where the update line is missing:

```text
count = 1
while count <= 5:
    print("Round", count)
```

The program would print `Round 1` again and again until you press Ctrl+C. (It is shown as text because running it would never finish.) The loops below are guarded with a safety counter so that they stop:

```python
count = 1
safety = 0
while count <= 3 and safety < 5:
    print("Round", count)
    safety += 1
print("stopped by the safety counter, count is still", count)
```

Output:

```text
Round 1
Round 1
Round 1
Round 1
Round 1
stopped by the safety counter, count is still 1
```

Another subtle infinite loop comes from floating-point numbers. A loop that tests for exact equality may never reach it:

```python
x = 0.0
rounds = 0
while x != 1.0 and rounds < 15:
    x += 0.1
    rounds += 1
print(rounds, x)
```

Output:

```text
15 1.5000000000000002
```

After ten additions, `x` is `0.9999999999999999`, not `1.0`, so `x != 1.0` stays true and `x` sails past 1. Without the `rounds < 15` guard the loop would never end. Use an inequality (`x < 1.0`) or an integer counter instead (floats are explained in [The Float Data Type](05-numeric-types-and-booleans.md#the-float-data-type)).

Other classic problems: updating the wrong variable, updating in the wrong direction (`n += 1` in a countdown), and an off-by-one in the condition (`<` versus `<=`):

```python
n = 3
while n > 0:
    print(n, end=" ")
    n -= 1
print()

n = 3
while n >= 0:
    print(n, end=" ")
    n -= 1
print()
```

Output:

```text
3 2 1 
3 2 1 0 
```

The first loop stops before 0; the second includes it. Decide which one matches the rule you were given.

A loop whose condition is false from the start never runs:

```python
level = 10
while level < 5:
    print("this never prints")
print("skipped the loop")
```

Output:

```text
skipped the loop
```

**8. Common mistakes**

- Forgetting to update the loop variable (infinite loop).
- Updating it in the wrong direction, or updating a different variable.
- Testing floats with `==` or `!=`.
- Off-by-one errors with `<` and `<=`.
- Forgetting to initialise the loop variable before the loop (`NameError`).
- Putting the update line outside the indented body.
- Using a `while` loop when a `for` loop over a collection is simpler.

**9. Real-world and AI applications**

`while` loops are used for retrying a failed network request, polling for a result, reading data until a stream ends, running a game or server loop, and iterative numerical methods that repeat until the error is small enough. In machine learning, training is conceptually a loop that runs until a stopping rule is met (for example, "until validation loss has not improved for several rounds"), and chat applications run a loop that reads a message, calls a model and prints the reply until the user quits. Every such loop needs a clear stopping rule and, in production, a maximum number of rounds as a safety net.

**10. Practice**

1. Print the numbers from 10 down to 1 using a `while` loop, then print `"Liftoff!"`.
2. Compute the factorial of 6 with a `while` loop (the product of the integers from 1 to 6).
3. Count how many digits an integer has by repeatedly dividing by 10. Test with 0 (it has one digit), 7, 1234 and 100000.
4. Starting with 100, how many times can you halve the number (using integer division) before it reaches 0? Print each value.
5. The population of a town is 50,000 and grows 3% per year. After how many years does it first exceed 100,000?
6. Explain why `while x != 10:` is dangerous if `x` starts at 1 and increases by 2, and fix it.

**11. Interview questions**

- *When is a `while` loop better than a `for` loop?* When the number of repetitions is not known in advance and depends on a condition.
- *What is an infinite loop and how do you stop one?* A loop whose condition never becomes false; stop it with Ctrl+C and fix the missing or wrong update.
- *When is the body of a `while` loop never executed?* When the condition is false the first time it is tested.
- *What are the three steps for a safe loop variable?* Initialise, test, update.

**12. Quick revision**

- `while condition:` repeats the body as long as the condition is true; the condition is checked before every round.
- Initialise the loop variable, test it, update it.
- Missing update gives an infinite loop; Ctrl+C stops it.
- Avoid `==` and `!=` with floats; mind `<` versus `<=`.
- Use `while` for "until" loops and `for` for "each item" loops.

---

## The break Statement

**Timestamp:** [4:30:49](https://www.youtube.com/watch?v=J9BI0jGOds8&t=16249s)

**Learning objectives:**

- Use `break` to leave a loop immediately.
- Write the `while True:` loop with a `break` for "repeat until" logic.
- Explain how `break` affects the loop's `else` clause and nested loops.

**1. Intuition**

`break` is an emergency exit. When something happens inside the loop that makes continuing pointless (you found what you were looking for, the user typed "quit", an error occurred), you jump out at once instead of finishing the round and testing the condition.

**2. Why does it exist?**

Sometimes the stopping rule is easier to express in the middle of the loop body than in the loop condition. For example, "read an answer; if it is valid, stop" needs the answer to be read before it can be tested. `break` also allows a search to stop as soon as the item is found.

**3. Technical explanation**

When Python executes `break`, it ends the innermost loop that contains it immediately. Execution continues with the first statement after that loop. The rest of the loop body for the current round is skipped, and the loop condition is not tested again.

- `break` only works inside a loop. Elsewhere it is a `SyntaxError`.
- In nested loops, `break` leaves only the innermost loop.
- If the loop has an `else` block, `break` skips it. This makes the `else` of a loop useful for searches: the `else` means "the loop finished without finding anything".
- `while True:` creates a loop that runs until a `break` (or `return`, or an exception) ends it. This is a common and legitimate pattern, but every such loop must have at least one reachable exit.

**4. Syntax**

```text
while condition:
    ...
    if exit_condition:
        break
    ...
```

This is a pattern, not runnable code. `break` is usually written inside an `if`.

**5. Example 1 — Basic**

```python
for number in [3, 8, 15, 4, 20]:
    if number > 10:
        print("First number above 10:", number)
        break
    print("checked", number)
print("after the loop")

count = 0
while True:
    count += 1
    if count == 3:
        break
print("count is", count)
```

Output:

```text
checked 3
checked 8
First number above 10: 15
after the loop
count is 3
```

Line by line:

- The `for` loop (see [The for Loop](17-for-loop-range-and-nested-loops.md#the-for-loop)) looks at each number in turn. When it reaches 15, `break` ends the loop at once, so `4` and `20` are never examined.
- The `while True:` loop has no condition that can fail, so only the `break` can stop it.

**6. Example 2 — Practical**

A menu loop with scripted choices, a search with `else`, and a prime check:

```python
choices = ["1", "2", "x", "1"]
position = 0
while True:
    choice = choices[position]
    position += 1
    if choice == "x":
        print("Goodbye")
        break
    elif choice == "1":
        print("You chose option 1")
    elif choice == "2":
        print("You chose option 2")
    else:
        print("Unknown option")
print("Choices used:", position)

names = ["Asha", "Ravi", "Meena"]
wanted = "Ravi"
for name in names:
    if name == wanted:
        print(wanted, "found")
        break
else:
    print(wanted, "not found")

wanted = "Kiran"
for name in names:
    if name == wanted:
        print(wanted, "found")
        break
else:
    print(wanted, "not found")


def is_prime(n):
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


print([n for n in range(2, 30) if is_prime(n)])
```

Output:

```text
You chose option 1
You chose option 2
Goodbye
Choices used: 3
Ravi found
Kiran not found
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

Line by line:

- The menu loop runs "forever" and ends only when the choice is `"x"`. In a real program the choice would come from `input()`. The last `"1"` in the script is never read, because the loop was left at `"x"`.
- In the first search, the `break` skips the `else` block, so `not found` is not printed. In the second search the loop runs to the end without `break`, so the `else` block runs. This is the loop-`else` pattern.
- `is_prime` stops testing as soon as a divisor is found (`return` also leaves a loop). It only tests divisors up to the square root of `n`, because a larger divisor would pair with a smaller one that has already been tried.

**7. Example 3 — Edge case or common mistake**

`break` leaves only the innermost loop, and a `while True` without a reachable exit never ends:

```python
for row in range(3):
    for column in range(3):
        if column == 2:
            break
        print(row, column)
    print("end of row", row)
```

Output:

```text
0 0
0 1
end of row 0
1 0
1 1
end of row 1
2 0
2 1
end of row 2
```

The `break` ends the inner `for` each time `column` reaches 2, but the outer loop keeps going, so all three rows are processed. To leave both loops at once, put the loops in a function and use `return`, or set a flag variable that the outer loop checks:

```python
found = None
for row in range(1, 5):
    for column in range(1, 5):
        if row * column == 6:
            found = (row, column)
            break
    if found:
        break
print(found)
```

Output:

```text
(2, 3)
```

`break` outside a loop is a syntax error (shown as text, because it is not valid Python):

```text
x = 5
if x > 3:
    break
```

```text
  File "example.py", line 3
    break
    ^^^^^
SyntaxError: 'break' outside loop
```

A `while True:` loop is dangerous if the exit condition can never happen. For example, if the code waits for the typed answer `"yes"` but the program checks `"Yes"`, the loop never stops. Always test the exit condition with the real kinds of input, and consider a maximum number of rounds as a safety net.

**8. Common mistakes**

- Expecting `break` to leave several nested loops.
- Using `break` outside a loop.
- Writing `while True:` with no reachable `break` or `return`.
- Putting code after `break` in the same block (it never runs).
- Assuming the loop `else` runs when `break` was used. It runs only when the loop was *not* ended by `break`.
- Replacing a clear loop condition with `while True` and `break` when a normal condition would be clearer.

**9. Real-world and AI applications**

`break` is used for early exit in searches, for ending a retry loop after the first success, and for stopping a read loop at an end marker. In machine learning, early stopping is a `break` in the training loop when the validation loss has not improved for a number of rounds. Chat programs use `while True:` with `break` when the user types `quit`. In agent code (see [Model Context Protocol and AI Agents](38-mcp-and-ai-agents.md)), a loop of "ask the model, run a tool, repeat" ends with a `break` when the model gives a final answer or a maximum number of steps is reached.

**10. Practice**

1. Write a loop that goes through `[4, 9, 15, 22, 31]` and stops at the first multiple of 5, printing it.
2. Write a "repeat until valid" loop that uses a scripted list of answers `["", "xx", "7"]` and stops when the answer is a digit string.
3. Use the loop `else` to print `"no even number"` if a list contains no even number, and the first even number otherwise. Test with `[3, 5, 7]` and `[3, 8, 7]`.
4. Write `first_negative(numbers)` that returns the index of the first negative number, or `-1` if there is none.
5. What does this print, and why? `for i in range(5): if i == 3: break` followed by `print(i)`.

**11. Interview questions**

- *What does `break` do?* It ends the innermost loop immediately and continues after it.
- *When does a loop's `else` block run?* When the loop finishes without being ended by `break`.
- *How do you leave two nested loops at once?* Use a function with `return`, or a flag checked by the outer loop.
- *Is `while True:` bad practice?* No, if it contains a reachable exit; it is the usual way to write "repeat until" logic.

**12. Quick revision**

- `break` leaves the innermost loop at once; the rest of the body is skipped.
- `while True:` plus `break` is the standard "repeat until" form.
- A loop's `else` runs only if there was no `break`.
- `break` outside a loop is a `SyntaxError`.
- Nested loops need a flag or a `return` to leave both.

---

## The continue Statement

**Timestamp:** [4:37:52](https://www.youtube.com/watch?v=J9BI0jGOds8&t=16672s)

**Learning objectives:**

- Use `continue` to skip the rest of the current round and start the next.
- Distinguish `continue` from `break`.
- Know the trap of `continue` in a `while` loop before the update line.

**1. Intuition**

`break` leaves the whole loop; `continue` only skips this one round. Picture sorting letters: when you meet an envelope that is not for you, you set it aside and take the next one, but you keep sorting.

**2. Why does it exist?**

Often most items need processing but a few must be skipped (blank lines, invalid records, comments). Without `continue` you would wrap the whole body in an `if` and indent everything one level deeper. `continue` handles the exception early and keeps the main work at the left.

**3. Technical explanation**

When Python executes `continue`, it skips the remaining statements of the loop body for the current round and goes straight to the next round. In a `for` loop it moves to the next item. In a `while` loop it jumps back to the condition test.

Because of that, in a `while` loop the update statement must run *before* a `continue`, or the loop variable will never change and the loop will repeat the same round forever.

`continue` affects only the innermost loop, and it is valid only inside a loop.

**4. Syntax**

```text
for item in collection:
    if skip_condition:
        continue
    process(item)
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
for number in range(1, 11):
    if number % 2 == 0:
        continue
    print(number, end=" ")
print()

for letter in "python":
    if letter == "h":
        continue
    print(letter, end="")
print()
```

Output:

```text
1 3 5 7 9 
pyton
```

Line by line: the first loop skips even numbers and prints the odd ones. The second loop prints every letter of `python` except `h`, because for that letter the `print` is skipped and the loop goes on with `o`.

**6. Example 2 — Practical**

Cleaning data: skip blank lines, comments and invalid values, then process the rest.

```python
lines = ["10", "", "# a comment", "20", "abc", "30", "  ", "-5"]
total = 0
valid_count = 0
for line in lines:
    text = line.strip()
    if text == "" or text.startswith("#"):
        continue
    if not text.lstrip("-").isdigit():
        print("skipping invalid entry:", repr(text))
        continue
    value = int(text)
    if value < 0:
        print("skipping negative value:", value)
        continue
    total += value
    valid_count += 1
print("Total of", valid_count, "valid values:", total)
```

Output:

```text
skipping invalid entry: 'abc'
skipping negative value: -5
Total of 3 valid values: 60
```

Line by line: each `continue` handles one reason to skip a line, and after the checks the lines that remain are valid. The main work (`total += value`) stays at the left margin of the loop, rather than inside three nested `if` statements.

**7. Example 3 — Edge case or common mistake**

In a `while` loop, a `continue` placed before the update creates an infinite loop:

```text
i = 0
while i < 5:
    if i == 2:
        continue
    print(i)
    i += 1
```

When `i` reaches 2, `continue` jumps back to the test without running `i += 1`, so `i` stays 2 forever. (It is shown as text because it never finishes.) The fix is to update first, or to restructure:

```python
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i, end=" ")
print()

# a safer pattern: use a for loop when the count is known
for i in range(1, 6):
    if i == 3:
        continue
    print(i, end=" ")
print()
```

Output:

```text
1 2 4 5 
1 2 4 5 
```

The first loop increments before testing, so every round progresses. A `for` loop over `range` has no such risk, because the loop variable is advanced automatically.

Another detail: `continue` and `break` differ in what happens to the remaining items:

```python
data = [1, 2, 3, 4, 5]

seen_with_continue = []
for x in data:
    if x == 3:
        continue
    seen_with_continue.append(x)

seen_with_break = []
for x in data:
    if x == 3:
        break
    seen_with_break.append(x)

print(seen_with_continue)
print(seen_with_break)
```

Output:

```text
[1, 2, 4, 5]
[1, 2]
```

`continue` skips only the value 3; `break` stops everything at 3.

**8. Common mistakes**

- Putting `continue` before the update statement in a `while` loop.
- Confusing `continue` with `break`.
- Placing code after `continue` in the same block, where it can never run.
- Using many `continue` statements so that the loop's logic is hard to follow. If a loop has three or four of them, consider a helper function.
- Using `continue` where an `if`/`else` would be clearer.

**9. Real-world and AI applications**

Data cleaning loops use `continue` to skip empty rows, comment lines, missing values and records that fail validation. In AI data preparation, you might skip images that fail to load, texts that are empty or too long, and labels outside the known set, while counting how many were skipped (an important number to report). A training loop may skip a batch that contains invalid values after logging the problem.

**10. Practice**

1. Print the numbers 1 to 20 but skip the multiples of 3.
2. From `["apple", "", "kiwi", "  ", "fig"]`, print only the non-blank words in upper case.
3. Sum the positive numbers of `[5, -3, 8, 0, -1, 4]` using `continue` to skip the others.
4. Fix the infinite loop: `i = 0`, `while i < 6:`, `if i % 2 == 0: continue`, `print(i)`, `i += 1`.
5. Print the characters of `"Mississippi"` without repeating a letter that was already printed (hint: keep the printed letters in a string).

**11. Interview questions**

- *What is the difference between `break` and `continue`?* `break` ends the loop; `continue` skips to the next iteration.
- *Why can `continue` cause an infinite loop in a `while` loop?* If it skips the statement that updates the loop variable.
- *Does `continue` work in `for` loops?* Yes; it moves on to the next item.

**12. Quick revision**

- `continue` skips the rest of the current round and starts the next.
- In `for`, the next item follows; in `while`, the condition is re-tested.
- Update the loop variable before `continue` in a `while` loop.
- `break` stops the loop; `continue` only skips one round.

---

## The pass Statement

**Timestamp:** [4:45:36](https://www.youtube.com/watch?v=J9BI0jGOds8&t=17136s)

**Learning objectives:**

- Explain that `pass` does nothing and why Python needs it.
- Use `pass` as a placeholder in blocks, functions and classes.
- Distinguish `pass` from `continue`, `break` and comments.

**1. Intuition**

Python blocks cannot be empty: after a colon, something must follow. `pass` is a polite "nothing here yet" sign: a stand-in statement that does nothing so that the block is valid.

**2. Why does it exist?**

When you outline a program, you often write the structure first (the functions, conditions and classes) and fill in the bodies later. Because Python uses indentation and requires at least one statement in a block, an empty block would be a syntax error. A comment alone does not count as a statement, so `pass` fills the gap.

**3. Technical explanation**

`pass` is a *null statement*: when it runs, nothing happens. It is allowed anywhere a statement is allowed, and its only purpose is to satisfy the syntax. Typical uses:

- A placeholder for code you will write later (`if`, `elif`, `else`, `for`, `while`, `def`, `class`, `try`/`except`).
- A deliberately empty branch, to make a decision explicit (for example, "in this case do nothing").
- An empty class used as a simple container or a custom exception.

How `pass` differs from the other statements: `continue` skips the rest of the current round; `break` leaves the loop; `pass` does nothing and the rest of the block still runs. A comment is not a statement and cannot replace `pass`. An alternative placeholder is the ellipsis literal `...`, which is also valid and is common in unfinished function definitions and type-hint stubs.

Be careful with `except SomeError: pass`. It silently swallows an error and can hide real bugs. If you must ignore an error, catch only the specific exception you expect and add a comment explaining why.

**4. Syntax**

```text
if condition:
    pass
def function_name():
    pass
class ClassName:
    pass
```

This is a pattern, not runnable code.

**5. Example 1 — Basic**

```python
def not_ready_yet():
    pass


class Empty:
    pass


for number in range(3):
    pass

print("function returns:", not_ready_yet())
print("object type:", type(Empty()).__name__)
print("loop variable after the loop:", number)

if 5 > 3:
    pass
else:
    print("never reached")
print("done")
```

Output:

```text
function returns: None
object type: Empty
loop variable after the loop: 2
done
```

Line by line: the function, the class, the loop and the `if` all have valid, empty bodies. Calling the function returns `None`, as any function without a `return` does. The loop ran three times and did nothing, and `number` still holds the last value, 2.

**6. Example 2 — Practical**

Using `pass` as a deliberate "do nothing" branch, and building a program outline:

```python
def classify(n):
    if n < 0:
        pass
    elif n == 0:
        return "zero"
    else:
        return "positive"


print(classify(-3), classify(0), classify(8))

def load_data():
    pass


def clean_data(data):
    pass


def train_model(data):
    pass


def main():
    data = load_data()
    data = clean_data(data)
    model = train_model(data)
    print("pipeline outline ran; model is", model)


main()

for value in ["1", "x", "3"]:
    try:
        number = int(value)
    except ValueError:
        pass
    else:
        print("converted", number)
```

Output:

```text
None zero positive
pipeline outline ran; model is None
converted 1
converted 3
```

Line by line:

- `classify(-3)` returns `None` because the first branch does nothing and the function ends without a `return`. This may or may not be what you want; an explicit `return "negative"` would be clearer.
- The outline shows how `pass` lets you write and run the structure of a program before the details exist. Each stub returns `None`, so `main` runs, but the final message shows `None` for the model. Replacing the stubs one at a time is a good way to build programs step by step.
- In the last loop, `except ValueError: pass` quietly ignores the bad value `"x"`. This is acceptable when ignoring is the intended behaviour, but silently ignoring broad errors is dangerous.

**7. Example 3 — Edge case or common mistake**

An empty block without `pass` is a syntax error, and a comment does not help. These are not valid Python, so they are shown as text:

```text
def not_ready_yet():
    # TODO: write this later
```

```text
  File "example.py", line 3
    
    ^
IndentationError: expected an indented block after function definition on line 1
```

Using `pass` where `continue` was meant changes the behaviour:

```python
numbers = [1, 2, 3, 4, 5, 6]

with_pass = []
for n in numbers:
    if n % 2 == 0:
        pass
    with_pass.append(n)

with_continue = []
for n in numbers:
    if n % 2 == 0:
        continue
    with_continue.append(n)

print(with_pass)
print(with_continue)
```

Output:

```text
[1, 2, 3, 4, 5, 6]
[1, 3, 5]
```

`pass` does nothing, so the `append` after it still runs for every number. `continue` skips the rest of the round, so the even numbers are not added.

A final caution:

```python
def risky(a, b):
    try:
        return a / b
    except Exception:
        pass


print(risky(10, 2))
print(risky(10, 0))
print(risky("10", 2))
```

Output:

```text
5.0
None
None
```

Both failures return `None` with no message, even though they have different causes (division by zero, and a wrong type). The caller cannot tell what went wrong. Catch the specific exception you can handle, and let others show up.

**8. Common mistakes**

- Leaving a block empty (or with only a comment) and getting an `IndentationError`.
- Confusing `pass` with `continue`.
- Writing `except Exception: pass` and hiding real errors.
- Leaving `pass` in finished code where a real implementation was meant.
- Forgetting that a function with only `pass` returns `None`.

**9. Real-world and AI applications**

Teams use `pass` (or `...`) in skeletons: abstract methods, interface definitions, unfinished functions with a `# TODO` comment, empty custom exception classes, and tests that will be filled in. In AI projects, the outline of a pipeline (`load_data`, `clean`, `train`, `evaluate`) is often written as stubs first, then filled in step by step, with each step tested before the next is added.

**10. Practice**

1. Write an outline of a program with three functions (`read_input`, `process`, `show_result`) that run without errors but do nothing yet.
2. Write a class `Marker` with no content. Create two objects of it and print their type names.
3. Explain what is wrong with `if score > 50:` followed only by the comment `# pass the student`, and fix it.
4. In what way do `pass` and `continue` behave differently in a loop that appends numbers to a list? Show with `range(5)`.
5. Rewrite `except Exception: pass` so that it only ignores `ValueError` and prints a message for anything else (hint: a second `except` clause with `raise`, or simply no second clause).

**11. Interview questions**

- *What does `pass` do?* Nothing. It is a placeholder that makes an empty block syntactically valid.
- *What is the difference between `pass` and `continue`?* `pass` does nothing and execution proceeds with the next statement; `continue` jumps to the next loop iteration.
- *Why not just use a comment?* A comment is not a statement; a block must contain at least one statement.
- *Is `...` an alternative to `pass`?* Yes, as a placeholder expression statement, though `pass` states the intent more clearly.

**12. Quick revision**

- `pass` is a statement that does nothing; blocks cannot be empty.
- Use it for placeholders, outlines, empty classes, and deliberate "do nothing" branches.
- Not the same as `continue` or `break`.
- Avoid `except ...: pass` for broad errors.
- A function with only `pass` returns `None`.

---

## Answers to Practice Exercises

### Answers: The while Loop

1.

```python
number = 10
while number >= 1:
    print(number, end=" ")
    number -= 1
print()
print("Liftoff!")
```

Output:

```text
10 9 8 7 6 5 4 3 2 1 
Liftoff!
```

2.

```python
n = 6
factorial = 1
i = 1
while i <= n:
    factorial *= i
    i += 1
print(factorial)
```

Output:

```text
720
```

3.

```python
def count_digits(number):
    number = abs(number)
    digits = 1
    while number >= 10:
        number //= 10
        digits += 1
    return digits


for value in [0, 7, 1234, 100000]:
    print(value, count_digits(value))
```

Output:

```text
0 1
7 1
1234 4
100000 6
```

Starting `digits` at 1 handles the case `0`, which has one digit but would not enter a `while number > 0` loop at all.

4.

```python
value = 100
while value > 0:
    print(value, end=" ")
    value //= 2
print()
```

Output:

```text
100 50 25 12 6 3 1 
```

5.

```python
population = 50000
years = 0
while population <= 100000:
    population *= 1.03
    years += 1
print(years, round(population))
```

Output:

```text
24 101640
```

6. Starting at 1 and adding 2 gives 1, 3, 5, 7, 9, 11, ... The value 10 is never reached, so `x != 10` stays true forever. Use an inequality that also covers jumping past the target:

```python
x = 1
while x < 10:
    x += 2
print(x)
```

Output:

```text
11
```

### Answers: The break Statement

1.

```python
for number in [4, 9, 15, 22, 31]:
    if number % 5 == 0:
        print("first multiple of 5:", number)
        break
```

Output:

```text
first multiple of 5: 15
```

2.

```python
answers = ["", "xx", "7"]
position = 0
while True:
    answer = answers[position]
    position += 1
    if answer.isdigit():
        print("accepted", answer)
        break
    print("invalid:", repr(answer))
```

Output:

```text
invalid: ''
invalid: 'xx'
accepted 7
```

3.

```python
def first_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            print("first even:", n)
            break
    else:
        print("no even number")


first_even([3, 5, 7])
first_even([3, 8, 7])
```

Output:

```text
no even number
first even: 8
```

4.

```python
def first_negative(numbers):
    index = 0
    while index < len(numbers):
        if numbers[index] < 0:
            return index
        index += 1
    return -1


print(first_negative([4, 7, -2, 9]), first_negative([1, 2, 3]), first_negative([]))
```

Output:

```text
2 -1 -1
```

5. It prints `3`. The loop variable `i` keeps its last value after the loop, and `break` stopped the loop when `i` was 3.

```python
for i in range(5):
    if i == 3:
        break
print(i)
```

Output:

```text
3
```

### Answers: The continue Statement

1.

```python
for number in range(1, 21):
    if number % 3 == 0:
        continue
    print(number, end=" ")
print()
```

Output:

```text
1 2 4 5 7 8 10 11 13 14 16 17 19 20 
```

2.

```python
for word in ["apple", "", "kiwi", "  ", "fig"]:
    if word.strip() == "":
        continue
    print(word.upper())
```

Output:

```text
APPLE
KIWI
FIG
```

3.

```python
total = 0
for number in [5, -3, 8, 0, -1, 4]:
    if number <= 0:
        continue
    total += number
print(total)
```

Output:

```text
17
```

4. The update `i += 1` is skipped when `continue` runs. Update first:

```python
i = 0
while i < 6:
    current = i
    i += 1
    if current % 2 == 0:
        continue
    print(current, end=" ")
print()
```

Output:

```text
1 3 5 
```

5.

```python
printed = ""
for letter in "Mississippi":
    if letter in printed:
        continue
    printed += letter
    print(letter, end="")
print()
```

Output:

```text
Misp
```

### Answers: The pass Statement

1.

```python
def read_input():
    pass


def process(data):
    pass


def show_result(result):
    pass


show_result(process(read_input()))
print("outline runs")
```

Output:

```text
outline runs
```

2.

```python
class Marker:
    pass


first = Marker()
second = Marker()
print(type(first).__name__, type(second).__name__, first is second)
```

Output:

```text
Marker Marker False
```

3. A comment is not a statement, so the block is empty, and Python raises `IndentationError: expected an indented block`. Add `pass` (or a real statement):

```python
score = 60
if score > 50:
    pass  # pass the student
print("ok")
```

Output:

```text
ok
```

4.

```python
with_pass = []
with_continue = []
for n in range(5):
    if n % 2 == 0:
        pass
    with_pass.append(n)
for n in range(5):
    if n % 2 == 0:
        continue
    with_continue.append(n)
print(with_pass, with_continue)
```

Output:

```text
[0, 1, 2, 3, 4] [1, 3]
```

5.

```python
def to_int(text):
    try:
        return int(text)
    except ValueError:
        pass
    return None


print(to_int("42"), to_int("x"))
```

Output:

```text
42 None
```

Only `ValueError` is caught. Any other exception (for example `TypeError` for `to_int(None)`) is not handled and appears as a normal error, which is what you want.

---

## Chapter Summary and Key Takeaways

- `while condition:` repeats its body while the condition is true; initialise, test and update the loop variable, or the loop becomes infinite (stop it with Ctrl+C).
- `while True:` with `break` is the standard "repeat until" form; every such loop needs a reachable exit.
- `break` leaves the innermost loop at once and skips the loop's `else`; `continue` skips to the next round (update the loop variable first in a `while` loop); `pass` does nothing and only fills an empty block.
- A loop's `else` runs only when the loop ended without `break`, which makes it handy for searches.
- Avoid `==` / `!=` with floats in loop conditions, and check `<` versus `<=` at the boundaries.

Next: [Chapter 17 — for Loops, range() and Nested Loops](17-for-loop-range-and-nested-loops.md) covers the loop that visits every item of a collection or repeats a known number of times.

For definitions of terms, see the [glossary](../docs/GLOSSARY.md).
