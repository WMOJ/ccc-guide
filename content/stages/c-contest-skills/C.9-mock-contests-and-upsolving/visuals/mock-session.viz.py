import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
count = int(tokens[0])
pos = 1
stretches = []
for _ in range(count):
    problem = int(tokens[pos])
    start = int(tokens[pos + 1])
    end = int(tokens[pos + 2])
    verdict = tokens[pos + 3]
    pos += 4
    stretches.append((problem, start, end, verdict))

shown = []
subs = {}
accepted_at = {}
used = 0
labels = {"A": "OK", "W": "WA", "N": "no submit"}
states = {"A": "done", "W": "invalid", "N": "compare"}
first_start = stretches[0][1]


def frame():
    return vz.line(0, 180, tick=30, intervals=list(shown))


for k, (problem, start, end, verdict) in enumerate(stretches):
    shown.append((start, end, labels[verdict], states[verdict], problem - 1))
    used += end - start
    if verdict != "N":
        subs[problem] = subs.get(problem, 0) + 1
    if verdict == "A":
        accepted_at.setdefault(problem, end)
    before = sum(1 for s in stretches[:k] if s[0] == problem)
    head = f"Minute {start} to {end}, problem {problem}."
    if k == 0 and first_start > 0:
        head = f"Minutes 0 to {first_start} went to reading the statements. Then minute {start} to {end}, problem {problem}."
    if verdict == "A":
        if before == 0:
            tail = " One stretch, and the submission is accepted."
        else:
            ordinal = {1: "second", 2: "third"}[before]
            tail = f" This is its {ordinal} stretch, and the submission is accepted."
    elif verdict == "W":
        tail = " The submission gets wrong answer."
        if before:
            tail = " Another submission, and it gets wrong answer again."
    else:
        tail = " The clock runs out before any submission, so the bar ends open."
    rec.step(head + tail + f" That is {used} minutes in stretches so far.", line=frame())

lines = []
for problem in sorted(set(s[0] for s in stretches)):
    n = subs.get(problem, 0)
    if n == 0:
        lines.append(f"problem {problem}: no submission")
        continue
    word = "submission" if n == 1 else "submissions"
    if problem in accepted_at:
        text = f"accepted at minute {accepted_at[problem]}"
    else:
        text = "never accepted"
    lines.append(f"problem {problem}: {n} {word}, {text}")
last_end = stretches[-1][2]
lines.append(f"{used} of 180 minutes in stretches, last one ended at minute {last_end}")
unsolved = [str(p) for p in sorted(set(s[0] for s in stretches)) if p not in accepted_at]
if unsolved:
    names = " and ".join(unsolved)
    noun = "Problem" if len(unsolved) == 1 else "Problems"
    verb = "was" if len(unsolved) == 1 else "were"
    pron = "it comes" if len(unsolved) == 1 else "they come"
    ending = f"{noun} {names} {verb} never accepted, so {pron} first when upsolving."
else:
    ending = f"Every problem attempted is accepted, and minutes {last_end} to 180 went unused."
rec.step(
    f"The finished log has one row per problem; a row with several bars took several submissions. {ending}",
    line=frame(),
)
rec.output("\n".join(lines) + "\n")
