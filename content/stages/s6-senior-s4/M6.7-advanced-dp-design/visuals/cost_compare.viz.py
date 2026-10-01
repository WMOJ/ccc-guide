from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, k = (int(x) for x in rec.readline().split())
scores = [int(x) for x in rec.readline().split()]

dp = [0] * n
dp[0] = scores[0]
dq = deque([0])
reads_col = [""] * n
steps_col = [""] * n
run_reads = [""] * n
run_steps = [""] * n
total_reads = 0
total_steps = 0


def table(current=None):
    cells = [[reads_col[i], steps_col[i], run_reads[i], run_steps[i]] for i in range(n)]
    states = ["____"] * n
    if current is not None:
        states[current] = "cccc"
    return vz.table(
        cells,
        states=states,
        row_heads=[str(i) for i in range(n)],
        col_heads=["scan", "deque", "Σscan", "Σdeque"],
        row_title="stone",
    )


def record(i, reads, steps, text):
    global total_reads, total_steps
    total_reads += reads
    total_steps += steps
    reads_col[i] = reads
    steps_col[i] = steps
    run_reads[i] = total_reads
    run_steps[i] = total_steps
    rec.step(text, t=table(i))


record(0, 0, 1, f"Stone 0 has no earlier stone to read, and the deque takes one append. "
       f"Each row counts what stone `i` costs: `scan` is the stones a plain scan would read "
       f"(up to {k}), `deque` is the appends and pops the deque does. The last two columns are running totals.")

for i in range(1, n):
    steps = 0
    while dq[0] < i - k:
        dq.popleft()
        steps += 1
    dp[i] = scores[i] + dp[dq[0]]
    while dq and dp[dq[-1]] <= dp[i]:
        dq.pop()
        steps += 1
    dq.append(i)
    steps += 1
    reads = min(i, k)
    word = "stone" if reads == 1 else "stones"
    record(i, reads, steps,
           f"Stone {i}: a scan reads {reads} earlier {word}. The deque does {steps} "
           f"{'step' if steps == 1 else 'steps'} (pops from the front or back, plus one append). "
           f"Totals so far: {total_reads + reads} reads, {total_steps + steps} deque steps.")

rec.step(
    f"Finished: the scan read {total_reads} stones and the deque did {total_steps} steps. The "
    f"deque can never exceed 2 x {n} = {2 * n}, since each stone is appended once and removed at "
    "most once. A scan pays up to the window size per stone, so the gap opens as the window grows.",
    t=table(),
)
rec.output(f"{dp[n - 1]}\n")
