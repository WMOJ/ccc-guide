import sys


def update(tree, i, delta):
    n = len(tree) - 1
    while i <= n:
        tree[i] += delta
        i += i & -i


def query(tree, i):
    total = 0
    while i > 0:
        total += tree[i]
        i -= i & -i
    return total


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        update(tree, i, int(data[i]))

    q = int(data[n + 1])
    pos = n + 2
    answers = []
    for _ in range(q):
        kind = data[pos]
        a = int(data[pos + 1])
        b = int(data[pos + 2])
        pos += 3
        if kind == "U":
            update(tree, a, b)
        else:
            answers.append(query(tree, b) - query(tree, a - 1))

    print("\n".join(map(str, answers)))


if __name__ == "__main__":
    main()
