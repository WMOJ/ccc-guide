import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
numbers = [int(x) for x in tokens]


def numbers_frame(i, stop=False):
    n = len(numbers)
    states = ["done" if j < i else "none" for j in range(n)]
    if i < n:
        states[i] = "invalid" if stop else "current"
    return vz.array(numbers, states=states, pointers={"i": i} if i < n else None)


def seen_frame(items):
    return vz.struct("set", items, name="seen")


seen = []
first_dup = -1

rec.step(
    "Before scanning, the seen set is empty. Nothing has been read yet.",
    numbers=numbers_frame(0),
    seen=seen_frame(seen),
)

for i, num in enumerate(numbers):
    if num in seen:
        first_dup = num
        rec.step(
            f"{num} at position {i} is already in seen, so it is the first duplicate. The scan stops here.",
            numbers=numbers_frame(i, stop=True),
            seen=seen_frame(seen),
        )
        break
    seen.append(num)
    word = "value" if len(seen) == 1 else "values"
    rec.step(
        f"{num} at position {i} is not in seen, so it joins the set: seen now has {len(seen)} {word}.",
        numbers=numbers_frame(i + 1),
        seen=seen_frame(seen),
    )
else:
    rec.step(
        "The scan reached the end with no repeat, so first_dup stays -1.",
        numbers=numbers_frame(len(numbers)),
        seen=seen_frame(seen),
    )

rec.output(f"{first_dup}\n")
