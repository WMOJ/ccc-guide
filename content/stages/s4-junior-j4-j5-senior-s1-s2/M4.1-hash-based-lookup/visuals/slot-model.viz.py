import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
pos = 0
n = int(data[pos])
pos += 1
codes = []
for _ in range(n):
    codes.append(int(data[pos]))
    pos += 1
q = int(data[pos])
pos += 1
queries = []
for _ in range(q):
    queries.append(int(data[pos]))
    pos += 1

SLOTS = 8
table = [None] * SLOTS
lines = []


def codes_frame(i):
    states = []
    for j in range(n):
        if j < i:
            states.append("done")
        elif j == i:
            states.append("current")
        else:
            states.append("none")
    return vz.array(codes, states=states, pointers={"i": i} if i < n else None)


def slots_frame(highlight, probed):
    vals = [v if v is not None else "_" for v in table]
    states = ["none"] * SLOTS
    for s in probed:
        states[s] = "compare"
    states[highlight] = "current"
    return vz.array(vals, states=states, index_base=0)


for i, code in enumerate(codes):
    home = code % SLOTS
    slot = home
    probed = []
    while table[slot] is not None and table[slot] != code:
        probed.append(slot)
        slot = (slot + 1) % SLOTS
    table[slot] = code
    lines.append(f"{code} -> slot {slot}")
    if probed:
        how = "wraps past slot 7 and lands it" if slot < home else "lands it"
        caption = (
            f"{code} % {SLOTS} = {home}, but slot {home} is taken. "
            f"Probing forward {how} in slot {slot}."
        )
    else:
        caption = f"{code} % {SLOTS} = {home}: an empty slot, so it goes straight in."
    rec.step(caption, codes=codes_frame(i), slots=slots_frame(slot, probed))

for code in queries:
    home = code % SLOTS
    slot = home
    probed = []
    while table[slot] is not None and table[slot] != code:
        probed.append(slot)
        slot = (slot + 1) % SLOTS
    found = table[slot] == code
    verdict = "found" if found else "missing"
    lines.append(f"lookup {code}: {verdict} at slot {slot}")
    if probed and found:
        caption = (
            f"Looking up {code}: {code} % {SLOTS} = {home}, but slot {home} holds a different "
            f"code, so probing forward finds {code} in slot {slot}."
        )
    elif probed and not found:
        if len(probed) == 1:
            taken = f"slot {home} holds another code"
        else:
            taken = f"slots {probed[0]} to {probed[-1]} hold other codes"
        caption = (
            f"Looking up {code}: {code} % {SLOTS} = {home}, but {taken}. "
            f"Slot {slot} is empty, so {code} was never stored."
        )
    elif found:
        caption = f"Looking up {code}: {code} % {SLOTS} = {home}, and slot {home} holds it directly."
    else:
        caption = (
            f"Looking up {code}: {code} % {SLOTS} = {home}, and slot {home} is empty, "
            f"so {code} was never stored."
        )
    rec.step(caption, codes=codes_frame(n), slots=slots_frame(slot, probed))

rec.output("\n".join(lines) + "\n")
