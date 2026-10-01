"""StepThrough: the format spec `>{WIDTH}.2f` applied to one float, one part at a time.

One ArrayViz panel of characters; each padding space is drawn as a dot. Consistency: rec.output()
must equal field_width.py's real stdout for the same stdin.
"""

import vizrec as vz

rec = vz.Recorder()

raw = rec.readline().strip()
x = float(raw)
WIDTH = 7

digits = f"{x:.2f}"
pad = max(0, WIDTH - len(digits))
field = f"{x:>{WIDTH}.2f}"

rec.step(
    f"`x` holds {x}. The spec `>{WIDTH}.2f` has three parts: `.2f` for the decimals, `{WIDTH}` for the "
    "width, and `>` for the alignment. Python applies them in that order.",
    text=vz.array(list(repr(x)), states="c" * len(repr(x))),
)

rec.step(
    f"`.2f` turns the float into text with exactly two digits after the point: {digits}. That text "
    f"is {len(digits)} characters long.",
    text=vz.array(list(digits), states="d" * len(digits)),
)

if pad:
    rec.step(
        f"`{WIDTH}` asks for a field at least {WIDTH} wide. The text is {len(digits)}, so {pad} padding spaces "
        "are needed, drawn here as dots. `>` puts them on the left, which lines the text up against "
        "the right edge.",
        text=vz.array(
            ["·"] * pad + list(digits),
            states="m" * pad + "d" * len(digits),
            ranges=[(0, pad + len(digits) - 1, f"width {WIDTH}")],
        ),
    )
else:
    rec.step(
        f"`{WIDTH}` asks for a field at least {WIDTH} wide. The text is already {len(digits)}, so no padding "
        "is added. A width is a minimum: Python never cuts a number short to fit it.",
        text=vz.array(
            list(digits),
            states="d" * len(digits),
            ranges=[(0, len(digits) - 1, f"wider than {WIDTH}")],
        ),
    )

rec.step(
    f"`print` shows [{field}]. The brackets belong to the f-string, so you can see where the field "
    "begins and ends.",
    text=vz.array(["·"] * pad + list(digits), states="d" * (pad + len(digits))),
)

rec.output(f"[{field}]\n")
rec.done()
