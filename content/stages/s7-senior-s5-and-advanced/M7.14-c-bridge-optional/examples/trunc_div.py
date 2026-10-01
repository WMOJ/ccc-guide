import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    a = int(tokens[0])
    b = int(tokens[1])

    # C++ divides toward zero, and its remainder takes the sign of a.
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    r = a - q * b

    print(f"python {a // b} {a % b}")
    print(f"c++ {q} {r}")


if __name__ == "__main__":
    main()
