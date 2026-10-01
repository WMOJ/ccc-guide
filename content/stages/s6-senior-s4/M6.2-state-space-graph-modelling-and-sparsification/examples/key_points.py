import heapq
import sys


def dijkstra(adj, src):
    best = [-1] * len(adj)
    done = [False] * len(adj)
    best[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            nd = d + w
            if not done[v] and (best[v] == -1 or nd < best[v]):
                best[v] = nd
                heapq.heappush(heap, (nd, v))
    return best


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    pos = 3
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        w = int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    keys = [0]
    for _ in range(k):
        keys.append(int(data[pos]))
        pos += 1
    dist = [dijkstra(adj, room) for room in keys]

    size = 1 << k
    full = size - 1
    done = [False] * ((k + 1) * size)
    settled = 0
    answer = -1
    heap = [(0, 0, 0)]
    while heap:
        d, i, mask = heapq.heappop(heap)
        s = i * size + mask
        if done[s]:
            continue
        done[s] = True
        settled += 1
        if mask == full:
            answer = d
            break
        for j in range(1, k + 1):
            bit = 1 << (j - 1)
            w = dist[i][keys[j]]
            if not (mask & bit) and w != -1:
                heapq.heappush(heap, (d + w, j, mask | bit))

    print("distance", answer)
    print("settled", settled, "of", (k + 1) * size, "states")


if __name__ == "__main__":
    main()
