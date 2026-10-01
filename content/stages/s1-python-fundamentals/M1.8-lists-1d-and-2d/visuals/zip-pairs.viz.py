import vizrec as vz

rec = vz.Recorder()
names = rec.readline().split()
scores = [int(x) for x in rec.readline().split()]
shorter = min(len(names), len(scores))
out = ""

n_states = ["unvisited"] * len(names)
s_states = ["unvisited"] * len(scores)


def frames(at):
    return {
        "a": vz.array(names, states=n_states, pointers=[("name", at, None, True)] if at is not None else None, indices=True),
        "b": vz.array(scores, states=s_states, pointers=[("score", at, None, True)] if at is not None else None, indices=True),
    }


for i in range(shorter):
    n_states[i] = "current"
    s_states[i] = "current"
    out += f"{names[i]} {scores[i]}\n"
    if i == 0:
        caption = f'`zip(names, scores)` pairs the values at the same index. Pass 0 pairs "{names[i]}" with {scores[i]}, and the loop prints `{names[i]} {scores[i]}`.'
    else:
        caption = f'Pass {i} pairs index {i} of both lists: "{names[i]}" with {scores[i]}. The loop prints `{names[i]} {scores[i]}`.'
    rec.step(caption, **frames(i))
    n_states[i] = "done"
    s_states[i] = "done"

if len(names) == len(scores):
    rec.step(
        f"Both lists run out together after {shorter} passes, so the loop ends.",
        **frames(None),
    )
else:
    longer_states = n_states if len(names) > len(scores) else s_states
    which = "names" if len(names) > len(scores) else "scores"
    short = "scores" if which == "names" else "names"
    for j in range(shorter, len(longer_states)):
        longer_states[j] = "invalid"
    rec.step(
        f"`{short}` has only {shorter} values, so `zip` stops after pass {shorter - 1}. The extra values in `{which}` are never visited.",
        **frames(None),
    )

rec.output(out)
