import vizrec as vz

rec = vz.Recorder()
front = list(map(int, rec.readline().split()))
back = list(map(int, rec.readline().split()))
n = len(front)


def arr(values, states, name=None):
    return vz.array(values, states=states, indices=True, name=name)


rec.step(
    f"front = {front}. `front.pop(0)` removes the value at index 0, which is {front[0]}.",
    a=arr(front, ["current"] + ["none"] * (n - 1), "front"),
)

work = [""] + front[1:]
rec.step(
    f"{front[0]} is gone, so index 0 is empty. A list has no gaps, so Python closes it by moving every later value one slot left.",
    a=arr(work, ["invalid"] + ["none"] * (n - 1), "front"),
)

for i in range(1, n):
    work[i - 1] = front[i]
    work[i] = ""
    states = ["done"] * i + ["invalid"] + ["none"] * (n - 1 - i)
    if i == n - 1:
        rec.step(
            f"{front[i]} moves from index {i} to index {i - 1}. That was the last move: `pop(0)` moved {n - 1} value{'s' if n - 1 != 1 else ''}, and the cell at index {n - 1} leaves the list.",
            a=arr(work, states, "front"),
        )
    else:
        rec.step(
            f"{front[i]} moves from index {i} to index {i - 1}. The empty slot is now at index {i}.",
            a=arr(work, states, "front"),
        )

after_front = front[1:]
rec.step(
    f"Now `front` is {after_front}. One `pop(0)` on a list of {n} values cost {n - 1} move{'s' if n - 1 != 1 else ''}, and a longer list costs more.",
    a=arr(after_front, ["done"] * len(after_front), "front"),
)

m = len(back)
rec.step(
    f"back = {back}. `back.pop()` with no index removes the last value, {back[-1]}, at index {m - 1}.",
    a=arr(back, ["none"] * (m - 1) + ["current"], "back"),
)

after_back = back[:-1]
rec.step(
    f"Now `back` is {after_back}. Nothing sits after the removed value, so no value moved and every other index stayed the same.",
    a=arr(after_back, ["done"] * len(after_back), "back"),
)

rec.output(f"{after_front}\n{after_back}\n")
