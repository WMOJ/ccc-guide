import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos])
    pos += 1
    k = int(data[pos])
    pos += 1
    values = [int(x) for x in data[pos:pos + n]]
    pos += n

    window_sum = sum(values[0:k])
    best = window_sum

    for start in range(1, n):
        leaving = values[(start - 1) % n]
        entering = values[(start + k - 1) % n]
        window_sum = window_sum - leaving + entering
        best = max(best, window_sum)

    print(best)


if __name__ == "__main__":
    main()
