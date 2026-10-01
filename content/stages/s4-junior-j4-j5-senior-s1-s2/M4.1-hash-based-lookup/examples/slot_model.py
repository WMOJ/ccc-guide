import sys

SLOTS = 8


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    pos = 0
    n = int(data[pos])
    pos += 1

    table = [None] * SLOTS
    lines = []
    for _ in range(n):
        code = int(data[pos])
        pos += 1
        slot = code % SLOTS
        while table[slot] is not None and table[slot] != code:
            slot = (slot + 1) % SLOTS
        table[slot] = code
        lines.append(f"{code} -> slot {slot}")

    q = int(data[pos])
    pos += 1
    for _ in range(q):
        code = int(data[pos])
        pos += 1
        slot = code % SLOTS
        while table[slot] is not None and table[slot] != code:
            slot = (slot + 1) % SLOTS
        found = table[slot] == code
        verdict = "found" if found else "missing"
        lines.append(f"lookup {code}: {verdict} at slot {slot}")

    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
