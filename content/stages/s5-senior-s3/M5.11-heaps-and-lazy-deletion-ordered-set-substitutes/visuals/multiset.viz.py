import heapq

import vizrec as vz

rec = vz.Recorder()
m = int(rec.readline())

heap = []  # (-value, id) tuples, ordered as a max-heap
pending = {}
count = 0
seq = 0
distinct = []


def heap_items(highlight=None, state="current"):
    out = []
    for neg_value, sid in sorted(heap):
        s = state if sid == highlight else None
        out.append((sid, -neg_value, s))
    return out


def pending_table():
    row = [pending.get(v, 0) for v in distinct]
    return vz.table([row], row_heads=["pending"], col_heads=distinct)


lines = []
for _ in range(m):
    op, raw = rec.readline().split()
    value = int(raw)
    if value not in distinct:
        distinct.append(value)
    if op == "A":
        seq += 1
        sid = f"e{seq}"
        heapq.heappush(heap, (-value, sid))
        count += 1
        lines.append(f"Added {value}, count = {count}")
        unit = "item" if count == 1 else "items"
        rec.step(
            f"Add {value}: it goes into the heap as {-value}. The multiset now holds {count} {unit}.",
            h=vz.heap(heap_items(highlight=sid)),
            p=pending_table(),
        )
    else:
        pending[value] = pending.get(value, 0) + 1
        count -= 1
        lines.append(f"Removed {value}, count = {count}")
        rec.step(
            f"Remove {value}: count drops to {count} right away, but the heap keeps its stale "
            f"entry. `pending[{value}]` becomes {pending[value]}, so a later query can skip it.",
            h=vz.heap(heap_items()),
            p=pending_table(),
        )

while heap:
    neg_value, sid = heap[0]
    value = -neg_value
    if pending.get(value, 0) > 0:
        before = pending[value]
        pending[value] -= 1
        rec.step(
            f"The top of the heap is {value}, but `pending[{value}]` is {before}. This entry stands "
            f"for an item that was removed, so it is discarded and the count stays {count}.",
            h=vz.heap(heap_items(highlight=sid, state="invalid")),
            p=pending_table(),
        )
        heapq.heappop(heap)
        continue
    lines.append(f"Maximum: {value}, remaining count: {count}")
    rec.step(
        f"The top of the heap is {value} and `pending[{value}]` is 0, so this entry is still in the "
        f"multiset. It is the maximum.",
        h=vz.heap(heap_items(highlight=sid, state="current")),
        p=pending_table(),
    )
    break

rec.output("\n".join(lines) + "\n")
