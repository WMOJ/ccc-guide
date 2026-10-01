import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
pos = 1
teams = []
scores = []
for _ in range(n):
    teams.append(data[pos])
    scores.append(int(data[pos + 1]))
    pos += 2

by_team = {}


def entries_frame(i):
    states = []
    for j in range(n):
        if j < i:
            states.append("done")
        elif j == i:
            states.append("current")
        else:
            states.append("none")
    return vz.array(teams, states=states, pointers={"i": i} if i < n else None)


def groups_frame(highlight=None):
    names = sorted(by_team.keys())
    cells = [[",".join(str(s) for s in by_team[t]) for t in names]]
    states = None
    if highlight is not None and highlight in names:
        idx = names.index(highlight)
        states = [["c" if k == idx else "_" for k in range(len(names))]]
    return vz.table(cells, states=states, row_heads=["scores"], col_heads=names, col_title="team")


for i, (team, score) in enumerate(zip(teams, scores)):
    by_team.setdefault(team, []).append(score)
    rec.step(
        f'Score {score} joins team "{team}": by_team["{team}"] is now {by_team[team]}.',
        entries=entries_frame(i),
        groups=groups_frame(highlight=team),
    )

lines = []
for team in sorted(by_team):
    lines.append(f"{team}: {max(by_team[team])}")
rec.step(
    "Every entry is grouped. Taking the highest score in each group answers the query.",
    entries=entries_frame(n),
    groups=groups_frame(),
)

rec.output("\n".join(lines) + "\n")
