import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
arr = [int(x) for x in rec.readline().split()]
rec.readline()  # query count, always 1 for this recording
target = int(rec.readline())


def frame(lo_l, hi_l, mid_l, lo_r, hi_r, mid_r):
    def one(lo, hi, mid):
        states = ["."] * n
        for i in range(0, lo):
            states[i] = "d"
        for i in range(hi, n):
            states[i] = "d"
        if mid is not None:
            states[mid] = "c"
        pointers = [("lo", lo, "below"), ("hi", hi, "below")]
        if mid is not None:
            pointers.append(("mid", mid, "above", True))
        return vz.array(arr, states=states, pointers=pointers)

    return {
        "l": one(lo_l, hi_l, mid_l),
        "r": one(lo_r, hi_r, mid_r),
    }


lo_l, hi_l = 0, n
lo_r, hi_r = 0, n
rounds = []
steps_l = []
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    steps_l.append((lo, hi, mid))
    if arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid
final_left = lo

steps_r = []
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    steps_r.append((lo, hi, mid))
    if arr[mid] <= target:
        lo = mid + 1
    else:
        hi = mid
final_right = lo

rec.step(
    f"Both searches start with `lo = 0` and `hi = {n}`, the whole array still a candidate. "
    f"Target is `{target}`.",
    **frame(0, n, None, 0, n, None),
)

rounds = max(len(steps_l), len(steps_r))
for i in range(rounds):
    if i < len(steps_l):
        lo_l, hi_l, mid_l = steps_l[i]
        caption_l = (
            f"left: `arr[{mid_l}]` is `{arr[mid_l]}`, "
            + (f"less than `{target}`, so `lo` moves to `{mid_l + 1}`." if arr[mid_l] < target
               else f"not less than `{target}`, so `hi` moves to `{mid_l}`.")
        )
    else:
        lo_l, hi_l, mid_l = final_left, final_left, None
        caption_l = f"left: already settled at `{final_left}`."
    if i < len(steps_r):
        lo_r, hi_r, mid_r = steps_r[i]
        caption_r = (
            f"right: `arr[{mid_r}]` is `{arr[mid_r]}`, "
            + (f"at most `{target}`, so `lo` moves to `{mid_r + 1}`." if arr[mid_r] <= target
               else f"greater than `{target}`, so `hi` moves to `{mid_r}`.")
        )
    else:
        lo_r, hi_r, mid_r = final_right, final_right, None
        caption_r = f"right: already settled at `{final_right}`."
    rec.step(f"{caption_l} {caption_r}", **frame(lo_l, hi_l, mid_l, lo_r, hi_r, mid_r))

count = final_right - final_left
occurrence_word = "occurrence" if count == 1 else "occurrences"
rec.step(
    f"`bisect_left` returns `{final_left}`, the first position `{target}` could sit at. "
    f"`bisect_right` returns `{final_right}`, the position just past it. "
    f"That is `{count}` {occurrence_word} of `{target}` in the array.",
    **frame(final_left, final_left, None, final_right, final_right, None),
)

rec.output(f"{target}: left={final_left} right={final_right} count={final_right - final_left}\n")
