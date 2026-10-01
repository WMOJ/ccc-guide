import vizrec as vz

rec = vz.Recorder()
month = int(rec.readline())

days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WINDOW = 6


def window(k):
    """The last up to WINDOW months checked so far, ending at k (a phone-width slice)."""
    lo = max(1, k - WINDOW + 1)
    return lo, k


def ladder_frame(k, matched):
    lo, hi = window(k)
    months = list(range(lo, hi + 1))
    states = []
    for m in months:
        if m < k:
            states.append("done")
        else:
            states.append("compare" if matched else "current")
    return vz.array(months, states=states, index_base=lo)


def table_frame(k, reveal=None):
    lo, hi = window(k)
    days = days_in_month[lo:hi + 1]
    states = ["none"] * len(days)
    if reveal is not None and lo <= reveal <= hi:
        states[reveal - lo] = "current"
    return vz.array(days, states=states, index_base=lo)


for k in range(1, 13):
    matched = k == month
    if matched:
        caption = (
            f"elif month == {k} is true: the chain took {k} comparison"
            f"{'s' if k != 1 else ''} to get here. The table needed one index, "
            f"days_in_month[{k}], to reach the same answer."
        )
    else:
        caption = f"elif month == {k} is false, so the chain moves to the next elif."
    rec.step(
        caption,
        ladder=ladder_frame(k, matched),
        table=table_frame(k, month if matched else None),
    )
    if matched:
        break

rec.output(f"{days_in_month[month]}\n")
