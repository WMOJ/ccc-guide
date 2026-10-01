import sys


def go(i, n, path):
    if i == n:
        print(path)
        return
    for v in (0, 1):
        path.append(v)
        go(i + 1, n, path)
        path.pop()


def solve() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    n = int(tokens[0])
    go(0, n, [])


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
