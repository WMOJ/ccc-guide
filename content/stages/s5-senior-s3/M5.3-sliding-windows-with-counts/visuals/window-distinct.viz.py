import vizrec as vz

rec = vz.Recorder()
lines = rec.stdin.split("\n")
text = lines[0]
k = int(lines[1])

letters = sorted(set(text))
counts = {c: 0 for c in letters}
left = 0
distinct = 0
best = 0
best_range = (0, -1)


def text_frame(right, is_best=False):
    states = ["none"] * len(text)
    for idx in range(len(text)):
        if idx < left:
            states[idx] = "done"
        elif left <= idx <= right:
            states[idx] = "current"
    if is_best:
        for idx in range(best_range[0], best_range[1] + 1):
            if states[idx] != "current":
                states[idx] = "path"
    pointers = []
    if right >= 0:
        pointers.append(("right", right))
    pointers.append(("left", left))
    return vz.array(list(text), states=states, pointers=pointers)


def counts_table():
    return vz.table(
        [[counts[c] for c in letters]],
        row_heads=["count"],
        col_heads=list(letters),
    )


rec.step(
    f"The window starts empty at the left end. K is {k} distinct letters.",
    text=text_frame(-1),
    counts=counts_table(),
)

for right in range(len(text)):
    char = text[right]
    if counts[char] == 0:
        distinct += 1
    counts[char] += 1

    start_left = left
    over_by = distinct - k if distinct > k else 0
    while distinct > k:
        left_char = text[left]
        counts[left_char] -= 1
        if counts[left_char] == 0:
            distinct -= 1
        left += 1

    if left > start_left:
        dropped = text[start_left:left]
        shrink_caption = (
            f" That pushes distinct letters {over_by} over K, so the left pointer drops "
            f"\"{dropped}\" and moves to index {left}."
        )
    else:
        shrink_caption = ""

    window_len = right - left + 1
    if window_len > best:
        best = window_len
        best_range = (left, right)

    letter_word = "letter" if distinct == 1 else "letters"
    rec.step(
        f"Add text[{right}] = '{char}': its count becomes {counts[char]}, {distinct} distinct "
        f"{letter_word} in the window." + shrink_caption + f" Longest so far: {best}.",
        text=text_frame(right, is_best=(window_len == best)),
        counts=counts_table(),
    )

rec.step(
    f"The scan reaches the end. The longest window with at most {k} distinct letters is "
    f"\"{text[best_range[0]:best_range[1] + 1]}\", length {best}.",
    text=text_frame(len(text) - 1, is_best=True),
    counts=counts_table(),
)

rec.output(f"{best}\n")
