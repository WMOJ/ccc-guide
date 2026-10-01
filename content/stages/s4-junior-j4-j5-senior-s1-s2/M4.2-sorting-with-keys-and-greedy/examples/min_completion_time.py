import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return

    n = int(data[0])
    times = []
    for k in range(n):
        t = int(data[1 + k])
        times.append(t)

    order = sorted(times)

    total = 0
    finish = 0
    for t in order:
        finish += t
        total += finish

    print(*order)
    print(total)


if __name__ == "__main__":
    main()
