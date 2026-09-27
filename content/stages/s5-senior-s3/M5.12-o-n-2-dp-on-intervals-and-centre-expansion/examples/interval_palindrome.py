s = "ababa"
n = len(s)

dp = [[False] * n for _ in range(n)]

# Every single character is a palindrome
for i in range(n):
    dp[i][i] = True

# Check pairs and longer
for length in range(2, n + 1):
    for l in range(n - length + 1):
        r = l + length - 1
        # A pair, or a longer interval whose inner part is a palindrome
        if s[l] == s[r] and (length == 2 or dp[l + 1][r - 1]):
            dp[l][r] = True

# Count palindromes
count = 0
for l in range(n):
    for r in range(l, n):
        if dp[l][r]:
            count += 1
            print(f"Palindrome: {s[l:r+1]}")

print(f"Total: {count}")
