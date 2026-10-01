from fractions import Fraction

import vizrec as vz

rec = vz.Recorder()
n, p_text = rec.readline().split()
n = int(n)
p = Fraction(p_text)
q = 1 - p


def show(f):
    return str(f)


# Build the whole tree of paths once; leaves are landings on or past square n.
index = {}
nodes = []  # dicts: id, label, note, kids, parent, leaf info


def build(square, chance, turns, steps, parent):
    nid = "r" + "".join(str(x) for x in steps)
    node = {"id": nid, "square": square, "chance": chance, "turns": turns, "steps": steps,
            "kids": [], "parent": parent}
    nodes.append(node)
    index[nid] = node
    if square < n:
        node["kids"].append(build(square + 1, chance * p, turns + 1, steps + [1], nid))
        node["kids"].append(build(square + 2, chance * q, turns + 1, steps + [2], nid))
    return nid


build(0, Fraction(1), 0, [], None)
leaves = [x["id"] for x in nodes if x["square"] >= n]


def word(k):
    return "1 turn" if k == 1 else f"{k} turns"


def short(k):
    return f"t={k}"


def tree_frame(current, done):
    on_path = set()
    if current is not None:
        at = current
        while at is not None:
            on_path.add(at)
            at = index[at]["parent"]

    def make(nid):
        x = index[nid]
        if x["square"] >= n:
            label = short(x["turns"])
        else:
            label = f"sq{x['square']}"
        note = "start" if nid == "r" else f"p {show(x['chance'])}"
        if nid == current:
            state = "current"
        elif nid in done:
            state = "done"
        elif nid in on_path:
            state = "path"
        else:
            state = None
        edge = "path" if nid in on_path and nid != "r" else None
        kids = [make(k) for k in x["kids"]] or None
        return vz.node(nid, label, children=kids, state=state, note=note, edge=edge)

    return vz.tree(make("r"))


heads = [",".join(str(s) for s in index[i]["steps"]) for i in leaves] + ["sum"]


def table_frame(filled, current=None):
    cells = []
    states = {}
    total = Fraction(0)
    for r, lid in enumerate(leaves):
        x = index[lid]
        if r < filled:
            contrib = x["chance"] * x["turns"]
            total += contrib
            cells.append([show(x["chance"]), x["turns"], show(contrib)])
            states[(r, 0)] = states[(r, 1)] = states[(r, 2)] = "done"
            if r == current:
                states[(r, 2)] = "current"
        else:
            cells.append(["-", "-", "-"])
    last = len(leaves)
    if filled == len(leaves):
        cells.append(["", "", show(total)])
        states[(last, 2)] = "current"
    else:
        cells.append(["", "", "-"])
    return vz.table(cells, states=states, row_heads=heads, col_heads=["chance", "turns", "product"], row_title="steps")


rec.step(
    f"A token starts on square 0 and each turn moves it 1 square with chance {show(p)} or 2 squares "
    f"with chance {show(q)}. The game ends on square {n} or beyond. Every node is a square, and its "
    "note is the chance of reaching it by that route, and a leaf t=3 is a game of 3 turns. The table is still empty.",
    tree=tree_frame(None, set()), table=table_frame(0),
)
done = set()
expected = Fraction(0)
for r, lid in enumerate(leaves):
    x = index[lid]
    contrib = x["chance"] * x["turns"]
    expected += contrib
    done.add(lid)
    steps_text = ", then ".join("1 square" if s == 1 else "2 squares" for s in x["steps"])
    rec.step(
        f"Path {r + 1}: move {steps_text}. The game lasts {word(x['turns'])} and this path has chance "
        f"{show(x['chance'])}, so it adds {show(x['chance'])} x {x['turns']} = {show(contrib)} to the sum.",
        tree=tree_frame(lid, done - {lid}), table=table_frame(r + 1, r),
    )
rec.step(
    f"All {len(leaves)} paths are added. Their chances total 1, and the weighted sum of the turns is "
    f"{show(expected)}, which is {float(expected):.4f}. That is the expected number of turns.",
    tree=tree_frame(None, done), table=table_frame(len(leaves)),
)
rec.output(f"paths: {len(leaves)}\nexpected turns: {float(expected):.4f}\n")
