import sys

LIMIT = 10 ** 7


def main() -> None:
    tokens = sys.stdin.read().split()
    count = int(tokens[0])
    pos = 1
    lines = []
    for k in range(1, count + 1):
        power = int(tokens[pos])
        pos += 1
        reached = 0
        for _ in range(3):
            bound = int(tokens[pos])
            pos += 1
            if bound ** power <= LIMIT:
                reached += 1
        lines.append(f"problem {k}: brute force reaches {reached} of 3 subtasks")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
