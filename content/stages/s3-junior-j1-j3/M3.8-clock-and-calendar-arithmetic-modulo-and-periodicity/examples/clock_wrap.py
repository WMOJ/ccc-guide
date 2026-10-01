import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    hour = int(tokens[0])
    offset = int(tokens[1])
    total = hour + offset
    print(total % 24)


if __name__ == "__main__":
    main()
