import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
fields = data[1:1 + n]

crop_count = {}


def fields_frame(i):
    states = []
    for j in range(n):
        if j < i:
            states.append("done")
        elif j == i:
            states.append("current")
        else:
            states.append("none")
    return vz.array(fields, states=states, pointers={"i": i} if i < n else None)


def counts_frame(highlight=None):
    crops = sorted(crop_count.keys())
    cells = [[crop_count[c] for c in crops]]
    states = None
    if highlight is not None and highlight in crops:
        idx = crops.index(highlight)
        states = [["c" if k == idx else "_" for k in range(len(crops))]]
    return vz.table(cells, states=states, row_heads=["count"], col_heads=crops, col_title="crop")


for i, crop in enumerate(fields):
    crop_count[crop] = crop_count.get(crop, 0) + 1
    if crop_count[crop] == 1:
        caption = f'crop_count["{crop}"] becomes 1, the first time "{crop}" appears.'
    else:
        caption = f'crop_count["{crop}"] becomes {crop_count[crop]}. "{crop}" has appeared before.'
    rec.step(caption, fields=fields_frame(i), counts=counts_frame(highlight=crop))

result = sum(1 for c in crop_count.values() if c > 1)
repeats = ", ".join(sorted(c for c in crop_count if crop_count[c] > 1))
if repeats and result == 1:
    final_caption = f"After the scan, 1 crop appears more than once, namely {repeats}."
elif repeats:
    final_caption = f"After the scan, {result} crops appear more than once, namely {repeats}."
else:
    final_caption = "After the scan, every crop appears exactly once."
rec.step(final_caption, fields=fields_frame(n), counts=counts_frame())

rec.output(f"{result}\n")
