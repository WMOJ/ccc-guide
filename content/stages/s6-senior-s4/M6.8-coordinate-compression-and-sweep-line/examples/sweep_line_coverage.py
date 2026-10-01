import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    pos = 1
    events = []
    for _ in range(n):
        start = int(data[pos])
        end = int(data[pos + 1])
        pos += 2
        events.append((start, 1))
        events.append((end, -1))
    events.sort()

    active = 0
    best = 0
    covered = 0
    prev = events[0][0]
    for x, delta in events:
        if active > 0:
            covered += x - prev
        active += delta
        best = max(best, active)
        prev = x

    print(covered)
    print(best)


if __name__ == "__main__":
    main()
