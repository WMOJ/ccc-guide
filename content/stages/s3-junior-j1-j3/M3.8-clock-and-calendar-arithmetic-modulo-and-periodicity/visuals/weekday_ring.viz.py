import vizrec as vz

rec = vz.Recorder()
day = int(rec.readline())

NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
FULL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
label = f"{day:,}" if abs(day) >= 10000 else str(day)


def ring(at, done=()):
    states = ["c" if k == at else ("d" if k in done else "_") for k in range(7)]
    return vz.array(NAMES, states=states, pointers=[("hand", at, None, True)], circular=True, indices=True)


rec.step(
    f"Day 0 is a Monday, so the hand starts on index 0. The week repeats, so the ring has 7 "
    f"entries and the period is 7. The question is day {label}.",
    ring=ring(0),
)

laps, rest = divmod(day, 7)
if laps > 0:
    rec.step(
        f"{label} = 7 * {laps:,} + {rest}. Each full week of 7 days puts the hand back on Monday, "
        f"so all {laps:,} weeks can be ignored.",
        ring=ring(0, (0,)),
    )
elif laps < 0:
    rec.step(
        f"{label} is before day 0. Python gives {label} // 7 = {laps} and {label} % 7 = {rest}, "
        "never a negative remainder, so the index stays inside 0 to 6.",
        ring=ring(0, (0,)),
    )

pos = 0
if day >= 0:
    for _ in range(rest):
        pos += 1
        rec.step(f"One more day: the hand moves to index {pos}, {FULL[pos]}.", ring=ring(pos, (0,)))
else:
    for _ in range((-day) % 7):
        pos = (pos - 1) % 7
        rec.step(
            f"One day back: the hand wraps around to index {pos}, {FULL[pos]}.",
            ring=ring(pos, (0,)),
        )

rec.step(
    f"{label} % 7 = {day % 7}, and DAY_NAMES[{day % 7}] is {FULL[day % 7]}.",
    ring=ring(day % 7),
)
rec.output(f"{FULL[day % 7]}\n")
