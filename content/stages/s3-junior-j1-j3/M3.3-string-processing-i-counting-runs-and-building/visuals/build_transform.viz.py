import vizrec as vz

VOWELS = "aeiou"

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def source_frame(i):
    states = ["done" if pos < i else "_" for pos in range(n)]
    states[i] = "current"
    return vz.array(list(s), states=states, pointers={"i": i})


def parts_frame(parts):
    return vz.array(parts, states=["done"] * (len(parts) - 1) + ["current"])


parts = []
for i, char in enumerate(s):
    if char in VOWELS:
        parts.append("*")
        reason = f"s[{i}] is '{char}', a vowel: append '*' to parts."
    else:
        parts.append(char)
        reason = f"s[{i}] is '{char}', not a vowel: append '{char}' to parts."
    rec.step(reason, source=source_frame(i), parts=parts_frame(list(parts)))

rec.output("".join(parts) + "\n")
