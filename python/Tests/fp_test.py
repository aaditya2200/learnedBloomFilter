from python.Filter.BloomFilter import BloomFilter
from python.Hashes import hash
hash_lib = hash.Hash()
bf = BloomFilter(4, 1000, 0.1, [hash_lib.division_hash, hash_lib.sax_hash, hash_lib.multiplication_hash,
                                            hash_lib.bitwise_xor_hash])
even_numbers = []
odd_numbers = []
hash_lib = hash.Hash()
# Generate even and odd numbers between 0 and 9999
for num in range(1000):
    if num % 2 == 0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)

for item in odd_numbers:
    bf.insert(item)

for num in even_numbers:
    if bf.query(num) and bf.query_nn(num):
        print('Found FP')


