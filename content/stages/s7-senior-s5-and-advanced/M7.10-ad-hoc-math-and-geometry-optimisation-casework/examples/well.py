import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    n = int(data[0])
    houses = []
    for i in range(n):
        houses.append(int(data[1 + i]))
    houses.sort()

    prefix = [0]
    for h in houses:
        prefix.append(prefix[-1] + h)

    best_at = 0
    best_cost = None
    for i in range(n):
        h = houses[i]
        left = h * i - prefix[i]
        right = prefix[n] - prefix[i + 1] - h * (n - 1 - i)
        if best_cost is None or left + right < best_cost:
            best_at = h
            best_cost = left + right

    print(best_at, best_cost)


if __name__ == "__main__":
    main()
