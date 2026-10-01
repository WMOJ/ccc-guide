import sys


def main() -> None:
    d = sys.stdin.read().split()
    v = list(map(int, d))
    g = [v[0:3], v[3:6], v[6:9]]
    t = []
    for i in range(2):
        x, y = g[i], g[i + 1]
        row = []
        for j in range(2):
            a = x[j:j + 2]
            b = y[j:j + 2]
            row += [max(a + b)]
        t += [row]
    print(max(t[0] + t[1]))


if __name__ == "__main__":
    main()
