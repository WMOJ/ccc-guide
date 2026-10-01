import math

import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
n = int(tokens[0])

limit = int(math.isqrt(n))
tested = []


wall = (limit, "limit", "wall")


def frame(current=None, current_state="current"):
    points = list(tested)
    used_x = {p[0] for p in points} | ({current} if current is not None else set())
    if limit not in used_x:
        points = points + [wall]
    if current is not None:
        points = points + [(current, str(current), current_state)]
    return vz.line(0, limit + 2, points=points)


rec.step(
    f"Test divisors of {n} from 2 up to its square root, about {limit}.",
    line=frame(),
)

factor = None
d = 2
while d <= limit:
    if n % d == 0:
        factor = d
        rec.step(
            f"{d} divides {n} evenly ({n} // {d} = {n // d}), so {n} is not prime. "
            f"{d} is its smallest prime factor.",
            line=frame(current=d, current_state="compare"),
        )
        break
    rec.step(
        f"{d} does not divide {n}. Move to the next candidate.",
        line=frame(current=d, current_state="current"),
    )
    tested.append((d, str(d), "done"))
    d += 1

if factor is None:
    rec.step(
        f"No candidate up to {limit} divides {n}. Past {limit}, any factor would already "
        f"have shown up paired with one below it, so {n} is prime.",
        line=frame(),
    )

factor_value = factor if factor is not None else n
is_prime = n >= 2 and factor_value == n
rec.output(f"{factor_value}\n{is_prime}\n")
