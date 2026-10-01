import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    m = int(input_data[0])

    if m <= 2:
        print("Impossible")
        return

    half = (m + 1) // 2
    result = [""] * m
    for i in range(half):
        ch = "a"
        if i == half - 1:
            ch = "b"
        result[i] = ch
        result[m - 1 - i] = ch

    print("".join(result))


if __name__ == "__main__":
    main()
