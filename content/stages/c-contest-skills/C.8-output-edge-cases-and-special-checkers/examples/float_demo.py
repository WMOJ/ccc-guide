import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    a = int(tokens[0])
    b = int(tokens[1])
    q = a / b
    print(q)
    print(f"{q:.6f}")
    print(f"{q:.2f}")


if __name__ == "__main__":
    main()
