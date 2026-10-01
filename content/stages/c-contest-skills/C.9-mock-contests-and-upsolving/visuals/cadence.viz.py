import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
cycle = int(tokens[0])
upsolve = int(tokens[1])
wait = int(tokens[2])
retry_day = upsolve + wait
events = [
    (0, "mock"),
    (1, "upsolve"),
    (retry_day, "retry"),
    (cycle, "next"),
]
events.sort(key=lambda e: e[0])

points = []
intervals = []


def frame():
    return vz.line(0, 16, tick=2, points=list(points), intervals=list(intervals))


lines = []
for day, kind in events:
    if kind == "mock":
        points.append((day, "mock", "done"))
        lines.append("day 0: mock contest")
        rec.step(
            "Day 0 is the mock contest: one sitting of three hours on a past contest, logged as "
            "in the earlier figures.",
            line=frame(),
        )
    elif kind == "upsolve":
        intervals.append((1, upsolve, "upsolve", "current", 0))
        lines.append(f"days 1 to {upsolve}: upsolve")
        rec.step(
            f"Days 1 to {upsolve} are for upsolving, using the first steps from the log. "
            "You are working on problems from one contest while it is fresh.",
            line=frame(),
        )
    elif kind == "retry":
        late = retry_day > cycle
        points.append((retry_day, "retry", "invalid" if late else "path"))
        lines.append(f"day {retry_day}: retry the problems you stalled on, from a blank file")
        text = (
            f"Day {retry_day} is {wait} days after the upsolve ends: retry the problems you stalled "
            "on, from a blank file. Whatever you can rebuild now is what you learned."
        )
        if late:
            text = (
                f"Day {retry_day} is {wait} days after the upsolve ends, but the next mock contest "
                f"already happened on day {cycle}. The retry has slipped behind the mock it was meant "
                "to prepare for."
            )
        rec.step(text, line=frame())
    else:
        points.append((cycle, "mock", "done"))
        lines.append(f"day {cycle}: next mock contest")
        rec.step(
            f"Day {cycle} is the next mock contest, which closes the cycle and starts the next log.",
            line=frame(),
        )
if retry_day > cycle:
    lines.append("the retry falls after the next mock, so shorten the wait")
    tail = "Shorten the wait, or lengthen the cycle, so the retry lands before the next mock."
else:
    tail = "Each cycle ends with a retry before the next mock, so a fresh log can show whether it helped."
rec.step(tail, line=frame())
rec.output("\n".join(lines) + "\n")
