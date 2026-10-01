import vizrec as vz

rec = vz.Recorder()
letter = rec.readline()
code = ord(letter)
after = chr(code + 1)

rows = []


def frame():
    states = ["dd"] * (len(rows) - 1) + ["cc"]
    return vz.table(rows, states=states, col_heads=["call", "result"])


rows.append([f'ord("{letter}")', code])
rec.step(
    f'`code = ord(letter)` turns the letter "{letter}" into its code point, {code}.',
    t=frame(),
)

rows.append([f"chr({code})", letter])
rec.step(
    f'`chr(code)` goes the other way: code point {code} is "{letter}" again.',
    t=frame(),
)

rows.append([f"chr({code} + 1)", after])
if letter == "z":
    why = f"{code + 1} comes right after \"z\" and is not a letter, which is why a letter shift needs `%` to wrap around."
else:
    why = "adding 1 to the code point steps to the next character in the alphabet."
rec.step(
    f'`chr(code + 1)` is "{after}": {why} The program prints {code}, {letter} and {after}.',
    t=frame(),
)

rec.output(f"{code}\n{letter}\n{after}\n")
