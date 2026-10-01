"""StepThrough: a set rejecting a duplicate, traced alongside set_basics.py.

Two panels: `seen`, built the same way on every preset (three hardcoded adds), and `unique`,
built from the preset's own stdin via the set comprehension. Consistency: this file's rec.output()
must equal set_basics.py's real stdout for the same stdin.
"""

import vizrec as vz


def frame(order, members, current=None, rejected=None):
    items = []
    for v in order:
        if v == rejected:
            s = "x"
        elif v == current:
            s = "c"
        else:
            s = "d"
        items.append({"v": v, "s": s})
    return vz.struct("set", items)


rec = vz.Recorder()

empty = vz.struct("set", [])

seen_order = []
seen_members = set()


def add_seen(v):
    if v not in seen_members:
        seen_order.append(v)
    seen_members.add(v)


add_seen(3)
rec.step(
    "`seen = set()` starts empty, then `seen.add(3)` inserts 3.",
    seen=frame(seen_order, seen_members, current=3),
    unique=empty,
)

add_seen(3)
rec.step(
    "Adding 3 again does nothing. A set never stores the same value twice, so `seen` still holds only one 3.",
    seen=frame(seen_order, seen_members, rejected=3),
    unique=empty,
)

add_seen(5)
rec.step("`seen.add(5)` inserts 5. `seen` now holds 3 and 5.", seen=frame(seen_order, seen_members, current=5), unique=empty)
rec.step(
    "`len(seen)` is 2, not 3: the second `add(3)` never grew the set.",
    seen=frame(seen_order, seen_members),
    unique=empty,
)
rec.step(
    "`3 in seen` is True, checked the same way as `in` on a dict's keys.",
    seen=frame(seen_order, seen_members, current=3),
    unique=empty,
)

final_seen = frame(seen_order, seen_members)

tokens = rec.readline().split()
uniq_order = []
uniq_members = set()
for tok in tokens:
    n = int(tok)
    dup = n in uniq_members
    if not dup:
        uniq_order.append(n)
    uniq_members.add(n)
    if dup:
        rec.step(
            f"The next token is {n} again. Adding a duplicate to a set changes nothing, so `unique` still holds {sorted(uniq_members)}.",
            seen=final_seen,
            unique=frame(uniq_order, uniq_members, rejected=n),
        )
    else:
        rec.step(
            f"The comprehension reads {n} and adds it to `unique`.",
            seen=final_seen,
            unique=frame(uniq_order, uniq_members, current=n),
        )

rec.step(
    f"`sorted(unique)` prints {sorted(uniq_members)}: every duplicate token collapsed into the one value already there.",
    seen=final_seen,
    unique=frame(uniq_order, uniq_members),
)

out_lines = [str(len(seen_members)), str(3 in seen_members), str(sorted(uniq_members))]
rec.output("\n".join(out_lines) + "\n")
rec.done()
