import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
edges = []
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, rec.readline().split())
    edges.append((u, v))
    adj[u].append(v)

disc = [-1] * n
fin = [-1] * n
kind_of = {}
children = [[] for _ in range(n)]
clock = 0
out_edges = []
for root in range(n):
    if disc[root] != -1:
        continue
    disc[root] = clock
    clock += 1
    st = [[root, 0]]
    while st:
        fr = st[-1]
        node = fr[0]
        idx = fr[1]
        if idx == len(adj[node]):
            st.pop()
            fin[node] = clock
            clock += 1
            continue
        fr[1] = idx + 1
        nb = adj[node][idx]
        if disc[nb] == -1:
            kind = "tree"
            children[node].append(nb)
            disc[nb] = clock
            clock += 1
            st.append([nb, 0])
        elif fin[nb] == -1:
            kind = "back"
        elif disc[node] < disc[nb]:
            kind = "forward"
        else:
            kind = "cross"
        kind_of[(node, nb)] = kind
        out_edges.append(f"{node} {nb} {kind}")

KIND_STATE = {"tree": "path", "back": "invalid", "forward": "compare", "cross": "frontier"}


def build(v):
    return vz.node(f"n{v}", v, children=[build(c) for c in children[v]], note=f"{disc[v]}/{fin[v]}",
                   state="done")


cells = []
states = []
for u, v in edges:
    kind = kind_of[(u, v)]
    cells.append([f"{u} → {v}", f"[{disc[u]}, {fin[u]}]", f"[{disc[v]}, {fin[v]}]", kind])
    states.append([None, None, None, KIND_STATE[kind]])
rec.step(
    "Each node shows discovery/finish. A child's interval sits inside its parent's. Comparing the "
    "intervals at the two ends of an edge gives its kind: a finished descendant is inside the "
    "start's interval, an ancestor contains it, and a cross edge ends before the start begins.",
    tree=vz.tree(build(0)),
    t=vz.table(cells, states=states, col_heads=["edge", "from", "to", "kind"]),
)
lines = out_edges + [f"{v} {disc[v]} {fin[v]}" for v in range(n)]
rec.output("\n".join(lines) + "\n")
