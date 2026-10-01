import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
text = data[0]
pattern = data[1]

base = 31
mod = (1 << 61) - 1
pattern_len = len(pattern)
text_len = len(text)

powers = [1] * (pattern_len + 1)
for i in range(1, pattern_len + 1):
    powers[i] = (powers[i - 1] * base) % mod

pattern_hash = 0
for c in pattern:
    pattern_hash = (pattern_hash * base + ord(c)) % mod


def text_frame(left):
    right = left + pattern_len - 1
    states = []
    for j in range(text_len):
        states.append("current" if left <= j <= right else "none")
    return vz.array(
        list(text),
        states=states,
        pointers=[("L", left, "above"), ("R", right, "above")],
        ranges=[(left, right, "window")],
        name="text",
    )


def hash_frame(window_hash):
    verdict = "match" if window_hash == pattern_hash else "differ"
    return vz.array(
        [pattern_hash, window_hash],
        compare=(0, 1, verdict),
    )


window_hash = 0
for c in text[:pattern_len]:
    window_hash = (window_hash * base + ord(c)) % mod

matches = [0] if window_hash == pattern_hash else []
rec.step(
    f"The first window, text[0:{pattern_len}], is built the same way pattern_hash was: window_hash = "
    f"{window_hash}.",
    text=text_frame(0),
    hash=hash_frame(window_hash),
)

for i in range(1, text_len - pattern_len + 1):
    old_hash = window_hash
    left_val = ord(text[i - 1]) * powers[pattern_len - 1]
    stripped = (old_hash - left_val) % mod
    window_hash = (stripped * base + ord(text[i + pattern_len - 1])) % mod
    if window_hash == pattern_hash:
        matches.append(i)
    rec.step(
        f"Slide right: drop '{text[i - 1]}' (worth {left_val} at the top power), multiply by "
        f"{base}, add '{text[i + pattern_len - 1]}' ({ord(text[i + pattern_len - 1])}). "
        f"old_hash {old_hash} -> new_hash {window_hash}.",
        text=text_frame(i),
        hash=hash_frame(window_hash),
    )

rec.output("\n".join(str(p) for p in matches) + "\n" if matches else "")
