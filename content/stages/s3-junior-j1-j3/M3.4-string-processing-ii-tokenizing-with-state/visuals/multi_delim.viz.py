import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def quoted(tokens):
    return ", ".join(f'"{t}"' for t in tokens) or "(none)"


def chars_frame(i, width, consumed_to):
    states = ["done" if pos < consumed_to else "_" for pos in range(n)]
    for pos in range(i, min(i + width, n)):
        states[pos] = "compare"
    return vz.array(
        list(s),
        states=states,
        pointers={"i": i},
        ranges=[(i, min(i + 1, n - 1), "slice")],
    )


def state_frame(slice_text, buf, tokens):
    return vz.table(
        cells=[[f'"{slice_text}"'], [f'"{"".join(buf)}"'], [quoted(tokens)]],
        row_heads=["line[i:i+2]", "buf", "tokens"],
        col_heads=["value"],
    )


tokens = []
buf = []
i = 0
while i < n:
    piece = s[i:i + 2]
    if piece == "::":
        tokens.append("".join(buf))
        closed = "".join(buf)
        buf = []
        rec.step(
            f'line[{i}:{i + 2}] is "::": the delimiter. Token "{closed}" is complete, and i jumps by 2, past both colons.',
            chars=chars_frame(i, 2, i),
            state=state_frame(piece, buf, tokens),
        )
        i += 2
    else:
        buf.append(s[i])
        rec.step(
            f'line[{i}:{i + 2}] is "{piece}", not "::": line[{i}] is \'{s[i]}\' and joins buf, which is now "{"".join(buf)}". i moves by 1.',
            chars=chars_frame(i, 1, i),
            state=state_frame(piece, buf, tokens),
        )
        i += 1

tokens.append("".join(buf))
rec.step(
    f'The line ends. The last token, "{"".join(buf)}", is appended after the loop: {len(tokens)} tokens in total.',
    chars=vz.array(list(s), states=["done"] * n),
    state=state_frame("", [], tokens),
)

rec.output("\n".join(tokens) + "\n")
