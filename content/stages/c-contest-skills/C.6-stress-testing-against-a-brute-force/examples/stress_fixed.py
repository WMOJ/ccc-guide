import random
import sys


def new_case():
    n = random.randint(1, 3)
    return [
        random.randint(-3, 3)
        for _ in range(n)
    ]


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
    seed = int(tokens[0])
    random.seed(seed)
    failed = None
    for trial in range(1, 1001):
        values = new_case()
        want = brute(values)
        got = fast(values)
        if want != got:
            failed = trial
            break
    if failed is None:
        print("no mismatch")
    else:
        print("trial", failed)
        print("input", values)
        print("brute", want)
        print("fast", got)


if __name__ == "__main__":
    main()
