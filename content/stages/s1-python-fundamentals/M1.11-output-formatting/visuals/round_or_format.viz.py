"""StepThrough: round(x, 2) next to f"{x:.2f}", a number versus a piece of text.

One TableViz panel with a row per line of round_or_format.py. Consistency: rec.output() must equal
round_or_format.py's real stdout for the same stdin.
"""

import vizrec as vz

rec = vz.Recorder()

x = float(rec.readline())
rounded = round(x, 2)
text = f"{x:.2f}"
ROWS = ["round(x, 2)", 'f"{x:.2f}"']


def table(filled, current):
    cells = [["-", "-"], ["-", "-"]]
    states = [["."] * 2, ["."] * 2]
    if filled >= 1:
        cells[0] = ["float", str(rounded)]
    if filled >= 2:
        cells[1] = ["str", text]
    for r in range(filled):
        states[r] = ["d", "d"]
    if current is not None:
        states[current] = ["c", "c"]
    return vz.table(cells, states=["".join(r) for r in states], row_heads=ROWS, col_heads=["gives", "prints"])


rec.step(
    f"`x = float(input())` reads {x}. Both lines below start from this one value.",
    table=table(0, None),
)
rec.step(
    f"`round(x, 2)` returns a float rounded to 2 places, {rounded}. A float has no memory of how "
    f"many digits you wanted, so `print` shows {rounded}.",
    table=table(1, 0),
)
rec.step(
    f'`f"{{x:.2f}}"` returns text with exactly 2 digits after the point: {text}. It is a string, '
    "so the digits are kept as written.",
    table=table(2, 1),
)
if str(rounded) == text:
    tail = (
        f"Both lines print {text} this time, because {x} already has at least two decimals. "
        "The difference shows up when it has fewer."
    )
else:
    tail = (
        f"The two lines print {rounded} and {text} for the same value. A problem that asks for "
        "exactly two decimal places wants the second line."
    )
rec.step(tail, table=table(2, None))

rec.output(f"{rounded}\n{text}\n")
rec.done()
