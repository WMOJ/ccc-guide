import vizrec as vz

rec = vz.Recorder()
lines = rec.stdin.split("\n")
if lines and lines[-1] == "":
    lines.pop()
n_lines = len(lines)
total = sum(int(x) for x in rec.stdin.split()[1:])


def noun(count):
    return f"{count} call{'s' if count != 1 else ''}"


def lines_frame(done):
    states = ["done" if i < done else "_" for i in range(n_lines)]
    return vz.array(lines, states=states, indices=True)


def calls_frame(loop_calls):
    return vz.table(
        cells=[[loop_calls], [1]],
        row_heads=["input() loop", "read() once"],
        col_heads=["calls so far"],
        states=["c", "d"] if loop_calls else None,
    )


rec.step(
    "The input has "
    + (f"{n_lines} lines: a count, then one value per line. " if n_lines != 1 else "1 line: just the count, 0. ")
    + "One read() call already holds all of them. The input() loop has made 1 call so far, for the count.",
    lines=lines_frame(1),
    calls=calls_frame(1),
)
for k in range(2, n_lines + 1):
    rec.step(
        f"The loop calls input() again for line {k - 1}, '{lines[k - 1]}': {noun(k)} so far. read() is still at 1.",
        lines=lines_frame(k),
        calls=calls_frame(k),
    )

if n_lines == 1:
    tail = "With a count of 0 there is nothing else to read, so both ways make 1 call."
else:
    tail = f"The loop made {n_lines} calls and read() made 1, for the same values."
rec.step(
    f"Every line is consumed and the sum is {total} either way. {tail}",
    lines=lines_frame(n_lines),
    calls=calls_frame(n_lines),
)

rec.output(f"{total}\n")
