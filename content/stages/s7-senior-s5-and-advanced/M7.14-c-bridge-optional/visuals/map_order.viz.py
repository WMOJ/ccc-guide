import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
counts = {}
order = []


def cells(keys):
    return [f"{k}:{counts[k]}" for k in keys]


for key in tokens:
    new = key not in counts
    counts[key] = counts.get(key, 0) + 1
    if new:
        order.append(key)
    sk = sorted(counts)
    di = order.index(key)
    mi = sk.index(key)
    dstates = {di: "current"}
    mstates = {mi: "current"}
    if new:
        text = (
            f"`{key}` is new. The dict puts it at the end, position {di}. The map puts it in "
            f"sorted position {mi}, among the keys {sk}."
        )
    else:
        text = f"`{key}` is already there, so both containers only raise its count to {counts[key]}."
    rec.step(
        text,
        d=vz.array(cells(order), states=dstates),
        m=vz.array(cells(sk), states=mstates),
    )

sk = sorted(counts)
rec.step(
    "The program prints the dict in the order keys first appeared and the map in key order. "
    + ("The two orders match." if sk == order else "The orders differ."),
    d=vz.array(cells(order), states="d" * len(order)),
    m=vz.array(cells(sk), states="d" * len(sk)),
)
rec.output(
    "dict " + " ".join(f"{k}:{counts[k]}" for k in order) + "\n"
    + "map  " + " ".join(f"{k}:{counts[k]}" for k in sk) + "\n"
)
