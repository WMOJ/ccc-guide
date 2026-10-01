"""StepThrough: read_global.py, how Python finds x (local) and rate (global).

Two panels: the global scope and the local scope of the running scaled() call.
Consistency: rec.output() must equal read_global.py's real stdout for the same stdin.
"""

import vizrec as vz

rec = vz.Recorder()

n = int(rec.readline())
rate = 3


def g(current=None):
    return vz.struct(
        "map",
        [
            {"k": "rate", "v": rate, "s": "c" if current == "rate" else None},
            {"k": "scaled", "v": "function"},
            {"k": "n", "v": n},
        ],
    )


def local(items):
    return vz.struct("map", items)


rec.step(
    f"The top-level lines ran: `rate` is {rate}, `scaled` is a function, and `n` is {n}, read from "
    "input. All three names live in the global scope. No call is running, so the local scope is empty.",
    global_scope=g(),
    local_scope=local([]),
)
rec.step(
    f"`scaled(n)` is called. Python makes a local scope for this call and puts the parameter `x` in "
    f"it, set to {n}.",
    global_scope=g(),
    local_scope=local([{"k": "x", "v": n, "s": "c"}]),
)
rec.step(
    f"`x * rate` needs `x` first. Python looks in the local scope, finds `x` there, and uses {n}.",
    global_scope=g(),
    local_scope=local([{"k": "x", "v": n, "s": "c"}]),
)
rec.step(
    f"Next it needs `rate`. The local scope has no `rate`, so Python looks in the global scope "
    f"and finds {rate}. Reading a global needs no `global` line.",
    global_scope=g(current="rate"),
    local_scope=local([{"k": "x", "v": n}]),
)
result = n * rate
rec.step(
    f"`{n} * {rate}` is {result}. `return` hands it back, and the local scope disappears. The "
    "global names are unchanged.",
    global_scope=g(),
    local_scope=local([]),
)
rec.step(
    f"`print(scaled(n))` shows {result}, the returned value.",
    global_scope=g(),
    local_scope=local([]),
)

rec.output(f"{result}\n")
rec.done()
