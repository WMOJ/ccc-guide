import vizrec as vz

WIDTH = 6


def digital_root(n):
    while n >= 10:
        total = 0
        while n > 0:
            total += n % 10
            n //= 10
        n = total
    return n


rec = vz.Recorder()
data = rec.stdin.split()
start = int(data[0])

top = [digital_root(n) for n in range(start, start + WIDTH)]
bottom = [digital_root(n) for n in range(start + 9, start + 9 + WIDTH)]


def row_frame(values, filled):
    vals = []
    states = []
    for i in range(WIDTH):
        if i < filled:
            vals.append(values[i])
            states.append("done")
        elif i == filled:
            vals.append(values[i])
            states.append("current")
        else:
            vals.append(None)
            states.append("none")
    return vz.array(vals, states=states)


for c in range(WIDTH):
    n_top = start + c
    n_bottom = start + 9 + c
    rec.step(
        f"N = {n_top} gives {top[c]}; N = {n_bottom}, nine higher, gives {bottom[c]} too.",
        first=row_frame(top, c),
        second=row_frame(bottom, c),
    )

rec.step(
    "Every position agrees: nine steps later, the same values come back.",
    first=row_frame(top, WIDTH),
    second=row_frame(bottom, WIDTH),
)
rec.output(" ".join(str(x) for x in top) + "\n")
rec.done()
