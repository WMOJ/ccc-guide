import random
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    seed = int(data[2])
    values = list(map(int, data[3:3 + n]))

    random.seed(seed)
    rank = k - 1
    rounds = 0
    while True:
        rounds += 1
        pivot = values[random.randrange(len(values))]
        smaller = [v for v in values if v < pivot]
        larger = [v for v in values if v > pivot]
        equal = len(values) - len(smaller) - len(larger)
        if rank < len(smaller):
            values = smaller
        elif rank < len(smaller) + equal:
            answer = pivot
            break
        else:
            rank -= len(smaller) + equal
            values = larger

    word = "round" if rounds == 1 else "rounds"
    print(f"smallest number {k}: {answer}, found in {rounds} {word}")


if __name__ == "__main__":
    main()
