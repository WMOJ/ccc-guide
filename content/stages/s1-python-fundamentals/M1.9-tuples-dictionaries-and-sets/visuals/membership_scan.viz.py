"""StepThrough: `target in nums` scanning a list, then `target in seen` on a set.

Two panels: `nums` (ArrayViz) and `seen` (StructViz set). Consistency: rec.output() must equal
membership_scan.py's real stdout for the same stdin.
"""

import vizrec as vz

rec = vz.Recorder()

nums = list(map(int, rec.readline().split()))
target = int(rec.readline())
seen_items = [{"v": v} for v in dict.fromkeys(nums)]


def set_frame(hit=False):
    items = []
    for it in seen_items:
        s = "c" if hit and it["v"] == target else None
        items.append({"v": it["v"], "s": s})
    return vz.struct("set", items)


def list_frame(upto, found_at=None):
    states = []
    for i in range(len(nums)):
        if found_at is not None and i == found_at:
            states.append("c")
        elif i <= upto:
            states.append("d")
        else:
            states.append(".")
    return vz.array(nums, states=states, pointers=[("i", upto)] if upto >= 0 else None)


rec.step(
    f"`nums` holds {len(nums)} numbers in order, and `seen = set(nums)` holds the same values. "
    f"The question is whether {target} is among them.",
    nums=vz.array(nums, states="." * len(nums)),
    seen=set_frame(),
)

found_at = None
for i, v in enumerate(nums):
    if v == target:
        found_at = i
        rec.step(
            f"`nums[{i}]` is {v}, equal to {target}. The scan stops with True after {i + 1} "
            f"{'comparison' if i == 0 else 'comparisons'}.",
            nums=list_frame(i, found_at=i),
            seen=set_frame(),
        )
        break
    rec.step(
        f"`{target} in nums` compares {target} with `nums[{i}]`, which is {v}. No match, so it moves "
        "to the next cell.",
        nums=list_frame(i),
        seen=set_frame(),
    )

if found_at is None:
    rec.step(
        f"The scan ran off the end after {len(nums)} comparisons. {target} is not in `nums`, so "
        "the answer is False.",
        nums=list_frame(len(nums) - 1),
        seen=set_frame(),
    )

hit = target in nums
if hit:
    cap = (
        f"`{target} in seen` does not scan. The set goes straight to where {target} would be "
        "stored and finds it there: True, in one step."
    )
else:
    cap = (
        f"`{target} in seen` does not scan either. The set checks where {target} would be stored, "
        "finds nothing, and answers False in one step."
    )
rec.step(
    cap,
    nums=list_frame(len(nums) - 1 if found_at is None else found_at, found_at=found_at),
    seen=set_frame(hit=hit),
)

rec.output(f"{hit}\n{hit}\n")
rec.done()
