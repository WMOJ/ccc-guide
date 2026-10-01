import sys

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    day_number = int(tokens[0])
    print(DAY_NAMES[day_number % 7])


if __name__ == "__main__":
    main()
