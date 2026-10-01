import sys


def main() -> None:
    d = sys.stdin.read().split()
    target = int(d[-1])
    a = list(map(int, d[1:-1]))
    seen = {0: 1}
    prefix = 0
    answer = 0
    for x in a:
        prefix += x - target
        c = seen.get(prefix, 0)
        answer += c
        seen[prefix] = c + 1
    print(answer)


if __name__ == "__main__":
    main()
