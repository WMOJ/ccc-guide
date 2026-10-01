import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    max_signs = int(data[1])
    gap = int(data[2])
    pos = 3

    sites = []
    for _ in range(n):
        x = int(data[pos])
        pos += 1
        profit = int(data[pos])
        pos += 1
        sites.append((x, profit))
    sites.sort()

    # prev[i] = best profit using exactly `signs - 1` signs, the last at site i.
    # A 0 means no legal way (every profit is positive).
    prev = [profit for _, profit in sites]
    answer = max(prev)

    for signs in range(2, max_signs + 1):
        cur = [0] * n
        best_before = 0
        p = 0
        for i in range(n):
            limit = sites[i][0] - gap
            while sites[p][0] <= limit:
                best_before = max(best_before, prev[p])
                p += 1
            if best_before > 0:
                cur[i] = best_before + sites[i][1]
        answer = max(answer, max(cur))
        prev = cur

    print(answer)


if __name__ == "__main__":
    main()
