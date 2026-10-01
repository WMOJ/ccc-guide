import vizrec as vz

rec = vz.Recorder()
word = rec.readline()
n = len(word)
letters = list(word)
states = ["none"] * n
result = ""


def frame(at):
    return vz.array(letters, states=states, pointers=[("ch", at, None, True)], name=f"'{result}'")


for i, ch in enumerate(word):
    old = len(result)
    result += ch
    states[i] = "current"
    if old == 0:
        caption = f'`ch` is "{ch}". `result += ch` builds a new string, "{result}", from the empty string and this one character.'
    else:
        caption = (
            f'`ch` is "{ch}". `result += ch` builds a new {len(result)}-character string: '
            f"Python copies the {old} old character{'s' if old != 1 else ''} and adds one."
        )
    rec.step(caption, w=frame(i))
    states[i] = "done"

rec.step(
    f'The loop is over. `result` is "{result}".' + (f" It was built as {n} separate strings, each one longer than the last." if n > 1 else " A one-letter word needs only one new string."),
    w=frame(n),
)
rec.output(f"{result}\n")
