import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()


def frame(current):
    states = ["done" if i < current else ("current" if i == current else "none") for i in range(len(tokens))]
    return vz.array(tokens, states=states, pointers={"pos": current}, indices=True)


rec.step(
    f"The whole input becomes one list of strings: {tokens}. pos starts at 0.",
    tokens=frame(0),
)

n = int(tokens[0])
pos = 1
rec.step(
    f"tokens[0] is '{tokens[0]}', so n = {n}. pos moves to {pos}.",
    tokens=frame(pos),
)

total = 0
for i in range(n):
    val = int(tokens[pos])
    total += val
    pos += 1
    rec.step(
        f"tokens[{pos - 1}] is '{val}'. Adding it makes the running total {total}. pos moves to {pos}.",
        tokens=frame(pos),
    )

if n == 0:
    rec.step(
        "n is 0, so the loop body never runs: there are no value tokens to read.",
        tokens=frame(pos),
    )

rec.output(f"{total}\n")
