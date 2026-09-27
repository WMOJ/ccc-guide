s = "racecar"

def expand(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return right - left - 1

longest = 0
for i in range(len(s)):
    # Odd length
    length = expand(s, i, i)
    longest = max(longest, length)

    # Even length
    if i < len(s) - 1:
        length = expand(s, i, i + 1)
        longest = max(longest, length)

print(f"Longest palindrome in '{s}': length {longest}")
