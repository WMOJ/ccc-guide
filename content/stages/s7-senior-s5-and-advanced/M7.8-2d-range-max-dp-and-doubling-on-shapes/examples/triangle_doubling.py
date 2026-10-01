import sys


def main() -> None:
    raw = sys.stdin.read()
    d = raw.split()
    n = int(d[0])
    k = int(d[1])
    pos = 2
    cur = []
    for i in range(n):
        cur.append(list(map(int, d[pos:pos + i + 1])))
        pos += i + 1

    # cur[i][j]: max of the size-m triangle with its apex at (i, j)
    m = 1
    while m < k:
        if m == 1:
            size = 2
        else:
            size = min(k, 2 * m - 1)
        off = size - m
        new = []
        for i in range(n - size + 1):
            row = []
            for j in range(i + 1):
                row.append(max(
                    cur[i][j],
                    cur[i + off][j],
                    cur[i + off][j + off],
                ))
            new.append(row)
        cur = new
        m = size

    for row in cur:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    main()
