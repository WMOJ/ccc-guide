import random
import sys


def comparisons(values, rank, use_random):
    work = 0
    while True:
        if use_random:
            pivot = values[random.randrange(len(values))]
        else:
            pivot = values[0]
        work += len(values)
        smaller = [v for v in values if v < pivot]
        larger = [v for v in values if v > pivot]
        equal = len(values) - len(smaller) - len(larger)
        if rank < len(smaller):
            values = smaller
        elif rank < len(smaller) + equal:
            return work
        else:
            rank -= len(smaller) + equal
            values = larger


def main() -> None:
    data = sys.stdin.read().split()
    kind = data[0]
    random.seed(int(data[1]))

    lines = []
    for token in data[2:]:
        n = int(token)
        values = list(range(n))
        if kind == "shuffled":
            random.shuffle(values)
        elif kind == "equal":
            values = [7] * n
        first = comparisons(values, n // 2, False)
        rand = comparisons(values, n // 2, True)
        lines.append(f"n = {n}: first-element pivot {first}, random pivot {rand}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
