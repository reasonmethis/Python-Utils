import hashlib

def hash_one(n):
    """A somewhat CPU-intensive task. 
    
    From https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html"""

    for i in range(1, n):
        hashlib.pbkdf2_hmac("sha256", b"password", b"salt", i * 10000)

    return "done"
