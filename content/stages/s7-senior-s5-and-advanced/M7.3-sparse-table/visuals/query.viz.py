import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
a = list(map(int, rec.readline().split()))
q = int(rec.readline())
left, last = map(int, rec.readline().split())

LOG = n.bit_length()
sp = [a]
for k in range(1, LOG):
    prev = sp[k - 1]
    half = 1 << (k - 1)
    sp.append([min(prev[i], prev[i + half]) for i in range(n - (1 << k) + 1)])

length = last - left + 1
k = length.bit_length() - 1
size = 1 << k
second = last - size + 1
front = sp[k][left]
back = sp[k][second]
answer = min(front, back)


def frame(states=None, ranges=None, pointers=None):
    return vz.array(a, states=states, ranges=ranges, pointers=pointers, name="a")


def states_for(first_block=False, second_block=False, inside=True):
    st = {}
    if inside:
        for i in range(left, last + 1):
            st[i] = "queued"
    f = set(range(left, left + size)) if first_block else set()
    s = set(range(second, second + size)) if second_block else set()
    for i in f | s:
        st[i] = "done"
    for i in f & s:
        st[i] = "compare"
    return st


ptrs = [("l", left, "below"), ("r", last, "below")] if left != last else [("l=r", left, "below")]
rec.step(
    f"Query: the minimum of a[{left}..{last}]. The range has length {length}, marked by the pointers.",
    array=frame(states=states_for(), pointers=ptrs),
)
rec.step(
    f"The largest power of two that fits is 2^{k} = {size}, since ({length}).bit_length() - 1 = {k}. "
    f"So blocks of length {size} will cover the range.",
    array=frame(states=states_for(), pointers=ptrs),
)
rec.step(
    f"First block: sp[{k}][{left}] covers a[{left}..{left + size - 1}], the block of length {size} that starts "
    f"at the left end. Its minimum is {front}.",
    array=frame(states=states_for(first_block=True), pointers=ptrs,
                ranges=[(left, left + size - 1, f"sp[{k}][{left}]", "above")]),
)
overlap = size * 2 - length
if left == second:
    tail = " The length is a power of two, so the two blocks are the same block."
elif overlap > 0:
    tail = f" The {overlap} shared {'cell is' if overlap == 1 else 'cells are'} in both blocks."
else:
    tail = " The two blocks meet exactly, with no shared cell."
if left == second:
    second_text = f"Second block: sp[{k}][{second}] also starts at {left}, so it is the first block again. Its minimum is {back}."
else:
    second_text = (f"Second block: sp[{k}][{second}] covers a[{second}..{last}], the block of length {size} that "
                   f"ends at the right end. Its minimum is {back}.")
rec.step(
    second_text + tail,
    array=frame(states=states_for(first_block=True, second_block=True), pointers=ptrs,
                ranges=[(left, left + size - 1, f"sp[{k}][{left}]", "above"),
                        (second, last, f"sp[{k}][{second}]", "below")] if left != second
                else [(left, left + size - 1, f"sp[{k}][{left}]", "above")]),
)
rec.step(
    f"The answer is min({front}, {back}) = {answer}. Two lookups and one comparison, whatever the length of the range.",
    array=frame(states=states_for(first_block=True, second_block=True), pointers=ptrs),
)
rec.output(f"{answer}\n")
