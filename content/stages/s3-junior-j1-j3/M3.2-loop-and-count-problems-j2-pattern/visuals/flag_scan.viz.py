import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
scores = [int(rec.readline()) for _ in range(n)]

high = 0
low = 0
all_high = True
states = ["_"] * n


def arr(i):
    pointers = [("i", i, None, True)] if i is not None else None
    return vz.array(scores, states=states, pointers=pointers, indices=True)


def tab(states_map=None):
    return vz.table([[high], [low], [all_high]], states=states_map, row_heads=["high", "low", "all_high"])


for i in range(n):
    states[i] = "c"
    rec.step(
        f"Position {i}: score {scores[i]}. Is it above 75?",
        array=arr(i),
        table=tab(),
    )
    if scores[i] > 75:
        high += 1
        states[i] = "d"
        rec.step(
            f"{scores[i]} > 75 is True, so high becomes {high}. low is {low} and all_high stays {all_high}.",
            array=arr(i),
            table=tab({(0, 0): "path"}),
        )
    else:
        low += 1
        all_high = False
        states[i] = "x"
        rec.step(
            f"{scores[i]} > 75 is False, so low becomes {low} and all_high becomes False for good.",
            array=arr(i),
            table=tab({(1, 0): "path", (2, 0): "path"}),
        )

rec.step(
    f"The scan is done: high = {high}, low = {low}, all_high = {all_high}. "
    f"The program prints {high} {low}, then {'Yes' if all_high else 'No'}.",
    array=vz.array(scores, states=states, indices=True),
    table=tab({(0, 0): "path", (1, 0): "path", (2, 0): "path"}),
)

rec.output(f"{high} {low}\n" + ("Yes" if all_high else "No") + "\n")
