"""
@author Aaditya and Sam Blesswin
@version 0.1
@since 17-03-2024
NOT FOR USE, THIS IS ONLY TEST CODE
"""
from Filter import BloomFilter
from Hashes import hash

even_numbers = []
odd_numbers = []
hash_lib = hash.Hash()
# Generate even and odd numbers between 0 and 9999
for num in range(1000):
    if num % 2 == 0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)

bf = BloomFilter.BloomFilter(5, 1000, 0.1, [hash_lib.division_hash, hash_lib.sax_hash, hash_lib.multiplication_hash,
                                            hash_lib.bitwise_xor_hash])
print('Created bloom filter')

for item in odd_numbers:
    bf.insert(item)
# bf.train(even_numbers)
nums = odd_numbers + even_numbers
fp = 0
for item in nums:
    ret = bf.query_nn(item)
    if item not in odd_numbers and ret:
        fp += 1

print('false positive rate = ', fp / 1000)
