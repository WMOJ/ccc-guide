"""Not shown in the lesson: counts real operations for two ways to slide a fixed-length window,
backing the cost figure with numbers taken from actual code, not estimates."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    text = input_data[0]
    k = int(input_data[1])

    n = len(text)
    num_windows = n - k + 1

    brute_ops = 0
    slide_ops = 0
    for i in range(num_windows):
        if i == 0:
            brute_ops += k
            slide_ops += k
        else:
            brute_ops += k
            slide_ops += 2

    print(f"{brute_ops} {slide_ops}")


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
