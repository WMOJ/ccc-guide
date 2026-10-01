import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    values = list(map(int, input_data[1:1 + n]))

    # Count inversions once, before any swap: pairs where an earlier value
    # is bigger than a later one.
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if values[i] > values[j]:
                inversions += 1

    # Repeatedly swap an adjacent pair that is out of order. Each swap
    # fixes exactly one inversion, so the count can only fall.
    swaps = 0
    changed = True
    while changed:
        changed = False
        for i in range(n - 1):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                swaps += 1
                changed = True

    lines = []
    lines.append(str(inversions))
    lines.append(str(swaps))
    lines.append(" ".join(str(v) for v in values))
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
