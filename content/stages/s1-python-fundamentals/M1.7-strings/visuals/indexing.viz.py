import vizrec as vz

rec = vz.Recorder()
word = rec.readline()
n = len(word)
letters = list(word)


def frame(pointer=None, at=None, states=None):
    pointers = [(pointer, at, None, True)] if pointer else None
    return vz.array(letters, states=states, pointers=pointers, indices=True)


rec.step(
    f'The word "{word}" has {n} characters. Indexing reads one of them by position, and the positions run from 0 to {n - 1}.',
    w=frame(),
)

first = word[0]
rec.step(
    f'`word[0]` is "{first}". Positions start at 0, so index 0 is the first character.',
    w=frame("[0]", 0, {0: "current"}),
)

last = word[-1]
rec.step(
    f'`word[-1]` is "{last}". A negative index counts back from the end, so -1 is always the last character, index {n - 1} here.',
    w=frame("[-1]", n - 1, {n - 1: "current"}),
)

rec.step(
    f'`word[-{n}]` is "{first}", the same character as `word[0]`. -{n} is -len(word), the furthest back an index can go.',
    w=frame(f"[-{n}]", 0, {0: "current"}),
)

rec.step(
    f"`word[10]` points past the last index, {n - 1}. No character is there, so Python raises `IndexError` instead of returning anything.",
    w=frame("[10]", n, {n - 1: "none"}),
)

rec.output(f"{first}\n{last}\n")
