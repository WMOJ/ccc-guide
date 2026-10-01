import math

import vizrec as vz

rec = vz.Recorder()
n, start, steps = (int(t) for t in rec.readline().split())

seen = {start: 0}
order = [start]
state = start
while True:
    state = 2 * min(state, n - state)
    if state in seen:
        break
    seen[state] = len(order)
    order.append(state)
first = seen[state]
length = len(order) - first
back_to = state
tail = order[:first]
ring = order[first:]

# Fixed layout: the cycle on a ring, the tail to its left.
cx, cy, r = 2.8, 1.9, 1.5
pos = {}
for k, v in enumerate(ring):
    ang = math.pi + 2 * math.pi * k / len(ring)
    pos[v] = (round(cx + r * math.cos(ang), 2), round(cy + r * math.sin(ang), 2))
for t, v in enumerate(reversed(tail)):
    pos[v] = (round(cx - r - 1.3 * (t + 1), 2), cy)


def graph_frame(upto, states=None, closing=False):
    shown = order[: upto + 1]
    nodes = [(v, pos[v][0], pos[v][1]) for v in shown]
    edges = [(shown[i], shown[i + 1]) for i in range(len(shown) - 1)]
    edge_states = {}
    if closing:
        edges.append((shown[-1], back_to))
        edge_states[(shown[-1], back_to)] = "current"
    return vz.graph(nodes, edges, node_states=states or {}, edge_states=edge_states, directed=True)


def array_frame(upto, pointer=None, ranges=None):
    ptrs = [("i", pointer, "above", True)] if pointer is not None else None
    return vz.array(order[: upto + 1], pointers=ptrs, ranges=ranges, indices=True)


rec.step(
    f"The map sends a numerator p, meaning the fraction p/{n}, to 2 * min(p, {n} - p). Start at "
    f"p = {start}. The dictionary `seen` records the step each numerator first appeared, so "
    f"seen[{start}] = 0. The list below is the numerators in step order.",
    g=graph_frame(0, {start: "current"}), a=array_frame(0, 0),
)
for k in range(1, len(order)):
    prev = order[k - 1]
    v = order[k]
    states = {u: "done" for u in order[:k]}
    states[v] = "current"
    rec.step(
        f"Step {k}: 2 * min({prev}, {n} - {prev}) = {v}. The value {v} is not in `seen`, so "
        f"seen[{v}] = {k} and it joins the list.",
        g=graph_frame(k, states), a=array_frame(k, k),
    )
k = len(order)
states = {u: "done" for u in tail}
states.update({u: "path" for u in ring})
rng = [(first, k - 1, "cycle")]
if first > 0:
    rng.insert(0, (0, first - 1, "tail"))
rec.step(
    f"Step {k}: 2 * min({order[-1]}, {n} - {order[-1]}) = {back_to}, and {back_to} is already in "
    f"`seen` at step {first}. From step {first} on, the same {length} numerators repeat. The cycle "
    f"starts at step {first} and has length {k} - {first} = {length}.",
    g=graph_frame(k - 1, states, closing=True), a=array_frame(k - 1, None, rng),
)
if steps < len(order):
    answer = order[steps]
    rec.step(
        f"A query asks for step {steps}. The list already reaches that far, so read it directly: "
        f"`order[{steps}]` = {answer}.",
        g=graph_frame(k - 1, {**states, answer: "current"}, closing=True),
        a=array_frame(k - 1, steps),
    )
else:
    idx = first + (steps - first) % length
    answer = order[idx]
    rec.step(
        f"A query asks for step {steps:,}. Subtract the tail, {steps:,} - {first}, and keep the "
        f"remainder after dividing by {length}: {(steps - first) % length}. That lands on list "
        f"position {first} + {(steps - first) % length} = {idx}, which holds {answer}.",
        g=graph_frame(k - 1, {**states, answer: "current"}, closing=True),
        a=array_frame(k - 1, idx),
    )
rec.output(
    f"{order}\ncycle starts at step {first}, length {length}\nnumerator after {steps} steps: {answer}\n"
)
