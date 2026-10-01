import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    pos = 1
    meetings = []
    for i in range(n):
        name = data[pos]
        start = int(data[pos + 1])
        end = int(data[pos + 2])
        pos += 3
        meetings.append((end, start, name))

    meetings.sort()

    last_end = 0
    chosen = []
    for end, start, name in meetings:
        if start >= last_end:
            chosen.append(name)
            last_end = end

    print(len(chosen))
    print(*chosen)


if __name__ == "__main__":
    main()
