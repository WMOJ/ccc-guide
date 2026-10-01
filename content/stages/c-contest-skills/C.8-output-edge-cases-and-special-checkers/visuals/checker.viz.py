import vizrec as vz

rec = vz.Recorder()
head = rec.readline().split()
k = int(head[1])
values = rec.readline().split()
answer = rec.readline().split()

# The steps of judge() in examples/check_pair.py.
RULES = ["two numbers?", "both available?", f"sum is {k}?"]


def arr(marked):
    states = ["none"] * len(values)
    for i in marked:
        states[i] = "compare"
    return vz.array(values, states=states, name="list", indices=True)


def tab(results):
    cells = []
    states = []
    for i, rule in enumerate(RULES):
        if i < len(results):
            ok, text = results[i]
            cells.append([text])
            states.append("d" if ok else "x")
        else:
            cells.append(["not checked"])
            states.append("_")
    return vz.table(cells=cells, states=states, row_heads=RULES, col_heads=["result"], row_title="check")


results = []
verdict = None
marked = []

rec.step(
    f"The checker gets the list, the target k = {k} and the contestant's answer, "
    f"{' '.join(answer) or '(empty)'}. It runs three checks in order.",
    list=arr([]),
    checks=tab([]),
)
if len(answer) != 2:
    results.append((False, f"{len(answer)} found"))
    verdict = "rejected: need two numbers"
    rec.step(
        f"The answer has {len(answer)} numbers, not two: {verdict}.",
        list=arr([]),
        checks=tab(results),
    )
else:
    results.append((True, "yes"))
    rec.step(
        "The answer has exactly two numbers, so the first check passes.",
        list=arr([]),
        checks=tab(results),
    )
    free = [True] * len(values)
    used = []
    for token in answer:
        spots = [i for i, v in enumerate(values) if v == token and free[i]]
        if not spots:
            results.append((False, f"{token} is taken"))
            verdict = f"rejected: {token} is not available"
            if token in values:
                why = f"every copy of {token} in the list is already used by the first number"
            else:
                why = f"{token} is not in the list"
            rec.step(f"{why.capitalize()}: {verdict}.", list=arr(used), checks=tab(results))
            break
        free[spots[0]] = False
        used.append(spots[0])
        rec.step(
            f"{token} is at position {spots[0]} of the list, and that position is now used up.",
            list=arr(used),
            checks=tab(results),
        )
    else:
        results.append((True, "yes"))
        rec.step(
            "Each number came from a different position of the list, so the second check passes.",
            list=arr(used),
            checks=tab(results),
        )
        total = int(answer[0]) + int(answer[1])
        if total != k:
            results.append((False, f"{total}"))
            verdict = "rejected: sum is not k"
            rec.step(
                f"{answer[0]} + {answer[1]} = {total}, not {k}: {verdict}.",
                list=arr(used),
                checks=tab(results),
            )
        else:
            results.append((True, f"{total}"))
            verdict = "accepted"
            rec.step(
                f"{answer[0]} + {answer[1]} = {total}, which is k. Every check passes: accepted, "
                "even though this pair need not match the pair the reference solution printed.",
                list=arr(used),
                checks=tab(results),
            )
rec.output(verdict + "\n")
