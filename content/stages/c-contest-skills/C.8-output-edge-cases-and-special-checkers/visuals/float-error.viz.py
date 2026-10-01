from fractions import Fraction

import vizrec as vz

rec = vz.Recorder()
a, b = map(int, rec.readline().split())
q = a / b
want = Fraction(a, b)
TOL = Fraction(1, 10 ** 6)

# The three lines printed by examples/float_demo.py.
texts = [str(q), f"{q:.6f}", f"{q:.2f}"]
names = ["print(q)", 'f"{q:.6f}"', 'f"{q:.2f}"']


def err(x):
    if x == 0:
        return "0"
    return f"{float(x):.1e}"


rows = []
states = []
verdicts = []


def frame():
    return vz.table(
        cells=[list(r) for r in rows],
        states=list(states),
        row_heads=[t for t in texts[: len(rows)]],
        col_heads=["abs error", "rel error"],
        row_title="printed",
    )


for name, text in zip(names, texts):
    got = Fraction(text)
    abs_err = abs(got - want)
    rel_err = abs_err / want
    abs_ok = abs_err <= TOL
    rel_ok = rel_err <= TOL
    verdicts.append((name, abs_ok, rel_ok))
    rows.append((err(abs_err), err(rel_err)))
    states.append(("d" if abs_ok else "x") + ("d" if rel_ok else "x"))
    if abs_ok and rel_ok:
        tail = "Both errors are under 10^-6, so either kind of tolerance checker accepts it."
    elif abs_ok:
        tail = (
            "The absolute error is under 10^-6 but the relative error is not: "
            "an absolute checker accepts it and a relative checker rejects it."
        )
    elif rel_ok:
        tail = (
            "The relative error is under 10^-6 but the absolute error is not: "
            "a relative checker accepts it and an absolute checker rejects it."
        )
    else:
        tail = "Neither error is under 10^-6, so a tolerance checker rejects it."
    rec.step(
        f"{name} writes {text}. The true value is {a} / {b}, so its absolute error is "
        f"{err(abs_err)} and its relative error is {err(rel_err)}. {tail}",
        table=frame(),
    )

both = [n for n, x, y in verdicts if x and y]
if both:
    summary = (
        f"For {a} / {b}, only {' and '.join(both)} {'stays' if len(both) == 1 else 'stay'} under 10^-6 on both the absolute "
        "and the relative error."
    )
else:
    summary = f"For {a} / {b}, no line stays under 10^-6 on both errors."
rec.step(summary, table=frame())
rec.output("".join(t + "\n" for t in texts))
