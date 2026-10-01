import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
n = int(tokens[0])
values = [int(t) for t in tokens[1 : 1 + n]]

results = []
for i, val in enumerate(values):
    squared = val * val
    results.append(str(squared))
    value_states = ["done" if j < i else ("current" if j == i else "none") for j in range(n)]
    rec.step(
        f"values[{i}] is {val}. Its square is {val} * {val} = {squared}, appended to results.",
        values=vz.array(values, states=value_states),
        results=vz.array(results, states=["done"] * len(results)),
    )

joined = "\n".join(results) + "\n"
rec.step(
    f'All results are collected. The join plus a final newline builds one string, {joined!r}, and write is called once.',
    values=vz.array(values, states=["done"] * n),
    results=vz.array(results, states=["current"] * len(results)),
)

rec.output("\n".join(results) + "\n")
