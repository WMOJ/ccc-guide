import vizrec as vz

rec = vz.Recorder()
lines = rec.stdin.split("\n")
text = lines[0]
pattern = lines[1]

k = len(pattern)
letters = sorted(set(text) | set(pattern))

target_count = {c: 0 for c in letters}
for char in pattern:
    target_count[char] += 1

window_count = {c: 0 for c in letters}
matches = sum(1 for c in letters if target_count[c] == 0)


def text_frame(right, left, match_start=None):
    states = ["none"] * len(text)
    for idx in range(len(text)):
        if left <= idx <= right:
            states[idx] = "current"
        elif idx < left:
            states[idx] = "done"
    if match_start is not None:
        for idx in range(match_start, match_start + k):
            states[idx] = "path"
    pointers = []
    if right >= 0:
        pointers.append(("right", right))
    if right >= k - 1:
        pointers.append(("left", left))
    return vz.array(list(text), states=states, pointers=pointers)


def counts_table():
    return vz.table(
        [[window_count[c] for c in letters], [target_count[c] for c in letters]],
        row_heads=["window", "target"],
        col_heads=list(letters),
    )


rec.step(
    f"The window is empty. matches starts at {matches}: that many of the {len(letters)} letters "
    "already have the count the target wants (0 for every letter not in the pattern).",
    text=text_frame(-1, 0),
    counts=counts_table(),
)

for right in range(len(text)):
    char = text[right]
    if window_count[char] == target_count[char]:
        matches -= 1
    window_count[char] += 1
    if window_count[char] == target_count[char]:
        matches += 1
    add_caption = f"Add text[{right}] = '{char}': window count for '{char}' becomes {window_count[char]}."

    remove_caption = ""
    if right >= k:
        left_char = text[right - k]
        if window_count[left_char] == target_count[left_char]:
            matches -= 1
        window_count[left_char] -= 1
        if window_count[left_char] == target_count[left_char]:
            matches += 1
        remove_caption = (
            f" Drop text[{right - k}] = '{left_char}', now that the window has grown past K = {k}: "
            f"its window count becomes {window_count[left_char]}."
        )

    left = max(0, right - k + 1)
    is_match = right >= k - 1 and matches == len(letters)
    match_caption = (
        f" matches reaches {matches}, all {len(letters)} letters: a permutation of \"{pattern}\" starts at {left}."
        if is_match
        else f" matches is {matches} of {len(letters)}."
    )

    rec.step(
        add_caption + remove_caption + match_caption,
        text=text_frame(right, left, match_start=left if is_match else None),
        counts=counts_table(),
    )

rec.step(
    "The scan reaches the end of the text. Every match found is highlighted above where it was "
    "spotted.",
    text=text_frame(len(text) - 1, max(0, len(text) - k)),
    counts=counts_table(),
)

starts = []
window_count2 = {c: 0 for c in letters}
target_count2 = dict(target_count)
matches2 = sum(1 for c in letters if target_count2[c] == 0)
for right in range(len(text)):
    char = text[right]
    if window_count2[char] == target_count2[char]:
        matches2 -= 1
    window_count2[char] += 1
    if window_count2[char] == target_count2[char]:
        matches2 += 1
    if right >= k:
        left_char = text[right - k]
        if window_count2[left_char] == target_count2[left_char]:
            matches2 -= 1
        window_count2[left_char] -= 1
        if window_count2[left_char] == target_count2[left_char]:
            matches2 += 1
    if right >= k - 1 and matches2 == len(letters):
        starts.append(right - k + 1)

rec.output((" ".join(str(s) for s in starts) if starts else "none") + "\n")
