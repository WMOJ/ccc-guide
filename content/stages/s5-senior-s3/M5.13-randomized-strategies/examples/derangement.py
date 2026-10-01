import random
import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    seed = int(data[1])
    if n < 2:
        print(-1)
        return

    random.seed(seed)
    tries = 0
    while True:
        tries += 1
        gift = list(range(n))
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            gift[i], gift[j] = gift[j], gift[i]
        stuck = 0
        for i in range(n):
            if gift[i] == i:
                stuck += 1
        if stuck == 0:
            break

    print(tries)
    print(" ".join(map(str, gift)))


if __name__ == "__main__":
    main()
