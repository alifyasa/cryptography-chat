from ecc import *
from keccak_hash import *
from random import randint
from keccak import *
from ecdh import *

def sign_message(private_key, message, G, n, a, p):
    z = int.from_bytes(keccak_hash(message), byteorder='big')
    r, s = 0, 0
    while r == 0 or s == 0:
        k = randint(1, n - 1)
        x, y = point_multiplication(k, G, a, p)
        r = x % n
        s = ((z + r * private_key) * mod_inverse(k, n)) % n
    return (r, s)

def verify_signature(public_key, message, signature, G, n, a, p):
    r, s = signature
    if not (1 <= r < n and 1 <= s < n):
        return False
    z = int.from_bytes(keccak_hash(message), byteorder='big')
    w = mod_inverse(s, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    x1, y1 = point_multiplication(u1, G, a, p)
    x2, y2 = point_multiplication(u2, public_key, a, p)
    x, y = point_addition((x1, y1), (x2, y2), a, p)
    return (x % n) == r

# Example Usage
if __name__ == "__main__":
    # Initialize curve parameters
    a = 2
    b = 3
    p = 17
    n = 19
    G = (5, 1)

    # Generate keys
    private_key, public_key = generate_key(n, G, a, p)
    print("Private Key:", private_key)
    print("Public Key:", public_key)

    # Sign a message
    message = b"Pesan untuk ditandatangani"
    signature = sign_message(private_key, message, G, n, a, p)
    print("Signature:", signature)

    # Verify the signature
    is_valid = verify_signature(public_key, message, signature, G, n, a, p)
    print("Is signature valid?", is_valid)
