import vizrec as vz

rec = vz.Recorder()
a, r, b, s = (int(t) for t in rec.readline().split())

x, y = a, b
while y != 0:
    x, y = y, x % y
g = x
limit = b // g
solvable = any((r + a * k) % b == s for k in range(limit))
cols = limit if solvable else limit + 2
cols = min(cols, 6)
tv = ["?"] * cols
rv = ["?"] * cols


def frame(current=None, repeat=(), found=None):
    states = {}
    for c in range(cols):
        if tv[c] != "?":
            states[(0, c)] = states[(1, c)] = "done"
    for c in repeat:
        states[(0, c)] = states[(1, c)] = "compare"
    if current is not None:
        states[(0, current)] = states[(1, current)] = "current"
    if found is not None:
        states[(1, found)] = "path"
    return vz.table([tv, rv], states=states, row_heads=["t", f"% {b}"], col_heads=list(range(cols)),
                    row_title="k")


rec.step(
    f"Find the smallest t with t % {a} = {r} and t % {b} = {s}. Every t with the first property is "
    f"{r} + {a}k. After {limit} candidates, t has moved by {a * limit}, which is lcm({a}, {b}) and a "
    f"whole number of laps of {b}. The remainders then repeat, so {limit} candidates are all there "
    "is to try. Nothing is tested yet (?).",
    t=frame(),
)
answer = None
for k in range(limit):
    t = r + a * k
    tv[k] = t
    rv[k] = t % b
    if t % b == s:
        answer = t
        rec.step(
            f"k = {k}: t = {r} + {a} * {k} = {t}, and {t} % {b} = {s}. Found: the smallest t is {t}.",
            t=frame(found=k),
        )
        break
    rec.step(
        f"k = {k}: t = {r} + {a} * {k} = {t}, and {t} % {b} = {t % b}, not {s}. Try the next k.",
        t=frame(current=k),
    )
if answer is None:
    for k in range(limit, cols):
        t = r + a * k
        tv[k] = t
        rv[k] = t % b
    rec.step(
        f"None of the {limit} candidates gave {s}. More candidates would not help: k = {limit} gives "
        f"t = {tv[limit]} with remainder {rv[limit]}, the same as k = 0, and the remainders go round in "
        f"the same loop of {limit}. So no t exists.",
        t=frame(repeat=list(range(limit, cols))),
    )
    rec.output(f"candidates to try: {limit}\nno t\n")
else:
    rec.output(f"candidates to try: {limit}\nsmallest t: {answer}\n")
