import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    gaps = []
    for i in range(1, n):
        a = int(tokens[i])
        b = int(tokens[i + 1])
        gap = b - a
        gaps.append(gap)
    print(max(gaps))


if __name__ == "__main__":
    main()
