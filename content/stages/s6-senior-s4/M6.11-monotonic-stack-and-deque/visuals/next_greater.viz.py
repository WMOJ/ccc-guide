import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
temps = [int(x) for x in rec.readline().split()]

wait = ["?"] * n
stack = []


def table(current=None):
    row = "_" * n
    if current is not None:
        row = "_" * current + "c" + "_" * (n - current - 1)
    return vz.table(
        [list(temps), list(wait)],
        states=[row, row],
        row_heads=["temp", "wait"],
        col_heads=[str(i) for i in range(n)],
    )


def stack_frame(marks=None, new=None):
    marks = marks or {}
    items = []
    for d in stack:
        s = marks.get(d)
        if d == new:
            s = "current"
        items.append((str(d), f"{d}: {temps[d]}", s))
    return vz.stack(items)


for i in range(n):
    popped_any = False
    while stack and temps[stack[-1]] < temps[i]:
        day = stack[-1]
        wait[day] = i - day
        dword = "day" if i - day == 1 else "days"
        rec.step(
            f"Day {i} is {temps[i]}, warmer than day {day} ({temps[day]}) on top of the stack. "
            f"Day {day} stops waiting: `wait[{day}]` = {i} - {day} = {i - day} {dword}. "
            "It is popped.",
            t=table(i), s=stack_frame(marks={day: "done"}),
        )
        stack.pop()
        popped_any = True
    if stack:
        top = stack[-1]
        why = (f"Day {i} ({temps[i]}) is not warmer than day {top} ({temps[top]}), so nothing "
               "pops.")
    elif popped_any:
        why = f"Day {i} ({temps[i]}) emptied the stack."
    else:
        why = f"Day {i} ({temps[i]}) arrives at an empty stack."
    stack.append(i)
    extra = ""
    if i == 0:
        extra = (" The stack holds the days still waiting for a warmer one, written "
                 "`day: temp`; `wait` is still `?` for every day.")
    rec.step(
        f"{why} Day {i} is pushed and starts waiting.{extra}",
        t=table(i), s=stack_frame(new=i),
    )

names = [str(d) for d in stack]
if len(names) == 1:
    lead = f"Day {names[0]} never met a warmer day, so its"
else:
    lead = f"Days {', '.join(names[:-1])} and {names[-1]} never met a warmer day, so their"
for d in stack:
    wait[d] = 0
result = " ".join(str(w) for w in wait)
rec.step(
    f"The input is used up. {lead} `wait` is 0. "
    f"The answer row reads {result}.",
    t=table(), s=stack_frame(),
)
rec.output(result + "\n")
