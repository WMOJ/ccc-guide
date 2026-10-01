import vizrec as vz

rec = vz.Recorder()
tier = rec.readline().strip()

discount = [20, 15, 10, 5, 0]
tiers = ["A", "B", "C", "D", "E"]
index = ord(tier) - ord("A")


def frame(col=None, row=None, arrow=False):
    states = {}
    if col is not None:
        states[(0, col)] = "current"
    if row is not None:
        states[(row, col)] = "current"
    arrows = [((0, col), (1, col))] if arrow else None
    return vz.table(
        [[0, 1, 2, 3, 4], discount],
        states=states,
        row_heads=["index", "discount"],
        col_heads=tiers,
        col_title="tier",
        arrows=arrows,
    )


rec.step(
    f'The tier letter read from the input is "{tier}". The table has one column per '
    "tier, but the program never searches them.",
    table=frame(),
)
rec.step(
    f'ord("{tier}") - ord("A") is {ord(tier)} - {ord("A")} = {index}, so tier {tier} '
    f"sits at index {index}.",
    table=frame(col=index),
)
rec.step(
    f"discount[{index}] is {discount[index]}: the index goes straight to that column's "
    f"discount, and the answer is {discount[index]}.",
    table=frame(col=index, row=1, arrow=True),
)

rec.output(f"{discount[index]}\n")
