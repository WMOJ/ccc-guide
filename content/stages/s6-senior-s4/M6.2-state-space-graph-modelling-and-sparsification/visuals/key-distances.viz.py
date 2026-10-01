import heapq

import vizrec as vz

rec = vz.Recorder()
n, m, k = map(int, rec.readline().split())
edges = []
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, rec.readline().split())
    edges.append((u, v, w))
    adj[u].append((v, w))
    adj[v].append((u, w))
stops = [int(x) for x in rec.readline().split()]
keys = [0] + stops
POS = {0: (0, 0), 1: (2, 0), 2: (4, 0), 3: (0, 2), 4: (4, 2)}
nodes = [(r, POS[r][0], POS[r][1]) for r in range(n)]


def dijkstra(src):
    best = [-1] * n
    parent = [-1] * n
    done = [False] * n
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
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    return best, parent


runs = [dijkstra(room) for room in keys]
dist = [r[0] for r in runs]
K = len(keys)
heads = ["start"] + [str(r) for r in stops]
key_state = {0: "current"}
for r in stops:
    key_state.setdefault(r, "compare")


def table(known):
    cells = []
    states = []
    for i in range(K):
        row = []
        srow = []
        for j in range(K):
            if i == j:
                row.append(0)
                srow.append("done")
            elif (min(i, j), max(i, j)) in known:
                d = dist[i][keys[j]]
                row.append(d if d != -1 else "∞")
                srow.append("done")
            else:
                row.append("–")
                srow.append(None)
        cells.append(row)
        states.append(srow)
    return vz.table(cells, states=states, row_heads=heads, col_heads=heads, row_title="from",
                    col_title="to")


def full_map(path=None):
    node_states = dict(key_state)
    edge_states = {}
    if path:
        for r in path:
            node_states.setdefault(r, "path")
        for a, b in zip(path, path[1:]):
            edge_states[(a, b)] = "path"
    return vz.graph(nodes, [(a, b, w) for a, b, w in edges], node_states=node_states,
                    edge_states=edge_states)


def rooms(rs):
    names = [str(r) for r in rs]
    if len(names) == 1:
        return "room " + names[0]
    return "rooms " + ", ".join(names[:-1]) + " and " + names[-1]


known = set()
rec.step(
    f"The map has {n} rooms. The key rooms are the start, room 0, and the checkpoints, "
    f"{rooms(stops)}. The table will hold the shortest distance between every pair of key rooms. "
    "Only the diagonal is filled so far: a room is 0 away from itself.",
    g=full_map(), t=table(known)
)
for i in range(K):
    for j in range(i + 1, K):
        a, b = keys[i], keys[j]
        d = dist[i][b]
        known.add((i, j))
        if d == -1:
            rec.step(
                f"No route joins room {a} and room {b}, so their cell holds ∞ and this pair gets no "
                "kept edge.",
                g=full_map(), t=table(known)
            )
            continue
        path = [b]
        while path[-1] != a:
            path.append(runs[i][1][path[-1]])
        path.reverse()
        mids = path[1:-1]
        route = " → ".join(str(r) for r in path)
        if not mids:
            note = "One corridor joins them."
        elif any(r in keys for r in mids):
            inner = [r for r in mids if r in keys]
            note = f"The route passes through {rooms(inner)}, another key room."
        else:
            which = "which is not a key room" if len(mids) == 1 else "which are not key rooms"
            note = f"The route only passes through {rooms(mids)}, {which}."
        rec.step(
            f"The shortest route from room {a} to room {b} is {route}, distance {d}. {note}",
            g=full_map(path), t=table(known)
        )

kept = []
for i in range(K):
    for j in range(i + 1, K):
        if dist[i][keys[j]] != -1:
            kept.append((keys[i], keys[j], dist[i][keys[j]]))
key_rooms = sorted(set(keys))
kept_graph = vz.graph(
    [(r, POS[r][0], POS[r][1]) for r in key_rooms], kept, node_states=key_state
)
rec.step(
    f"Keep only what the search needs: the {len(key_rooms)} key rooms and {len(kept)} "
    f"edge{'' if len(kept) == 1 else 's'}, each "
    f"weighted with a shortest distance. The other {n - len(key_rooms)} rooms and all {m} "
    "corridors are gone from the graph.",
    g=kept_graph, t=table(known)
)

size = 1 << k
full = size - 1
done = [False] * (K * size)
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
    for j in range(1, K):
        bit = 1 << (j - 1)
        w = dist[i][keys[j]]
        if not (mask & bit) and w != -1:
            heapq.heappush(heap, (d + w, j, mask | bit))
rec.output(f"distance {answer}\nsettled {settled} of {K * size} states\n")
