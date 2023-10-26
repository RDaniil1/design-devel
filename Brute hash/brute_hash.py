from hashlib import sha256 
from string import ascii_lowercase
import itertools 
from time import time
from multiprocessing import Pool 
from multiprocessing.pool import ThreadPool
from functools import partial

    
def get_hash_sha256(hashing_str: str):
    encoded_str = str.encode(hashing_str)
    h = sha256(encoded_str)
    return h.hexdigest()

def brute_hash(combination: tuple[str], current_hash: str):
    global curr_hash
    string = ''.join(combination)
    hash_value = get_hash_sha256(string)
    if hash_value == current_hash:
        return string
    return ''

def brute_multiple_threads(permutations, current_hash: str):        
    with Pool() as pool:
        for word in pool.imap(partial(brute_hash, current_hash=current_hash), 
                              permutations, 100000):
            if word:
                print(word)
                break

def brute_one_thread(permutations, current_hash: str):
    while True:
        try:
            next_value = next(permutations)
        except StopIteration:
            break
        string = brute_hash(next_value, current_hash)
        if string:
            print(string)
            break
        
def timer(function):
    def wrapper(hashes, hashing_len, multiple_threads):
        start_time = time()
        function(hashes, hashing_len, multiple_threads)
        print(f'Time {time() - start_time}')
    return wrapper

@timer
def brute(hashes: list[str], hashing_len: int, multiple_threads: bool):
    brute_func = brute_multiple_threads if multiple_threads else brute_one_thread
    for current_hash in hashes:
        permutations = itertools.product(ascii_lowercase, repeat=hashing_len)
        brute_func(permutations, current_hash)

if __name__ == '__main__':
    hashing_len = 5
    hashes = ['1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad', 
              '3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b', 
              '74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f']
    
    brute(hashes, hashing_len, multiple_threads=True)
    brute(hashes, hashing_len, multiple_threads=False)