import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return

    year = int(data[0])
    div4 = year % 4 == 0
    div100 = year % 100 == 0
    div400 = year % 400 == 0
    leap = div4
    if div100 and not div400:
        leap = False
    days = 29 if leap else 28
    print(days)


if __name__ == "__main__":
    main()
