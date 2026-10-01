import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    w = int(data[0])
    limit = int(data[1])

    hi = (w - 1) // 2
    hi = min(hi, limit)
    low = w // 4
    nxt = low + 1
    best_x = 0
    best_area = -1
    for pick in (low, nxt):
        x = min(hi, pick)
        x = max(1, x)
        area = x * (w - 2 * x)
        if area > best_area:
            best_x = x
            best_area = area

    print(best_x, best_area)


if __name__ == "__main__":
    main()
