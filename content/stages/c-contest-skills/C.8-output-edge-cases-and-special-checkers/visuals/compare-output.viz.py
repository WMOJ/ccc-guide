import vizrec as vz

rec = vz.Recorder()
raw = rec.stdin
tokens = raw.split()

# The two outputs of examples/format_demo.py: the loop version and the join version.
built = "".join(t + " " for t in tokens)
joined = " ".join(tokens)
produced = built + "\n"
expected = joined + "\n"


def show(ch):
    if ch == " ":
        return "·"
    if ch == "\n":
        return "\\n"
    return ch


def chars(text):
    return [show(c) for c in text]


def frame(values, name, marks, at=None):
    states = ["none"] * len(values)
    for i, s in marks.items():
        states[i] = s
    return vz.array(values, states=states, name=name,
                    pointers=[("i", at, "below", True)] if at is not None else None, indices=True)


exp_chars = chars(expected)
pro_chars = chars(produced)
n = max(len(exp_chars), len(pro_chars))

rec.step(
    "An exact checker compares every character, and the final newline too. Spaces are drawn as "
    "a dot, and the newline as a backslash n.",
    exp=frame(exp_chars, "expected", {}),
    pro=frame(pro_chars, "produced", {}),
)
same = {}
mismatch = None
for i in range(n):
    e = exp_chars[i] if i < len(exp_chars) else None
    p = pro_chars[i] if i < len(pro_chars) else None
    if e == p:
        marks = dict(same)
        marks[i] = "current"
        rec.step(
            f"Character {i}: both print {e}. They match.",
            exp=frame(exp_chars, "expected", marks, i),
            pro=frame(pro_chars, "produced", marks, i),
        )
        same[i] = "done"
    else:
        mismatch = i
        marks_e = dict(same)
        marks_p = dict(same)
        if i < len(exp_chars):
            marks_e[i] = "invalid"
        if i < len(pro_chars):
            marks_p[i] = "invalid"
        rec.step(
            f"Character {i}: expected {e}, produced {p}. The exact checker stops here: wrong answer.",
            exp=frame(exp_chars, "expected", marks_e, min(i, len(exp_chars) - 1)),
            pro=frame(pro_chars, "produced", marks_p, min(i, len(pro_chars) - 1)),
        )
        break
if mismatch is None:
    rec.step(
        "Every character matches, so the exact checker accepts. The loop added nothing, "
        "so there is no stray space.",
        exp=frame(exp_chars, "expected", {i: "done" for i in range(len(exp_chars))}),
        pro=frame(pro_chars, "produced", {i: "done" for i in range(len(pro_chars))}),
    )

# Token checker: split both outputs on whitespace, then compare token by token.
exp_tok = expected.split()
pro_tok = produced.split()
if not exp_tok:
    rec.step(
        "A token checker splits both outputs on whitespace. Neither output has a token (drawn as ∅), "
        "so the two lists are equal: accepted.",
        exp=frame(["∅"], "expected", {0: "done"}),
        pro=frame(["∅"], "produced", {0: "done"}),
    )
else:
    rec.step(
        "A token checker splits both outputs on whitespace first. The extra space and the newline "
        "disappear, and each side is a list of tokens.",
        exp=frame(exp_tok, "expected", {}),
        pro=frame(pro_tok, "produced", {}),
    )
    done = {}
    for i in range(len(exp_tok)):
        marks = dict(done)
        marks[i] = "current"
        rec.step(
            f"Token {i}: both are {exp_tok[i]}. They match.",
            exp=frame(exp_tok, "expected", marks, i),
            pro=frame(pro_tok, "produced", marks, i),
        )
        done[i] = "done"
    rec.step(
        "All tokens match, so the token checker accepts the output the exact checker rejected."
        if mismatch is not None
        else "All tokens match: accepted by the token checker too.",
        exp=frame(exp_tok, "expected", done),
        pro=frame(pro_tok, "produced", done),
    )
rec.output(f"{built!r}\n{joined!r}\n")
