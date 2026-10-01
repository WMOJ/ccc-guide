import heapq

import vizrec as vz

rec = vz.Recorder()
n, k = (int(x) for x in rec.readline().split())
values = [int(x) for x in rec.readline().split()]

heap = []
minimums = []


def heap_items(highlight=None, state="current"):
    out = []
    for v, i in sorted(heap):
        s = state if i == highlight else None
        out.append((str(i), v, s))
    return out


def array_frame(i, ptr_name="i"):
    ranges = None
    if i >= k - 1:
        ranges = [(i - k + 1, i, "window")]
    return vz.array(values, pointers={ptr_name: i}, ranges=ranges, name="values")


for i in range(n):
    heapq.heappush(heap, (values[i], i))
    top_v, top_i = heap[0]
    rec.step(
        f"Push `({values[i]}, {i})`. The heap orders entries by value first, so the top entry is "
        f"now `({top_v}, {top_i})`, whichever index carries the smallest value.",
        a=array_frame(i),
        h=vz.heap(heap_items(highlight=i)),
    )
    while heap[0][1] <= i - k:
        stale_v, stale_i = heap[0]
        rec.step(
            f"The top entry `({stale_v}, {stale_i})` has an index that already left the window "
            f"`[{i - k + 1}, {i}]`. It is discarded without ever being read.",
            a=array_frame(i),
            h=vz.heap(heap_items(highlight=stale_i, state="invalid")),
        )
        heapq.heappop(heap)
    if i >= k - 1:
        v, idx = heap[0]
        minimums.append(v)
        rec.step(
            f"The window `[{i - k + 1}, {i}]` is complete. The heap's top entry, `({v}, {idx})`, is "
            f"still inside it, so {v} is the window's minimum.",
            a=array_frame(i),
            h=vz.heap(heap_items(highlight=idx, state="current")),
        )

rec.output(" ".join(str(x) for x in minimums) + "\n")
