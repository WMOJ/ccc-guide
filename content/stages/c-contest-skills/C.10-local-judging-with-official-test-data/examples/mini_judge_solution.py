import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    values = list(map(int, data[1 : 1 + n]))
    for v in values:
        print(v * 2)


if __name__ == "__main__":
    main()
