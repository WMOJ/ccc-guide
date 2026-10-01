import heapq

import vizrec as vz

rec = vz.Recorder()
n, m, k = map(int, rec.readline().split())
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, rec.readline().split())
    adj[u].append((v, w))
    adj[v].append((u, w))
stops = [int(x) for x in rec.readline().split()] if k else []
bit = [0] * n
for i, room in enumerate(stops):
    bit[room] = 1 << i
size = 1 << k
full = size - 1

best = [-1] * (n * size)
done = [False] * (n * size)
heap = []


def frame(current=None, heap_marks=None):
    cells = []
    states = []
    for u in range(n):
        row = []
        srow = []
        for mask in range(size):
            s = u * size + mask
            if best[s] == -1:
                row.append("–")
                srow.append(None)
                continue
            row.append(best[s])
            if current == s:
                srow.append("current")
            elif done[s]:
                srow.append("done")
            else:
                srow.append("frontier")
        cells.append(row)
        states.append(srow)
    items = []
    for d, u, mask in sorted(heap):
        items.append((f"{d},{u},{mask}", (heap_marks or {}).get((d, u, mask))))
    return {
        "t": vz.table(cells, states=states, row_heads=list(range(n)),
                      col_heads=list(range(size)), row_title="room", col_title="mask"),
        "h": vz.heap(items),
    }


names = [f"{1 << i} means room {room}" + (" is collected" if i == 0 else "") for i, room in enumerate(stops)]
meaning = ", ".join(names) + (f", and {full} means both" if k == 2 else f", and {full} means all" if k > 2 else "")
start_mask = bit[0]
best[start_mask] = 0
heapq.heappush(heap, (0, 0, start_mask))
rec.step(
    f"Start in room 0 with mask {start_mask}. "
    + (f"Mask {meaning}. " if k else "")
    + f"The table has one cell for each of {n} rooms times {size} masks. Only the start cell has "
    f"a distance. The heap holds `0,0,{start_mask}`: distance, room, mask.",
    **frame()
)

settled = 0
answer = -1
while heap:
    d, u, mask = heap[0]
    s = u * size + mask
    if done[s]:
        rec.step(
            f"The smallest entry is `{d},{u},{mask}`, but the state (room {u}, mask {mask}) is "
            f"already settled at {best[s]}. The entry is out of date, so it is thrown away.",
            **frame(heap_marks={(d, u, mask): "invalid"})
        )
        heapq.heappop(heap)
        continue
    if mask == full:
        done[s] = True
        settled += 1
        answer = d
        rec.step(
            f"The smallest entry is `{d},{u},{mask}`: room {u} with every checkpoint collected. "
            f"It is settled at distance {d}, which is the answer, so the search stops.",
            **frame(current=s, heap_marks={(d, u, mask): "current"})
        )
        break
    rec.step(
        f"The smallest entry is `{d},{u},{mask}`: distance {d}, room {u}, mask {mask}. That state "
        f"is new, so it is settled at distance {d}.",
        **frame(current=s, heap_marks={(d, u, mask): "current"})
    )
    heapq.heappop(heap)
    done[s] = True
    settled += 1
    marks = {}
    parts = []
    for v, w in adj[u]:
        nmask = mask | bit[v]
        t = v * size + nmask
        nd = d + w
        if done[t]:
            parts.append(f"Room {v} with mask {nmask} is already settled.")
        elif best[t] == -1 or nd < best[t]:
            best[t] = nd
            heapq.heappush(heap, (nd, v, nmask))
            marks[(nd, v, nmask)] = "frontier"
            why = f" (a checkpoint, so mask {mask} becomes {nmask})" if nmask != mask else ""
            parts.append(f"Room {v} gets `{nd},{v},{nmask}`{why}.")
        else:
            parts.append(f"Room {v} with mask {nmask}: {nd} does not beat {best[t]}.")
    rec.step(f"State (room {u}, mask {mask}) is done. " + " ".join(parts), **frame(heap_marks=marks))

total = n * size
touched = sum(1 for b in best if b != -1)
if answer == -1:
    rec.step(
        f"The heap is empty and no settled state had every checkpoint, so the answer is -1. The "
        f"search settled {settled} of {total} states, every state it could reach.",
        **frame()
    )
else:
    rec.step(
        f"The answer is {answer}. The search settled {settled} of {total} states and queued "
        f"{touched - settled} more. The {total - touched} dashes are states it never built.",
        **frame()
    )
rec.output(f"distance {answer}\nsettled {settled} of {total} states\n")
