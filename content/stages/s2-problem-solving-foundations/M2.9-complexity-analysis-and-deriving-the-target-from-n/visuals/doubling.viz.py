import vizrec as vz

rec = vz.Recorder()
start = int(rec.readline())


def pairs(k):
    return k * (k - 1) // 2


def ratio(new, old):
    if old == 0:
        return "-"
    return f"{new / old:.1f}x"


sizes = [start]
for _ in range(3 if start >= 100 else 4):
    sizes.append(sizes[-1] * 2)


def frame(upto):
    cells = []
    for idx in range(upto + 1):
        k = sizes[idx]
        if idx == 0:
            cells.append([f"{k:,}", f"{pairs(k):,}", "-"])
        else:
            prev = sizes[idx - 1]
            cells.append([f"{k:,}", f"{pairs(k):,}", ratio(pairs(k), pairs(prev))])
    states = ["___"] * upto + ["ccc"]
    return vz.table(
        cells=cells,
        states=states,
        row_heads=[f"{sizes[i]:,}" for i in range(upto + 1)],
        row_title="n",
        col_heads=["single", "pairs", "vs last"],
    )


op_word = "operation" if start == 1 else "operations"
rec.step(
    f"At n = {start:,} a single loop does {start:,} {op_word} and the pairs loop does "
    f"{pairs(start):,}. Now double n and watch both counts.",
    table=frame(0),
)
for idx in range(1, len(sizes)):
    k = sizes[idx]
    prev = sizes[idx - 1]
    if pairs(prev) == 0:
        tail = f"The pairs loop goes from 0 to {pairs(k):,}; there is no earlier count to compare."
    else:
        tail = (
            f"The pairs loop goes from {pairs(prev):,} to {pairs(k):,}, about "
            f"{pairs(k) / pairs(prev):.1f} times as many."
        )
    rec.step(
        f"Double n to {k:,}. The single loop doubles to {k:,} operations. {tail}",
        table=frame(idx),
    )
rec.output(f"{pairs(start)}\n")
