from Filter import BloomFilter
import hashlib
import zlib
import random

def mod_10_hash(key):
    return key % 10

def mod_9_hash(key):
    return key % 9

def mod_8_hash(key):
    return key % 8

def mod_7_hash(key):
    return key % 7


bf = BloomFilter.BloomFilter(5, 1000, 0.1, [mod_7_hash, mod_8_hash, mod_9_hash, mod_10_hash])
print('Created bloom filter')
# Test this out
# Idea: first generate 1000 random numbers, and insert them
# Next:
rand_nums = []
for i in range(0, 1000):
    rand_nums.append(random.randint(0, 999999))

save_nums = rand_nums[500:]
for item in rand_nums:
    bf.insert(item)

for i in range(0, 500):
    save_nums.append(random.randint(0, 999999))

fp = 0

for item in save_nums:
    ret = bf.query(item)
    if item not in rand_nums and ret:
        fp += 1

print('false positive rate = ', fp / 1000)
 