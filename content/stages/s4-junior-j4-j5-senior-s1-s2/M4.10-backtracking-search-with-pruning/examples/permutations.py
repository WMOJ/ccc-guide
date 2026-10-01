import sys


def backtrack(elements, used, current, results):
    if len(current) == len(elements):
        results.append(current[:])
        return
    for i in range(len(elements)):
        if used[i]:
            continue
        used[i] = True
        current.append(elements[i])
        backtrack(elements, used, current, results)
        current.pop()
        used[i] = False


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    elements = input_data
    used = [False] * len(elements)
    results = []
    backtrack(elements, used, [], results)
    lines = [" ".join(perm) for perm in results]
    print("\n".join(lines))


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
