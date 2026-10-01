import vizrec as vz

# Each preset's stdin is exactly one example's own .in file: two lines for eof_pitfall.py
# (which then has no third line to read), three lines for read_to_end.py. The number of
# lines read is what tells the two presets apart; there is no other signal available here.
rec = vz.Recorder()
values = [int(x) for x in rec.stdin.split() if x]
n = len(values)
is_pitfall = n == 2

# One phantom cell past the real lines, standing for "no more input".
display = values + [None]
states = ["none"] * (n + 1)


def frame(read_at):
    return vz.array(display, states=states, pointers=[("read", read_at, None, True)])


rec.step(f"There are {n} lines of input: {', '.join(str(v) for v in values)}.", a=frame(0))

total = 0
for i in range(n):
    total += values[i]
    states[i] = "done"
    rec.step(f"input() reads {values[i]}. total becomes {total}.", a=frame(min(i + 1, n)))

if is_pitfall:
    states[n] = "invalid"
    rec.step(
        "while True: never checks for a stop, so it tries to read a third line. There isn't "
        "one, and input() raises EOFError before total can be printed.",
        a=frame(n),
    )
else:
    states[n] = "done"
    rec.step(
        "for line in sys.stdin: checks for a next line, finds none, and the loop ends there, "
        "cleanly, with no error.",
        a=frame(n),
    )

rec.output(f"{total}\n")
