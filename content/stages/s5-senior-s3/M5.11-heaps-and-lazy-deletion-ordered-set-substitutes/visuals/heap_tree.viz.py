import heapq

import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(x) for x in rec.readline().split()]

heap = []


def build_tree(highlight=None, state="current"):
    def node_at(i):
        if i >= len(heap):
            return None
        kids = [c for c in (node_at(2 * i + 1), node_at(2 * i + 2)) if c is not None]
        s = state if i == highlight else None
        return vz.node(i, heap[i], children=kids or None, state=s)

    return node_at(0) if heap else None


lines = ["Heap list: " + str([])]
for value in values:
    heapq.heappush(heap, value)
    idx = heap.index(value)
    rec.step(
        f"Push {value}: it starts at the end of the list, then moves up past any parent that is "
        f"bigger than it. It settles at index {idx}.",
        t=vz.tree(build_tree(highlight=idx)),
        a=vz.array(heap, states={idx: "current"}, name="heap"),
    )
lines[0] = "Heap list: " + str(heap)

popped = []
while heap:
    root = heap[0]
    if len(heap) == 1:
        rec.step(
            f"{root} is the only item left. Popping it empties the heap.",
            t=vz.tree(build_tree(highlight=0)),
            a=vz.array(heap, states={0: "current"}, name="heap"),
        )
        heapq.heappop(heap)
        popped.append(root)
        break
    rec.step(
        f"The root, {root}, is the smallest item in the heap, so `heappop` returns it next.",
        t=vz.tree(build_tree(highlight=0)),
        a=vz.array(heap, states={0: "current"}, name="heap"),
    )
    heapq.heappop(heap)
    popped.append(root)
    moved = heap[0]
    rec.step(
        f"The last item in the list, {moved}, moves to the root and sifts down past any child "
        f"that is smaller than it, until both of its children are at least as big.",
        t=vz.tree(build_tree(highlight=0)),
        a=vz.array(heap, states={0: "current"}, name="heap"),
    )

output = lines[0] + "\n" + " ".join(str(x) for x in popped) + " \n"
rec.output(output)
