import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    a = int(tokens[0])
    b = int(tokens[1])
    m = int(tokens[2])
    # m is prime, so b to the power m - 2 is the inverse of b (Fermat).
    inverse = pow(b, m - 2, m)
    print(f"inverse of {b}: {inverse}")
    print(f"same as pow({b}, -1, {m}): {inverse == pow(b, -1, m)}")
    answer = a * inverse % m
    print(f"{a} / {b} mod {m} = {answer}")
    print(f"check: {answer * b % m == a % m}")


if __name__ == "__main__":
    main()
