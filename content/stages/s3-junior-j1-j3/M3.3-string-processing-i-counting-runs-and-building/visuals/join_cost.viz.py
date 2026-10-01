import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)

# Cost model, not a stopwatch: a worst-case += copies the whole result built so far, plus the
# new character, every time. A list append costs one step; join then copies the final result
# once, at the end.
concat_final = n * (n + 1) // 2
join_final = 2 * n
y_max = max(concat_final, join_final, 1)


def chars(count):
    return f"{count} character{'s' if count != 1 else ''}"


concat_pts = []
join_pts = []
concat_total = 0
join_total = 0

for k in range(1, n + 1):
    concat_total += k
    join_total += 1
    concat_pts.append((k, concat_total))
    join_pts.append((k, join_total))
    rec.step(
        f"After {chars(k)}: += has copied {chars(concat_total)} in total so far; "
        f"appending to a list has taken {join_total} step{'s' if join_total != 1 else ''}, "
        "with the join still ahead.",
        cost=vz.plot(
            x=(0, n, "characters appended"),
            y=(0, y_max, "characters copied"),
            series=[
                ("concat", "+= worst case", list(concat_pts), 0),
                ("join", "list + join", list(join_pts), 1),
            ],
        ),
    )

rec.step(
    f"The join runs once, copying {'all ' if n != 1 else ''}{chars(n)}: list + join finishes at {join_final} "
    f"total steps, against {concat_final} for += on the same string.",
    cost=vz.plot(
        x=(0, n, "characters appended"),
        y=(0, y_max, "characters copied"),
        series=[
            ("concat", "+= worst case", list(concat_pts), 0),
            ("join", "list + join", join_pts + [(n, join_final)], 1),
        ],
        markers=[(n, concat_final, "+=", "m"), (n, join_final, "join", "d")],
    ),
)

rec.output(f"{concat_final} {join_final}\n")
