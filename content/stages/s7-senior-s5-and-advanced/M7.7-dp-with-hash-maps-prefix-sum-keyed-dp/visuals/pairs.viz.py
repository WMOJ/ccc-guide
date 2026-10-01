import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
a = list(map(int, data[1:n + 1]))
target = int(data[n + 1])

shifted = [x - target for x in a]
prefixes = [0]
for x in shifted:
    prefixes.append(prefixes[-1] + x)

groups = {}
for i, p in enumerate(prefixes):
    groups.setdefault(p, []).append(i)
repeated = [(p, idx) for p, idx in groups.items() if len(idx) > 1]
total = sum(len(idx) * (len(idx) - 1) // 2 for _, idx in repeated)

rec.step(
    f"The values are {' '.join(map(str, a))} and the target average is {target}.",
    array=vz.array(a, name="a"),
)
rec.step(
    f"Subtract {target} from each one. A stretch with average {target} now adds up to exactly 0.",
    array=vz.array(shifted, name="a - target"),
)
rec.step(
    "The prefix sums of the shifted values, from the empty prefix prefix[0] = 0 up to "
    f"prefix[{n}]. The sum of a stretch is one prefix minus an earlier one.",
    array=vz.array(prefixes, states="d" * (n + 1), name="prefix"),
)
for p, idx in repeated:
    k = len(idx)
    states = {i: "compare" for i in idx}
    pairs = k * (k - 1) // 2
    if k == 2:
        i, j = idx
        which = f"element {i}" if j - i == 1 else f"elements {i} to {j - 1}"
        text = (
            f"prefix[{i}] and prefix[{j}] are both {p}, so the stretch of {which} "
            f"sums to {p} - {p} = 0. That is 1 matching pair."
        )
        ranges = [(i, j, f"elements {i}..{j - 1}" if j - i > 1 else f"element {i}")]
    else:
        text = (
            f"The value {p} appears {k} times, at prefixes {', '.join(map(str, idx))}. Any two of "
            f"them bound a stretch with sum 0: {k} * {k - 1} / 2 = {pairs} pairs."
        )
        ranges = None
    rec.step(
        text,
        array=vz.array(prefixes, states=states, ranges=ranges, name="prefix"),
    )
if not repeated:
    rec.step(
        "No prefix value repeats, so no stretch sums to 0 and none has the target average.",
        array=vz.array(prefixes, name="prefix"),
    )
rec.step(
    f"The answer is the number of pairs of equal prefix values: {total}.",
    array=vz.array(prefixes, states="d" * (n + 1), name="prefix"),
)
rec.output(f"{total}\n")
