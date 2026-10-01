import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
words = [rec.readline() for _ in range(n)]

VOWELS = "aeiouAEIOU"
rows = [[w, "?", "?"] for w in words]
state_map = {}
count = 0


def table():
    return vz.table([list(r) for r in rows], states=dict(state_map), col_heads=["word", "word[0]", "vowel?"])


rec.step(
    f"Count the words whose first letter is a vowel. The loop reads {n} words, "
    "and the test looks only at word[0].",
    table=table(),
)
for i, w in enumerate(words):
    first = w[0]
    hit = first in VOWELS
    rows[i][1] = first
    state_map[(i, 1)] = "current"
    rec.step(
        f"Word {i + 1} is {w}. Its first letter, word[0], is {first}.",
        table=table(),
    )
    rows[i][2] = "yes" if hit else "no"
    state_map[(i, 1)] = "none"
    state_map[(i, 2)] = "done" if hit else "invalid"
    if hit:
        count += 1
        rec.step(
            f"{first} is in \"aeiouAEIOU\", so vowel_count becomes {count}.",
            table=table(),
        )
    else:
        rec.step(
            f"{first} is not in \"aeiouAEIOU\", so vowel_count stays {count}.",
            table=table(),
        )
rec.step(
    f"The loop is over. vowel_count is {count}, the number printed.",
    table=table(),
)
rec.output(f"{count}\n")
