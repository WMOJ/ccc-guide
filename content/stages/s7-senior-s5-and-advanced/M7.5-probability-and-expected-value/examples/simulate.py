import random
import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    p = float(tokens[1])
    seed = int(tokens[2])
    rng = random.Random(seed)
    total = 0
    games = 0
    lines = []
    for limit in (10, 100, 1000, 10000):
        while games < limit:
            square = 0
            while square < n:
                if rng.random() < p:
                    square += 1
                else:
                    square += 2
                total += 1
            games += 1
        lines.append(f"after {limit} games: {total / games:.3f}")
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
