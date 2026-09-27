import math

red_plates = 18
blue_plates = 24
shared_factor = math.gcd(red_plates, blue_plates)

print(red_plates // shared_factor, blue_plates // shared_factor)
print(math.comb(6, 2))
