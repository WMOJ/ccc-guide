import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
pos = 0
n = int(tokens[pos])
pos += 1
costs = []
for _ in range(n):
    k = int(tokens[pos])
    pos += 1
    row = []
    for _ in range(k):
        word = tokens[pos]
        pos += 1
        row.append(None if word == "-" else int(word))
    costs.append(row)
plan_count = int(tokens[pos])
pos += 1
plans = []
for _ in range(plan_count):
    b = int(tokens[pos])
    pos += 1
    blocks = []
    for _ in range(b):
        problem = int(tokens[pos])
        pos += 1
        minutes = int(tokens[pos])
        pos += 1
        blocks.append((problem, minutes))
    plans.append(blocks)

shown = []
series = {}
finals = []


def frame_line():
    return vz.line(0, 180, tick=30, intervals=list(shown))


def frame_plot():
    out = []
    for index, name in enumerate(["A", "B"][:plan_count]):
        if name not in series:
            continue
        pts = series[name]
        out.append((name, "Plan " + name, list(pts), index))
    return vz.plot(
        (0, 180, "minute", [0, 60, 120, 180]),
        (0, 8, "subtasks cleared", [0, 2, 4, 6, 8]),
        out,
    )


ordinal = {1: "first", 2: "second", 3: "third"}

for index, blocks in enumerate(plans):
    name = "AB"[index]
    row = index
    worked = [0] * n
    cleared = [0] * n
    clock = 0
    total = 0
    series[name] = [(0, 0)]
    for problem, minutes in blocks:
        start = clock
        end = clock + minutes
        clock = end
        if problem == 0:
            shown.append((start, end, "R", "compare", row))
            series[name].append((end, total))
            rec.step(
                f"Plan {name}, minute {start} to {end}: read all five statements. "
                "Nothing can clear yet, so the count stays at 0.",
                line=frame_line(),
                plot=frame_plot(),
            )
            continue
        p = problem - 1
        worked[p] += minutes
        newly = []
        while cleared[p] < len(costs[p]):
            need = costs[p][cleared[p]]
            if need is None or need > worked[p]:
                break
            cleared[p] += 1
            newly.append(cleared[p])
            total += 1
        text = (
            f"Plan {name}, minute {start} to {end}: {minutes} minutes on problem {problem}, "
            f"bringing its total to {worked[p]}. "
        )
        if newly:
            word = "subtask" if len(newly) == 1 else "subtasks"
            which = " and ".join(str(k) for k in newly)
            text += f"That reaches the cost of {word} {which}, so {'it clears' if len(newly) == 1 else 'they clear'}. "
            state = "done"
        else:
            nxt = cleared[p]
            if nxt >= len(costs[p]):
                text += "Every subtask of this problem has already cleared. "
            elif costs[p][nxt] is None:
                text += f"Subtask {nxt + 1} has no idea behind it in this example, so these minutes buy nothing. "
            else:
                text += f"Subtask {nxt + 1} needs {costs[p][nxt]}, so it is still {costs[p][nxt] - worked[p]} away. "
            state = "invalid"
        text += f"Cleared so far: {total}."
        shown.append((start, end, str(problem), state, row))
        series[name].append((end, total))
        rec.step(text, line=frame_line(), plot=frame_plot())
    finals.append((name, total, list(cleared)))

summary = (
    "Both plans use all 180 minutes. "
    + " ".join(f"Plan {nm} clears {tot}." for nm, tot, _ in finals)
    + " Every bar drawn as cleared none is a stretch of minutes that moved no subtask."
)
rec.step(summary, line=frame_line(), plot=frame_plot())
rec.output(
    "\n".join(
        f"plan {nm}: {tot} subtasks cleared, by problem " + " ".join(str(c) for c in cl)
        for nm, tot, cl in finals
    )
    + "\n"
)
