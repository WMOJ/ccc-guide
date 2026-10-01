import vizrec as vz

rec = vz.Recorder()
word_a = rec.readline().strip()
word_b = rec.readline().strip()

letters = sorted(set(word_a) | set(word_b))
counts_a = {letter: 0 for letter in letters}
counts_b = {letter: 0 for letter in letters}


def frame(row=None, letter=None, final=None):
    cells = [[counts_a[c] for c in letters], [counts_b[c] for c in letters]]
    states = {}
    if row is not None:
        states[(row, letters.index(letter))] = "current"
    if final is not None:
        for k, c in enumerate(letters):
            for r in (0, 1):
                states[(r, k)] = final[c]
    return vz.table(
        cells,
        states=states,
        row_heads=["counts_a", "counts_b"],
        col_heads=letters,
        col_title="letter",
    )


rec.step(
    f'Both count rows start at 0 for every letter that appears in either word: '
    f"{', '.join(letters)}.",
    counts=frame(),
)

for char in word_a:
    counts_a[char] += 1
    rec.step(
        f'Reading "{char}" from "{word_a}": counts_a for {char} becomes {counts_a[char]}.',
        counts=frame(0, char),
    )

for char in word_b:
    counts_b[char] += 1
    rec.step(
        f'Reading "{char}" from "{word_b}": counts_b for {char} becomes {counts_b[char]}.',
        counts=frame(1, char),
    )

final = {}
for c in letters:
    final[c] = "done" if counts_a[c] == counts_b[c] else "compare"
mismatch = [c for c in letters if counts_a[c] != counts_b[c]]
if mismatch:
    shown = ", ".join(f"{c} ({counts_a[c]} against {counts_b[c]})" for c in mismatch)
    caption = f"Comparing column by column: the counts differ at {shown}. Not an anagram."
    result = "Not anagram"
else:
    caption = "Comparing column by column: every count matches, so the words are anagrams."
    result = "Anagram"
rec.step(caption, counts=frame(final=final))

rec.output(result + "\n")
