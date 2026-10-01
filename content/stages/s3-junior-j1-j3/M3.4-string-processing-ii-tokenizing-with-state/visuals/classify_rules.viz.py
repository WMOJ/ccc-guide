import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)

MODES = ["start", "letters", "number"]
KINDS = ["letter", "digit", "sign"]
# Rule for (mode before, kind of the next character): "new" closes the current token, if any,
# and starts a fresh one with this character; "extend" adds it to the current token.
RULES = [
    ["new", "new", "new"],
    ["extend", "new", "new"],
    ["new", "extend", "new"],
]


def chars_frame(i):
    states = ["done" if pos < i else "_" for pos in range(n)]
    states[i] = "current"
    return vz.array(list(s), states=states, pointers={"i": i})


def rules_frame(row, col):
    states = {}
    if row is not None:
        states[(row, col)] = "current"
    return vz.table(
        cells=RULES,
        states=states,
        row_heads=MODES,
        col_heads=KINDS,
        row_title="mode",
        col_title="next char",
    )


tokens = []
buf = []
mode = "start"
for i, char in enumerate(s):
    if char in "+-":
        kind = "sign"
    elif char.isalpha():
        kind = "letter"
    else:
        kind = "digit"
    row = MODES.index(mode)
    col = KINDS.index(kind)
    rule = RULES[row][col]
    closed = None
    if rule == "new" and buf:
        closed = "".join(buf)
        tokens.append(closed)
        buf = []
    buf.append(char)
    new_mode = "letters" if kind == "letter" else "number"
    if rule == "extend":
        what = f"the table says extend: '{char}' joins '{''.join(buf[:-1])}'."
    elif closed is None:
        what = f"the table says new: '{char}' starts the first token."
    else:
        what = f"the table says new: '{closed}' is complete and '{char}' starts a fresh token."
    rec.step(
        f"s[{i}] is '{char}', a {kind}; mode was {mode}, so {what} Mode is now {new_mode}.",
        chars=chars_frame(i),
        rules=rules_frame(row, col),
    )
    mode = new_mode

tokens.append("".join(buf))
rec.step(
    f"The line ends and '{''.join(buf)}' is appended: {len(tokens)} tokens, {', '.join(tokens)}.",
    chars=vz.array(list(s), states=["done"] * n),
    rules=rules_frame(None, None),
)

rec.output("\n".join(tokens) + "\n")
