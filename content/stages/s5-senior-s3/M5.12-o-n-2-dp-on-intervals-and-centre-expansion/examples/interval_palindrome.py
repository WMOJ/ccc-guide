import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    s = input_data[0]
    n = len(s)

    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True

    count = n
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            inner_ok = length == 2 or is_pal[left + 1][right - 1]
            if s[left] == s[right] and inner_ok:
                is_pal[left][right] = True
                count += 1
                print(f"length {length}: '{s[left:right + 1]}'")

    print(f"total: {count}")


if __name__ == "__main__":
    main()
