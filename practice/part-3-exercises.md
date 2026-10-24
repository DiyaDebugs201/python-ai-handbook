# Part 3 — Extra Practice: Operators and Control Flow

> [Practice index](README.md) · [Solutions for this part](solutions/part-3-solutions.md)

These 12 problems go beyond the exercises inside the chapters. Try each one on your own before opening the solutions. Run your code, compare with your prediction, and only then check the solution. Related chapters:

- [Chapter 11 — Operators Overview and Arithmetic Operators](../notes/11-arithmetic-operators.md)
- [Chapter 12 — Relational, Logical and Assignment Operators](../notes/12-relational-logical-assignment-operators.md)
- [Chapter 13 — Identity Operators and Operator Precedence](../notes/13-identity-operators-and-precedence.md)
- [Chapter 14 — Conditional Statements](../notes/14-conditional-statements.md)
- [Chapter 15 — Conditionals: Practice Problems](../notes/15-conditionals-practice.md)
- [Chapter 16 — while Loops and Loop Control](../notes/16-while-loop-and-loop-control.md)
- [Chapter 17 — for Loops, range() and Nested Loops](../notes/17-for-loop-range-and-nested-loops.md)

Tips: write a few lines at a time and run often; if you are stuck for more than ten minutes read only the hint again, then the solution's explanation; afterwards rewrite the solution from memory.

## P3.1 — FizzBuzz

For the numbers 1 to 15 print `Fizz` for multiples of 3, `Buzz` for multiples of 5, `FizzBuzz` for multiples of both, and the number otherwise.

*Hint:* Test the "both" case first, or build the word from parts.

## P3.2 — Grade classifier

Write `grade(score)` returning `A` for 90 and above, `B` for 80 to 89, `C` for 70 to 79, `D` for 60 to 69 and `F` below 60. Print the grades for 95, 80, 79.5, 60 and 12.

*Hint:* An `elif` ladder; order matters.

## P3.3 — Leap year

A year is a leap year if it is divisible by 4, except years divisible by 100, unless also divisible by 400. Test 1900, 2000, 2024 and 2026.

*Hint:* Combine conditions with `and`, `or`, `not`.

## P3.4 — Operator precedence

Predict, then compute: `2 + 3 * 4 ** 2 / 8`, `(2 + 3) * 4 ** 2 / 8`, `-3 ** 2`, `(-3) ** 2`, `not True or True`.

*Hint:* Exponent before multiplication, before addition; unary minus binds less tightly than `**`.

## P3.5 — is versus ==

Create `a = [1, 2]`, `b = [1, 2]`, `c = a`. Print `a == b`, `a is b`, `a is c`. Then show that `None` should be compared with `is`.

*Hint:* `==` compares values, `is` compares identity.

## P3.6 — Sum of digits

Use a `while` loop to compute the sum of the digits of 90871 without converting to a string.

*Hint:* `n % 10` gives the last digit; `n //= 10` removes it.

## P3.7 — Multiplication table

Print a 4 by 4 multiplication table with right-aligned columns of width 4, using nested loops.

*Hint:* An outer loop for rows, an inner loop for columns; `end=""`.

## P3.8 — Primes with for/else

Print all prime numbers up to 30, using a `for ... else` with `break` for the divisibility test.

*Hint:* `else` after a `for` runs only if the loop did not `break`.

## P3.9 — break and continue

Given guesses `[5, 12, -1, 7, 42, 9]`, loop through them: skip negative numbers, stop at the first guess equal to 42, and print each guess that is processed. Then print how many were processed.

*Hint:* `continue` skips to the next iteration; `break` leaves the loop.

## P3.10 — Triangle pattern

Print a right triangle of stars with 5 rows (1 star in the first row, 5 in the last).

*Hint:* `"*" * row`.

## P3.11 — Collatz steps

Starting from 27, repeat: if the number is even halve it, otherwise multiply by 3 and add 1, until it reaches 1. Print the number of steps.

*Hint:* A `while` loop with an `if`/`else`.

## P3.12 — Chained comparisons

Write `in_range(x)` that returns whether `x` is at least 10 and below 20 using a single chained comparison. Test 9, 10, 19 and 20.

*Hint:* `10 <= x < 20`.

---

Solutions: [part-3-solutions.md](solutions/part-3-solutions.md) · Back to the [practice index](README.md).
