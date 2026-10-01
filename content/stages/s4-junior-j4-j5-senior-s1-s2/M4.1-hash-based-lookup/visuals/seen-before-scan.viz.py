import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
values = data[1:1 + n]

seen_order = []
seen_set = set()


def items_frame(i):
    states = []
    for j in range(n):
        if j < i:
            states.append("done")
        elif j == i:
            states.append("current")
        else:
            states.append("none")
    return vz.array(values, states=states, pointers={"i": i} if i < n else None)


def seen_frame(hit=None, new=None):
    items = []
    for v in seen_order:
        if v == hit:
            items.append((v, "compare"))
        elif v == new:
            items.append((v, "current"))
        else:
            items.append((v, "done"))
    return vz.struct("set", items)


results = []
for i, value in enumerate(values):
    if value in seen_set:
        rec.step(
            f'"{value}" is already in seen. This is a repeat.',
            items=items_frame(i),
            seen=seen_frame(hit=value),
        )
        results.append("seen")
    else:
        seen_order.append(value)
        seen_set.add(value)
        rec.step(
            f'"{value}" is not in seen yet. It is new, so it joins the set now.',
            items=items_frame(i),
            seen=seen_frame(new=value),
        )
        results.append("new")

rec.output("\n".join(results) + "\n")
