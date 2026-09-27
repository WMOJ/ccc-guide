import vizrec as vz

rec = vz.Recorder()
word = rec.readline()

freq = [0] * 26


def word_frame(i):
    states = ["done" if j < i else "none" for j in range(len(word))]
    if i < len(word):
        states[i] = "current"
    return vz.array(list(word), states=states, pointers={"i": i} if i < len(word) else None)


VISIBLE = 8  # slots a-h; the preset word only ever touches letters inside this range


def freq_frame(index=None):
    shown = freq[:VISIBLE]
    states = None
    if index is not None and index < VISIBLE:
        states = ["current" if j == index else "none" for j in range(VISIBLE)]
    return vz.array(shown, states=states, index_base=0)


rec.step(
    "Before reading any character, every slot in the frequency array is 0.",
    word=word_frame(0),
    freq=freq_frame(),
)

for i, char in enumerate(word):
    index = ord(char) - ord("a")
    freq[index] += 1
    rec.step(
        f"Character '{char}' at position {i} maps to slot {index}. "
        f"freq[{index}] becomes {freq[index]}.",
        word=word_frame(i),
        freq=freq_frame(index),
    )

rec.step(
    "After the last character, the non-zero slots hold the final letter counts.",
    word=word_frame(len(word)),
    freq=freq_frame(),
)

parts = []
for i in range(26):
    if freq[i] > 0:
        parts.append(f"{chr(ord('a') + i)}: {freq[i]}\n")
rec.output("".join(parts))
