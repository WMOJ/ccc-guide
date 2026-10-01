import vizrec as vz

rec = vz.Recorder()
word = rec.readline()

freq = [0] * 26

VISIBLE = 8  # slots a-h; every preset word only touches letters inside this range


def word_frame(i):
    states = ["done" if j < i else "none" for j in range(len(word))]
    if i < len(word):
        states[i] = "current"
    return vz.array(list(word), states=states, pointers={"i": i} if i < len(word) else None)


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
    if "a" <= char <= "z":
        index = ord(char) - ord("a")
        freq[index] += 1
        rec.step(
            f"Character '{char}' at position {i} maps to slot {index}. "
            f"freq[{index}] becomes {freq[index]}.",
            word=word_frame(i),
            freq=freq_frame(index),
        )
    else:
        rec.step(
            f"Character '{char}' at position {i} is outside a-z, so the filter skips it. "
            "No slot changes.",
            word=word_frame(i),
            freq=freq_frame(),
        )

rec.step(
    "After the last character, the non-zero slots hold the final letter counts. "
    "The second loop now reads them back in order, slot 0 to slot 25.",
    word=word_frame(len(word)),
    freq=freq_frame(),
)

for i in range(VISIBLE):
    if freq[i] > 0:
        letter = chr(ord("a") + i)
        rec.step(
            f"Slot {i} (letter '{letter}') is {freq[i]}, so the loop prints \"{letter}: {freq[i]}\".",
            word=word_frame(len(word)),
            freq=freq_frame(i),
        )

full_lines = []
for i in range(26):
    if freq[i] > 0:
        full_lines.append(f"{chr(ord('a') + i)}: {freq[i]}")
rec.output("\n".join(full_lines) + ("\n" if full_lines else ""))
