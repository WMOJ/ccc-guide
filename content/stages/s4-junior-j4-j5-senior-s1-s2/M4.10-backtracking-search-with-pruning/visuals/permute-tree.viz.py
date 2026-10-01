import vizrec as vz

rec = vz.Recorder()
elements = rec.readline().split()
n = len(elements)

nodes = {}
child_order = {}


def make_id(path):
    return "root" if not path else "n" + "".join(str(i) for i in path)


def add_node(path, label):
    nid = make_id(path)
    nodes[nid] = {"label": label, "state": "unvisited", "edge": "unvisited"}
    child_order[nid] = []
    if path:
        parent_id = make_id(path[:-1])
        child_order[parent_id].append(nid)
    return nid


def build(nid):
    kids = [build(c) for c in child_order[nid]]
    node = nodes[nid]
    return vz.node(nid, node["label"], children=kids or None, state=node["state"], edge=node["edge"])


def frame(stack_items):
    return {"tree": vz.tree(build("root")), "stack": vz.stack(stack_items)}


add_node([], "()")
nodes["root"]["state"] = "current"
nodes["root"]["edge"] = None
rec.step("The search starts with an empty choice: nothing is on the stack yet.", **frame([]))

output_lines = []


def backtrack(path, current, used):
    nid = make_id(path)
    if len(current) == n:
        output_lines.append(" ".join(current))
        rec.step(
            f"The stack holds {' '.join(current)}: every element is chosen, so this permutation is recorded.",
            **frame(list(current)),
        )
        return
    for i in range(n):
        if used[i]:
            continue
        used[i] = True
        current.append(elements[i])
        child_path = path + [i]
        child_id = add_node(child_path, elements[i])
        nodes[child_id]["state"] = "current"
        nodes[child_id]["edge"] = "current"
        nodes[nid]["state"] = "done"
        rec.step(
            f"Choose {elements[i]}: it joins the top of the stack, opening a new branch of the tree.",
            **frame(list(current)),
        )
        backtrack(child_path, current, used)
        nodes[child_id]["state"] = "done"
        nodes[child_id]["edge"] = "done"
        current.pop()
        used[i] = False
        if current:
            rec.step(
                f"Unchoose {elements[i]}: it comes off the top of the stack, and the branch below it is fully explored.",
                **frame(list(current)),
            )

backtrack([], [], [False] * n)
nodes["root"]["state"] = "done"
rec.step(
    "The stack is empty again and every branch from the root has been explored: the search is done.",
    **frame([]),
)
rec.output("\n".join(output_lines) + "\n")
