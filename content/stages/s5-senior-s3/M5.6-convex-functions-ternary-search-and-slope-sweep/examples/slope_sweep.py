def slope_sweep(positions, weights):
    """Find location c that minimizes sum of |c - p_i| * w_i."""
    n = len(positions)
    total_weight = sum(weights)
    events = sorted(zip(positions, weights))

    # At c = -infinity, all terms contribute negatively
    slope = -total_weight
    left_weight = 0
    best_cost = float('inf')
    best_loc = events[0][0]

    # Cost at the first position
    current_loc = events[0][0]
    current_cost = sum(abs(current_loc - p) * w for p, w in zip(positions, weights))

    for pos, w in events:
        # Move from current_loc to pos
        if pos > current_loc:
            current_cost += slope * (pos - current_loc)
            current_loc = pos

        if current_cost < best_cost:
            best_cost = current_cost
            best_loc = current_loc

        # At this breakpoint, slope changes
        left_weight += w
        right_weight = total_weight - left_weight
        slope = left_weight - right_weight

    return best_loc, best_cost


positions = [10, 40, 50, 100]
weights = [1, 2, 1, 3]
best_loc, best_cost = slope_sweep(positions, weights)

print(f"Best location: {best_loc}")
print(f"Minimum cost: {best_cost}")
