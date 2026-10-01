import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    n = int(data[0])
    pos = 1
    jobs = []
    for i in range(n):
        name = data[pos]
        t = int(data[pos + 1])
        d = int(data[pos + 2])
        pos += 3
        jobs.append((d, name, t))

    jobs.sort()

    clock = 0
    worst = -10 ** 9
    for d, name, t in jobs:
        clock += t
        late = clock - d
        worst = max(worst, late)

    print(*[j[1] for j in jobs])
    print(worst)


if __name__ == "__main__":
    main()
