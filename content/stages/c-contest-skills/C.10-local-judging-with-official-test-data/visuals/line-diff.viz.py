import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = list(map(int, rec.readline().split()))[:n]
actual = [str(v * 2) for v in values]

m = int(rec.readline())
official = [rec.readline() for _ in range(m)]

rows = max(len(actual), len(official))


def show(line):
    if line is None:
        return "(none)"
    trimmed = line.rstrip(" ")
    trailing = len(line) - len(trimmed)
    return trimmed + "·" * trailing if trailing else line


def cells_and_state():
    cells = []
    states = []
    for i in range(rows):
        a = actual[i] if i < len(actual) else None
        o = official[i] if i < len(official) else None
        cells.append([show(a), show(o)])
        states.append("dd" if a == o else "xx")
    return cells, states


def frame(upto):
    cells, states = cells_and_state()
    return vz.table(
        cells=cells[:upto],
        states=states[:upto],
        row_heads=list(range(1, upto + 1)),
        col_heads=["actual", "official"],
        row_title="line",
    )


first_mismatch = None
for i in range(1, rows + 1):
    a = actual[i - 1] if i - 1 < len(actual) else None
    o = official[i - 1] if i - 1 < len(official) else None
    if a == o:
        caption = f"Line {i}: actual and official both print {show(a)}. They match."
    else:
        if first_mismatch is None:
            first_mismatch = i
        if a is None:
            caption = f"Line {i}: official expects {show(o)}, but the solution printed nothing here. Missing line."
        elif o is None:
            caption = f"Line {i}: the solution printed {show(a)}, but official has no line here."
        elif a.strip() == o.strip():
            caption = (
                f"Line {i}: official is {show(o)}, with trailing whitespace made visible (·). "
                f"The solution's {show(a)} does not match it character for character."
            )
        else:
            caption = f"Line {i}: official expects {show(o)}, the solution printed {show(a)}. First mismatch."
    rec.step(caption, table=frame(i))

if first_mismatch is None:
    verdict = "Every line matches: matches."
else:
    verdict = f"Line {first_mismatch} is the first mismatch, marked invalid: does NOT match."
rec.step(verdict, table=frame(rows))
rec.output("".join(v + "\n" for v in actual))
