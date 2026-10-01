import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
idx += 1
runners = []
for _ in range(n):
    name = data[idx]
    time = float(data[idx + 1])
    bib = int(data[idx + 2])
    runners.append((name, time, bib))
    idx += 3


def table_frame(order, states=None):
    return vz.table(
        [[r[0] for r in order], [r[1] for r in order], [r[2] for r in order]],
        states=states,
        row_heads=["name", "time", "bib"],
        col_heads=list(range(len(order))),
        col_title="position",
    )


rec.step(
    "Each runner's key is the tuple (time, bib), read in the order the input lists them.",
    table=table_frame(runners),
)

ranked = sorted(runners, key=lambda r: (r[1], r[2]))
tied_times = {t for t in (r[1] for r in runners) if [r[1] for r in runners].count(t) > 1}
if tied_times:
    highlight = ["_" * len(ranked), "".join("c" if r[1] in tied_times else "_" for r in runners), "_" * len(ranked)]
    rec.step(
        "Two runners share the same time, so the first key alone cannot rank them.",
        table=table_frame(runners, states=highlight),
    )
    rec.step(
        "The tuple's second element, bib number, breaks the tie: sorted() compares it only "
        "when the first elements are equal.",
        table=table_frame(ranked, states=["_" * len(ranked), "".join("c" if r[1] in tied_times else "_" for r in ranked), "_" * len(ranked)]),
    )
else:
    rec.step(
        "Every time is distinct here, so the tuple's second element, bib, never needs to break a tie.",
        table=table_frame(ranked),
    )

rec.step(
    "sorted() rearranges the runners by (time, bib), ascending: the fastest time first.",
    table=table_frame(ranked),
)

lines = [f"{name} {time} {bib}" for name, time, bib in ranked]
rec.output("\n".join(lines) + "\n")
