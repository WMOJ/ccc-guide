def row() -> list:
    s = input().split()
    return [int(x) for x in s]


def main() -> None:
    a = int(input())
    b = int(input())
    depth = row()
    up = [row(), row(), row()]
    LOG = len(up)
    if depth[a] < depth[b]:
        a, b = b, a
    diff = depth[a] - depth[b]
    for k in range(LOG):
        if (diff >> k) & 1:
            a = up[k][a]
    if a == b:
        print(a)
        return
    for k in reversed(range(LOG)):
        if up[k][a] != up[k][b]:
            a = up[k][a]
            b = up[k][b]
    print(up[0][a])


if __name__ == "__main__":
    main()
