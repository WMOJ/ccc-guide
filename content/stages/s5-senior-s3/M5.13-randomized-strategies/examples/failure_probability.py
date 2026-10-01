import sys


def main() -> None:
    data = sys.stdin.read().split()
    digits = int(data[0])
    target = 10.0 ** -digits

    lines = []
    for token in data[1:]:
        p = float(token)
        if p <= 0 or p >= 1:
            continue
        failure = 1.0
        trials = 0
        while failure >= target:
            failure *= 1 - p
            trials += 1
        lines.append(f"p = {p}: {trials} trials, failure {failure:.1e}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
