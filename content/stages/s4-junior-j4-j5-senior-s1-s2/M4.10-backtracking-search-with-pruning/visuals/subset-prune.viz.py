import vizrec as vz

rec = vz.Recorder()
line1 = rec.readline().split()
n, target = int(line1[0]), int(line1[1])
values = [int(v) for v in rec.readline().split()]

nodes = {}
child_order = {}


def make_id(path):
    return "root" if not path else "n" + "".join(str(i) for i in path)


def add_node(path, label):
    nid = make_id(path)
    nodes[nid] = {"label": label, "state": "unvisited"}
    child_order[nid] = []
    if path:
        parent_id = make_id(path[:-1])
        child_order[parent_id].append(nid)
    return nid


def build(nid):
    kids = [build(c) for c in child_order[nid]]
    node = nodes[nid]
    return vz.node(nid, node["label"], children=kids or None, state=node["state"])


def frame():
    return {"tree": vz.tree(build("root"))}


add_node([], f"rem {0}")
nodes["root"]["state"] = "current"
found = 0


def search(path, index, remaining):
    global found
    nid = make_id(path)
    if remaining > target:
        nodes[nid]["state"] = "invalid"
        rec.step(
            f"The running sum is already {remaining}, past the target {target}. No element added "
            "from here can bring it back down, so this branch is pruned without going further.",
            **frame(),
        )
        return
    if index == n:
        if remaining == target:
            nodes[nid]["state"] = "path"
            found += 1
            rec.step(
                f"Every element has been decided and the sum is exactly {target}: this subset counts.",
                **frame(),
            )
        else:
            nodes[nid]["state"] = "done"
            rec.step(
                f"Every element has been decided and the sum is {remaining}, not {target}: this "
                "subset does not count.",
                **frame(),
            )
        return
    for choice, new_remaining, verb in (
        (False, remaining, "Skip"),
        (True, remaining + values[index], "Take"),
    ):
        child_path = path + [1 if choice else 0]
        child_id = add_node(child_path, f"rem {new_remaining}")
        nodes[child_id]["state"] = "current"
        nodes[nid]["state"] = "done"
        rec.step(
            f"{verb} {values[index]}: the running sum becomes {new_remaining}.",
            **frame(),
        )
        search(child_path, index + 1, new_remaining)


search([], 0, 0)
rec.output(f"{found}\n")
