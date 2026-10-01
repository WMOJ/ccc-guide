import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def chars_frame(i):
    states = ["done" if pos < i else "_" for pos in range(n)]
    states[i] = "current"
    return vz.array(list(s), states=states, pointers={"i": i})


def state_frame(mode, buf, tokens):
    current = "".join(buf) if buf else "(empty)"
    return vz.table(
        cells=[[mode or "(none)"], [current], [", ".join(tokens) or "(none)"]],
        row_heads=["mode", "current token", "tokens so far"],
        col_heads=["value"],
    )


tokens = []
buf = []
mode = ""
for i, char in enumerate(s):
    is_sign = char in "+-"
    kind = "letters" if char.isalpha() else "number"
    starts_new = is_sign or kind != mode
    if starts_new and buf:
        tokens.append("".join(buf))
        buf = []
    if is_sign:
        caption = f"s[{i}] is '{char}': a sign always starts a new number token."
    elif starts_new:
        caption = f"s[{i}] is '{char}', a {kind} character: the mode changes from {mode or '(none)'}."
    else:
        caption = f"s[{i}] is '{char}': mode stays {mode}."
    mode = kind
    buf.append(char)
    rec.step(
        caption + f" The current token is now '{''.join(buf)}'.",
        chars=chars_frame(i),
        state=state_frame(mode, buf, tokens),
    )

tokens.append("".join(buf))
rec.step(
    f"The string ends: '{''.join(buf)}' joins the tokens, giving {len(tokens)} in total.",
    chars=chars_frame(n - 1),
    state=state_frame(mode, [], tokens),
)

rec.output("\n".join(tokens) + "\n")
