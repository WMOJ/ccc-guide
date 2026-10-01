import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
m = int(data[0])

if m <= 2:
    rec.step(
        f"Length {m}: with only {m} position(s), each one mirrored onto another, "
        "there is no position left over to hold a second letter. A palindrome this "
        "short can only repeat one letter throughout. Impossible.",
        row=vz.array(["?"] * m, states=["invalid"] * m),
    )
    rec.output("Impossible\n")
else:
    half = (m + 1) // 2
    result = [None] * m
    states = ["none"] * m
    for i in range(half):
        ch = "a"
        if i == half - 1:
            ch = "b"
        result[i] = ch
        result[m - 1 - i] = ch
        states[i] = "current"
        states[m - 1 - i] = "current"
        if i == half - 1:
            what = f"the innermost position, {i}, is set to b so the row holds both letters"
        else:
            what = f"position {i} is set to a"
        rec.step(
            f"Choose: {what}. Mirror it into position {m - 1 - i}.",
            row=vz.array(result, states=states),
        )
    rec.step(
        "Every mirrored pair matches, so the row reads the same forwards and backwards.",
        row=vz.array(result, states=["done"] * m),
    )
    rec.output("".join(result) + "\n")

rec.done()
