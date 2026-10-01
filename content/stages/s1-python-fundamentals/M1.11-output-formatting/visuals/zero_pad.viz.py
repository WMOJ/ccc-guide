"""StepThrough: zero_padding.py building "HH:MM" one field at a time.

One ArrayViz panel of the characters built so far; a padding zero is drawn with the compare state.
Consistency: rec.output() must equal zero_padding.py's real stdout for the same stdin.
"""

import vizrec as vz

rec = vz.Recorder()

hours, minutes = map(int, rec.readline().split())
h_text = f"{hours:02d}"
m_text = f"{minutes:02d}"


def cells(text, padded):
    """Characters of text; the leading zeros that padding added get the compare state."""
    return list(text), ["m" if i < padded else "d" for i in range(len(text))]


h_pad = len(h_text) - len(str(hours))
m_pad = len(m_text) - len(str(minutes))


def why(name, value, text, pad):
    if pad:
        return (
            f"`{name}:02d` wants at least 2 digits. `{name}` is {value}, one digit, so a 0 goes in "
            f"front: {text}. The highlighted 0 is padding, not part of the value."
        )
    return f"`{name}:02d` wants at least 2 digits. `{name}` is {value}, which already has {len(text)}, so nothing is added: {text}."


v, s = cells(h_text, h_pad)
rec.step(why("hours", hours, h_text, h_pad), text=vz.array(v, states=s))

v2, s2 = cells(m_text, m_pad)
rec.step(
    "The `:` is plain text in the f-string, copied as it is. " + why("minutes", minutes, m_text, m_pad),
    text=vz.array(v + [":"] + v2, states=s + ["d"] + s2),
)

line = f"{h_text}:{m_text}"
rec.step(
    f"`print` shows {line}. Both numbers keep the same width, so times line up whatever the values.",
    text=vz.array(list(line), states="d" * len(line)),
)

rec.output(line + "\n")
rec.done()
