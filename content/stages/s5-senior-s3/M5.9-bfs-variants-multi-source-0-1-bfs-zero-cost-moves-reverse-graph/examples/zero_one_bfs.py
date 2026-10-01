import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    start = int(data[2])
    pos = 3

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        w = int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = [-1] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            nd = dist[u] + w
            if dist[v] == -1 or nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)

    print(" ".join(str(x) for x in dist))


if __name__ == "__main__":
    main()
