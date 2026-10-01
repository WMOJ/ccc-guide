import sys


def wrap32(x: int) -> int:
    # Emulates a 32-bit signed int that wraps around on overflow.
    return (x + 2**31) % 2**32 - 2**31


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    start = int(tokens[0])
    step = int(tokens[1])
    count = int(tokens[2])

    exact = start
    lines = []
    for k in range(1, count + 1):
        exact += step
        lines.append(f"{k} {exact} {wrap32(exact)}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
