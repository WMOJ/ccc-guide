import vizrec as vz

rec = vz.Recorder()
tokens = rec.readline().split()
text = tokens[0]
k = int(tokens[1])

n = len(text)
num_windows = n - k + 1

brute_pts = []
slide_pts = []
brute_ops = 0
slide_ops = 0


def frame():
    y_max = max(brute_ops, slide_ops, 1)
    return vz.plot(
        x=(0, max(num_windows - 1, 1), "window"),
        y=(0, y_max, "operations so far"),
        series=[
            ("brute", "recompute", list(brute_pts), 0),
            ("slide", "slide", list(slide_pts), 1),
        ],
    )


for i in range(num_windows):
    if i == 0:
        brute_ops += k
        slide_ops += k
        caption = (
            f"Window 0 has to be built from scratch either way: {k} characters checked, "
            f"{k} operations for both."
        )
    else:
        brute_ops += k
        slide_ops += 2
        caption = (
            f"Window {i}: recomputing from scratch checks all {k} characters again "
            f"({brute_ops} total). Sliding only checks the one character leaving and the one "
            f"arriving, 2 operations ({slide_ops} total)."
        )
    brute_pts.append((i, brute_ops))
    slide_pts.append((i, slide_ops))
    rec.step(caption, plot=frame())

rec.output(f"{brute_ops} {slide_ops}\n")
