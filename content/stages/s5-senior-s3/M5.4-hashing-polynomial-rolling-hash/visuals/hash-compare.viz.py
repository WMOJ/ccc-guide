import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
text = data[0]
i = int(data[1])
j = int(data[2])
length = int(data[3])

base = 31
mod = (1 << 61) - 1
n = len(text)

powers = [1] * (n + 1)
for k in range(1, n + 1):
    powers[k] = (powers[k - 1] * base) % mod

prefix_hash = [0] * (n + 1)
for k in range(n):
    prefix_hash[k + 1] = (prefix_hash[k] * base + ord(text[k])) % mod


def window_hash(start, length):
    end = start + length
    return (prefix_hash[end] - prefix_hash[start] * powers[length]) % mod


def text_frame(active):
    states = []
    for k in range(n):
        if i <= k < i + length and j <= k < j + length:
            states.append("compare")
        elif i <= k < i + length:
            states.append("current" if "a" in active else "done")
        elif j <= k < j + length:
            states.append("current" if "b" in active else "done")
        else:
            states.append("none")
    return vz.array(
        list(text),
        states=states,
        ranges=[(i, i + length - 1, "hash_a"), (j, j + length - 1, "hash_b")],
        name="text",
    )


hash_a = window_hash(i, length)
rec.step(
    f"hash_a = window_hash({i}, {length}) reads prefix_hash directly: prefix_hash[{i + length}] - "
    f"prefix_hash[{i}] * powers[{length}] = {hash_a}. No character of this window is rebuilt.",
    text=text_frame({"a"}),
    hash=vz.array([hash_a, None], name="hashes"),
)

hash_b = window_hash(j, length)
rec.step(
    f"hash_b = window_hash({j}, {length}) the same way: {hash_b}.",
    text=text_frame({"b"}),
    hash=vz.array([hash_a, hash_b], name="hashes"),
)

if hash_a != hash_b:
    verdict = "differ"
    text_a = text[i : i + length]
    text_b = text[j : j + length]
    caption = (
        f"hash_a and hash_b differ, so the windows cannot be equal: \"{text_a}\" and \"{text_b}\" "
        "are reported different without comparing a single character."
    )
    output = "different\n"
else:
    verdict = "match"
    text_a = text[i : i + length]
    text_b = text[j : j + length]
    if text_a == text_b:
        caption = (
            f"hash_a and hash_b agree at {hash_a}. Checking the characters confirms it: "
            f"\"{text_a}\" equals \"{text_b}\", reported equal."
        )
        output = "equal\n"
    else:
        caption = (
            f"hash_a and hash_b agree at {hash_a}, but the characters differ: a rare collision, "
            "caught by the direct check and reported as one."
        )
        output = "collision\n"

rec.step(caption, text=text_frame({"a", "b"}), hash=vz.array([hash_a, hash_b], compare=(0, 1, verdict), name="hashes"))

rec.output(output)
