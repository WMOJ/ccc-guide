import sys
from heapq import heapify, heappushpop, heapreplace


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    item = int(tokens[0])
    start = [int(t) for t in tokens[1:]]
    heapify(start)

    first = list(start)
    got = heappushpop(first, item)
    print(f"heappushpop: returned {got}, heap {sorted(first)}")

    second = list(start)
    got = heapreplace(second, item)
    print(f"heapreplace: returned {got}, heap {sorted(second)}")


if __name__ == "__main__":
    main()
