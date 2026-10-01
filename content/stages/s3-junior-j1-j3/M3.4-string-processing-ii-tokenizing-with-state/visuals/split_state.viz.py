import vizrec as vz

rec = vz.Recorder()
s = rec.readline()
n = len(s)


def chars_frame(i):
    states = ["done" if pos < i else "_" for pos in range(n)]
    states[i] = "current"
    return vz.array(list(s), states=states, pointers={"i": i})


def tokens_frame(tokens, current_token):
    items = [(t, "done") for t in tokens]
    if current_token:
        items.append((current_token, "current"))
    return vz.queue(items, name="tokens")


tokens = []
current_token = ""
for i, char in enumerate(s):
    if char == ",":
        tokens.append(current_token)
        current_token = ""
        rec.step(
            f"s[{i}] is the delimiter ',': the token '{tokens[-1]}' is complete. A new token starts empty.",
            chars=chars_frame(i),
            tokens=tokens_frame(tokens, current_token),
        )
    else:
        current_token += char
        rec.step(
            f"s[{i}] is '{char}': it joins the current token, now '{current_token}'.",
            chars=chars_frame(i),
            tokens=tokens_frame(tokens, current_token),
        )

if current_token:
    tokens.append(current_token)
    rec.step(
        f"The string ends with '{current_token}' still being built: append it as the last token.",
        chars=chars_frame(n - 1),
        tokens=tokens_frame(tokens, ""),
    )
else:
    rec.step(
        "The string ends right after a delimiter: nothing is left to append.",
        chars=chars_frame(n - 1),
        tokens=tokens_frame(tokens, ""),
    )

rec.output("\n".join(tokens) + "\n")
