import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    rainfall = []
    for k in range(n):
        day = int(data[1 + k])
        rainfall.append(day)

    total = 0
    prefix = [0]
    for day in rainfall:
        total += day
        prefix.append(total)

    q = int(data[n + 1])
    pos = n + 2
    answers = []
    for _ in range(q):
        i = int(data[pos])
        j = int(data[pos + 1])
        pos += 2
        hi = prefix[j + 1]
        lo = prefix[i]
        answers.append(hi - lo)

    for answer in answers:
        print(answer)


if __name__ == "__main__":
    main()
