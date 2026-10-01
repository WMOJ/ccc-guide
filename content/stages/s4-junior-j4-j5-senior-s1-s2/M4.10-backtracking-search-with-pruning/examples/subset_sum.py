import sys


def count_subsets(values, index, remaining, target):
    if remaining > target:
        return 0
    if index == len(values):
        return 1 if remaining == target else 0
    skip = count_subsets(values, index + 1, remaining, target)
    take = count_subsets(values, index + 1, remaining + values[index], target)
    return skip + take


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    pos = 0
    n = int(input_data[pos])
    pos += 1
    target = int(input_data[pos])
    pos += 1
    values = [int(v) for v in input_data[pos:pos + n]]
    print(count_subsets(values, 0, 0, target))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
