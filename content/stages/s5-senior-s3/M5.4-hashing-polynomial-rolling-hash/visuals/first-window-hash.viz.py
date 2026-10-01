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


def text_frame(i):
    states = []
    for j in range(text_len):
        if j < pattern_len:
            states.append("done" if j < i else ("current" if j == i else "none"))
        else:
            states.append("none")
    return vz.array(list(text), states=states, name="text")


def hash_frame(h):
    return vz.array([h], name="window_hash")


window_hash = 0
for i in range(pattern_len):
    c = text[i]
    prev = window_hash
    window_hash = (window_hash * base + ord(c)) % mod
    rec.step(
        f"window_hash = {prev} * {base} + ord('{c}') ({ord(c)}) = {window_hash}.",
        text=text_frame(i),
        hash=hash_frame(window_hash),
    )

verdict = "matches pattern_hash" if window_hash == pattern_hash else "does not match pattern_hash"
rec.step(
    f"The first window's hash is {window_hash}, pattern_hash is {pattern_hash}: the window {verdict}.",
    text=text_frame(pattern_len),
    hash=hash_frame(window_hash),
)

# Silently finish the same search substring_hash.py performs, for the consistency check.
matches = []
if window_hash == pattern_hash:
    matches.append(0)
for i in range(1, text_len - pattern_len + 1):
    left_val = ord(text[i - 1]) * powers[pattern_len - 1]
    window_hash = (window_hash - left_val) % mod
    window_hash = (window_hash * base + ord(text[i + pattern_len - 1])) % mod
    if window_hash == pattern_hash:
        matches.append(i)

rec.output("\n".join(str(p) for p in matches) + "\n" if matches else "")
