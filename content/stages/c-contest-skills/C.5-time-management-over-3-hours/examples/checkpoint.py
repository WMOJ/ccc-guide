import sys


def main() -> None:
    raw = sys.stdin.read()
    t = raw.split()
    left = int(t[0])
    best = 0
    best_cost = 0
    for p in range(1, 6):
        word = t[2 * p]
        if word == "-":
            continue
        cost = int(word)
        if cost > left:
            continue
        if best == 0 or cost < best_cost:
            best = p
            best_cost = cost
    if best == 0:
        print("nothing fits in", left, "minutes")
    else:
        print("pick problem", best, "for", best_cost, "minutes")


if __name__ == "__main__":
    main()
