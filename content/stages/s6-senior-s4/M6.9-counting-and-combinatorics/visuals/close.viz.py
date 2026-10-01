import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
limit = int(data[1])
heights = sorted(map(int, data[2:2 + n]))


def frame(left, right):
    states = []
    for j in range(n):
        if j < left:
            states.append("done")
        elif j == right:
            states.append("current")
        elif left <= j < right:
            states.append("frontier")
        else:
            states.append("none")
    if left == right:
        pointers = [("left, right", left)]
    else:
        pointers = [("left", left), ("right", right)]
    ranges = [(left, right - 1, "partners")] if right > left else None
    return vz.array(heights, states=states, pointers=pointers, ranges=ranges, indices=True)


rec.step(
    f"The heights sorted: {' '.join(map(str, heights))}. Both pointers start at index 0 and "
    f"`count` is 0. The limit is {limit}.",
    a=frame(0, 0),
)
count = 0
left = 0
for right in range(n):
    while heights[right] - heights[left] > limit:
        gap = heights[right] - heights[left]
        rec.step(
            f"right = {right}: {heights[right]} - {heights[left]} = {gap} is over {limit}, so "
            f"index {left} is too far from this height and from every later one. `left` moves "
            f"to {left + 1}.",
            a=frame(left, right),
        )
        left += 1
    count += right - left
    gap = heights[right] - heights[left]
    partners = right - left
    if partners == 0:
        detail = f"Nothing before right is close enough, so `count` stays {count}."
    else:
        detail = (
            f"{partners} {'height' if partners == 1 else 'heights'} from left up to just before "
            f"right can pair with it, so `count` grows by {partners} to {count}."
        )
    rec.step(
        f"right = {right}: {heights[right]} - {heights[left]} = {gap}, within {limit}. {detail}",
        a=frame(left, right),
    )

rec.output(f"{count}\n")
