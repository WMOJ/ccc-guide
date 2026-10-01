import vizrec as vz
from itertools import product

rec = vz.Recorder()
tokens = rec.stdin.split()
max_len = int(tokens[0])
values = int(tokens[1])


def brute(a):
    best = 1
    for i in range(len(a)):
        for j in range(i, len(a)):
            ok = True
            for k in range(i + 1, j + 1):
                if a[k] <= a[k - 1]:
                    ok = False
            if ok:
                best = max(best, j - i + 1)
    return best


def attempt(a):
    best = 1
    run = 1
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            run += 1
        else:
            run = 0
        best = max(best, run)
    return best


def fixed(a):
    best = 1
    run = 1
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            run += 1
        else:
            run = 1
        best = max(best, run)
    return best


def span(first, last):
    if first == last:
        return f"input {first}"
    return f"inputs {first} to {last}"


groups = []
total = 0
for n in range(1, max_len + 1):
    group = [list(c) for c in product(range(values), repeat=n)]
    groups.append(group)
    total += len(group)

tested = 0
failing = None
last_table = None


def frame_array(a, state, ranges=None):
    return vz.array(a, states=state * len(a) if len(state) == 1 else state, ranges=ranges)


def frame_table(k, b, t, same):
    return vz.table(
        cells=[[str(b), str(t), "yes" if same else "no"]],
        states=["_" + ("d" if same else "x") + ("d" if same else "x")],
        row_heads=[f"#{k}"],
        col_heads=["brute", "attempt", "same?"],
    )


for group in groups:
    n = len(group[0])
    size = len(group)
    fail_at = None
    for idx, a in enumerate(group):
        if attempt(a) != brute(a):
            fail_at = idx
            break
    a = group[0]
    tested += 1
    b = brute(a)
    t = attempt(a)
    last_table = frame_table(tested, b, t, b == t)
    if b == t:
        rec.step(
            f"Input {tested}, {a}. The brute force says {b} and the attempt says {t}. They match.",
            array=frame_array(a, "d"),
            table=last_table,
        )
    else:
        failing = a
    if failing is None and fail_at is not None:
        if fail_at > 1:
            last = group[fail_at - 1]
            first_skipped = tested + 1
            tested += fail_at - 1
            rec.skip(
                f"The next inputs of length {n} also match ({span(first_skipped, tested)}). "
                f"The last of them is {last}.",
                fail_at - 1,
                array=frame_array(last, "d"),
                table=frame_table(tested, brute(last), attempt(last), True),
            )
        a = group[fail_at]
        tested += 1
        failing = a
        b = brute(a)
        t = attempt(a)
        last_table = frame_table(tested, b, t, False)
    if failing is not None:
        rec.step(
            f"Input {tested}, {failing}. The brute force says {brute(failing)} and the attempt says "
            f"{attempt(failing)}. They differ: this is the smallest failing input, found in size order.",
            array=frame_array(failing, "x"),
            table=last_table,
        )
        break
    if size > 1:
        last = group[-1]
        first_skipped = tested + 1
        tested += size - 1
        rec.skip(
            f"The rest of the inputs of length {n} also match ({span(first_skipped, tested)}). "
            f"The last of them is {last}.",
            size - 1,
            array=frame_array(last, "d"),
            table=frame_table(tested, brute(last), attempt(last), True),
        )

lines = []
bad = sum(1 for g in groups for a in g if fixed(a) != brute(a))
if failing is None:
    lines.append(f"no failing input among {total} inputs")
    rec.step(
        f"No failing input among {total} inputs up to length {max_len}. The attempt is not proven "
        "right: the bug may need a longer input, so raise the limit and search again.",
        array=frame_array(groups[-1][-1], "d"),
        table=last_table,
    )
else:
    b = brute(failing)
    t = attempt(failing)
    lines.append(f"first failing input: {failing}")
    lines.append(f"brute force says {b}, attempt says {t}")
    rec.step(
        f"On {failing} the brute force finds the increasing run 0, 1 of length {b}. The attempt "
        f"returns {t}: at the repeated 0 it reset run to 0, so the 1 that followed only brought "
        "it back to 1. A new run already holds the current value, so it should restart at 1.",
        array=frame_array(failing, "_pp", ranges=[(1, 2, "run of " + str(b))]),
        table=last_table,
    )
    f = fixed(failing)
    rec.step(
        f"With run reset to 1, the attempt returns {f} on {failing}, matching the brute force. "
        f"Over all {total} inputs, " + (
            "the fixed attempt never differs from the brute force."
            if bad == 0
            else f"the fixed attempt still differs on {bad}."
        ),
        array=frame_array(failing, "d"),
        table=frame_table(tested, b, f, f == b),
    )
lines.append(f"fixed attempt differs from brute force on {bad} of {total} inputs")
rec.output("\n".join(lines) + "\n")
