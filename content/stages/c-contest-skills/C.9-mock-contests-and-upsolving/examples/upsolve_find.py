import sys
from itertools import product


def brute(a):
    best = 1
    for i in range(len(a)):
        for j in range(i, len(a)):
            ok = True
            for k in range(i + 1, j + 1):
                if a[k] <= a[k - 1]:
                    ok = False
            if ok:
                best = max(best, j - i + 1)
    return best


def attempt(a):
    best = 1
    run = 1
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            run += 1
        else:
            run = 0
        best = max(best, run)
    return best


def fixed(a):
    best = 1
    run = 1
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            run += 1
        else:
            run = 1
        best = max(best, run)
    return best


def main() -> None:
    tokens = sys.stdin.read().split()
    max_len = int(tokens[0])
    values = int(tokens[1])
    inputs = []
    for n in range(1, max_len + 1):
        for combo in product(range(values), repeat=n):
            inputs.append(list(combo))
    failing = None
    for a in inputs:
        if attempt(a) != brute(a):
            failing = a
            break
    lines = []
    if failing is None:
        lines.append(f"no failing input among {len(inputs)} inputs")
    else:
        lines.append(f"first failing input: {failing}")
        lines.append(f"brute force says {brute(failing)}, attempt says {attempt(failing)}")
    bad = sum(1 for a in inputs if fixed(a) != brute(a))
    lines.append(f"fixed attempt differs from brute force on {bad} of {len(inputs)} inputs")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
