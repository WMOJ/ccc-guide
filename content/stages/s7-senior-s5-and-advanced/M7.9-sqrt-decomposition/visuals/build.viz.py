import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
a = [int(x) for x in rec.readline().split()]
rec.readline()
kind, x, y = map(int, rec.readline().split())

b = 1
while b * b < n:
    b += 1
blocks = (n + b - 1) // b

heads = []
for k in range(blocks):
    lo = k * b
    hi = min(lo + b, n) - 1
    heads.append(f"{lo}-{hi}" if hi > lo else f"{lo}")


def frame(done, now):
    cells = []
    states = []
    for k in range(blocks):
        row = []
        for j in range(b):
            i = k * b + j
            row.append(a[i] if i < n else "-")
        total = sum(a[k * b:k * b + b])
        if k < done:
            row.append(total)
        else:
            row.append("?")
        cells.append(row)
        st = ["_"] * (b + 1)
        if k == now:
            st = ["c"] * (b + 1)
        elif k < done:
            st[b] = "d"
        states.append("".join(st))
    return {
        "t": vz.table(
            cells,
            states=states,
            row_heads=heads,
            col_heads=[f"+{j}" for j in range(b)] + ["sum"],
        )
    }


rec.step(
    f"{n} values, so the block size is `b` = {b}, the smallest number whose square reaches {n}. "
    f"Each row of the table is one block of up to {b} positions. The sums are not computed yet.",
    **frame(0, -1)
)
for k in range(blocks):
    lo = k * b
    part = a[lo:lo + b]
    expr = " + ".join(str(v) for v in part)
    extra = ""
    if len(part) < b:
        extra = f" This last block has only {len(part)} values, so it is shorter."
    rec.step(
        f"`sums[{k}]` is the total of positions {heads[k]}: {expr} = {sum(part)}.{extra}",
        **frame(k + 1, k)
    )
rec.step(
    f"Done: {blocks} sums for {n} values. Position `i` lives in block `i // {b}`, so position "
    f"{n - 1} is in block {(n - 1) // b}. Adding all the sums gives {sum(a)}, the total of "
    "every value.",
    **frame(blocks, -1)
)
rec.output(f"{sum(a)}\n")
