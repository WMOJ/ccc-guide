import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    fields = input_data[1:n+1]

    crop_count = {}
    for crop in fields:
        crop_count[crop] = crop_count.get(crop, 0) + 1

    result = sum(1 for count in crop_count.values() if count > 1)
    sys.stdout.write(str(result) + "\n")


if __name__ == "__main__":
    main()
