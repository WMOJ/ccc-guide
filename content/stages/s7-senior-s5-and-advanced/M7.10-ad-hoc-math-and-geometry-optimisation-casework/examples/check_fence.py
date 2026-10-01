import sys


def brute(w):
    best_x = 0
    best_area = 0
    for x in range(1, (w - 1) // 2 + 1):
        area = x * (w - 2 * x)
        if area > best_area:
            best_x = x
            best_area = area
    return best_x, best_area


def shortcut(w, picks):
    hi = (w - 1) // 2
    best_x = 0
    best_area = 0
    for pick in picks:
        x = max(1, min(hi, pick))
        area = x * (w - 2 * x)
        if area > best_area:
            best_x = x
            best_area = area
    return best_x, best_area


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    top = int(data[0])

    first_miss = None
    both_misses = 0
    for w in range(3, top + 1):
        want = brute(w)
        if shortcut(w, [w // 4]) != want and first_miss is None:
            first_miss = w
        if shortcut(w, [w // 4, w // 4 + 1]) != want:
            both_misses += 1

    if first_miss is None:
        print("floor only: no wrong answer")
    else:
        print("floor only: first wrong at", first_miss)
    print("floor and next: wrong", both_misses, "times")


if __name__ == "__main__":
    main()
