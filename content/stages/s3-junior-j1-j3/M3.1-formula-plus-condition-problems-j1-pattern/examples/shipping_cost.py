import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return
    kg = int(data[0])
    km = int(data[1])

    cost = kg * 2
    cost += km // 10

    if cost <= 20:
        print("Standard")
    elif cost <= 50:
        print("Priority")
    else:
        print("Express")


if __name__ == "__main__":
    main()
