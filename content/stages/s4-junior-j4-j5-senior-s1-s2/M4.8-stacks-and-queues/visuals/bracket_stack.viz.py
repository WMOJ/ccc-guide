import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
pairs = {"(": ")", "[": "]", "{": "}"}
stack = []


def chars_frame(i, invalid=False):
    states = []
    for j in range(len(s)):
        if invalid and j == i:
            states.append("invalid")
        elif j < i:
            states.append("done")
        elif j == i:
            states.append("current")
        else:
            states.append("none")
    return vz.array(list(s), states=states)


def stack_frame(top_state=None):
    states = ["done"] * len(stack)
    if top_state and stack:
        states[-1] = top_state
    return vz.stack(list(zip(stack, states)))


ok = True
for i, c in enumerate(s):
    if c in pairs:
        stack.append(c)
        rec.step(
            f"'{c}' is an opener. Push it. The stack is now {stack}.",
            chars=chars_frame(i),
            stack=stack_frame("current"),
        )
        continue
    if not stack:
        rec.step(
            f"'{c}' is a closer, but the stack is empty. Nothing to match it: invalid.",
            chars=chars_frame(i, invalid=True),
            stack=stack_frame(),
        )
        ok = False
        break
    top = stack[-1]
    if pairs[top] == c:
        stack.pop()
        rec.step(
            f"'{c}' matches the top of the stack, '{top}'. Pop it. The stack is now {stack}.",
            chars=chars_frame(i),
            stack=stack_frame(),
        )
    else:
        rec.step(
            f"'{c}' does not match the top of the stack, '{top}'. Invalid.",
            chars=chars_frame(i, invalid=True),
            stack=stack_frame("invalid"),
        )
        ok = False
        break

if ok:
    if stack:
        rec.step(
            f"Every character is read, but {stack} is still on the stack: an unclosed opener. Invalid.",
            chars=chars_frame(len(s)),
            stack=stack_frame("invalid"),
        )
        ok = False
    else:
        rec.step(
            "Every character is read and the stack is empty. The string is valid.",
            chars=chars_frame(len(s)),
            stack=stack_frame(),
        )

rec.output(f"{ok}\n")
