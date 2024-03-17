from Filter import BloomFilter
import hashlib
import zlib
import random

def mod_10_hash(key):
    return key % 10

def division_hash(key):
    return key % 997

def multiplication_hash(key):
    return (key * 2654435761) & 0xFFFFFFFF

def bitwise_xor_hash(key):
    return key ^ (key >> 16)

def sax_hash(key):
    key = (~key) + (key << 21)  # key = (key << 21) - key - 1;
    key = key ^ (key >> 24)
    key = (key + (key << 3)) + (key << 8)  # key * 265
    key = key ^ (key >> 14)
    key = (key + (key << 2)) + (key << 4)  # key * 21
    key = key ^ (key >> 28)
    key = key + (key << 31)
    return key


def mod_9_hash(key):
    return key % 9

def mod_8_hash(key):
    return key % 8

def mod_7_hash(key):
    return key % 7


even_numbers = []
odd_numbers = []

# Generate even and odd numbers between 0 and 9999
for num in range(1000):
    if num % 2 == 0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)



bf = BloomFilter.BloomFilter(5, 1000, 0.1, [division_hash, sax_hash, multiplication_hash, bitwise_xor_hash])
print('Created bloom filter')

for item in odd_numbers:
    bf.insert(item)
#bf.train(even_numbers)
nums = odd_numbers + even_numbers
fp = 0
for item in nums:
    ret = bf.query_nn(item)
    if item not in odd_numbers and ret:
        fp += 1

print('false positive rate = ', fp / 1000)
 