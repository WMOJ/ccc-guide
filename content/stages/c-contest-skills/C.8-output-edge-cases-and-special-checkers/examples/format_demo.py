import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    built = ""
    for t in tokens:
        built += t + " "
    joined = " ".join(tokens)
    print(repr(built))
    print(repr(joined))


if __name__ == "__main__":
    main()
