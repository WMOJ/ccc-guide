import sys


def fast(values):
    n = len(values)
    total = 0
    prefix = [0]
    for v in values:
        total += v
        prefix.append(total)
    low = prefix[0]
    best = values[0]
    for j in range(n):
        end = prefix[j + 1]
        cand = end - low
        best = max(best, cand)
        low = min(low, end)
    return best


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    nums = tokens[1:n + 1]
    values = list(map(int, nums))
    print(fast(values))


if __name__ == "__main__":
    main()
