import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    digits = tokens[0]

    freq = [0] * 10
    for char in digits:
        freq[int(char)] += 1

    lines = []
    for d in range(10):
        if freq[d] > 0:
            lines.append(f"{d}: {freq[d]}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
