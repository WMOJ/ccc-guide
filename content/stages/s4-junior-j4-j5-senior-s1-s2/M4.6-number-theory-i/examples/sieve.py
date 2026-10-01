import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    n = int(tokens[0])
    composite = [False] * (n + 1)
    p = 2
    while p * p <= n:
        if not composite[p]:
            multiple = p * p
            while multiple <= n:
                composite[multiple] = True
                multiple += p
        p += 1
    primes = []
    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
    print(len(primes))
    print(" ".join(str(i) for i in primes))


if __name__ == "__main__":
    main()
