import vizrec as vz

rec = vz.Recorder()
sizes = [int(x) for x in rec.readline().split()]

leaves = []
nodes_used = []
lines = []
for size in sizes:
    lo = 1 + size
    hi = size - 1 + size
    nodes = 0
    while lo < hi:
        if lo % 2 == 1:
            nodes += 1
            lo += 1
        if hi % 2 == 1:
            hi -= 1
            nodes += 1
        lo //= 2
        hi //= 2
    leaves.append(size - 2)
    nodes_used.append(nodes)
    lines.append("size " + str(size) + ": " + str(size - 2) + " leaves, " + str(nodes) + " nodes")

rec.step(
    "Take a range that nearly fills the array, from position 1 up to `size - 1`. Adding to "
    f"it leaf by leaf needs {leaves[0]} writes at size {sizes[0]} and {leaves[-1]:,} writes at "
    f"size {sizes[-1]:,}. Tagging the covering nodes needs {nodes_used[0]} and "
    f"{nodes_used[-1]}. Each sixteenfold jump in size adds just 8 nodes.",
    v=vz.table(
        [leaves, nodes_used],
        row_heads=["leaves", "nodes"],
        col_heads=[str(s) for s in sizes],
        col_title="array size",
    )
)
rec.output("\n".join(lines) + "\n")
