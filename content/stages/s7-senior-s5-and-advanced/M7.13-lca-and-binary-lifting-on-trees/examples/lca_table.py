import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    pos = 1
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        adj[u].append(v)
        adj[v].append(u)

    parent = [0] * n
    depth = [-1] * n
    depth[0] = 0
    queue = deque([0])
    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if depth[nb] == -1:
                depth[nb] = depth[node] + 1
                parent[nb] = node
                queue.append(nb)

    LOG = max(1, max(depth).bit_length())
    up = [parent]
    for k in range(1, LOG):
        prev = up[k - 1]
        row = [prev[x] for x in prev]
        up.append(row)

    out = [f"depth = {depth}"]
    for k in range(LOG):
        out.append(f"up[{k}] = {up[k]}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
