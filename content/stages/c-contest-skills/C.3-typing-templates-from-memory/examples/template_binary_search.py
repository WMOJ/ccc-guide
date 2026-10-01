import sys


def trips_for(weights, cap):
    used = 1
    load = 0
    for w in weights:
        if load + w > cap:
            used += 1
            load = w
        else:
            load += w
    return used


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    trips = int(data[1])
    weights = [int(x) for x in data[2 : 2 + n]]
    del data

    lo = max(weights)
    hi = sum(weights)

    while lo < hi:
        mid = (lo + hi) // 2
        if trips_for(weights, mid) <= trips:
            hi = mid
        else:
            lo = mid + 1

    print(lo)


if __name__ == "__main__":
    main()
