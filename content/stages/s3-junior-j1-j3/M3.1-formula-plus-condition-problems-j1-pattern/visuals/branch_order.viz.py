import vizrec as vz

rec = vz.Recorder()
kg = int(rec.readline())
km = int(rec.readline())
cost = kg * 2 + km // 10

rows = [["cost <= 20"], ["cost <= 50"], ["(always runs)"]]
heads = ["if", "elif", "else"]


def frame(states):
    return vz.table(rows, states=states, row_heads=heads, col_title="Condition")


rec.step(
    f"The cost is {cost}. Python checks the first condition: "
    "is it at most 20?",
    table=frame({(0, 0): "current"}),
)

if cost <= 20:
    rec.step(
        f"It is. A cost of {cost} takes the if branch right away, and "
        "the elif and else are skipped entirely.",
        table=frame({(0, 0): "path"}),
    )
    label = "Standard"
else:
    rec.step(
        f"A cost of {cost} is over 20, so Python moves on to the elif: "
        "is it at most 50?",
        table=frame({(0, 0): "invalid", (1, 0): "current"}),
    )
    if cost <= 50:
        rec.step(
            "It is. The elif branch runs here, so the else never gets "
            "a turn.",
            table=frame({(0, 0): "invalid", (1, 0): "path"}),
        )
        label = "Priority"
    else:
        rec.step(
            f"A cost of {cost} is over 50 too, so neither the if nor "
            "the elif ever matched. Whatever is left over runs the else.",
            table=frame({(0, 0): "invalid", (1, 0): "invalid", (2, 0): "path"}),
        )
        label = "Express"

rec.output(f"{label}\n")
