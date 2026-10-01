from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, k = map(int, rec.readline().split())
important = [False] * n
for node_id in rec.readline().split():
    important[int(node_id)] = True
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, rec.readline().split())
    adj[a].append(b)
    adj[b].append(a)

LAYOUTS = {
    5: [(2, 1), (0.5, 0.3), (0.5, 1.7), (3.5, 0.3), (3.5, 1.7)],
    6: [(0, 1), (1, 0.2), (1, 1.8), (2.4, 0.2), (2.4, 1.8), (3.6, 1)],
    8: [(0, 1), (1, 0.3), (1, 1.7), (2, 0), (2.2, 1.7), (3.2, 0), (1, 2.7), (2, 3.4)],
}
pos = LAYOUTS.get(n, [(i, 1) for i in range(n)])
nodes = [(i, pos[i][0], pos[i][1]) for i in range(n)]
edges = [(u, v) for u in range(n) for v in adj[u] if u < v]

degree = [len(adj[i]) for i in range(n)]
removed = [False] * n


def frame(current=None):
    node_states = {}
    values = {}
    for i in range(n):
        if removed[i]:
            node_states[i] = "invalid"
        elif i == current:
            node_states[i] = "current"
        elif important[i]:
            node_states[i] = "path"
        elif degree[i] == 1:
            node_states[i] = "frontier"
        values[i] = degree[i]
    live_edges = [(u, v) for u, v in edges if not removed[u] and not removed[v]]
    return {
        "t": vz.graph(nodes, live_edges, node_states=node_states, values=values, value_label="deg"),
        "q": vz.queue([f"room {i}" for i in range(n) if degree[i] == 1 and not important[i]
                        and not removed[i]]),
    }


queue = deque(i for i in range(n) if degree[i] == 1 and not important[i])
removed_edges = 0
rec.step(
    "Every leaf room, marked here by degree 1, that is not an important meeting room joins the "
    "queue. Important leaves, shown in the darker color, are never queued, no matter their "
    "degree.",
    **frame()
)
while queue:
    node = queue.popleft()
    if removed[node]:
        continue
    live_neighbor = next((v for v in adj[node] if not removed[v]), None)
    removed[node] = True
    for other in adj[node]:
        if removed[other]:
            continue
        degree[other] -= 1
        removed_edges += 1
        if degree[other] == 1 and not important[other]:
            queue.append(other)
    if live_neighbor is None:
        what = "it was the last room left."
    elif degree[live_neighbor] == 1 and not important[live_neighbor] and not removed[live_neighbor]:
        what = f"room {live_neighbor}'s degree drops to 1, so it joins the queue too."
    else:
        what = f"room {live_neighbor}'s degree drops to {degree[live_neighbor]}."
    rec.step(
        f"Room {node} is a dead-end room and not important, so it closes: {what}",
        **frame()
    )

kept = [i for i in range(n) if not removed[i]]
rec.step(
    f"The queue is empty: rooms {kept} are kept, and {removed_edges} hallway"
    f"{'s' if removed_edges != 1 else ''} closed with the rooms behind them.",
    **frame()
)
rec.output(f"Rooms kept: {kept}\nHallways closed: {removed_edges}\n")
