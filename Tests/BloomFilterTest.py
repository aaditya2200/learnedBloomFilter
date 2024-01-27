from Filter import BloomFilter
import hashlib
import zlib

def sha1_hash(key):
    return int(hashlib.sha1(key.encode()).hexdigest(), 16)

def md5_hash(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

def sha256_hash(key):
    return hashlib.sha256(key.encode()).hexdigest()

def crc32_hash(key):
    return zlib.crc32(key.encode())

bf = BloomFilter.BloomFilter(5, 1000, 0.1, [sha256_hash, sha1_hash, md5_hash, crc32_hash])
print('Created bloom filter')
