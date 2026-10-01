import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
meetings = []
for k in range(n):
    meetings.append((int(data[3 + 3 * k]), int(data[2 + 3 * k]), data[1 + 3 * k]))
meetings.sort()
span = max(m[0] for m in meetings)

# A row for each interval so that overlapping ones never share one.
rows = {}
row_end = []
for end, start, name in sorted(meetings, key=lambda m: (m[1], m[0])):
    for r in range(len(row_end)):
        if row_end[r] <= start:
            row_end[r] = end
            rows[name] = r
            break
    else:
        row_end.append(end)
        rows[name] = len(row_end) - 1

status = {name: "_" for end, start, name in meetings}


def draw(last_end, current=None):
    ivs = []
    for end, start, name in meetings:
        state = "current" if name == current else status[name]
        ivs.append((start, end, name, state, rows[name]))
    return vz.line(0, span, tick=1, intervals=ivs, sweep=(last_end, "last end"))


order = " ".join(f"{name}({end})" for end, start, name in meetings)
rec.step(
    f"Sort the meetings by end time: {order}. Nothing is chosen yet, so the last chosen end is 0.",
    line=draw(0),
)
last_end = 0
chosen = []
for end, start, name in meetings:
    if start >= last_end:
        chosen.append(name)
        status[name] = "done"
        touch = " It starts exactly when the last one ends, which is allowed." if start == last_end and last_end else ""
        rec.step(
            f"{name} runs {start} to {end}. It starts at {start}, not before the last end "
            f"{last_end}, so take it. The last end moves to {end}.{touch}",
            line=draw(end, name),
        )
        last_end = end
    else:
        status[name] = "invalid"
        rec.step(
            f"{name} runs {start} to {end}. It starts at {start}, before the last end "
            f"{last_end}, so it overlaps a chosen meeting and is skipped.",
            line=draw(last_end, name),
        )
rec.step(
    f"{len(chosen)} meeting{'s' if len(chosen) != 1 else ''} chosen: {' '.join(chosen)}. "
    "Every chosen one ends as early as it could, which leaves the most room for the rest.",
    line=draw(last_end),
)
rec.output(f"{len(chosen)}\n" + " ".join(chosen) + "\n")
