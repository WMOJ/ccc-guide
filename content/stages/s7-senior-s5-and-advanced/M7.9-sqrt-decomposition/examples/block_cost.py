import sys


def worst_cost(n, b):
    worst = 0
    for lo0 in range(n):
        for hi in range(lo0 + 1, n + 1):
            lo = lo0
            steps = 0
            while lo < hi and lo % b != 0:
                steps += 1
                lo += 1
            while lo + b <= hi:
                steps += 1
                lo += b
            while lo < hi:
                steps += 1
                lo += 1
            worst = max(worst, steps)
    return worst


def main() -> None:
    n = int(sys.stdin.read().split()[0])
    best_b = 1
    best_cost = worst_cost(n, 1)
    for b in range(2, n + 1):
        cost = worst_cost(n, b)
        if cost < best_cost:
            best_b = b
            best_cost = cost
    print(n, best_b, best_cost)
    print("b=1:", worst_cost(n, 1), "b=n:", worst_cost(n, n))


if __name__ == "__main__":
    main()
