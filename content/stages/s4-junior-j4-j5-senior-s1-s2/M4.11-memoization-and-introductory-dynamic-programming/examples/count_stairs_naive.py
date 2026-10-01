import sys


def count_ways(stair, target):
    if stair >= target:
        return 1
    return count_ways(stair + 1, target) + count_ways(stair + 2, target)


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    target = int(input_data[0])
    print(count_ways(0, target))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
