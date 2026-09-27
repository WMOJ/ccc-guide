import sys
import math

def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx])
    idx += 1

    # Build tree
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    depth = [-1] * n
    parent = [-1] * n

    def dfs(u, p, d):
        depth[u] = d
        parent[u] = p
        for v in adj[u]:
            if v != p:
                dfs(v, u, d + 1)

    dfs(0, -1, 0)

    LOG = math.ceil(math.log2(n)) + 1
    ancestors = [[-1] * LOG for _ in range(n)]

    for u in range(n):
        ancestors[u][0] = parent[u]

    for k in range(1, LOG):
        for u in range(n):
            if ancestors[u][k - 1] != -1:
                ancestors[u][k] = ancestors[ancestors[u][k - 1]][k - 1]

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if (diff >> k) & 1:
                u = ancestors[u][k]
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if ancestors[u][k] != ancestors[v][k]:
                u = ancestors[u][k]
                v = ancestors[v][k]
        return ancestors[u][0]

    q = int(data[idx])
    idx += 1
    output = []
    for _ in range(q):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        output.append(str(lca(a, b)))

    sys.stdout.write("\n".join(output) + "\n")

if __name__ == "__main__":
    main()
