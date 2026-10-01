import math
import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
k = int(data[0])
sizes = list(map(int, data[1:1 + k]))

lefts = []
left = sum(sizes)
for size in sizes:
    lefts.append(left)
    left -= size


def frame(upto, ways, products):
    cells = []
    states = {}
    for g in range(k):
        done = g <= upto
        cells.append([
            sizes[g],
            lefts[g],
            ways[g] if done else None,
            products[g] if done else None,
        ])
        for c in range(4):
            if g < upto:
                states[(g, c)] = "done"
            elif g == upto:
                states[(g, c)] = "current"
    return vz.table(cells, states=states, row_heads=[f"group {g + 1}" for g in range(k)],
                    col_heads=["size", "left", "ways", "product"])


ways = []
products = []
ways_total = 1
for g in range(k):
    w = math.comb(lefts[g], sizes[g])
    ways.append(w)
    ways_total *= w
    products.append(ways_total)
    caption = (
        f"Group {g + 1} takes {sizes[g]} of the {lefts[g]} items still unplaced: "
        f"C({lefts[g]}, {sizes[g]}) = {w} {'way' if w == 1 else 'ways'}. The running product is {ways_total}."
    )
    if g == k - 1:
        caption += " Every item is placed, so this product is the answer."
    rec.step(caption, t=frame(g, ways, products))

rec.output(f"{ways_total}\n")
