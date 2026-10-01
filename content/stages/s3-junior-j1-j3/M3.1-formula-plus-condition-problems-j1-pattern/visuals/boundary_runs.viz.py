import vizrec as vz

rec = vz.Recorder()
runs = []
for _ in range(3):
    kg, km = rec.readline().split()
    runs.append((int(kg), int(km)))


def tier(cost):
    if cost <= 20:
        return "Standard"
    if cost <= 50:
        return "Priority"
    return "Express"




def table(k):
    rows = []
    for j, (kg, km) in enumerate(runs):
        cost = kg * 2 + km // 10
        if j < k:
            rows.append([f"{kg}, {km}", cost, tier(cost)])
        else:
            rows.append([f"{kg}, {km}", "?", "?"])
    states = {}
    for j in range(k):
        states[(j, 1)] = "done"
        states[(j, 2)] = "done"
    if k < 3:
        states[(k, 0)] = "current"
    return vz.table(rows, states=states, col_heads=["kg, km", "cost", "output"])


rec.step(
    "Three inputs, run one after another. The expected tier for each is worked out by hand "
    "first, then compared with what the program prints.",
    table=table(0),
    line=vz.line(0, 60, tick=10, intervals=[(0, 20, "Standard", None, 0), (21, 50, "Priority", None, 0), (51, 60, "Express", None, 0)]),
)
for k in range(3):
    kg, km = runs[k]
    cost = kg * 2 + km // 10
    rec.step(
        f"Run {k + 1}: {kg} * 2 + {km} // 10 = {cost}"
        + (f" ({km} // 10 rounds down to {km // 10})" if km % 10 else "")
        + f", so the program prints {tier(cost)}.",
        table=table(k + 1),
        line=vz.line(
            0,
            60,
            tick=10,
            points=[(cost, f"cost {cost}", "current")],
            intervals=[
                (0, 20, "Standard", "path" if cost <= 20 else None, 0),
                (21, 50, "Priority", "path" if 20 < cost <= 50 else None, 0),
                (51, 60, "Express", "path" if cost > 50 else None, 0),
            ],
        ),
    )
final_cost = [kg * 2 + km // 10 for kg, km in runs]
rec.step(
    f"The costs {final_cost[0]}, {final_cost[1]} and {final_cost[2]} give "
    f"{tier(final_cost[0])}, {tier(final_cost[1])} and {tier(final_cost[2])}. "
    "Each matches the answer worked out by hand.",
    table=table(3),
    line=vz.line(0, 60, tick=10, intervals=[(0, 20, "Standard", None, 0), (21, 50, "Priority", None, 0), (51, 60, "Express", None, 0)]),
)
rec.output(f"{tier(runs[0][0] * 2 + runs[0][1] // 10)}\n")
