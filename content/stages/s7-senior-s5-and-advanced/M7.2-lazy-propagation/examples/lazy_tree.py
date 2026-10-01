import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1

    size = 1
    while size < n:
        size *= 2

    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)
    for i in range(n):
        tree[size + i] = int(data[pos + i])
    pos += n
    for i in range(size - 1, 0, -1):
        tree[i] = tree[2 * i] + tree[2 * i + 1]

    def push(node, length):
        tag = lazy[node]
        if tag != 0:
            half = length // 2
            tree[2 * node] += tag * half
            lazy[2 * node] += tag
            tree[2 * node + 1] += tag * half
            lazy[2 * node + 1] += tag
            lazy[node] = 0

    def update(node, node_lo, node_hi, l, r, v):
        if r <= node_lo or node_hi <= l:
            return
        if l <= node_lo and node_hi <= r:
            tree[node] += v * (node_hi - node_lo)
            lazy[node] += v
            return
        push(node, node_hi - node_lo)
        mid = (node_lo + node_hi) // 2
        update(2 * node, node_lo, mid, l, r, v)
        update(2 * node + 1, mid, node_hi, l, r, v)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    def query(node, node_lo, node_hi, l, r):
        if r <= node_lo or node_hi <= l:
            return 0
        if l <= node_lo and node_hi <= r:
            return tree[node]
        push(node, node_hi - node_lo)
        mid = (node_lo + node_hi) // 2
        left_sum = query(2 * node, node_lo, mid, l, r)
        right_sum = query(2 * node + 1, mid, node_hi, l, r)
        return left_sum + right_sum

    q = int(data[pos])
    pos += 1

    results = []
    for _ in range(q):
        kind = int(data[pos])
        pos += 1
        if kind == 1:
            l = int(data[pos])
            r = int(data[pos + 1])
            v = int(data[pos + 2])
            pos += 3
            update(1, 0, size, l, r, v)
        else:
            l = int(data[pos])
            r = int(data[pos + 1])
            pos += 2
            results.append(query(1, 0, size, l, r))

    sys.stdout.write("\n".join(map(str, results)) + "\n")


if __name__ == "__main__":
    main()
