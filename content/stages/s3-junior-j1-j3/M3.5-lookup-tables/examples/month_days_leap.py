import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    pos = 0
    year = int(data[pos])
    pos += 1
    month = int(data[pos])
    pos += 1

    days = days_in_month[month]
    is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    if month == 2 and is_leap:
        days = 29

    sys.stdout.write(f"{days}\n")


if __name__ == "__main__":
    main()
