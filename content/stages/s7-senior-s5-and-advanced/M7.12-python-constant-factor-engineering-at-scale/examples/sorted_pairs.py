import sys

BASE = 1000


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    keys = []
    pos = 1
    for _ in range(n):
        a = int(tokens[pos])
        b = int(tokens[pos + 1])
        pos += 2
        keys.append(a * BASE + b)

    keys.sort()

    lines = []
    for key in keys:
        a, b = divmod(key, BASE)
        lines.append(f"{a} {b}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
