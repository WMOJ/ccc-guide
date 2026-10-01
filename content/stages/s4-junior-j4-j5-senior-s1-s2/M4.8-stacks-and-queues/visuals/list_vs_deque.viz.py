import vizrec as vz

rec = vz.Recorder()
orders = rec.stdin.split()

items = list(orders)
moves = 0
n = len(items)


def frames(list_states=None, deque_items=None):
    return dict(
        plain=vz.array(items, states=list_states, indices=True),
        dq=vz.struct("deque", deque_items if deque_items else [(x, "done") for x in items]),
    )


rec.step(
    f"Both lines hold the same {n} {'order' if n == 1 else 'orders'}. A list line is served with "
    "pop(0), a deque line with popleft(). Count how many items each has to move.",
    **frames(),
)
served = []
while len(items) > 1:
    first = items.pop(0)
    served.append(first)
    shifted = len(items)
    moves += shifted
    rec.step(
        f"pop(0) removes '{first}' and slides the other {shifted} "
        f"{'item' if shifted == 1 else 'items'} one slot left ({moves} moves so far). "
        f"popleft() removes '{first}' and moves nothing (0 moves).",
        **frames(list_states=["compare"] * len(items)),
    )
last = items.pop(0)
served.append(last)
rec.step(
    f"'{last}' is the only order left, so pop(0) has nothing to slide. Serving all {n} "
    f"{'order' if n == 1 else 'orders'} cost the list {moves} moves and the deque 0. The "
    "served order is the same either way.",
    plain=vz.array(["-"], states=["none"]),
    dq=vz.struct("deque", [("empty", "none")]),
)
rec.output("\n".join(f"Served: {o}" for o in served) + "\n")
