import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    pos = 1
    jobs = []
    for i in range(n):
        name = data[pos]
        t = int(data[pos + 1])
        w = int(data[pos + 2])
        pos += 3
        jobs.append((t / w, name, t, w))

    jobs.sort()

    clock = 0
    cost = 0
    for ratio, name, t, w in jobs:
        clock += t
        cost += w * clock

    print(*[j[1] for j in jobs])
    print(cost)


if __name__ == "__main__":
    main()
