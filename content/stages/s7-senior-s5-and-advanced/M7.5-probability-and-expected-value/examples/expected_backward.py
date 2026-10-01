import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    p = float(tokens[1])
    q = 1 - p
    e = [0.0] * (n + 2)
    for i in range(n - 1, -1, -1):
        e[i] = 1
        e[i] += p * e[i + 1]
        e[i] += q * e[i + 2]
    print(e[:n])


if __name__ == "__main__":
    main()
