import sys


def main() -> None:
    raw = sys.stdin.read()
    d = raw.split()
    target = int(d[-1])
    a = list(map(int, d[1:-1]))
    n = len(a)
    answer = 0
    for i in range(n):
        total = 0
        for j in range(i, n):
            total += a[j]
            if total == target * (j - i + 1):
                answer += 1
    print(answer)


if __name__ == "__main__":
    main()
