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

    q = int(data[pos])
    pos += 1
    out = []
    moves = 0
    for _ in range(q):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        while depth[a] > depth[b]:
            a = parent[a]
            moves += 1
        while depth[b] > depth[a]:
            b = parent[b]
            moves += 1
        while a != b:
            a = parent[a]
            b = parent[b]
            moves += 2
        out.append(str(a))
    out.append(f"parent moves: {moves}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
