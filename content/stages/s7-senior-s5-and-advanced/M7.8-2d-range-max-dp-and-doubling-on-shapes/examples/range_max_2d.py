import sys


def main() -> None:
    raw = sys.stdin.read()
    d = raw.split()
    n = int(d[0])
    grid = []
    pos = 1
    for _ in range(n):
        row = list(map(int, d[pos:pos + n]))
        grid.append(row)
        pos += n
    q = int(d[pos])
    pos += 1

    # table[k][i][j]: max of the 2^k by 2^k block with top-left (i, j)
    table = [grid]
    for k in range(1, n.bit_length()):
        half = 1 << (k - 1)
        prev = table[k - 1]
        span = n - (1 << k) + 1
        layer = []
        for i in range(span):
            row = []
            for j in range(span):
                row.append(max(
                    prev[i][j],
                    prev[i][j + half],
                    prev[i + half][j],
                    prev[i + half][j + half],
                ))
            layer.append(row)
        table.append(layer)

    out = []
    for _ in range(q):
        r = int(d[pos])
        c = int(d[pos + 1])
        side = int(d[pos + 2])
        pos += 3
        k = side.bit_length() - 1
        t = table[k]
        far = side - (1 << k)
        out.append(max(
            t[r][c],
            t[r][c + far],
            t[r + far][c],
            t[r + far][c + far],
        ))
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
