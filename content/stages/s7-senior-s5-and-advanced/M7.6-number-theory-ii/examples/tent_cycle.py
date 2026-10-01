import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    n = int(tokens[0])
    start = int(tokens[1])
    steps = int(tokens[2])
    seen = {start: 0}
    order = [start]
    state = start
    while True:
        state = 2 * min(state, n - state)
        if state in seen:
            break
        seen[state] = len(order)
        order.append(state)
    first = seen[state]
    length = len(order) - first
    print(order)
    print(f"cycle starts at step {first}, length {length}")
    if steps < len(order):
        answer = order[steps]
    else:
        answer = order[first + (steps - first) % length]
    print(f"numerator after {steps} steps: {answer}")


if __name__ == "__main__":
    main()
