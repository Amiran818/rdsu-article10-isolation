import artfast

assert artfast.gcd(84, 36) == 12
assert artfast.gcd(-7, 0) == 7
assert artfast.popcount(0) == 0
assert artfast.popcount(0xFF00FF) == 16
print("artfast: ok")
