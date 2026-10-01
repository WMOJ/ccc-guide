import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])
    rows = input_data[2:2 + n]

    row_counts = []
    for row in rows:
        vowels = 0
        for ch in row:
            if ch == "a":
                vowels += 1
        row_counts.append(vowels)

    col_counts = []
    for c in range(m):
        vowels = 0
        for row in rows:
            if row[c] == "a":
                vowels += 1
        col_counts.append(vowels)

    rows_ok = min(row_counts) == max(row_counts)
    cols_ok = min(col_counts) == max(col_counts)
    halves_ok = True
    for count in row_counts:
        if count * 2 != m:
            halves_ok = False

    if rows_ok and cols_ok and halves_ok:
        print("valid")
    else:
        print("invalid")


if __name__ == "__main__":
    main()
