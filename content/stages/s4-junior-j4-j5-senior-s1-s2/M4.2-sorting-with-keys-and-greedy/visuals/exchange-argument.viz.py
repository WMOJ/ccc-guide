import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
times = list(map(int, data[1:n + 1]))

rec.step(
    "These jobs run one after another on a single machine, in the order they arrive.",
    jobs=vz.array(times),
)

# Find the first adjacent pair that is out of order (a later job shorter than an earlier one).
swap_i = None
for i in range(n - 1):
    if times[i] > times[i + 1]:
        swap_i = i
        break

if swap_i is None:
    rec.step(
        "Every adjacent pair is already shortest first, so no swap changes the total.",
        jobs=vz.array(times),
    )
else:
    a, b = times[swap_i], times[swap_i + 1]
    before = 2 * a + b
    rec.step(
        f"Jobs at positions {swap_i} and {swap_i + 1} are out of order: {a} runs before {b}. "
        f"Only their own two finish times change if they swap, and those add up to "
        f"2 x {a} + {b} = {before}.",
        jobs=vz.array(
            times,
            pointers=[("i", swap_i, "above", True), ("i+1", swap_i + 1, "above")],
        ),
    )
    swapped = list(times)
    swapped[swap_i], swapped[swap_i + 1] = swapped[swap_i + 1], swapped[swap_i]
    after = 2 * b + a
    rec.step(
        f"Swap them, shortest first: their two finish times now add up to 2 x {b} + {a} = "
        f"{after}, which is {before - after} less. Putting the shorter job first never costs "
        f"more, and strictly helps whenever the jobs differ.",
        jobs=vz.array(
            swapped,
            pointers=[("i", swap_i, "above", True), ("i+1", swap_i + 1, "above")],
            compare=(swap_i, swap_i + 1, f"-{before - after}"),
        ),
    )
    rec.skip(
        "Repeating this swap at every out-of-order adjacent pair, each time strictly improving "
        "or leaving the total unchanged, ends with the whole list shortest first.",
        max(n - 2, 1),
        jobs=vz.array(swapped),
    )

order = sorted(times)
finish = 0
total = 0
for t in order:
    finish += t
    total += finish

rec.step(
    f"Sorted shortest first: {', '.join(map(str, order))}. The sum of every finish time is "
    f"{total}, the smallest possible for these jobs.",
    jobs=vz.array(order),
)

rec.output(" ".join(map(str, order)) + "\n" + str(total) + "\n")
