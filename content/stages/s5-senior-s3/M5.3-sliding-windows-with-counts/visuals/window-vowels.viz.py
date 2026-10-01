import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
text = tokens[0]
k = int(tokens[1])

vowels = set("aeiou")


def frame(left, right, best_range=None):
    states = ["none"] * len(text)
    for idx in range(left, right + 1):
        states[idx] = "current" if text[idx] in vowels else "none"
        if states[idx] == "none":
            states[idx] = "done"
    if best_range:
        for idx in range(best_range[0], best_range[1] + 1):
            if text[idx] in vowels:
                states[idx] = "path"
    pointers = [("left", left), ("right", right)]
    return vz.array(list(text), states=states, pointers=pointers)


count = 0
for i in range(k):
    if text[i] in vowels:
        count += 1

best = count
best_range = (0, k - 1)

vowel_word = "vowel" if count == 1 else "vowels"
rec.step(
    f"The first window, text[0:{k}], holds {count} {vowel_word}. Best so far: {best}.",
    text=frame(0, k - 1, best_range),
)

for right in range(k, len(text)):
    left = right - k + 1
    gained = text[right] in vowels
    lost = text[right - k] in vowels
    if gained:
        count += 1
    if lost:
        count -= 1
    if count > best:
        best = count
        best_range = (left, right)

    parts = []
    if gained:
        parts.append(f"gains a vowel at text[{right}] = '{text[right]}'")
    else:
        parts.append(f"adds text[{right}] = '{text[right]}', not a vowel")
    if lost:
        parts.append(f"drops the vowel at text[{right - k}] = '{text[right - k]}'")
    else:
        parts.append(f"drops text[{right - k}] = '{text[right - k]}', not a vowel")

    rec.step(
        f"The window slides to text[{left}:{right + 1}]: it {parts[0]} and {parts[1]}. "
        f"Count is now {count}. Best so far: {best}.",
        text=frame(left, right, best_range),
    )

best_word = "vowel" if best == 1 else "vowels"
rec.step(
    f"The scan reaches the end. The best window, text[{best_range[0]}:{best_range[1] + 1}], holds "
    f"{best} {best_word}.",
    text=frame(len(text) - k, len(text) - 1, best_range),
)

rec.output(f"{best}\n")
