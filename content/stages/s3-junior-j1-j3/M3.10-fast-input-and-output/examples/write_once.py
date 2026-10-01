import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    idx = 0
    n = int(tokens[idx])
    idx += 1

    results = []
    for i in range(n):
        val = int(tokens[idx])
        idx += 1
        results.append(str(val * val))

    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    main()
