s = input()
tokens = []
current_token = ""

for char in s:
    if char == ",":
        tokens.append(current_token)
        current_token = ""
    else:
        current_token += char

if current_token:
    tokens.append(current_token)

for token in tokens:
    print(token)
