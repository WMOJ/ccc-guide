import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def source_frame(i):
    states = ["done" if pos < i else "_" for pos in range(n)]
    states[i] = "current"
    states[i + 1] = "current"
    return vz.array(list(s), states=states, pointers={"i": i}, ranges=[(i, i + 1, "one pair")])


def parts_frame(parts):
    return vz.array(parts, states=["done"] * (len(parts) - 1) + ["current"])


parts = []
i = 0
while i < n:
    count = int(s[i])
    c = s[i + 1]
    parts.append(c * count)
    rec.step(
        f"s[{i}] is '{count}' and s[{i + 1}] is '{c}': append '{c}' * {count} = '{c * count}' to parts.",
        encoded=source_frame(i),
        parts=parts_frame(list(parts)),
    )
    i += 2

rec.step(
    f"No pairs are left. \"\".join(parts) builds '{''.join(parts)}' once, the string the encoding came from.",
    encoded=vz.array(list(s), states=["done"] * n),
    parts=vz.array(parts, states=["current"] * len(parts)),
)

rec.output("".join(parts) + "\n")
