import math

import vizrec as vz

rec = vz.Recorder()
n, q = map(int, rec.readline().split())
nxt = list(map(int, rec.readline().split()))
start, k = map(int, rec.readline().split())


def place(v):
    angle = -math.pi / 2 + 2 * math.pi * v / n
    return (round(2.2 + 2 * math.cos(angle), 2), round(2.2 + 2 * math.sin(angle), 2))


nodes = [(v, place(v)[0], place(v)[1]) for v in range(n)]
edges = [(v, nxt[v]) for v in range(n)]

visited = {start}
arrived = {start: 0}
taken = []


def frame(here, last_edge=None):
    node_states = {v: "done" for v in visited}
    node_states[here] = "current"
    edge_states = {e: "done" for e in taken}
    if last_edge is not None:
        edge_states[last_edge] = "current"
    return vz.graph(nodes, edges, node_states=node_states, edge_states=edge_states,
                    values=dict(arrived), directed=True, value_label="jump no.")


here = start
rec.step(
    f"Station {start} is the start, and the rider must make {k} "
    f"{'jump' if k == 1 else 'jumps'}. Each station has exactly one teleporter, drawn as an arrow to "
    f"its next station. Jumps made so far: 0.",
    graph=frame(here),
)
for j in range(1, k + 1):
    there = nxt[here]
    taken_before = list(taken)
    visited.add(there)
    arrived[there] = j
    edge = (here, there)
    rec.step(
        f"Jump {j}: the teleporter at station {here} sends the rider to station {there}. "
        f"Jumps made so far: {j}.",
        graph=frame(there, edge),
    )
    taken.append(edge)
    here = there

if k == 0:
    rec.step(
        f"K is 0, so no teleporter is used and the rider is still at station {start}. "
        f"This query cost 0 hops.",
        graph=frame(here),
    )
else:
    rec.step(
        f"After {k} jumps the rider is at station {here}, the answer. The walk took {k} hops, one per "
        f"jump, and that cost is paid again for every query.",
        graph=frame(here),
    )
rec.output(f"{here}\nhops made: {k}\n")
