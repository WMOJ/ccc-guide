import vizrec as vz

rec = vz.Recorder()
kg = int(rec.readline())
km = int(rec.readline())

weight_part = kg * 2
distance_part = km // 10
cost = weight_part + distance_part
if cost <= 20:
    label, win = "Standard", 0
elif cost <= 50:
    label, win = "Priority", 1
else:
    label, win = "Express", 2

heads = ["kg * 2", "km // 10", "cost"]
bands = [(0, 20, "Standard"), (21, 50, "Priority"), (51, 60, "Express")]


def parts(values, states=None):
    return vz.table([[v] for v in values], states=states, row_heads=heads, col_title="Value")


def line(point=None, winner=None):
    ivs = [(a, b, name, "path" if winner == k else None, 0) for k, (a, b, name) in enumerate(bands)]
    pts = [(point, f"cost {point}", "current")] if point is not None else None
    return vz.line(0, 60, tick=10, points=pts, intervals=ivs)


rec.step(
    f"A package of {kg} kg over {km} km. The cost has two parts, weight and distance, "
    "and the bands on the line are the three tiers.",
    parts=parts(["?", "?", "?"]),
    line=line(),
)
rec.step(
    f"The weight part is {kg} * 2 = {weight_part}.",
    parts=parts([weight_part, "?", "?"], {(0, 0): "current"}),
    line=line(),
)
rec.step(
    f"The distance part is {km} // 10 = {distance_part}, rounded down because a partial 10 km does not count.",
    parts=parts([weight_part, distance_part, "?"], {(1, 0): "current"}),
    line=line(),
)
rec.step(
    f"cost = {weight_part} + {distance_part} = {cost}. That one number is placed on the line.",
    parts=parts([weight_part, distance_part, cost], {(2, 0): "current"}),
    line=line(cost),
)
rec.step(
    f"{cost} falls in the {label} band, so the program prints {label}.",
    parts=parts([weight_part, distance_part, cost], {(2, 0): "done"}),
    line=line(cost, win),
)
rec.output(f"{label}\n")
