import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
a = list(map(int, data[1:n + 1]))
target = int(data[n + 1])

prefixes = [0]
for x in a:
    prefixes.append(prefixes[-1] + x - target)
SLOTS = 6

seen = {}
order = []


def dict_frame(highlight=None, state="current"):
    keys = order + [None] * (SLOTS - len(order))
    counts = [seen[k] if k is not None else None for k in keys]
    states = {}
    if highlight is not None:
        states[(0, order.index(highlight))] = state
        states[(1, order.index(highlight))] = state
    return vz.table([keys, counts], states=states, row_heads=["key", "count"])


def array_frame(upto, pointer=None, pstate="current"):
    vals = [prefixes[i] if i <= upto else None for i in range(n + 1)]
    states = {i: "done" for i in range(upto + 1)}
    if pointer is not None:
        states[pointer] = pstate
    ptrs = {"j": pointer} if pointer is not None else None
    return vz.array(vals, states=states, pointers=ptrs, name="prefix")


seen[0] = 1
order.append(0)
rec.step(
    f"Every element of a has target {target} subtracted as it is read. The running total starts at "
    "prefix[0] = 0, the empty prefix, so the dictionary starts with key 0 seen once.",
    array=array_frame(0),
    table=dict_frame(0),
)
answer = 0
for j in range(1, n + 1):
    x = a[j - 1]
    p = prefixes[j]
    c = seen.get(p, 0)
    shift = f"{x} - {target} = {x - target}"
    if c:
        rec.step(
            f"prefix[{j}] = prefix[{j - 1}] + ({shift}) = {p}. The key {p} was seen {c} "
            f"{'time' if c == 1 else 'times'} before, so {c} earlier "
            f"{'prefix matches' if c == 1 else 'prefixes match'}: {c} more "
            f"{'subarray ends' if c == 1 else 'subarrays end'} here. Total {answer + c}.",
            array=array_frame(j, j, "compare"),
            table=dict_frame(p, "compare"),
        )
    else:
        rec.step(
            f"prefix[{j}] = prefix[{j - 1}] + ({shift}) = {p}. The key {p} is new, so no earlier "
            f"prefix matches and no subarray ends here. Total {answer}.",
            array=array_frame(j, j),
            table=dict_frame(),
        )
    answer += c
    if p not in seen:
        seen[p] = 0
        order.append(p)
    seen[p] += 1
    rec.step(
        f"Record it: key {p} now has count {seen[p]}.",
        array=array_frame(j, j),
        table=dict_frame(p, "done"),
    )
rec.step(
    f"All {n} elements are read. {answer} {'subarray has' if answer == 1 else 'subarrays have'} "
    f"average exactly {target}.",
    array=array_frame(n),
    table=dict_frame(),
)
rec.output(f"{answer}\n")
