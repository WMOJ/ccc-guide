import sys


def add_one_in_place(values: list) -> None:
    for i in range(len(values)):
        values[i] += 1


def add_one_to_copy(values: list) -> list:
    copy = values[:]
    for i in range(len(copy)):
        copy[i] += 1
    return copy


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    values = []
    for token in tokens:
        values.append(int(token))

    made = add_one_to_copy(values)
    print("after copy", values, made)
    add_one_in_place(values)
    print("after in place", values)


if __name__ == "__main__":
    main()
