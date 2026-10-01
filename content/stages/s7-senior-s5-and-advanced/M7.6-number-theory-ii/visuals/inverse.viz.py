import vizrec as vz

rec = vz.Recorder()
a, m = (int(t) for t in rec.readline().split())
xs = list(range(1, m))
prod = ["?"] * len(xs)
rem = ["?"] * len(xs)


def frame(current=None, found=None, none=False):
    states = {}
    for c in range(len(xs)):
        if prod[c] != "?":
            states[(0, c)] = states[(1, c)] = "done"
            if none:
                states[(1, c)] = "invalid"
    if current is not None:
        states[(0, current)] = states[(1, current)] = "current"
    if found is not None:
        states[(1, found)] = "current"
    return vz.table([prod, rem], states=states, row_heads=[f"{a}*x", f"% {m}"], col_heads=xs, row_title="x")


rec.step(
    f"An inverse of {a} modulo {m} is an x where {a} * x leaves remainder 1 after dividing by {m}. "
    f"Try x = 1 up to {m - 1} and read the remainder. Nothing is computed yet (?).",
    t=frame(),
)
answer = 0
for c, x in enumerate(xs):
    prod[c] = a * x
    rem[c] = a * x % m
    if a * x % m == 1:
        answer = x
        rec.step(
            f"x = {x}: {a} * {x} = {a * x}, and {a * x} % {m} = 1. The search stops here: "
            f"{x} is the inverse of {a} modulo {m}.",
            t=frame(found=c),
        )
        break
    rec.step(
        f"x = {x}: {a} * {x} = {a * x}, and {a * x} % {m} = {a * x % m}. That is not 1, so try the next x.",
        t=frame(current=c),
    )
if answer:
    rec.output(f"inverse of {a} mod {m} is {answer}\n")
else:
    rec.step(
        f"No x from 1 to {m - 1} left remainder 1. {a} and {m} share a factor, so the remainders only "
        f"ever take values that share it too. {a} has no inverse modulo {m}.",
        t=frame(none=True),
    )
    rec.output(f"no inverse of {a} mod {m}\n")
