import math

def trials_needed(success_prob, target_failure_prob):
    """Calculate trials needed for a given failure probability."""
    if success_prob <= 0 or success_prob >= 1:
        return None
    # (1 - p)^k < target_failure_prob
    # k > log(target) / log(1 - p)
    k = math.log(target_failure_prob) / math.log(1 - success_prob)
    return int(k) + 1

print("Trials needed for different probabilities:")
for p in [0.5, 0.3, 0.1]:
    trials = trials_needed(p, 1e-6)
    print(f"p={p}: {trials} trials for failure prob < 10^-6")
