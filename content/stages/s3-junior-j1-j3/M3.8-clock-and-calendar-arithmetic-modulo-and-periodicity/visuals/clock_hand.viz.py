import vizrec as vz

rec = vz.Recorder()
hour = int(rec.readline())
offset = int(rec.readline())
N = 24


def wheel(at):
    return vz.line(0, N, kind="wheel", at=at, points=[(hour, "start", "done")])


pos = hour
rec.step(
    f"The hand starts at hour {hour}. The wheel has {N} positions, 0 through {N - 1}, "
    f"and the offset to add is {offset}.",
    wheel=wheel(pos),
)

sign = 1 if offset > 0 else -1
magnitude = abs(offset)
laps, rest = divmod(magnitude, N)
if laps:
    rec.step(
        f"{magnitude} hours is {laps} full laps of {N} plus {rest}. "
        f"Each full lap returns the hand to where it started, hour {hour}.",
        wheel=wheel(pos),
    )
    magnitude = rest

for _ in range(magnitude):
    raw = pos + sign
    pos = raw % N
    if raw != pos:
        rec.step(
            f"{'Forward' if sign > 0 else 'Back'} one hour: {raw} is off the wheel, "
            f"and {raw} % {N} is {pos}, so the hand wraps to {pos}.",
            wheel=wheel(pos),
        )
    else:
        rec.step(
            f"{'Forward' if sign > 0 else 'Back'} one hour: the hand is at {pos}.",
            wheel=wheel(pos),
        )

total = hour + offset
rec.step(
    f"Directly: {hour} + {offset if offset >= 0 else f'({offset})'} = {total}, and {total} % {N} = {total % N}. "
    f"The hand ended on hour {pos}, the same place.",
    wheel=wheel(pos),
)
rec.output(f"{total % N}\n")
