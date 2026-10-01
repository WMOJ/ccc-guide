import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
count = int(tokens[0])
pos = 1
history = {}
for _ in range(count):
    problem = int(tokens[pos])
    verdict = tokens[pos + 3]
    pos += 4
    history.setdefault(problem, []).append(verdict)

problems = sorted(history)
first = ["?"] * len(problems)
marks = ["___"] * len(problems)
lines = []


def frame():
    cells = []
    for i, problem in enumerate(problems):
        verdicts = history[problem]
        tries = sum(1 for v in verdicts if v != "N")
        ok = "yes" if "A" in verdicts else "no"
        cells.append([str(tries), ok, first[i]])
    return vz.table(
        cells=cells,
        states=list(marks),
        row_heads=[f"P{p}" for p in problems],
        col_heads=["tries", "accepted", "first step"],
    )


rec.step(
    "The log from a mock session, reduced to a row per problem: how many submissions it took and "
    "whether one was accepted. The first-step column is still empty.",
    table=frame(),
)
for i, problem in enumerate(problems):
    verdicts = history[problem]
    if verdicts == ["N"]:
        word, text, mark = "brute", "write a brute force for the first subtask", "__m"
        why = (
            f"Problem {problem} has no submission. A brute force for its first subtask gives you "
            "a correct program to start from."
        )
    elif "A" not in verdicts:
        word, text, mark = "stress", "stress test the last attempt against a brute force", "__x"
        why = (
            f"Problem {problem} was never accepted. Stress test the last attempt against a brute "
            "force, and the smallest input where they disagree points at the bug."
        )
    elif verdicts[0] == "A":
        word, text, mark = "none", "nothing to upsolve", "__d"
        why = f"Problem {problem} was accepted on the first submission, so there is nothing to upsolve."
    else:
        word, text, mark = "compare", "compare the first attempt with the accepted one", "__p"
        why = (
            f"Problem {problem} needed several submissions. Run the first attempt and the accepted "
            "one on small inputs to see what the change fixed."
        )
    first[i] = word
    marks[i] = mark
    lines.append(f"problem {problem}: {text}")
    rec.step(why, table=frame())
rec.step(
    "Each problem now has one next action, chosen from what the log shows. A problem can need more "
    "than one step, but the log tells you where to begin.",
    table=frame(),
)
rec.output("\n".join(lines) + "\n")
