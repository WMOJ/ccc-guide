import vizrec as vz

rec = vz.Recorder()
s = list(rec.readline())
pairs = {"(": ")", "[": "]", "{": "}"}
original = "".join(s)

looked = 0
passes = 0
rec.step(
    f"The brute force deletes adjacent pairs until none is left. Start with {original}, "
    f"{len(s)} characters. Each pass scans from the left for an opener directly followed "
    "by its closer.",
    chars=vz.array(s, indices=True),
)
while True:
    found = -1
    for i in range(len(s) - 1):
        if s[i] in pairs and pairs[s[i]] == s[i + 1]:
            found = i
            break
    passes += 1
    if found < 0:
        looked += len(s)
        rec.step(
            f"Pass {passes}: scanning all {len(s)} characters finds no adjacent pair, so nothing "
            f"more can be deleted. {''.join(s)} is left, which is not empty: invalid. "
            f"Total look-ups: {looked}.",
            chars=vz.array(s, states=["invalid"] * len(s), indices=True),
        )
        ok = False
        break
    looked += found + 2
    states = ["none"] * len(s)
    states[found] = "compare"
    states[found + 1] = "compare"
    if len(s) == 2:
        rec.step(
            f"Pass {passes}: the pair at positions {found} and {found + 1} is found after "
            f"{found + 2} look-ups. Deleting it leaves nothing, so the string is valid. "
            f"Total look-ups: {looked}.",
            chars=vz.array(s, states=["done"] * 2, indices=True),
        )
        ok = True
        break
    rec.step(
        f"Pass {passes}: the scan reaches the pair at positions {found} and {found + 1} after "
        f"{found + 2} look-ups. Delete it. Total look-ups: {looked}.",
        chars=vz.array(s, states=states, indices=True),
    )
    del s[found:found + 2]

rec.output(f"{ok}\n")
