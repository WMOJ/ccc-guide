import random
import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
seed = int(data[1])
random.seed(seed)


def frame(gift, name, states=None, pointers=None):
    return vz.array(gift, states=states, pointers=pointers, indices=True, name=name)


tries = 0
while True:
    tries += 1
    name = f"gift, try {tries}"
    gift = list(range(n))
    if tries == 1:
        rec.step(
            f"Try 1 starts with `gift[i] = i`: every friend gives to themselves. "
            f"The shuffle fixes one position at a time, starting at position {n - 1}"
            f"{' and stopping at 1' if n > 2 else ''}.",
            a=frame(gift, name),
        )
    else:
        rec.step(
            f"Try {tries} starts over from the same list, `gift[i] = i`.",
            a=frame(gift, name),
        )
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        gift[i], gift[j] = gift[j], gift[i]
        finished = (
            f"Position {i} is now finished." if i == n - 1
            else f"Positions {i} to {n - 1} are now finished."
        )
        states = ["none"] * n
        for k in range(i + 1, n):
            states[k] = "done"
        states[i] = "current"
        if j == i:
            caption = (
                f"`random.randint(0, {i})` gives j = {i}, the same position, so `gift[{i}]` "
                f"swaps with itself and stays {gift[i]}."
            )
            pointers = [("i, j", i)]
        else:
            states[j] = "compare"
            caption = (
                f"`random.randint(0, {i})` gives j = {j}, so `gift[{i}]` and `gift[{j}]` swap. "
                f"{finished}"
            )
            pointers = [("i", i), ("j", j)]
        rec.step(caption, a=frame(gift, name, states, pointers))
    fixed = [i for i in range(n) if gift[i] == i]
    if fixed:
        states = ["invalid" if gift[i] == i else "done" for i in range(n)]
        if len(fixed) == 1:
            who = f"Friend {fixed[0]} gives to themselves"
        else:
            who = "Friends " + " and ".join(str(i) for i in fixed) + " give to themselves"
        rec.step(
            f"Checking the finished shuffle: {who}, so it is not valid. Throw it away and "
            "shuffle again.",
            a=frame(gift, name, states),
        )
    else:
        rec.step(
            f"Checking the finished shuffle: no friend gives to themselves. Try {tries} is "
            f"the answer, `{' '.join(map(str, gift))}`, after {tries} "
            f"{'try' if tries == 1 else 'tries'}.",
            a=frame(gift, name, ["done"] * n),
        )
        break

rec.output(f"{tries}\n{' '.join(map(str, gift))}\n")
