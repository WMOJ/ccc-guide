import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    numbers = list(range(n))

    seen_list = []
    list_ops = 0
    for num in numbers:
        for value in seen_list:
            list_ops += 1
            if value == num:
                break
        seen_list.append(num)

    seen_set = set()
    set_ops = 0
    for num in numbers:
        set_ops += 1
        if num in seen_set:
            pass
        seen_set.add(num)

    print(list_ops, set_ops)


if __name__ == "__main__":
    main()
