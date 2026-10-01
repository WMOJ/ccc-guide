import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    target = int(data[2])
    pos = 3

    rev_adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        rev_adj[v].append(u)

    dist = [-1] * n
    dist[target] = 0
    queue = deque([target])
    while queue:
        u = queue.popleft()
        for v in rev_adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    print(" ".join(str(x) for x in dist))


if __name__ == "__main__":
    main()
