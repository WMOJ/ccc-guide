from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, m, start = map(int, rec.readline().split())
adj = [[] for _ in range(n)]
adj_w = [[] for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, rec.readline().split())
    adj[u].append(v)
    adj[v].append(u)
    adj_w[u].append((v, w))
    adj_w[v].append((u, w))

# Plain BFS: counts edges, ignoring weight.
edge_dist = [-1] * n
edge_dist[start] = 0
plain_queue = deque([start])
while plain_queue:
    u = plain_queue.popleft()
    for v in adj[u]:
        if edge_dist[v] == -1:
            edge_dist[v] = edge_dist[u] + 1
            plain_queue.append(v)

# 0-1 BFS: respects weight with a deque.
cost_dist = [-1] * n
cost_dist[start] = 0
dq = deque([start])
while dq:
    u = dq.popleft()
    for v, w in adj_w[u]:
        nd = cost_dist[u] + w
        if cost_dist[v] == -1 or nd < cost_dist[v]:
            cost_dist[v] = nd
            if w == 0:
                dq.appendleft(v)
            else:
                dq.append(v)

wrong = {(0, i) for i in range(n) if edge_dist[i] != cost_dist[i]}

rec.step(
    "Plain BFS counts edges and ignores weight, so it calls node 1 one hop away, through "
    "the direct stairwell. 0-1 BFS finds the true cost: three free doors reach node 1 for "
    "nothing, and that shorter route also makes node 4 one minute closer. The marked cells "
    "are where counting edges gives the wrong answer.",
    t=vz.table(
        [[edge_dist[i] for i in range(n)], [cost_dist[i] for i in range(n)]],
        states={cell: "invalid" for cell in wrong},
        row_heads=["Plain BFS (edges)", "0-1 BFS (cost)"],
        col_heads=[str(i) for i in range(n)],
        col_title="Node",
    )
)
rec.output(" ".join(str(x) for x in cost_dist) + "\n")
