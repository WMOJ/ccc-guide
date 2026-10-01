import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
n = int(tokens[0])
k = int(tokens[1])
arr = [int(x) for x in tokens[2 : n + 2]]


def frame(left, right, added_range=None):
    states = ["none"] * len(arr)
    for idx in range(len(arr)):
        if idx < left or idx > right:
            states[idx] = "done"
    pointers = []
    if left <= right:
        pointers.append(("left", left))
        pointers.append(("right", right))
    ranges = [added_range] if added_range else None
    return vz.array(arr, states=states, pointers=pointers, ranges=ranges)


left = 0
right = n - 1
count = 0

rec.step(
    f"left starts at index 0 ({arr[left] if n else '-'}), right starts at index {right} "
    f"({arr[right] if n else '-'}). K is {k}. count starts at 0."
    if n
    else "The array is empty, so there are no pairs to count.",
    numbers=frame(left, right),
)

while left < right:
    total = arr[left] + arr[right]
    if total <= k:
        added = right - left
        pair_word = "pair" if added == 1 else "pairs"
        rec.step(
            f"arr[{left}] + arr[{right}] = {total}, at most K. Every partner between left and right "
            f"also sums to at most K with arr[{left}], since the array is sorted: that is {added} more "
            f"{pair_word}. count becomes {count + added}. left moves right.",
            numbers=frame(left, right, added_range=(left + 1, right, f"+{added}")),
        )
        count += added
        left += 1
    else:
        rec.step(
            f"arr[{left}] + arr[{right}] = {total}, over K. arr[{right}] cannot pair with anything "
            "smaller and still fit. right moves left.",
            numbers=frame(left, right),
        )
        right -= 1

rec.step(
    f"left and right meet or cross. The final count of pairs summing to at most {k} is {count}.",
    numbers=frame(left, right),
)

rec.output(f"{count}\n")
