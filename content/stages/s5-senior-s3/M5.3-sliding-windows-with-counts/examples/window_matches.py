"""Fixed-length window with a matches counter: find every start of a permutation of a pattern."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    text = input_data[0]
    pattern = input_data[1]

    k = len(pattern)
    target_count = [0] * 26
    for char in pattern:
        target_count[ord(char) - ord("a")] += 1

    window_count = [0] * 26
    matches = 0
    for i in range(26):
        if target_count[i] == 0:
            matches += 1

    starts = []
    for right in range(len(text)):
        right_idx = ord(text[right]) - ord("a")
        if window_count[right_idx] == target_count[right_idx]:
            matches -= 1
        window_count[right_idx] += 1
        if window_count[right_idx] == target_count[right_idx]:
            matches += 1

        if right >= k:
            left_idx = ord(text[right - k]) - ord("a")
            if window_count[left_idx] == target_count[left_idx]:
                matches -= 1
            window_count[left_idx] -= 1
            if window_count[left_idx] == target_count[left_idx]:
                matches += 1

        if right >= k - 1 and matches == 26:
            starts.append(right - k + 1)

    if starts:
        print(" ".join(str(s) for s in starts))
    else:
        print("none")


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
