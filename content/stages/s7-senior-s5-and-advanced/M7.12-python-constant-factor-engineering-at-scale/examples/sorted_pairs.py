import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])

    # Pack pairs (a, b) where we sort by a then b
    PACK = 1000
    pairs = []
    for i in range(1, 2 * n + 1, 2):
        a = int(data[i])
        b = int(data[i + 1])
        packed = a * PACK + b
        pairs.append(packed)

    pairs.sort()

    # Unpack and output
    output = []
    for p in pairs:
        a = p // PACK
        b = p % PACK
        output.append(f"{a} {b}")

    sys.stdout.write("\n".join(output) + "\n")


if __name__ == "__main__":
    main()
