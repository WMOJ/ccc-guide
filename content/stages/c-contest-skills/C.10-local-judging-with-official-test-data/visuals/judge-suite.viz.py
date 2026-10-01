import vizrec as vz

rec = vz.Recorder()
t = int(rec.readline())
tests = []
for _ in range(t):
    data = int(rec.readline())
    want = rec.readline()
    tests.append((data, want))

rows = []
states = []
output = ""
bad = []


def frame():
    return vz.table(
        cells=[list(r) for r in rows],
        states=list(states),
        row_heads=list(range(1, len(rows) + 1)),
        col_heads=["input", "got", "want", "verdict"],
        row_title="test",
    )


for k, (data, want) in enumerate(tests, start=1):
    got = str(2 * data)
    if got == want:
        verdict = "matches"
        shown = "match"
        states.append("___d")
        caption = (
            f"Test {k}: the input is {data}, the solution prints {got}, and the official output "
            f"is {want}. The strings are equal: matches."
        )
    else:
        verdict = "differs"
        shown = "differ"
        bad.append(k)
        states.append("___x")
        caption = (
            f"Test {k}: the input is {data}, the solution prints {got}, but the official output "
            f"is {want}. The strings are not equal: differs."
        )
    rows.append((data, got, want, shown))
    output += f"{k} {verdict}\n"
    rec.step(caption, table=frame())

if bad:
    first = bad[0]
    if len(bad) == 1:
        count_text = f"One of the {t} tests differs"
    else:
        count_text = f"{len(bad)} of the {t} tests differ"
    summary = (
        f"{count_text}. The loop ran every test, so you see all failures at once. "
        f"Start with test {first}: what does the solution do on that input?"
    )
else:
    summary = f"All {t} tests match, every one checked exactly."
rec.step(summary, table=frame())
rec.output(output)
