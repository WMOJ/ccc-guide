import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
passes = int(data[1])

players = list(range(n))
current_player = 0


def frame(holder):
    states = ["none"] * n
    states[holder] = "current"
    return vz.array(
        players,
        states=states,
        circular=True,
        pointers=[("token", holder, None, True)],
    )


seat_word = "seat" if n == 1 else "seats"
rec.step(
    f"The token starts with player 0, one of {n} {seat_word} arranged in a circle.",
    ring=frame(current_player),
)

for step_num in range(passes):
    previous = current_player
    current_player = (current_player + 1) % n
    wrapped = previous == n - 1
    if wrapped:
        caption = (
            f"Pass {step_num + 1}: player {previous} passes to (player {previous} + 1) % {n} = "
            f"0. The count reaches the last seat and wraps straight back to player 0."
        )
    else:
        caption = (
            f"Pass {step_num + 1}: player {previous} passes to (player {previous} + 1) % {n} = "
            f"{current_player}."
        )
    rec.step(caption, ring=frame(current_player))

rec.step(
    f"After {passes} passes, player {current_player} holds the token. "
    f"{passes} % {n} = {passes % n} names the same seat directly, with no loop needed.",
    ring=frame(current_player),
)

rec.output(f"{current_player}\n")
