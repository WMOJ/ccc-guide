import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    hour = int(tokens[0])
    minute = int(tokens[1])
    added = int(tokens[2])

    total = hour * 60 + minute + added
    hours_total, minutes = divmod(total, 60)
    days, hours = divmod(hours_total, 24)

    print(days, hours, minutes)


if __name__ == "__main__":
    main()
