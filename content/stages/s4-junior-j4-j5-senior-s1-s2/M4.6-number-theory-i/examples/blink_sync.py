import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    pos = 0
    q = int(tokens[pos])
    pos += 1
    lines = []
    for _ in range(q):
        a = int(tokens[pos])
        b = int(tokens[pos + 1])
        t = int(tokens[pos + 2])
        pos += 3
        x = a
        y = b
        while y != 0:
            x, y = y, x % y
        g = x
        period = a * b // g
        remainder = t % period
        if remainder == 0:
            answer = t
        else:
            answer = t + (period - remainder)
        lines.append(str(answer))
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
