import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    values = []
    for k in range(n):
        values.append(int(tokens[1 + k]))

    rest = values
    total = 0
    copied = 0
    while rest:
        total += rest[0]
        rest = rest[1:]
        copied += len(rest)

    index_total = 0
    for i in range(n):
        index_total += values[i]
    print(total, copied, index_total)


if __name__ == "__main__":
    main()
