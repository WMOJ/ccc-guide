import vizrec as vz


def frame(label, pos, done=False):
    state = "done" if done else None
    states = [[state, state]] if state else None
    return vz.table(
        cells=[[pos, pos % 2]],
        states=states,
        row_heads=[label],
        col_heads=["position", "mod 2"],
    )


def moves_for(difference):
    """A concrete move sequence, built from net +2 or net -2 blocks, that
    closes an even difference."""
    if difference == 0:
        return []
    if difference > 0:
        return [4, -6, 4] * (difference // 2)
    return [4, -6] * (-difference // 2)


rec = vz.Recorder()
data = rec.stdin.split()
# data[0] is the query count (always 1 for a preset); the same stdin
# format examples/token_reachability.py reads.
start = int(data[1])
target = int(data[2])

difference = target - start

rec.step(
    f"Start at {start}, target {target}. Every move is +4 or -6, both even, so the position's "
    f"parity never changes. Check target - start = {difference} first.",
    table=frame("start", start),
)

if difference % 2 != 0:
    rec.step(
        f"{difference} is odd. The position can never change parity, so the target is "
        "unreachable, no move sequence needs to be tried.",
        table=frame("start", start, done=True),
    )
    rec.output("no\n")
else:
    pos = start
    for move in moves_for(difference):
        pos += move
        rec.step(
            f"Move {'+' if move > 0 else ''}{move}: position is {pos}, still {pos % 2} mod 2, "
            "exactly as the invariant says it must be.",
            table=frame("position", pos),
        )
    rec.step(
        f"The position reached {pos}, the target, using only +4 and -6 moves.",
        table=frame("position", pos, done=True),
    )
    rec.output("yes\n")
