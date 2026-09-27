import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    text = input_data[0]
    pattern = input_data[1]

    if len(pattern) > len(text):
        return

    base = 31
    mod = (1 << 61) - 1

    pattern_len = len(pattern)
    text_len = len(text)

    # Precompute powers
    powers = [1] * (pattern_len + 1)
    for i in range(1, pattern_len + 1):
        powers[i] = (powers[i - 1] * base) % mod

    # Hash the pattern
    pattern_hash = 0
    for c in pattern:
        pattern_hash = (pattern_hash * base + ord(c)) % mod

    # Hash the first window
    window_hash = 0
    for i in range(pattern_len):
        window_hash = (window_hash * base + ord(text[i])) % mod

    matches = []
    if window_hash == pattern_hash:
        matches.append(0)

    # Slide the window
    for i in range(1, text_len - pattern_len + 1):
        # Remove the leftmost character
        left_val = ord(text[i - 1]) * powers[pattern_len - 1]
        window_hash = (window_hash - left_val) % mod
        # Shift left and add the new rightmost character
        window_hash = (window_hash * base + ord(text[i + pattern_len - 1])) % mod

        if window_hash == pattern_hash:
            matches.append(i)

    for pos in matches:
        print(pos)


if __name__ == "__main__":
    main()
