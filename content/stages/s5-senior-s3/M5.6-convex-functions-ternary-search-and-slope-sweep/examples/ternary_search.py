def cost(c, targets):
    """Total distance from location c to all targets."""
    return sum(abs(x - c) for x in targets)


def ternary_search(targets, lo, hi):
    """Find the location that minimizes cost using ternary search."""
    epsilon = 1e-6
    while hi - lo > epsilon:
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if cost(m1, targets) > cost(m2, targets):
            lo = m1
        else:
            hi = m2
    return (lo + hi) / 2


targets = [10, 40, 50, 100]
best_loc = ternary_search(targets, 0, 1000)
best_cost = cost(best_loc, targets)

print(f"Best location: {best_loc:.2f}")
print(f"Minimum cost: {best_cost:.2f}")
