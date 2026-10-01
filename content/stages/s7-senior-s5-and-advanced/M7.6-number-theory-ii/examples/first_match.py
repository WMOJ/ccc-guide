import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    a = int(tokens[0])
    r = int(tokens[1])
    b = int(tokens[2])
    s = int(tokens[3])
    x = a
    y = b
    while y != 0:
        x, y = y, x % y
    g = x
    limit = b // g
    print(f"candidates to try: {limit}")
    for k in range(limit):
        t = r + a * k
        if t % b == s:
            print(f"smallest t: {t}")
            return
    print("no t")


if __name__ == "__main__":
    main()
