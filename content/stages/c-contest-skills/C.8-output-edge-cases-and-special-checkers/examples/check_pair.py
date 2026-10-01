import sys


def judge(values, k, answer):
    if len(answer) != 2:
        return "rejected: need two numbers"
    pool = list(values)
    for token in answer:
        if token not in pool:
            return "rejected: " + token + " is not available"
        pool.remove(token)
    if int(answer[0]) + int(answer[1]) != k:
        return "rejected: sum is not k"
    return "accepted"


def main() -> None:
    lines = sys.stdin.read().split("\n")
    k = int(lines[0].split()[1])
    values = lines[1].split()
    answer = lines[2].split()
    print(judge(values, k, answer))


if __name__ == "__main__":
    main()
