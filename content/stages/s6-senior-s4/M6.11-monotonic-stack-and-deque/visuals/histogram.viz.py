import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
heights = [int(x) for x in rec.readline().split()]
heights.append(0)

stack = []
best = 0


def array(i, top=None, rect=None):
    st = {top: "current"} if top is not None else None
    return vz.array(heights, states=st, pointers=[("i", i)], ranges=rect, indices=True)


def stack_frame(marks=None, new=None):
    marks = marks or {}
    items = []
    for b in stack:
        s = marks.get(b)
        if b == new:
            s = "current"
        items.append((str(b), f"{b}: {heights[b]}", s))
    return vz.stack(items)


for i in range(n + 1):
    arrive = ""
    if i == 0:
        arrive = (" The stack holds bars whose right edge is still open, written `bar: height`. "
                  "The extra last cell is a bar of height 0 that will pop everything.")
    popped_here = False
    while stack and heights[stack[-1]] >= heights[i]:
        top = stack[-1]
        left = stack[-2] if len(stack) > 1 else -1
        width = i - left - 1
        area = heights[top] * width
        best = max(best, area)
        if left >= 0:
            edge = f"Its left edge is bar {left}, the next bar down the stack."
            wtext = f"{i} - {left} - 1"
        else:
            edge = "Nothing is below it on the stack, so it reaches the left wall."
            wtext = f"{i} - (-1) - 1"
        cur = f"Bar {i} ({heights[i]})" if i < n else "The sentinel (0)"
        rec.step(
            f"{cur} is not taller than bar {top} ({heights[top]}), so bar {top} cannot stretch "
            f"past it. {edge} Width {wtext} = {width}, area {heights[top]} x {width} = {area}. "
            f"Best so far: {best}.",
            a=array(i, top=top, rect=[(left + 1, i - 1, f"{heights[top]} high, {width} wide")]),
            s=stack_frame(marks={top: "done"}),
        )
        stack.pop()
        popped_here = True
    stack.append(i)
    if i == n:
        rec.step(
            f"The sentinel of height 0 has popped every bar and joined the stack. The largest "
            f"area seen is {best}, the answer.",
            a=array(i), s=stack_frame(new=i),
        )
    else:
        if stack[:-1]:
            why = f"Bar {i} ({heights[i]}) is taller than bar {stack[-2]} ({heights[stack[-2]]}) below it, so the stack stays rising. "
        else:
            why = f"Bar {i} ({heights[i]}) now sits at the bottom of the stack. "
        rec.step(
            f"{why}Bar {i} is pushed.{arrive}",
            a=array(i), s=stack_frame(new=i),
        )

rec.output(f"{best}\n")
