import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    p = int(tokens[1])
    x = p / n
    lines = []
    for step in range(1, 61):
        x = 2 * min(x, 1 - x)
        p = 2 * min(p, n - p)
        if step % 10 == 0:
            lines.append(f"step {step}: float {x}, exact {p}/{n}")
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
