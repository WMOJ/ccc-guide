import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
target = int(tokens[0])
numbers = [int(x) for x in tokens[1:]]
n = len(numbers)


def numbers_frame(i, found=False):
    states = ["done" if j < i else "none" for j in range(n)]
    if i < n:
        states[i] = "path" if found else "current"
    return vz.array(numbers, states=states, pointers={"i": i} if i < n else None)


def cost_frame(list_cost):
    return vz.table(
        cells=[[list_cost], [1]],
        row_heads=["list scan", "set lookup"],
        col_heads=["comparisons"],
    )


rec.step(
    f"Looking for {target} among {n} numbers. A list has to scan from the front, one comparison "
    f"per cell. A set would find {target} with one hash lookup.",
    numbers=numbers_frame(0),
    cost=cost_frame(0),
)

position = -1
comparisons = 0
for i in range(n):
    comparisons += 1
    if numbers[i] == target:
        position = i
        word = "comparison" if comparisons == 1 else "comparisons"
        rec.step(
            f"numbers[{i}] is {numbers[i]}, a match after {comparisons} {word}. The scan stops at position {i}.",
            numbers=numbers_frame(i, found=True),
            cost=cost_frame(comparisons),
        )
        break
    rec.step(
        f"numbers[{i}] is {numbers[i]}, not {target}. That was comparison {comparisons}; the scan moves on.",
        numbers=numbers_frame(i + 1),
        cost=cost_frame(comparisons),
    )
else:
    rec.step(
        f"The scan reached the end after {comparisons} comparisons without finding {target}, so the "
        f"answer is -1. A missing value costs the most, because every cell is checked.",
        numbers=numbers_frame(n),
        cost=cost_frame(comparisons),
    )

rec.output(f"{position} {comparisons}\n")
