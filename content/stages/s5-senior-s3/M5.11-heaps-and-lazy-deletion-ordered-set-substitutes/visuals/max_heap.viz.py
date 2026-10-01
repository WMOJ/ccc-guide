import heapq

import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]

heap = []

stored_line = ""
popped = []

for value in values:
    heapq.heappush(heap, -value)
    idx = heap.index(-value)
    rec.step(
        f"Push {value}: it is stored as {-value}, so the heap keeps the biggest value where a "
        f"min-heap would keep the smallest.",
        s=vz.array(heap, states={idx: "current"}, name="stored"),
        v=vz.array([-x for x in heap], states={idx: "current"}, name="represented"),
    )

stored_line = "Stored as negatives: " + str(heap)

while heap:
    top = -heap[0]
    if len(heap) == 1:
        rec.step(
            f"{top} is the only item left. Popping it empties the heap.",
            s=vz.array(heap, states={0: "current"}, name="stored"),
            v=vz.array([-x for x in heap], states={0: "current"}, name="represented"),
        )
        heapq.heappop(heap)
        popped.append(top)
        break
    rec.step(
        f"The root is stored as {heap[0]}, so it represents {top}, the biggest value still in the "
        f"heap. Negating it on the way out gives back {top}.",
        s=vz.array(heap, states={0: "current"}, name="stored"),
        v=vz.array([-x for x in heap], states={0: "current"}, name="represented"),
    )
    heapq.heappop(heap)
    popped.append(top)
    rec.step(
        f"After the pop, the last stored value moves to the root and sifts down, keeping the "
        f"biggest remaining value, {-heap[0]}, at the top.",
        s=vz.array(heap, states={0: "current"}, name="stored"),
        v=vz.array([-x for x in heap], states={0: "current"}, name="represented"),
    )

output = stored_line + "\nItems in descending order:\n" + " ".join(str(x) for x in popped) + " \n"
rec.output(output)
