import vizrec as vz


def slice_step(word, a, b, label):
    n = len(word)
    lo = max(0, min(a, n))
    hi = max(0, min(b, n))
    states = ["current" if lo <= i < hi else "none" for i in range(n)]
    ranges = [(lo, hi - 1, label)] if lo < hi else None
    result = word[a:b]
    frame = vz.array(list(word), states=states, ranges=ranges, indices=True)
    return frame, result


rec = vz.Recorder()
word = rec.readline()

rec.step(f'Start with the word "{word}".', w=vz.array(list(word), indices=True))

frame, first = slice_step(word, 1, 4, "word[1:4]")
caption = f'`word[1:4]` is "{first}": everything from index 1 up to, but not including, index 4.'
if not first:
    caption = '`word[1:4]` is "": nothing is left starting from index 1, so the slice is empty.'
rec.step(caption, w=frame)

frame, second = slice_step(word, 0, 3, "word[:3]")
caption = f'`word[:3]` is "{second}": leaving out the start begins from index 0.'
if not second:
    caption = '`word[:3]` is "": the word runs out before index 3 is reached.'
rec.step(caption, w=frame)

frame, third = slice_step(word, 3, len(word), "word[3:]")
caption = f'`word[3:]` is "{third}": leaving out the stop runs to the end of the word.'
if not third:
    caption = '`word[3:]` is "": index 3 is already at or past the last character.'
rec.step(caption, w=frame)

rec.output(f"{first}\n{second}\n{third}\n")
