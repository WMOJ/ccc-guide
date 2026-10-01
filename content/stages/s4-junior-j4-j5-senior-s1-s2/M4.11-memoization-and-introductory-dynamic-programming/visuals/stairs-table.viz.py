import vizrec as vz

rec = vz.Recorder()
target = int(rec.readline())

ways = [None] * (target + 2)


def frame(current=None, sources=()):
    states = []
    for i, v in enumerate(ways):
        if i == current:
            states.append("current")
        elif i in sources:
            states.append("compare")
        elif v is not None:
            states.append("done")
        else:
            states.append("unvisited")
    return {"table": vz.array(ways, states=states, name="ways")}


ways[target] = 1
ways[target + 1] = 1
rec.step(
    f"Stairs {target} and {target + 1} are the base cases: landing on either one finishes "
    "the climb, so both start at 1.",
    **frame(),
)
stair = target - 1
while stair >= 0:
    a, b = ways[stair + 1], ways[stair + 2]
    rec.step(
        f"`ways[{stair}]` reads the two cells one and two steps ahead, `ways[{stair + 1}]` = "
        f"{a} and `ways[{stair + 2}]` = {b}.",
        **frame(current=stair, sources=(stair + 1, stair + 2)),
    )
    ways[stair] = a + b
    rec.step(
        f"`ways[{stair}]` is set to {a} + {b} = {ways[stair]}.",
        **frame(current=stair),
    )
    stair -= 1

rec.output(f"{ways[0]}\n")
