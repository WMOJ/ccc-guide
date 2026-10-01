import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
pos = 1
intervals = []
for _ in range(n):
    start = int(data[pos])
    end = int(data[pos + 1])
    pos += 2
    intervals.append((start, end))

events = []
for idx, (start, end) in enumerate(intervals):
    events.append((start, 1, idx))
    events.append((end, -1, idx))
events.sort()
hi = max(end for _, end in intervals)
names = "ABCD"

active_row = [None] * len(events)
covered_row = [None] * len(events)
change_row = ["+1" if d == 1 else "-1" for _, d, _ in events]
x_row = [x for x, _, _ in events]
status = ["none"] * n


def line_frame(sweep=None):
    shown = []
    for idx, (start, end) in enumerate(intervals):
        shown.append((start, end, names[idx], status[idx], idx))
    return vz.line(0, hi, tick=1, intervals=shown, sweep=sweep)


def table_frame(cur=None):
    states = {}
    if cur is not None:
        for r in range(4):
            states[(r, cur)] = "current"
    return vz.table(
        [x_row, change_row, active_row, covered_row],
        states=states or None,
        row_heads=["x", "change", "active", "covered"],
        col_heads=list(range(1, len(events) + 1)),
        col_title="event",
    )


rec.step(
    f"The {n} intervals become {2 * n} events, a +1 at each start and a -1 at each end, sorted by "
    "position. The sweep has not moved yet, so active and covered are still blank.",
    line=line_frame(),
    events=table_frame(),
)

active = 0
best = 0
covered = 0
prev = events[0][0]
for k, (x, delta, idx) in enumerate(events):
    if k == 0:
        move = f"The sweep starts at x = {x}, where nothing is active yet."
    elif x == prev:
        move = f"The sweep is still at x = {x}, so this stretch has length 0."
    elif active > 0:
        covered += x - prev
        move = (
            f"The stretch from {prev} to {x} had {active} active, so it counts once: "
            f"covered grows by {x - prev}."
        )
    else:
        move = f"Nothing was active from {prev} to {x}, so the stretch adds nothing."
    before = active
    active += delta
    best = max(best, active)
    status[idx] = "current" if delta == 1 else "done"
    what = f"interval {names[idx]} starts" if delta == 1 else f"interval {names[idx]} ends"
    active_row[k] = active
    covered_row[k] = covered
    rec.step(
        f"{move} Then {what}, so active goes from {before} to {active}.",
        line=line_frame(sweep=(x, f"active {active}")),
        events=table_frame(cur=k),
    )
    prev = x

rec.step(
    f"All events are processed. The covered length is {covered} and at most {best} "
    f"interval{'s were' if best != 1 else ' was'} active at once.",
    line=line_frame(),
    events=table_frame(),
)
rec.output(f"{covered}\n{best}\n")
