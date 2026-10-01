import vizrec as vz

rec = vz.Recorder()
nums = [int(x) for x in rec.readline().split()]
n = len(nums)
states = ["unvisited"] * n
evens = []


def label():
    return f"evens {evens}"


def frame(at):
    return vz.array(nums, states=states, pointers=[("x", at, None, True)], name=label())


for i, x in enumerate(nums):
    states[i] = "current"
    if x % 2 == 0:
        evens.append(x)
        caption = f"x is {x}. {x} % 2 == 0 is True, so the condition passes and {x} is added to `evens`."
    else:
        caption = f"x is {x}. {x} % 2 == 0 is False, so the condition fails and {x} is skipped."
    rec.step(caption, a=frame(i))
    states[i] = "done" if x % 2 == 0 else "invalid"

if evens:
    last = f"Every value has been checked. `evens` is {evens}."
else:
    last = "Every value has been checked. Nothing passed the condition, so `evens` is the empty list, []."
rec.step(last, a=frame(n))
rec.output(f"{nums}\n{evens}\n")
