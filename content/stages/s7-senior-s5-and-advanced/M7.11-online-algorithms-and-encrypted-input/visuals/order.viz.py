import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
start = [int(x) for x in rec.readline().split()]
q = int(rec.readline())
lines = [tuple(int(t) for t in rec.readline().split()) for _ in range(q)]
texts = [f"{k} {x} {y}" for k, x, y in lines]
repeated = len(set(texts)) < q


def run(order):
    a = list(start)
    last = 0
    rows = []
    for i in order:
        kind, x, y = lines[i]
        used = last
        if kind == 1:
            p = (x + used) % n
            v = (y + used) % 100
            a[p] = v
            rows.append([texts[i], used, f"a{p}={v}", "-"])
        else:
            f = (x + used) % n
            s = (y + used) % n
            lo, hi = min(f, s), max(f, s)
            last = sum(a[lo:hi + 1])
            rows.append([texts[i], used, f"[{lo},{hi}]", last])
    return rows


def table(rows, heads, states):
    return {
        "t": vz.table(
            rows,
            states=states,
            col_heads=["raw", "last", "means", "answer"],
            row_heads=heads,
        )
    }


right = run(list(range(q)))
heads = [str(i + 1) for i in range(q)]
unknown = [[t, "?", "?", "?"] for t in texts]
if repeated:
    same = [i for i in range(q) if texts.index(texts[i]) != i][0]
    first = texts.index(texts[same])
    rec.step(
        f"All {q} raw lines can be read at once, since reading needs no answers. Lines "
        f"{first + 1} and {same + 1} are the same text, `{texts[same]}`. An offline plan would "
        "answer that question once and copy the answer.",
        **table(unknown, heads, ["____"] * q)
    )
    copied = [list(r) for r in right[:same]] + [[t, "?", "?", "?"] for t in texts[same:]]
    copied[same] = [texts[same], right[first][1], right[first][2], right[first][3]]
    st = ["____"] * q
    st[same] = "xxxx"
    rec.step(
        f"Copying line {first + 1} into line {same + 1} gives {right[first][3]}, the sum of "
        f"range {right[first][2]}. But line {same + 1} is decoded with "
        f"`last` = {right[same][1]}, not {right[first][1]}, so it asks about other positions, and "
        "every later line would be decoded from a wrong answer.",
        **table(copied, heads, st)
    )
    st = ["dddd"] * q
    st[same] = "cccc"
    rec.step(
        f"Decoding in order, line {same + 1} asks for range {right[same][2]} and the "
        f"answer is {right[same][3]}. The same text meant two different questions.",
        **table(right, heads, st)
    )
else:
    rec.step(
        f"All {q} raw lines can be read at once, since reading needs no answers. A batching plan "
        "might want to process the last two lines in the other order, for example to reuse work. "
        "It cannot decode them yet, because `last` is not known.",
        **table(unknown, heads, ["____"] * q)
    )
    order = list(range(q - 2)) + [q - 1, q - 2]
    wrong = run(order)
    wheads = [str(i + 1) for i in order]
    st = ["____"] * q
    st[q - 2] = "xxxx"
    st[q - 1] = "xxxx"
    rec.step(
        f"Forced to go ahead, the plan handles line {q} before line {q - 1}. Line {q} is then "
        f"decoded with `last` = {wrong[q - 2][1]} instead of {right[q - 1][1]}, so it asks for "
        f"range {wrong[q - 2][2]}. Its answer {wrong[q - 2][3]} changes the next `last` too, and line "
        f"{q - 1} asks for range {wrong[q - 1][2]}.",
        **table(wrong, wheads, st)
    )
    rec.step(
        f"In the order given, line {q - 1} asks for range {right[q - 2][2]} and answers "
        f"{right[q - 2][3]}, then line {q} asks for range {right[q - 1][2]} and answers "
        f"{right[q - 1][3]}. Only this order gives the questions the sender meant.",
        **table(right, heads, ["dddd"] * q)
    )
rec.output("\n".join(str(r[3]) for r in right if r[3] != "-") + "\n")
