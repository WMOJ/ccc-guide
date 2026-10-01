import sys


def brute(values):
    n = len(values)
    return max(
        sum(values[i:j + 1])
        for i in range(n)
        for j in range(i, n)
    )


def fast(values):
    n = len(values)
    total = 0
    prefix = [0]
    for v in values:
        total += v
        prefix.append(total)
    low = prefix[1]
    best = values[0]
    for j in range(n):
        end = prefix[j + 1]
        cand = end - low
        best = max(best, cand)
        low = min(low, end)
    return best


def still_fails(values):
    return brute(values) != fast(values)


def shrink(values):
    changed = True
    while changed:
        changed = False
        for k in range(len(values)):
            smaller = values[:k] + values[k + 1:]
            if smaller and still_fails(smaller):
                values = smaller
                changed = True
                break
    return values


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    values = [int(t) for t in tokens[1:n + 1]]
    small = shrink(values)
    print("start", values)
    print("shrunk", small)
    print("brute", brute(small))
    print("fast", fast(small))


if __name__ == "__main__":
    main()
