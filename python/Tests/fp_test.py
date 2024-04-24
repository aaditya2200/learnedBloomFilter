from python.Filter.BloomFilter import BloomFilter
from python.Hashes import hash
from interface import api
hash_lib = hash.Hash()
lbf = api.LearnedBloomFilter(api.MODE.DEBUG)
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
    lbf.insert(item)

for num in even_numbers:
    if lbf.query(num):
        print('Found FP')


