import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

quotients = [n // d for d in range(1, n + 1)]
blocks = []
d = 1
while d <= n:
    q = n // d
    last = n // q
    blocks.append((d, last, q))
    d = last + 1

rows = len(blocks) + 1


def table(filled, label_total=None):
    cells = []
    for i in range(rows - 1):
        if i < filled:
            a, b, q = blocks[i]
            span = str(a) if a == b else f"{a}-{b}"
            cells.append([span, q, b - a + 1, q * (b - a + 1)])
        else:
            cells.append(["?", "?", "?", "?"])
    total = sum(q * (b - a + 1) for a, b, q in blocks[:filled])
    cells.append(["", "", "sum", total if filled else "?"])
    states = {}
    if filled:
        for c in range(4):
            states[(filled - 1, c)] = "current"
    return vz.table(cells, states=states or None,
                    row_heads=[f"block {i + 1}" for i in range(rows - 1)] + [""],
                    col_heads=["d", "q", "size", "adds"])


def array(filled, current=None):
    states = {}
    for i in range(filled):
        a, b, q = blocks[i]
        for k in range(a - 1, b):
            states[k] = "done"
    ranges = None
    pointers = None
    if current is not None:
        a, b, q = current
        for k in range(a - 1, b):
            states[k] = "current"
        pointers = [("d", a - 1)]
        ranges = [(a - 1, b - 1, f"q = {q}")]
    return vz.array(quotients, states=states or None, pointers=pointers, ranges=ranges,
                    index_base=1)


rec.step(
    f"For n = {n}, the array shows `n // d` for d = 1 up to {n}. Equal neighbors form "
    "a block. The loop visits one block at a time and fills one table row for each.",
    a=array(0), t=table(0)
)
total = 0
for i, (a, b, q) in enumerate(blocks):
    size = b - a + 1
    total += q * size
    if size == 1:
        body = f"The block is just d = {a}"
    else:
        body = f"The block is d = {a} to {b}, {size} values"
    rec.step(
        f"d = {a}: q = {n} // {a} = {q}. The last d that still gives {q} is {n} // {q} = {b}. "
        f"{body}, so it adds {q} * {size} = {q * size}. Total so far {total}.",
        a=array(i, current=(a, b, q)), t=table(i + 1)
    )
rec.step(
    f"d jumps past {n}, so the loop ends: {len(blocks)} block{'s' if len(blocks) != 1 else ''} "
    f"added up to {total}, the same as adding all {n} term{'s' if n != 1 else ''} one by one.",
    a=array(len(blocks)), t=table(len(blocks))
)
rec.output(f"{total}\n{len(blocks)}\n")
