import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
arr = list(map(int, data[1:n + 1]))


def arr_frame(states=None, pointers=None):
    return vz.array(arr, states=states, pointers=pointers)


rec.step(
    "This is the original array. Read it once, front to back, to build its difference array.",
    arr=arr_frame(),
    diff=vz.array([None] * n),
)

diff = [0] * n
diff[0] = arr[0]
rec.step(
    f"diff[0] copies arr[0] directly: {diff[0]}. There is no earlier entry to subtract.",
    arr=arr_frame(pointers=[("i", 0, "above", True)]),
    diff=vz.array([diff[0]] + [None] * (n - 1), states="c" + "_" * (n - 1)),
)

for i in range(1, n):
    diff[i] = arr[i] - arr[i - 1]
    shown = diff[: i + 1] + [None] * (n - i - 1)
    states = "d" * i + "c" + "_" * (n - i - 1)
    rec.step(
        f"diff[{i}] = arr[{i}] - arr[{i - 1}] = {arr[i]} - {arr[i - 1]} = {diff[i]}.",
        arr=arr_frame(pointers=[("i", i, "above", True)]),
        diff=vz.array(shown, states=states),
    )

rec.step(
    "That is the difference array. Now prefix-sum it, left to right, to rebuild the original.",
    arr=vz.array([None] * n),
    diff=vz.array(diff),
)

rebuilt = [0] * n
rebuilt[0] = diff[0]
rec.step(
    f"rebuilt[0] is just diff[0]: {rebuilt[0]}.",
    arr=vz.array([rebuilt[0]] + [None] * (n - 1), states="c" + "_" * (n - 1)),
    diff=vz.array(diff, pointers=[("i", 0, "above", True)]),
)

for i in range(1, n):
    rebuilt[i] = rebuilt[i - 1] + diff[i]
    shown = rebuilt[: i + 1] + [None] * (n - i - 1)
    states = "d" * i + "c" + "_" * (n - i - 1)
    rec.step(
        f"rebuilt[{i}] = rebuilt[{i - 1}] + diff[{i}] = {rebuilt[i - 1]} + {diff[i]} = "
        f"{rebuilt[i]}.",
        arr=vz.array(shown, states=states),
        diff=vz.array(diff, pointers=[("i", i, "above", True)]),
    )

rec.step(
    f"The rebuilt array, {rebuilt}, matches the original exactly. diff and arr hold the same "
    "information in two different forms; a prefix sum turns one into the other.",
    arr=vz.array(rebuilt),
    diff=vz.array(diff),
)

rec.output(" ".join(map(str, diff)) + "\n" + " ".join(map(str, rebuilt)) + "\n")
