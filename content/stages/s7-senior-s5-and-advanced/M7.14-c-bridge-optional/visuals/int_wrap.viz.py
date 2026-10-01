import vizrec as vz

LO = -(2**31)
HI = 2**31 - 1


def wrap32(x):
    return (x + 2**31) % 2**32 - 2**31


rec = vz.Recorder()
start, step, count = map(int, rec.readline().split())

rows = [["?", "?"] for _ in range(count)]
heads = [f"add {k}" for k in range(1, count + 1)]
exact = start
out = []
for k in range(1, count + 1):
    exact += step
    w = wrap32(exact)
    rows[k - 1] = [str(exact), str(w)]
    states = {}
    for j in range(k - 1):
        states[(j, 0)] = "done"
        states[(j, 1)] = "done"
    if w == exact:
        states[(k - 1, 0)] = "current"
        states[(k - 1, 1)] = "current"
        text = (
            f"{exact - step} + {step} = {exact}, inside the 32-bit range {LO} to {HI}. "
            f"Both columns agree."
        )
    else:
        states[(k - 1, 0)] = "current"
        states[(k - 1, 1)] = "invalid"
        edge = HI if exact > HI else LO
        shift = -(2**32) if exact > HI else 2**32
        side = "above" if exact > HI else "below"
        text = (
            f"{exact - step} + {step} = {exact}, which is {side} {edge}, the end of the 32-bit range. "
            f"A 32-bit int keeps {exact} {'-' if shift < 0 else '+'} {2**32} = {w}. "
            f"Python's int is still {exact}."
        )
    rec.step(text, t=vz.table(rows, states=states, row_heads=heads, col_heads=["Python", "32-bit"]))
    out.append(f"{k} {exact} {w}")

rec.output("\n".join(out) + "\n")
