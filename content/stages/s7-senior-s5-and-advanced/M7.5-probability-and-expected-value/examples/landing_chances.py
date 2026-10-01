import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    p = float(tokens[1])
    q = 1 - p
    land = [0.0] * n
    land[0] = 1.0
    for i in range(1, n):
        land[i] = p * land[i - 1]
        if i >= 2:
            land[i] += q * land[i - 2]
    # One turn ends on each square 1..n-1 at most once, plus the last turn.
    expected = 1 + sum(land[1:])
    print(land)
    print(f"expected turns: {expected:.4f}")


if __name__ == "__main__":
    main()
