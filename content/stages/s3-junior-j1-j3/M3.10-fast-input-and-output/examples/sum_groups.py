import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    pos = 0
    groups = int(tokens[pos])
    pos += 1

    results = []
    for g in range(groups):
        k = int(tokens[pos])
        pos += 1
        total = 0
        for j in range(k):
            total += int(tokens[pos])
            pos += 1
        results.append(str(total))

    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    main()
