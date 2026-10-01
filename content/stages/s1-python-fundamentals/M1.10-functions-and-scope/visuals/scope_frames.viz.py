"""StepThrough: the global scope next to add()'s local scope, traced alongside global_keyword.py.

Two panels, both StructViz kind "map": the global namespace and the local namespace that exists
only while add() is running. Consistency: rec.output() must equal global_keyword.py's real stdout.
"""

import vizrec as vz

rec = vz.Recorder()


def g(total, current=False):
    return vz.struct("map", [{"k": "total", "v": total, "s": "c" if current else None}])


def local(items):
    return vz.struct("map", items)


total = 0

rec.step(
    "Before either call, the global scope has one name, `total`, set to 0. No function is running, so there is no local scope yet.",
    global_scope=g(total),
    local_scope=local([]),
)


def add(x):
    global total
    rec.step(
        f"Calling add({x}) pushes a local scope holding only the parameter `x`. `global total` tells Python that `total` inside add refers to the global name, not a new local one.",
        global_scope=g(total),
        local_scope=local([{"k": "x", "v": x, "s": "c"}]),
    )
    total += x
    rec.step(
        f"`total += x` changes the global `total` directly, since `global total` ruled out a local copy. total is now {total}. The local scope still only holds x.",
        global_scope=g(total, current=True),
        local_scope=local([{"k": "x", "v": x}]),
    )


add(5)
rec.step(
    "add(5) returns. Its local scope, holding only x, disappears. The global total keeps the new value.",
    global_scope=g(total),
    local_scope=local([]),
)

add(3)
rec.step(
    "add(3) returns too. The global total ends at 8, changed by both calls, and no local total was ever created.",
    global_scope=g(total, current=True),
    local_scope=local([]),
)

rec.output(f"{total}\n")
rec.done()
