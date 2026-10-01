import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
n = int(tokens[0])
nxt = [int(x) for x in tokens[1 : n + 1]]
start = int(tokens[n + 1])


def frame(slow, fast, meet=False):
    states = ["none"] * n
    pointers = []
    if 0 <= slow < n:
        states[slow] = "path" if meet else "current"
        pointers.append(("slow", slow))
    if 0 <= fast < n and fast != slow:
        states[fast] = "compare"
        pointers.append(("fast", fast))
    elif 0 <= fast < n and fast == slow and meet:
        states[fast] = "path"
    return vz.array(nxt, states=states, pointers=pointers, name="nxt")


slow = start
fast = start
found = False

rec.step(
    f"slow and fast both start at index {start}.",
    nxt=frame(slow, fast),
)

while True:
    if fast == -1 or nxt[fast] == -1:
        rec.step(
            f"fast is at index {fast if fast != -1 else 'past the end'}: the next step runs off "
            "the sequence. There is no cycle to find.",
            nxt=frame(slow, fast),
        )
        break
    old_slow, old_fast = slow, fast
    slow = nxt[slow]
    fast = nxt[nxt[fast]]
    if slow == fast:
        found = True
        rec.step(
            f"slow moves one step, from {old_slow} to {slow}. fast moves two steps, from "
            f"{old_fast} to {fast}. They land on the same index: a cycle exists, met at index {slow}.",
            nxt=frame(slow, fast, meet=True),
        )
        break
    rec.step(
        f"slow moves one step, from {old_slow} to {slow}. fast moves two steps, from "
        f"{old_fast} to {fast}. Not the same index yet.",
        nxt=frame(slow, fast),
    )

if found:
    length = 1
    cur = nxt[slow]
    while cur != slow:
        cur = nxt[cur]
        length += 1
    length_word = "step" if length == 1 else "steps"
    rec.step(
        f"Walking forward from the meeting point back to itself takes {length} {length_word}: "
        f"the cycle length is {length}.",
        nxt=frame(slow, slow, meet=True),
    )
    rec.output(f"cycle length {length}\n")
else:
    rec.output("no cycle\n")
