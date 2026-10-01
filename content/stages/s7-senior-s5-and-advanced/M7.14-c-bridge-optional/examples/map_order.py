import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    counts = {}
    for key in tokens:
        counts[key] = counts.get(key, 0) + 1

    in_dict_order = []
    for key, count in counts.items():
        in_dict_order.append(f"{key}:{count}")

    in_map_order = []
    for key, count in sorted(counts.items()):
        in_map_order.append(f"{key}:{count}")

    print("dict", " ".join(in_dict_order))
    print("map ", " ".join(in_map_order))


if __name__ == "__main__":
    main()
