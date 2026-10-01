import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])

    values = []
    d = 1
    while d <= n:
        q = n // d
        values.append(q)
        d = n // q + 1
    values.reverse()

    cost = {}
    for v in values:
        total = v
        d = 2
        while d <= v:
            q = v // d
            last = v // q
            total += cost[q] * (last - d + 1)
            d = last + 1
        cost[v] = total

    print(len(values))
    print(cost[n])


if __name__ == "__main__":
    main()
