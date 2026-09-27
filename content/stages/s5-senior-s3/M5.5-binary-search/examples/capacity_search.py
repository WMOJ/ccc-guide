import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    trips = int(input_data[1])
    weights = [int(x) for x in input_data[2 : 2 + n]]

    def trips_needed(cap: int) -> int:
        used = 1
        load = 0
        for w in weights:
            if load + w > cap:
                used += 1
                load = w
            else:
                load += w
        return used

    lo = max(weights)
    hi = sum(weights)

    while lo < hi:
        mid = (lo + hi) // 2
        if trips_needed(mid) <= trips:
            hi = mid
        else:
            lo = mid + 1

    print(lo)


if __name__ == "__main__":
    main()
