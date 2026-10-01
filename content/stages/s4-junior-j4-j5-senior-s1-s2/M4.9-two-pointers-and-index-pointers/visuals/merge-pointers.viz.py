import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
pos = 0
n = int(tokens[pos])
pos += 1
a = [int(x) for x in tokens[pos : pos + n]]
pos += n
m = int(tokens[pos])
pos += 1
b = [int(x) for x in tokens[pos : pos + m]]


def a_frame(i, done=False):
    states = ["done" if idx < i else "none" for idx in range(len(a))]
    ptrs = [] if done or i >= len(a) else [("i", i)]
    return vz.array(a, states=states, pointers=ptrs)


def b_frame(j, done=False):
    states = ["done" if idx < j else "none" for idx in range(len(b))]
    ptrs = [] if done or j >= len(b) else [("j", j)]
    return vz.array(b, states=states, pointers=ptrs)


i = 0
j = 0
merged = []

rec.step(
    f"i starts at index 0 of A, j starts at index 0 of B. merged is empty.",
    a=a_frame(i),
    b=b_frame(j),
)

while i < n and j < m:
    if a[i] <= b[j]:
        merged.append(a[i])
        rec.step(
            f"A[{i}] = {a[i]} is at most B[{j}] = {b[j]}, so it comes next. "
            f"merged so far: {merged}. i advances.",
            a=a_frame(i + 1),
            b=b_frame(j),
        )
        i += 1
    else:
        merged.append(b[j])
        rec.step(
            f"B[{j}] = {b[j]} is smaller than A[{i}] = {a[i]}, so it comes next. "
            f"merged so far: {merged}. j advances.",
            a=a_frame(i),
            b=b_frame(j + 1),
        )
        j += 1

if i < n:
    tail = a[i:]
    merged.extend(tail)
    rec.step(
        f"B is exhausted. The rest of A, {tail}, is already sorted, so it is copied over as is. "
        f"merged: {merged}.",
        a=a_frame(n, done=True),
        b=b_frame(j, done=True),
    )
elif j < m:
    tail = b[j:]
    merged.extend(tail)
    rec.step(
        f"A is exhausted. The rest of B, {tail}, is already sorted, so it is copied over as is. "
        f"merged: {merged}.",
        a=a_frame(i, done=True),
        b=b_frame(m, done=True),
    )
else:
    rec.step(
        f"Both lists are exhausted at the same time. merged: {merged}.",
        a=a_frame(i, done=True),
        b=b_frame(j, done=True),
    )

rec.output(" ".join(str(x) for x in merged) + "\n")
