import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    period, offset, days = (int(x) for x in tokens[:3])

    if days <= offset:
        count = 0
    else:
        span = days - offset
        count = span // period + (1 if span % period else 0)

    print(count)


if __name__ == "__main__":
    main()
