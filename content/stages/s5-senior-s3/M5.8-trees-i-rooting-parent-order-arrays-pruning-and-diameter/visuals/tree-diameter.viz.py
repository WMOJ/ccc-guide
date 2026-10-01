from collections import deque

import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, rec.readline().split())
    adj[a].append(b)
    adj[b].append(a)

LAYOUTS = {
    5: [(2, 1), (0.5, 0.3), (0.5, 1.7), (3.5, 0.3), (3.5, 1.7)],
    6: [(0, 1), (0.9, 1), (1.8, 1), (2.7, 1), (3.6, 1), (4.5, 1)],
    7: [(0, 1), (1, 1), (2, 0), (2, 2), (3, 1.5), (4, 1.5), (3, 2.5)],
}
pos = LAYOUTS.get(n, [(i, 1) for i in range(n)])
nodes = [(i, pos[i][0], pos[i][1]) for i in range(n)]
edges = [(u, v) for u in range(n) for v in adj[u] if u < v]


def frame(dist, queue, current=None, done=None, path=None):
    done = done or set()
    path = path or set()
    node_states = {}
    values = {}
    for i in range(n):
        if i in path:
            node_states[i] = "path"
        elif i == current:
            node_states[i] = "current"
        elif i in queue:
            node_states[i] = "frontier"
        elif i in done:
            node_states[i] = "done"
        values[i] = dist[i] if dist[i] != -1 else "?"
    edge_states = {}
    if path:
        ordered = list(path)
        for u, v in edges:
            if u in path and v in path:
                edge_states[(u, v)] = "path"
    items = [(f"room {i}", None) for i in queue]
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, values=values, value_label="dist"),
        "q": vz.queue(items),
    }


def bfs(start, phase):
    dist = [-1] * n
    dist[start] = 0
    queue = deque([start])
    parent = [None] * n
    farthest = start
    max_dist = 0
    rec.step(
        f"{phase} starts at room {start}: its distance is 0 and it is the only room in the queue.",
        **frame(dist, queue)
    )
    done = set()
    while queue:
        node = queue.popleft()
        done.add(node)
        added = []
        for neighbor in adj[node]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[node] + 1
                parent[neighbor] = node
                queue.append(neighbor)
                added.append(neighbor)
                if dist[neighbor] > max_dist:
                    max_dist = dist[neighbor]
                    farthest = neighbor
        if added:
            names = ", ".join(f"room {r}" for r in added)
            what = f"{names} join{'s' if len(added) == 1 else ''} the queue at distance {dist[node] + 1}."
        else:
            what = "no new room joins the queue."
        rec.step(
            f"{phase}: room {node} leaves the queue at distance {dist[node]}; {what}",
            **frame(dist, queue, current=node, done=done)
        )
    return farthest, max_dist, parent


end_a, _first_len, _first_parent = bfs(0, "First BFS")
end_b, diameter, parent = bfs(end_a, "Second BFS")

path = {end_b}
walker = end_b
while parent[walker] is not None:
    walker = parent[walker]
    path.add(walker)
final_dist = [-1] * n
q = deque([end_a])
final_dist[end_a] = 0
while q:
    node = q.popleft()
    for neighbor in adj[node]:
        if final_dist[neighbor] == -1:
            final_dist[neighbor] = final_dist[node] + 1
            q.append(neighbor)
rec.step(
    f"The path from room {end_a} to room {end_b}, {diameter} rooms apart, is the diameter: no "
    "other pair of rooms is farther apart in this floor plan.",
    **frame(final_dist, [], done=set(range(n)), path=path)
)
rec.output(f"Diameter endpoints: {end_a} {end_b}\nDiameter: {diameter}\n")
