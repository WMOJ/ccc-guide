import sys


def solve() -> None:
    data = sys.stdin.read().split()
    pos = 0
    r = int(data[pos])
    c = int(data[pos + 1])
    pos += 2
    pos += r
    qr = int(data[pos])
    qc = int(data[pos + 1])
    pos += 2

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    for dr, dc in moves:
        nr, nc = qr + dr, qc + dc
        if 0 <= nr < r and 0 <= nc < c:
            count += 1

    print(count)


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
