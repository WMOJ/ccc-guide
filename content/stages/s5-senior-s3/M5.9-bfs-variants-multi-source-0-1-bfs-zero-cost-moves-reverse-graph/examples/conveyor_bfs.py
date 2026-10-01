import sys
from collections import deque


def resolve_landing(conveyor, n):
    """The real node each node ends at after riding conveyors, or -1 if the ride never ends.

    Each node is added to a chain at most once, so this is O(n) total, not O(n) per node.
    """
    landing = list(range(n))
    state = [0] * n  # 0: unseen, 1: on the chain being built right now, 2: resolved
    for start in range(n):
        if state[start] != 0:
            continue
        chain = []
        u = start
        while conveyor[u] != -1 and state[u] == 0:
            state[u] = 1
            chain.append(u)
            u = conveyor[u]
        if conveyor[u] == -1:
            end = u  # a real node with no outgoing conveyor
        elif state[u] == 1:
            end = -1  # u is already on this chain: the conveyors loop back on themselves
        else:
            end = landing[u]  # u was already resolved while building an earlier chain
        for node in chain:
            landing[node] = end
            state[node] = 2
    return landing


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    pos = 3

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        adj[u].append(v)
        adj[v].append(u)

    conveyor = [-1] * n
    for _ in range(k):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        conveyor[a] = b

    landing = resolve_landing(conveyor, n)

    dist = [-1] * n
    queue = deque()
    start = landing[0]
    if start != -1:
        dist[start] = 0
        queue.append(start)

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            lv = landing[v]
            if lv != -1 and dist[lv] == -1:
                dist[lv] = dist[u] + 1
                queue.append(lv)

    print(" ".join(str(x) for x in dist))


if __name__ == "__main__":
    main()
