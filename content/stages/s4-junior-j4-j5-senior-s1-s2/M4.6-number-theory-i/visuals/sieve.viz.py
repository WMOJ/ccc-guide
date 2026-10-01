import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
n = int(tokens[0])

numbers = list(range(2, n + 1))
struck = [False] * len(numbers)
cols = 6
rows = (len(numbers) + cols - 1) // cols


def grid_rows(current_index=None, final=False):
    row_strs = []
    value_rows = []
    for r in range(rows):
        row = []
        value_row = []
        for c in range(cols):
            idx = r * cols + c
            if idx >= len(numbers):
                continue
            value_row.append(numbers[idx])
            if idx == current_index:
                row.append("c")
            elif struck[idx]:
                row.append("x")
            elif final or idx < (current_index if current_index is not None else 0):
                row.append("d")
            else:
                row.append(".")
        row_strs.append("".join(row))
        value_rows.append(value_row)
    return row_strs, value_rows


rec.step(
    f"Numbers {numbers[0]} to {numbers[-1]}, none tested yet.",
    grid=vz.grid(*grid_rows()),
)

p_index = 0
while numbers[p_index] ** 2 <= n:
    if not struck[p_index]:
        p = numbers[p_index]
        multiple = p * p
        marked = []
        while multiple <= n:
            struck[multiple - 2] = True
            marked.append(multiple)
            multiple += p
        rec.step(
            f"{p} is still unmarked, so it is prime. Mark its multiples starting at "
            f"{p * p}, every {p}: {', '.join(str(m) for m in marked)}. Numbers already marked "
            "stay marked.",
            grid=vz.grid(*grid_rows(current_index=p_index)),
        )
    p_index += 1

primes = [numbers[i] for i in range(len(numbers)) if not struck[i]]
rec.step(
    f"No candidate past the square root of {n} still needs marking. Every number left "
    f"unmarked is prime: {', '.join(str(x) for x in primes)}.",
    grid=vz.grid(*grid_rows(final=True)),
)

rec.output(f"{len(primes)}\n{' '.join(str(x) for x in primes)}\n")
