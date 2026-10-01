import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
n = int(tokens[0])
arr = [int(x) for x in tokens[1 : n + 1]]


def frame(read, write, note=None):
    n_items = len(arr)
    states = ["none"] * n_items
    for idx in range(0, write + 1):
        states[idx] = "done"
    if note == "match":
        states[read] = "compare"
    elif note == "write":
        states[write] = "current"
    pointers = [("write", write)]
    if read < n_items:
        pointers.append(("read", read))
    return vz.array(arr, states=states, pointers=pointers)


if n == 0:
    rec.step("The list is empty, so there is nothing to deduplicate.", numbers=vz.array(arr))
    rec.output("\n")
else:
    write = 0
    rec.step(
        f"write starts at index 0, holding arr[0] = {arr[0]}. read starts one slot ahead.",
        numbers=frame(1 if n > 1 else 0, write, note="write"),
    )

    for read in range(1, n):
        if arr[read] != arr[write]:
            write += 1
            arr[write] = arr[read]
            rec.step(
                f"arr[{read}] = {arr[read]} is new, it does not match arr[write] = {arr[write - 1] if write else arr[write]}. "
                f"write advances to index {write} and stores {arr[write]}.",
                numbers=frame(min(read + 1, n), write, note="write"),
            )
        else:
            rec.step(
                f"arr[{read}] = {arr[read]} repeats the value write already holds ({arr[write]}). "
                "read moves on without writing.",
                numbers=frame(read, write, note="match"),
            )

    unique = arr[: write + 1]
    rec.step(
        f"read has reached the end. The first {write + 1} slots hold the unique values: "
        f"{unique}.",
        numbers=frame(n, write),
    )
    rec.output(" ".join(str(x) for x in unique) + "\n")
