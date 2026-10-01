import heapq
import sys


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

    bit = [0] * n
    for i in range(k):
        bit[int(data[pos])] = 1 << i
        pos += 1
    size = 1 << k
    full = size - 1

    best = [-1] * (n * size)
    done = [False] * (n * size)
    settled = 0
    answer = -1
    best[bit[0]] = 0
    heap = [(0, 0, bit[0])]
    while heap:
        d, u, mask = heapq.heappop(heap)
        s = u * size + mask
        if done[s]:
            continue  # an out-of-date entry
        done[s] = True
        settled += 1
        if mask == full:
            answer = d
            break
        for v, w in adj[u]:
            nmask = mask | bit[v]
            t = v * size + nmask
            nd = d + w
            if not done[t] and (best[t] == -1 or nd < best[t]):
                best[t] = nd
                heapq.heappush(heap, (nd, v, nmask))

    print("distance", answer)
    print("settled", settled, "of", n * size, "states")


if __name__ == "__main__":
    main()
