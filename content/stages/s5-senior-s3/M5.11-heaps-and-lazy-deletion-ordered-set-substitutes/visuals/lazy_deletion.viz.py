import heapq

import vizrec as vz

rec = vz.Recorder()
n, m = (int(x) for x in rec.readline().split())

INF = 10 ** 9
best = [INF] * n
heap = []
lines = []
seq = 0


def heap_items(highlight=None, state="current"):
    out = []
    for priority, item, sid in sorted(heap):
        s = state if item == highlight else None
        out.append((str(sid), f"{priority}, j{item}", s))
    return out


def describe_best(item):
    return "already handed out" if best[item] == -1 else str(best[item])


def best_table():
    def cell(i):
        if best[i] == INF:
            return "-"
        if best[i] == -1:
            return "out"
        return best[i]

    row = [cell(i) for i in range(n)]
    return vz.table([row], row_heads=["best"], col_heads=[f"j{i}" for i in range(n)])


for _ in range(m):
    op = rec.readline().split()
    if op[0] == "U":
        item, priority = int(op[1]), int(op[2])
        best[item] = priority
        seq += 1
        heapq.heappush(heap, (priority, item, seq))
        lines.append(f"Update job {item} to priority {priority}")
        rec.step(
            f"Update job {item} to priority {priority}: a new entry goes into the heap, and "
            f"`best[{item}]` becomes {priority}.",
            h=vz.heap(heap_items(highlight=item)),
            b=best_table(),
        )
    else:
        while True:
            priority, item, _sid = heap[0]
            if priority != best[item]:
                rec.step(
                    f"Pop `({priority}, j{item})`. `best[{item}]` is {describe_best(item)}, which "
                    f"does not match, so this entry is stale and is discarded.",
                    h=vz.heap(heap_items(highlight=item, state="invalid")),
                    b=best_table(),
                )
                lines.append(f"Skipping stale entry (priority {priority}, job {item})")
                heapq.heappop(heap)
                continue
            rec.step(
                f"Pop `({priority}, j{item})`. It matches `best[{item}]` = {best[item]}, so job "
                f"{item} is handed out at priority {priority}.",
                h=vz.heap(heap_items(highlight=item, state="current")),
                b=best_table(),
            )
            lines.append(f"Job {item} at priority {priority} is handed out")
            heapq.heappop(heap)
            best[item] = -1
            break

rec.output("\n".join(lines) + "\n")
