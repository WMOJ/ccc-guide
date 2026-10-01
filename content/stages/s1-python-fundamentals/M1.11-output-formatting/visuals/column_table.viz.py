"""StepThrough: column_table.py's loop filling an aligned table one row at a time.

One TableViz panel. Consistency: rec.output() must equal column_table.py's real stdout for the
same stdin.
"""

import vizrec as vz

rec = vz.Recorder()


def padded_cell(text, width, side):
    """The exact formatted field, with each padding space drawn as a dot."""
    if len(text) >= width:
        return text
    dots = "·" * (width - len(text))
    return text + dots if side == "left" else dots + text


n = int(rec.readline())
rows = []
for _ in range(n):
    name, score = rec.readline().split()
    rows.append((name, int(score)))

table_rows = [[None, None] for _ in rows]
out = ""
for i, (name, score) in enumerate(rows):
    table_rows[i] = [padded_cell(name, 10, "left"), padded_cell(str(score), 5, "right")]
    states = []
    for r in range(len(rows)):
        if r == i:
            states.append("cc")
        elif r < i:
            states.append("dd")
        else:
            states.append("__")
    if len(name) > 10:
        name_part = f'prints "{name}" in its own {len(name)} characters, past the 10-character minimum'
    else:
        name_part = f'left-aligns "{name}" in 10 characters'
    rec.step(
        f'Row {i}: f"{{name:<10}}{{score:>5}}" {name_part} and right-aligns {score} in 5.',
        table=vz.table(table_rows, states=states, col_heads=["name", "score"]),
    )
    out += f"{name:<10}{score:>5}\n"

overflow_name = next((name for name, _ in rows if len(name) > 10), None)
if overflow_name:
    closing_caption = (
        f'"{overflow_name}" is {len(overflow_name)} characters, more than the 10-character '
        "field. A width in a format spec is only a minimum: it never cuts text short, so this "
        "row's score field starts later than a shorter name's would."
    )
else:
    closing_caption = (
        "Every row lines up under the last one: the name column always starts at position 0, "
        "and the score column always ends at position 14, however long each name or score is."
    )
rec.step(
    closing_caption,
    table=vz.table(table_rows, states=["dd"] * len(rows), col_heads=["name", "score"]),
)

rec.output(out)
rec.done()
