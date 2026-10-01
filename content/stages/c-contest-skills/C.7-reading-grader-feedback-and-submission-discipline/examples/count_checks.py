import sys


def slow_checks(values):
    checks = 0
    for i in range(len(values)):
        for j in range(i):
            checks += 1
            if values[j] == values[i]:
                return checks
    return checks


def fast_checks(values):
    seen = set()
    checks = 0
    for v in values:
        checks += 1
        if v in seen:
            return checks
        seen.add(v)
    return checks


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    mode = tokens[0]
    for token in tokens[1:]:
        n = int(token)
        values = list(range(n))
        if mode == "front":
            values[1] = values[0]
        print(n, slow_checks(values), fast_checks(values))


if __name__ == "__main__":
    main()
