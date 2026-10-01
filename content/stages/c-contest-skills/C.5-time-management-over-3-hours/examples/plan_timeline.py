import sys


def run_plan(costs, blocks):
    worked = [0] * len(costs)
    cleared = [0] * len(costs)
    for problem, minutes in blocks:
        if problem == 0:
            continue
        p = problem - 1
        worked[p] += minutes
        while cleared[p] < len(costs[p]):
            need = costs[p][cleared[p]]
            if need is None or need > worked[p]:
                break
            cleared[p] += 1
    return cleared


def main() -> None:
    tokens = sys.stdin.read().split()
    pos = 0
    n = int(tokens[pos])
    pos += 1
    costs = []
    for _ in range(n):
        k = int(tokens[pos])
        pos += 1
        row = []
        for _ in range(k):
            word = tokens[pos]
            pos += 1
            row.append(None if word == "-" else int(word))
        costs.append(row)
    plans = int(tokens[pos])
    pos += 1
    lines = []
    for index in range(plans):
        b = int(tokens[pos])
        pos += 1
        blocks = []
        for _ in range(b):
            problem = int(tokens[pos])
            pos += 1
            minutes = int(tokens[pos])
            pos += 1
            blocks.append((problem, minutes))
        cleared = run_plan(costs, blocks)
        name = "AB"[index]
        by_problem = " ".join(str(c) for c in cleared)
        lines.append(f"plan {name}: {sum(cleared)} subtasks cleared, by problem {by_problem}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
