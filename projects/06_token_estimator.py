"""Project 6 - Token estimator and cost calculator.

IMPORTANT: this is a rough ESTIMATOR, not a real tokenizer. Real token counts
depend on the model. Prices are inputs YOU supply; the demo uses invented
prices. Use your provider's token counter and price list for real budgets.

Run:
    python 06_token_estimator.py --demo
    python 06_token_estimator.py "text to measure" --input-price 2 --output-price 8 --output-tokens 200
Standard library only.
"""
import argparse
import sys


def estimate_by_chars(text):
    return max(1, round(len(text) / 4)) if text else 0


def estimate_by_words(text):
    return round(len(text.split()) / 0.75)


def estimate_range(text):
    """Return (low, high) from the two rules of thumb; real counts can fall outside it."""
    a, b = estimate_by_chars(text), estimate_by_words(text)
    return min(a, b), max(a, b)


def call_cost(input_tokens, output_tokens, input_price_per_million, output_price_per_million):
    return (input_tokens * input_price_per_million + output_tokens * output_price_per_million) / 1_000_000


def fits_window(input_tokens, reserved_output, window):
    return input_tokens + reserved_output <= window


def conversation_input_tokens(turn_tokens, turns):
    """Total input tokens processed if the whole history is re-sent on every turn."""
    return sum(turn_tokens * t for t in range(1, turns + 1))


def run_demo():
    text = "Summarise the following article in three bullet points. " + "word " * 100
    low, high = estimate_range(text)
    print(f"estimated input tokens: {low} to {high}")
    cost = call_cost(high, 200, 2.0, 8.0)          # invented prices per million tokens
    print(f"one call (invented prices): {cost:.6f}; 10,000 calls: {cost * 10_000:.2f}")
    print("fits an 8,000-token window with 1,000 reserved:", fits_window(high, 1000, 8000))
    print("10-turn chat of 150 tokens per turn re-sends:", conversation_input_tokens(150, 10), "input tokens")


def main(argv):
    if not argv or argv[0] == "--demo":
        run_demo()
        return 0
    parser = argparse.ArgumentParser(description="Rough token and cost estimator (not a real tokenizer).")
    parser.add_argument("text")
    parser.add_argument("--input-price", type=float, required=True, help="price per million input tokens")
    parser.add_argument("--output-price", type=float, required=True, help="price per million output tokens")
    parser.add_argument("--output-tokens", type=int, default=0)
    args = parser.parse_args(argv)
    low, high = estimate_range(args.text)
    print(f"estimated input tokens: {low} to {high}")
    print(f"estimated cost range: {call_cost(low, args.output_tokens, args.input_price, args.output_price):.6f} "
          f"to {call_cost(high, args.output_tokens, args.input_price, args.output_price):.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
