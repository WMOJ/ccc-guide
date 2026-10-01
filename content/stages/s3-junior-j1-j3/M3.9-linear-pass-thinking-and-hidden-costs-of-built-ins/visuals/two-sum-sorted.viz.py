import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
target = int(tokens[0])
numbers = [int(x) for x in tokens[1:]]


def frame(left, right, final_states=None):
    n = len(numbers)
    if final_states is not None:
        states = final_states
    else:
        states = ["none"] * n
        for j in range(n):
            if j < left or j > right:
                states[j] = "done"
        if 0 <= left < n:
            states[left] = "current"
        if 0 <= right < n:
            states[right] = "current"
    pointers = []
    if 0 <= left < n:
        pointers.append(("left", left))
    if 0 <= right < n:
        pointers.append(("right", right))
    return vz.array(numbers, states=states, pointers=pointers)


left = 0
right = len(numbers) - 1
result = "none"

rec.step(
    f"left starts at position 0 ({numbers[left]}), right starts at the last position "
    f"({numbers[right]}). Target is {target}.",
    numbers=frame(left, right),
)

while left < right:
    total = numbers[left] + numbers[right]
    if total == target:
        result = f"{numbers[left]} {numbers[right]}"
        states = ["done"] * len(numbers)
        states[left] = "path"
        states[right] = "path"
        rec.step(
            f"{numbers[left]} + {numbers[right]} = {total}, exactly the target. Pointers stop here.",
            numbers=frame(left, right, final_states=states),
        )
        break
    if total < target:
        left += 1
        rec.step(
            f"{numbers[left - 1]} + {numbers[right]} = {total}, too small. left moves right, to "
            f"position {left}.",
            numbers=frame(left, right),
        )
    else:
        right -= 1
        rec.step(
            f"{numbers[left]} + {numbers[right + 1]} = {total}, too big. right moves left, to "
            f"position {right}.",
            numbers=frame(left, right),
        )
else:
    rec.step(
        "left and right met without a match, so no pair in this list sums to the target.",
        numbers=frame(left, right),
    )

rec.output(result + "\n")
