import sys


def matches(s: str) -> bool:
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack = []
    for c in s:
        if c in pairs:
            stack.append(c)
        else:
            if not stack or pairs[stack.pop()] != c:
                return False
    return len(stack) == 0


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    s = input_data[0]
    sys.stdout.write(f"{matches(s)}\n")


if __name__ == "__main__":
    main()
