import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = int(data[0])
    sys.stdout.write(f"{days_in_month[month]}\n")


if __name__ == "__main__":
    main()
