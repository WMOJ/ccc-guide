"""Four common output shapes, each written the way a judge expects it."""

# A single integer.
n = 42
print(n)

# Several integers on one line, one space between them, no trailing space.
numbers = [1, 2, 3, 4, 5]
print(" ".join(map(str, numbers)))

# A float rounded to a fixed number of decimal places, not Python's default.
value = 3.14159
print(f"{value:.2f}")

# One item per line, with no blank line at the end.
items = ["apple", "banana", "cherry"]
print("\n".join(items))
