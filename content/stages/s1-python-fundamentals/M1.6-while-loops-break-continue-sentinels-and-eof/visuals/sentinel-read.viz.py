import vizrec as vz

rec = vz.Recorder()
values = [int(x) for x in rec.stdin.split() if x]
n = len(values)
states = ["none"] * n
total = 0


def frame(read_at, name):
    return vz.array(values, states=states, pointers=[("read", read_at, None, True)], name=name)


rec.step(f"Read the first number before the loop starts. It is {values[0]}.", a=frame(0, "total: 0"))

i = 0
joins = 0
while values[i] != 0:
    just_read = values[i]
    total += just_read
    states[i] = "done"
    i += 1
    joins += 1
    if i < n:
        if joins == 1:
            caption = (
                f"{just_read} joins the running total since it is not the sentinel. The total "
                f"becomes {total}, and the next read is {values[i]}."
            )
        else:
            caption = (
                f"{just_read} behaves the same way (it is not the sentinel); the total now "
                f"stands at {total}, ready for the next read, {values[i]}."
            )
        rec.step(caption, a=frame(i, f"total: {total}"))

states[i] = "invalid"
rec.step(
    f"Then {values[i]} shows up. That is the sentinel, so the loop ends before total += number runs.",
    a=frame(i, f"total: {total}"),
)

rec.output(f"{total}\n")
