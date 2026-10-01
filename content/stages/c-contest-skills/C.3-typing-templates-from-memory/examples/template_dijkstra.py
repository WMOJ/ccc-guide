import heapq
import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])

    adj = [[] for _ in range(n)]
    pos = 2
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        w = int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    best = [-1] * n  # shortest distance found so far; -1 means none yet
    done = [False] * n  # True once a node's distance is final
    best[0] = 0
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue  # an out-of-date entry: u was done earlier
        done[u] = True
        for v, w in adj[u]:
            nd = d + w
            if not done[v] and (best[v] == -1 or nd < best[v]):
                best[v] = nd
                heapq.heappush(heap, (nd, v))

    print(" ".join(str(x) for x in best))


if __name__ == "__main__":
    main()
