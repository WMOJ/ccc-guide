"""StepThrough: dict_basics.py, one statement at a time.

Two panels: `ages`, the dict as key: value pairs, and `shown`, what the last statement printed.
Consistency: rec.output() must equal dict_basics.py's real stdout.
"""

import vizrec as vz

rec = vz.Recorder()


def ages_frame(pairs, current=None, missing=None):
    items = []
    for k, v in pairs:
        s = "c" if k == current else None
        items.append({"k": k, "v": v, "s": s})
    return vz.struct("map", items)


def result_frame(text, state=None):
    return vz.struct("map", [{"k": "output", "v": text, "s": state}])


pairs = [("Ana", 12), ("Bo", 13)]
out = ""

rec.step(
    '`ages = {"Ana": 12, "Bo": 13}` builds a dict with two keys. Each key sits next to its value.',
    ages=ages_frame(pairs),
    shown=result_frame("(nothing yet)"),
)

rec.step(
    '`print(ages["Bo"])` finds the key "Bo" and reads the value stored beside it: 13.',
    ages=ages_frame(pairs, current="Bo"),
    shown=result_frame("13", "c"),
)
out += "13\n"

pairs.append(("Cy", 11))
rec.step(
    '`ages["Cy"] = 11` stores a new pair. "Cy" was not a key yet, so the dict grows to three pairs.',
    ages=ages_frame(pairs, current="Cy"),
    shown=result_frame("(nothing new)"),
)

rec.step(
    '`print("Cy" in ages)` asks whether "Cy" is a key. It is now, so Python prints True.',
    ages=ages_frame(pairs, current="Cy"),
    shown=result_frame("True", "c"),
)
out += "True\n"

rec.step(
    '`print("Dee" in ages)` finds no key "Dee" among the three, so Python prints False. Nothing was stored.',
    ages=ages_frame(pairs),
    shown=result_frame("False", "x"),
)
out += "False\n"

rec.output(out)
rec.done()
