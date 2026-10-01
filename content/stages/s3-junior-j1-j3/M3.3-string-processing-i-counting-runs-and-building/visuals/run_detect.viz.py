import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def frame(done_upto, cur_start, cur_end, look=None):
    states = ["done" if pos < done_upto else "_" for pos in range(n)]
    for pos in range(cur_start, cur_end):
        states[pos] = "current"
    pointers = [("start", cur_start, None, True)]
    if look is not None:
        pointers.append(("look", look))
    return vz.array(list(s), states=states, pointers=pointers, indices=True)


lines = []
i = 0
while i < n:
    current_char = s[i]
    count = 1
    rec.step(
        f"A new run starts at index {i}: '{current_char}'.",
        chars=frame(i, i, i + 1),
    )
    while i + count < n and s[i + count] == current_char:
        rec.step(
            f"s[{i + count}] is also '{current_char}': count becomes {count + 1}.",
            chars=frame(i, i, i + count + 1, look=i + count),
        )
        count += 1
    if i + count < n:
        rec.step(
            f"s[{i + count}] is '{s[i + count]}', not '{current_char}': the run ends at length {count}.",
            chars=frame(i, i, i + count, look=i + count),
        )
    else:
        rec.step(
            f"Index {i + count} is past the end of the string: the run ends at length {count}.",
            chars=frame(i, i, i + count),
        )
    lines.append(f"{current_char} {count}")
    i += count

rec.output("\n".join(lines) + "\n")
