import sys


def solve() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    if not tokens:
        return
    target = int(tokens[0])
    size = target + 2
    ways = [0] * size
    ways[target] = 1
    ways[target + 1] = 1
    stair = target - 1
    while stair >= 0:
        a = ways[stair + 1]
        b = ways[stair + 2]
        ways[stair] = a + b
        stair -= 1
    print(ways[0])


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
