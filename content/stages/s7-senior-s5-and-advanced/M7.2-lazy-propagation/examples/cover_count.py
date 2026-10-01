import sys


def main() -> None:
    data = sys.stdin.read().split()
    lines = []
    for token in data:
        size = int(token)
        lo = 1 + size
        hi = size - 1 + size
        nodes = 0
        while lo < hi:
            if lo % 2 == 1:
                nodes += 1
                lo += 1
            if hi % 2 == 1:
                hi -= 1
                nodes += 1
            lo //= 2
            hi //= 2
        lines.append("size " + str(size) + ": " + str(size - 2) + " leaves, " + str(nodes) + " nodes")

    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
