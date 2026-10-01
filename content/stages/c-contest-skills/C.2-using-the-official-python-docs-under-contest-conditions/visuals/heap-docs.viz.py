import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
item = int(tokens[0])
start = sorted(int(t) for t in tokens[1:])

# Heaps are shown in sorted order so the smallest item is always the leftmost cell.


def cells(values, mark=None):
    states = ["current" if v == mark else "none" for v in values]
    return vz.array(values, states=states)


# heappushpop: push first, then pop the smallest.
pushed = sorted(start + [item])
popped_a = pushed[0]
after_a = pushed[1:]
# heapreplace: pop first, then push.
popped_b = start[0]
middle_b = start[1:]
after_b = sorted(middle_b + [item])

rec.step(
    f"Both calls start from the same heap, {start}, and the same item, {item}. "
    f"The docs describe heappushpop as push then pop, and heapreplace as pop and also push.",
    a=cells(start),
    b=cells(start),
)
rec.step(
    f"heappushpop pushes {item} first, so the heap briefly holds {pushed}.",
    a=cells(pushed, item),
    b=cells(start),
)
if popped_a == item and item in start:
    word_a = "equal to the item it just pushed"
elif popped_a == item:
    word_a = "the item it just pushed"
else:
    word_a = "an item that was already there"
rec.step(
    f"Then it pops the smallest, {popped_a}, which is {word_a}. It returns {popped_a}, "
    f"and the heap is {after_a}.",
    a=cells(after_a),
    b=cells(start),
)
rec.step(
    f"heapreplace pops first: the smallest, {popped_b}, leaves the heap, which becomes {middle_b}.",
    a=cells(after_a),
    b=cells(middle_b),
)
rec.step(
    f"Then it pushes {item}. It returns {popped_b}, and the heap is {after_b}.",
    a=cells(after_a),
    b=cells(after_b, item),
)
if popped_a == popped_b:
    final = (
        f"Both calls returned {popped_a} and left {after_a}. The order of push and pop only "
        f"matters when the new item is smaller than the heap's smallest."
    )
else:
    final = (
        f"heappushpop returned {popped_a} and kept {after_a}. heapreplace returned {popped_b} "
        f"and kept {after_b}. The results differ because the new item is smaller than the "
        f"heap's smallest."
    )
rec.step(final, a=cells(after_a), b=cells(after_b))
rec.output(
    f"heappushpop: returned {popped_a}, heap {after_a}\n"
    f"heapreplace: returned {popped_b}, heap {after_b}\n"
)
