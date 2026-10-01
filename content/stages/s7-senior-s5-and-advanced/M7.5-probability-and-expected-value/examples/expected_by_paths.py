import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    p = float(tokens[1])
    q = 1 - p
    # Each entry: (square, chance of this path, turns taken so far).
    stack = [(0, 1.0, 0)]
    paths = 0
    expected = 0.0
    while stack:
        square, chance, turns = stack.pop()
        if square >= n:
            paths += 1
            expected += chance * turns
            continue
        stack.append((square + 1, chance * p, turns + 1))
        stack.append((square + 2, chance * q, turns + 1))
    print(f"paths: {paths}")
    print(f"expected turns: {expected:.4f}")


if __name__ == "__main__":
    main()
