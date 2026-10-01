import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])

powers = []
p = 1
while p <= n:
    powers.append(p)
    p *= 2

count = 0
total = 2 ** len(powers)
for mask in range(total):
    included = []
    states = []
    s = 0
    for i in range(len(powers)):
        if mask & (1 << i):
            included.append("current")
            s += powers[i]
        else:
            included.append("none")
        states.append(included[i])
    match = s == n
    if match:
        count += 1
        states = ["done"] * len(powers)
        verdict = f"sums to {s}, matching {n}"
    else:
        verdict = f"sums to {s}, not {n}"
    rec.step(
        f"Subset {mask + 1} of {total}: {verdict}.",
        subset=vz.array(powers, states=states),
    )

verb = "sums" if count == 1 else "sum"
rec.step(
    f"Every subset of {{{', '.join(str(x) for x in powers)}}} is checked: {count} "
    f"of them {verb} to {n}.",
    subset=vz.array(powers, states=["none"] * len(powers)),
)
rec.output(str(count) + "\n")
rec.done()
