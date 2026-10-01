"""StepThrough: join_no_trailing.py, from a list of numbers to one line of text.

One ArrayViz panel that changes shape: the numbers, the strings, then the joined characters with
each separator drawn as a dot or comma. Consistency: rec.output() must equal
join_no_trailing.py's real stdout.
"""

import vizrec as vz

rec = vz.Recorder()

nums = [3, 5, 2]


def joined(sep, shown_sep):
    cells = []
    states = ""
    for i, n in enumerate(nums):
        if i:
            cells.append(shown_sep)
            states += "m"
        cells.append(str(n))
        states += "d"
    return cells, states


rec.step(
    "`nums` holds three numbers. To print them on one line you need text, and `.join()` only "
    "accepts text.",
    line=vz.array(nums, states="ccc", name="nums"),
)
rec.step(
    "`map(str, nums)` converts each number to its text form. Same digits, but each is now a string.",
    line=vz.array([str(n) for n in nums], states="ddd", name="strings"),
)
c, s = joined(" ", "·")
rec.step(
    '`" ".join(...)` puts one space (shown as a dot) between each pair. Three values have two gaps, '
    "and nothing is added before the first or after the last.",
    line=vz.array(c, states=s, name="line"),
)
rec.step(
    "`print` shows 3 5 2 and moves to the next line, with no space left at the end.",
    line=vz.array(c, states="d" * len(c), name="line"),
)
c2, s2 = joined(",", ",")
rec.step(
    'Changing the separator to `","` changes only the separator: `print` shows 3,5,2. The pattern is '
    "the same.",
    line=vz.array(c2, states=s2, name="line"),
)
c3, s3 = joined(" ", "·")
rec.step(
    'Compare a loop that calls `print(n, end=" ")` for each number. It writes a space after every '
    "value, including the last, so the line ends in a trailing space that a judge may reject.",
    line=vz.array(c3 + ["·"], states=s3 + "x", name="line"),
)

rec.output("3 5 2\n3,5,2\n")
rec.done()
