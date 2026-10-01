import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
numbers = [int(x) for x in tokens]


def numbers_frame(i):
    states = ["done" if j < i else "none" for j in range(len(numbers))]
    if i < len(numbers):
        states[i] = "current"
    return vz.array(numbers, states=states, pointers={"i": i} if i < len(numbers) else None)


def best_frame(min_val, max_val, changed=None):
    states = None
    if changed is not None:
        states = ["current" if s == changed else "none" for s in ("min", "max")]
    return vz.array([min_val, max_val], states=states)


min_val = numbers[0]
max_val = numbers[0]

rec.step(
    f"Before the loop, both running values start at the first number, {numbers[0]}.",
    numbers=numbers_frame(0),
    best=best_frame(min_val, max_val),
)

for i in range(1, len(numbers)):
    num = numbers[i]
    changed = None
    old_min, old_max = min_val, max_val
    if num < min_val:
        min_val = num
        changed = "min"
    if num > max_val:
        max_val = num
        changed = "max"

    if changed == "min":
        caption = f"{num} beats the running min of {old_min}. min_val drops to {min_val}."
    elif changed == "max":
        caption = f"{num} is a new high. max_val rises from {old_max} to {max_val}."
    else:
        caption = (
            f"{num} sits inside the range seen so far, {min_val} to {max_val}, so nothing changes."
        )
    rec.step(
        caption,
        numbers=numbers_frame(i),
        best=best_frame(min_val, max_val, changed),
    )

count_word = "number" if len(numbers) == 1 else "numbers"
rec.step(
    f"After one pass over all {len(numbers)} {count_word}, min_val is {min_val} and max_val is {max_val}.",
    numbers=numbers_frame(len(numbers)),
    best=best_frame(min_val, max_val),
)

rec.output(f"{min_val} {max_val}\n")
