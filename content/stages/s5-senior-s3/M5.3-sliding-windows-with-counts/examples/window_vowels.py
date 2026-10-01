"""Fixed-length window, no matches counter: the most vowels in any window of length K."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    text = input_data[0]
    k = int(input_data[1])

    vowels = set("aeiou")

    count = 0
    for i in range(k):
        if text[i] in vowels:
            count += 1

    best = count
    for right in range(k, len(text)):
        if text[right] in vowels:
            count += 1
        if text[right - k] in vowels:
            count -= 1
        best = max(best, count)

    print(best)


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
