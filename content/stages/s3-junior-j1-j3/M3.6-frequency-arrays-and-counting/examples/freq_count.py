word = input()
freq = [0] * 26

for char in word:
    if 'a' <= char <= 'z':
        index = ord(char) - ord('a')
        freq[index] += 1

for i in range(26):
    if freq[i] > 0:
        letter = chr(ord('a') + i)
        print(f"{letter}: {freq[i]}")
