import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
s = data[0]
n = len(s)


def expand(left, right):
    while left >= 0 and right < n and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right - 1


# First pass: find the overall best center, the way palindrome_centres.py does.
best_l, best_r = 0, -1
best_kind, best_i = "odd", 0
for i in range(n):
    left, right = expand(i, i)
    if right - left > best_r - best_l:
        best_l, best_r, best_kind, best_i = left, right, "odd", i
    if i < n - 1:
        left, right = expand(i, i + 1)
        if right - left > best_r - best_l:
            best_l, best_r, best_kind, best_i = left, right, "even", i


def text_frame(mark_l=None, mark_r=None, done_l=None, done_r=None):
    states = []
    for j in range(n):
        if done_l is not None and done_l <= j <= done_r:
            states.append("done")
        else:
            states.append("none")
    pointers = None
    compare = None
    if mark_l is not None and mark_r is not None:
        pointers = [("L", mark_l, "above"), ("R", mark_r, "above")]
        if 0 <= mark_l < n and 0 <= mark_r < n:
            compare = (mark_l, mark_r, "match" if s[mark_l] == s[mark_r] else "stop")
    return vz.array(list(s), states=states, pointers=pointers, compare=compare, name="text")


def best_frame(l, r):
    val = s[l:r + 1] if r >= l else "(none)"
    return vz.array([val], name="best")


current_l, current_r = 0, -1


def record_center(i, kind, detailed):
    global current_l, current_r
    if kind == "odd":
        left = right = i
        first_caption = f"Odd center at index {i}: '{s[i]}' matches itself, length 1."
    else:
        left, right = i, i + 1
        if s[left] != s[right]:
            if detailed:
                rec.step(
                    f"Even center between {i} and {i + 1}: '{s[left]}' and '{s[right]}' differ, "
                    f"so no even palindrome starts here.",
                    text=text_frame(left, right, current_l, current_r),
                    best=best_frame(current_l, current_r),
                )
            else:
                rec.skip(
                    f"Even center between {i} and {i + 1}: no match, skipped.",
                    1,
                    text=text_frame(None, None, current_l, current_r),
                    best=best_frame(current_l, current_r),
                )
            return
        first_caption = (
            f"Even center between {i} and {i + 1}: '{s[left]}' matches '{s[right]}', length 2."
        )

    if not detailed:
        # Silently expand to find the result, and report it as one skipped step.
        l2, r2 = expand(left, right)
        length = r2 - l2 + 1
        rec.skip(
            f"Center at {i} ({kind}): longest palindrome here is length {length}, not the best.",
            length,
            text=text_frame(None, None, current_l, current_r),
            best=best_frame(current_l, current_r),
        )
        return

    rec.step(first_caption, text=text_frame(left, right, current_l, current_r), best=best_frame(current_l, current_r))
    l, r = left, right
    while True:
        nl, nr = l - 1, r + 1
        if nl < 0 or nr >= n:
            rec.step(
                f"Expansion reaches the edge of the string at index {max(nl, -1)} or {min(nr, n)}: stop.",
                text=text_frame(nl, nr, l, r),
                best=best_frame(current_l, current_r),
            )
            break
        if s[nl] != s[nr]:
            rec.step(
                f"'{s[nl]}' at {nl} and '{s[nr]}' at {nr} differ: stop expanding.",
                text=text_frame(nl, nr, l, r),
                best=best_frame(current_l, current_r),
            )
            break
        l, r = nl, nr
        rec.step(
            f"'{s[l]}' matches '{s[r]}': the palindrome grows to '{s[l:r + 1]}', length {r - l + 1}.",
            text=text_frame(l, r, l, r),
            best=best_frame(current_l, current_r),
        )

    if r - l > current_r - current_l:
        current_l, current_r = l, r
        rec.step(
            f"New best: '{s[current_l:current_r + 1]}', length {current_r - current_l + 1}.",
            text=text_frame(None, None, current_l, current_r),
            best=best_frame(current_l, current_r),
        )


for i in range(n):
    record_center(i, "odd", i == best_i and best_kind == "odd")
    if i < n - 1:
        record_center(i, "even", i == best_i and best_kind == "even")

rec.output(
    f"Longest palindrome in '{s}': '{s[best_l:best_r + 1]}', length {best_r - best_l + 1}\n"
)
