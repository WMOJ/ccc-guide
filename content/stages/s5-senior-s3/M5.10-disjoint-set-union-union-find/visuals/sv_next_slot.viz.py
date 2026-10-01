import vizrec as vz

rec = vz.Recorder()
n, k = map(int, rec.readline().split())

# Slots 1..n, plus one sentinel slot at n + 1 that is never taken.
parent = list(range(n + 2))


def find(x):
    path = [x]
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
        path.append(x)
    return x, path


def frame(pointer_at=None, current=None):
    values = parent[1:n + 2]
    states = ["done" if parent[1 + i] != (1 + i) else None for i in range(n)] + ["wall"]
    if current is not None:
        states[current - 1] = "current"
    pointers = [("request", pointer_at - 1)] if pointer_at is not None else None
    return {
        "p": vz.array(values, states=states, pointers=pointers, index_base=1),
    }


slot_word = "slot starts" if n == 1 else "slots start"
rec.step(
    f"{n} {slot_word} free, each pointing at itself in `parent`. Slot {n + 1} is a "
    "sentinel that is never handed out, shown here as the hatched cell: it marks "
    "\"nothing free at or after here\".",
    **frame()
)

out_lines = []
for _ in range(k):
    slot, path = find(1)
    route = " -> ".join(str(p) for p in path)
    if slot == n + 1:
        rec.step(
            f"A new request. `find(1)` climbs {route} and reaches the sentinel at {n + 1}, so "
            "every real slot is taken. This request gets -1.",
            **frame(pointer_at=1, current=n + 1)
        )
        out_lines.append("-1")
        continue
    rec.step(
        (
            f"A new request. `find(1)` climbs {route}, hopping over every taken slot, and lands "
            f"on slot {slot}, the lowest one still free."
            if len(path) > 1
            else "A new request. Slot 1 points at itself, so `find(1)` stops at once: slot 1 is free."
        ),
        **frame(pointer_at=1, current=slot)
    )
    parent[slot] = slot + 1
    out_lines.append(str(slot))
    rec.step(
        f"Slot {slot} is now taken. `parent[{slot}]` points to {slot + 1}, so the next `find` "
        f"skips straight over it.",
        **frame(current=slot)
    )

rec.output("\n".join(out_lines) + "\n")
