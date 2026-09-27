s = input()
result = ""
i = 0

while i < len(s):
    current_char = s[i]
    count = 1

    while i + count < len(s) and s[i + count] == current_char:
        count += 1

    result += str(count) + current_char
    i += count

print(result)
