import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    idx = 0
    n = int(tokens[idx])
    idx += 1

    total = 0
    for i in range(n):
        val = int(tokens[idx])
        idx += 1
        total += val

    sys.stdout.write(str(total) + "\n")


if __name__ == "__main__":
    main()
