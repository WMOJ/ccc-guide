import vizrec as vz

rec = vz.Recorder()
target = int(rec.readline())

nodes = {}
child_order = {}
seen_count = {}


def make_id(path):
    return "root" if not path else "n" + "".join(str(i) for i in path)


def add_node(path, stair):
    nid = make_id(path)
    nodes[nid] = {"stair": stair, "state": "unvisited"}
    child_order[nid] = []
    if path:
        parent_id = make_id(path[:-1])
        child_order[parent_id].append(nid)
    return nid


def build(nid):
    kids = [build(c) for c in child_order[nid]]
    node = nodes[nid]
    label = f"ways({node['stair']})"
    return vz.node(nid, label, children=kids or None, state=node["state"])


def frame():
    return {"tree": vz.tree(build("root"))}


def visit(path, stair):
    nid = add_node(path, stair)
    seen_count[stair] = seen_count.get(stair, 0) + 1
    nodes[nid]["state"] = "current"
    ordinal = seen_count[stair]
    ordinal_words = {2: "second", 3: "third", 4: "fourth"}
    if ordinal == 1:
        seen_note = ""
    else:
        word = ordinal_words.get(ordinal, f"{ordinal}th")
        seen_note = f" This is the {word} time `ways({stair})` is called."
    if stair >= target:
        nodes[nid]["state"] = "path"
        rec.step(
            f"`ways({stair})` has reached or passed stair {target}, the top: it returns 1 "
            f"directly, with no further calls.{seen_note}",
            **frame(),
        )
        return 1
    rec.step(
        f"`ways({stair})` is called. It needs `ways({stair + 1})` and `ways({stair + 2})`.{seen_note}",
        **frame(),
    )
    left = visit(path + [0], stair + 1)
    right = visit(path + [1], stair + 2)
    total = left + right
    nodes[nid]["state"] = "done"
    rec.step(
        f"`ways({stair})` adds the two results it was waiting on, {left} + {right} = {total}, "
        "and returns.",
        **frame(),
    )
    return total


answer = visit([], 0)
rec.output(f"{answer}\n")
