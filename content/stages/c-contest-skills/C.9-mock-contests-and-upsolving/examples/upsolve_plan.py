import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    count = int(tokens[0])
    pos = 1
    history = {}
    for _ in range(count):
        problem = int(tokens[pos])
        pos += 3
        verdict = tokens[pos]
        pos += 1
        history.setdefault(problem, []).append(verdict)
    lines = []
    for problem in sorted(history):
        verdicts = history[problem]
        if verdicts == ["N"]:
            step = "write a brute force for the first subtask"
        elif "A" not in verdicts:
            step = "stress test the last attempt against a brute force"
        elif verdicts[0] == "A":
            step = "nothing to upsolve"
        else:
            step = "compare the first attempt with the accepted one"
        lines.append(f"problem {problem}: {step}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
