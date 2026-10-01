import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
a = int(tokens[1])
b = int(tokens[2])
t = int(tokens[3])

x, y = a, b
while y != 0:
    x, y = y, x % y
g = x
period = a * b // g

a_blinks = [k * a for k in range(1, period // a + 1)]
b_blinks = [k * b for k in range(1, period // b + 1)]
shared = [k * period for k in range(1, 2)]


def frame(mark_t=False, mark_answer=None):
    intervals = [(m, m, "A", "queued", 0) for m in a_blinks]
    intervals += [(m, m, "B", "queued", 1) for m in b_blinks]
    intervals += [(m, m, "both", "done", 2) for m in shared]
    points = []
    if mark_answer is not None and mark_answer == t:
        points.append((t, f"t={t}", "path"))
    else:
        if mark_t:
            points.append((t, "t", "compare"))
        if mark_answer is not None:
            points.append((mark_answer, str(mark_answer), "path"))
    return vz.line(0, period, points=points, intervals=intervals)


rec.step(
    f"Light A blinks every {a}s (the A marks), light B every {b}s (the B marks). Both blink together "
    f"every lcm({a}, {b}) = {period}s (the both marks).",
    line=frame(),
)

rec.step(
    f"The query asks for the first shared blink at or after second {t}.",
    line=frame(mark_t=True),
)

remainder = t % period
if remainder == 0:
    answer = t
    rec.step(
        f"{t} % {period} = 0: second {t} is already a shared blink.",
        line=frame(mark_t=True, mark_answer=answer),
    )
else:
    answer = t + (period - remainder)
    rec.step(
        f"{t} % {period} = {remainder}, so the next shared blink is "
        f"{t} + ({period} - {remainder}) = {answer}.",
        line=frame(mark_t=True, mark_answer=answer),
    )

rec.output(f"{answer}\n")
