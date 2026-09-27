"""Demonstrations of common output format mistakes and fixes."""

# Single integer: correct
n = 42
print(n)

# Multiple integers on one line: correct (no trailing space)
numbers = [1, 2, 3, 4, 5]
print(" ".join(map(str, numbers)))

# Floating point with specific precision: correct (2 decimals)
value = 3.14159
print(f"{value:.2f}")

# Multiple lines: correct
items = ["apple", "banana", "cherry"]
print("\n".join(items))

# Correct way to handle output with no trailing space on last line
lines = ["first", "second", "third"]
print("\n".join(lines))
