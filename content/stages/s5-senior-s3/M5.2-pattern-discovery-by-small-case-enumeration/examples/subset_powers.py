import sys


def count_subsets(n):
    powers = []
    p = 1
    while p <= n:
        powers.append(p)
        p *= 2

    count = 0
    total = 2 ** len(powers)
    for mask in range(total):
        s = 0
        for i in range(len(powers)):
            if mask & (1 << i):
                s += powers[i]
        if s == n:
            count += 1
    return count


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    print(count_subsets(n))


if __name__ == "__main__":
    main()
