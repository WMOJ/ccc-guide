import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
marks = [int(rec.readline()) for _ in range(n)]

rows = [[m, "?", "?"] for m in marks]
state_map = {}
ge = 0
gt = 0
heads = ["mark", ">= 50", "> 50"]


def table():
    return vz.table([list(r) for r in rows], states=dict(state_map), col_heads=heads)


rec.step(
    f"Two versions of the pass test, >= 50 and > 50, run on the same {n} marks. "
    "A mark of exactly 50 is the one that can tell them apart.",
    table=table(),
)
for i, m in enumerate(marks):
    a = m >= 50
    b = m > 50
    ge += 1 if a else 0
    gt += 1 if b else 0
    rows[i][1] = "pass" if a else "fail"
    rows[i][2] = "pass" if b else "fail"
    state_map[(i, 1)] = "done" if a else "invalid"
    state_map[(i, 2)] = "done" if b else "invalid"
    if a == b:
        why = f"Both versions {'pass' if a else 'fail'} it."
    else:
        why = "It is exactly 50, so >= 50 passes it but > 50 fails it."
    rec.step(f"Mark {m}. {why} Counts so far: {ge} with >=, {gt} with >.", table=table())
rec.step(
    f"Final counts: {ge} with >= 50 and {gt} with > 50. "
    + ("They agree here." if ge == gt else f"They differ by {ge - gt}, all from marks equal to 50."),
    table=table(),
)
rec.output(f"{ge}\n")
