"""StepThrough: the shared mutable default list, traced alongside mutable_default_bug.py.

Two panels: the call frame (item and basket) and the one default list, shown as index: value
pairs. Consistency: rec.output() must equal mutable_default_bug.py's real stdout.
"""

import vizrec as vz

rec = vz.Recorder()

shared = []


def frame(item, basket_text):
    return vz.struct("map", [{"k": "item", "v": item}, {"k": "basket", "v": basket_text, "s": "c"}])


def lst(highlight=None):
    items = []
    for i, v in enumerate(shared):
        items.append({"k": f"[{i}]", "v": v, "s": "c" if i == highlight else None})
    return vz.struct("map", items)


out = ""

rec.step(
    'When Python ran the `def` line, it built one empty list for `basket=[]` and kept it with the '
    'function. Now `add_item("apple")` is called without a `basket`, so `basket` is that list.',
    call=frame("apple", "default list"),
    shared=lst(),
)

shared.append("apple")
rec.step(
    '`basket.append(item)` adds "apple" to the default list itself, not to a copy.',
    call=frame("apple", "default list"),
    shared=lst(highlight=0),
)

out += repr(list(shared)) + "\n"
rec.step(
    f'`return basket` hands back the list, so `print` shows {shared!r}. The call is over, but the '
    "default list is still there, now holding one item.",
    call=frame("apple", "default list"),
    shared=lst(),
)

rec.step(
    '`add_item("pear")` also gives no `basket`, so Python again uses the same default list. It did not '
    "build a fresh one. The list already holds apple.",
    call=frame("pear", "default list"),
    shared=lst(),
)

shared.append("pear")
rec.step(
    '`basket.append(item)` adds "pear" after "apple" in that one list.',
    call=frame("pear", "default list"),
    shared=lst(highlight=1),
)

out += repr(list(shared)) + "\n"
rec.step(
    f"`print` shows {shared!r}. The second call's answer contains apple because both calls shared "
    "one list.",
    call=frame("pear", "default list"),
    shared=lst(),
)

rec.output(out)
rec.done()
