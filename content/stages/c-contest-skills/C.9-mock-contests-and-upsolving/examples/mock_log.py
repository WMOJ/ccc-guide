import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    count = int(tokens[0])
    pos = 1
    stretches = {}
    used = 0
    last_end = 0
    for _ in range(count):
        problem = int(tokens[pos])
        pos += 1
        start = int(tokens[pos])
        pos += 1
        end = int(tokens[pos])
        pos += 1
        verdict = tokens[pos]
        pos += 1
        stretches.setdefault(problem, []).append((end, verdict))
        used += end - start
        last_end = end
    lines = []
    for problem in sorted(stretches):
        rows = stretches[problem]
        subs = sum(1 for _, v in rows if v != "N")
        accepted = [end for end, v in rows if v == "A"]
        if subs == 0:
            lines.append(f"problem {problem}: no submission")
            continue
        word = "submission" if subs == 1 else "submissions"
        if accepted:
            text = f"accepted at minute {accepted[0]}"
        else:
            text = "never accepted"
        lines.append(f"problem {problem}: {subs} {word}, {text}")
    lines.append(f"{used} of 180 minutes in stretches, last one ended at minute {last_end}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
