s = "ababa"
n = len(s)

longest = [0] * n

for i in range(n):
    # Odd length: expand from i
    left, right = i, i
    while left >= 0 and right < n and s[left] == s[right]:
        longest[i] = max(longest[i], right - left + 1)
        left -= 1
        right += 1

    # Even length: expand from between i and i+1
    if i < n - 1:
        left, right = i, i + 1
        while left >= 0 and right < n and s[left] == s[right]:
            longest[i] = max(longest[i], right - left + 1)
            left -= 1
            right += 1

print("Longest palindrome from each position:", longest)
print(f"Overall longest: {max(longest)}")
