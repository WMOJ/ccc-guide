import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return
    n = int(data[0])
    pos = 1

    count = 0
    for i in range(n):
        mark = data[pos]
        mark = int(mark)
        pos += 1
        if mark >= 50:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
