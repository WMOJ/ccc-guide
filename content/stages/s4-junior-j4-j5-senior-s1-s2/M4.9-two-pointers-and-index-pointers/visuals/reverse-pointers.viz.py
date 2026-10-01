import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
n = int(tokens[0])
arr = [int(x) for x in tokens[1 : n + 1]]


def frame(left, right, swapped_at=None):
    states = ["none"] * len(arr)
    for idx in range(len(arr)):
        if idx < left or idx > right:
            states[idx] = "done"
    if swapped_at:
        states[swapped_at[0]] = "path"
        states[swapped_at[1]] = "path"
    pointers = []
    if left <= right:
        pointers.append(("left", left))
        pointers.append(("right", right))
    return vz.array(arr, states=states, pointers=pointers)


left = 0
right = n - 1

if left >= right:
    rec.step(
        "left and right already meet or cross, so there is nothing left to swap."
        if n > 1
        else "A single element has no partner to swap with; it is already its own reverse.",
        numbers=frame(left, right),
    )
else:
    rec.step(
        f"left starts at index 0 ({arr[left]}), right starts at index {right} ({arr[right]}).",
        numbers=frame(left, right),
    )

while left < right:
    arr[left], arr[right] = arr[right], arr[left]
    rec.step(
        f"Swap positions {left} and {right}: they now hold {arr[left]} and {arr[right]}. "
        "Both pointers step one slot inward.",
        numbers=frame(left, right, swapped_at=(left, right)),
    )
    left += 1
    right -= 1
    if left < right:
        rec.step(
            f"left is now at index {left}, right is now at index {right}.",
            numbers=frame(left, right),
        )

meet_note = "meet at the same slot" if left == right else "cross without a middle slot"
rec.step(
    f"left and right {meet_note}. The array is fully reversed: {arr}.",
    numbers=frame(left, right),
)

rec.output(" ".join(str(x) for x in arr) + "\n")
