from random import randint
from randomizer_curve import RandomizerCurve
from ecc import *

# Key generation function
def generate_key(n, G, a, p):
    private_key = randint(1, n - 1)  # Random integer between 1 and n-1
    public_key = point_multiplication(private_key, G, a, p)
    return private_key, public_key

# Shared secret generation function
def generate_shared_secret(private_key, public_key, a, p):
    shared_secret = point_multiplication(private_key, public_key, a, p)
    return shared_secret[0]  # Return only the x-coordinate as shared secret

if __name__ == "__main__":
    # Initialize curve parameters
    randomizerCurve = RandomizerCurve()
    a, b, gx, gy, p = randomizerCurve.get_all_parameters()
    G = (gx, gy)
    n = 19  # Order of the generator point (this should typically be the order of the base point, needs to be adapted for your curve)

    # Alice's side
    alice_private_key, alice_public_key = generate_key(n, G, a, p)
    print("Alice's private key:", alice_private_key)
    print("Alice's public key:", alice_public_key)

    # Bob's side
    bob_private_key, bob_public_key = generate_key(n, G, a, p)
    print("Bob's private key:", bob_private_key)
    print("Bob's public key:", bob_public_key)

    # Alice computes shared secret
    alice_shared_secret = generate_shared_secret(alice_private_key, bob_public_key, a, p)

    # Bob computes shared secret
    bob_shared_secret = generate_shared_secret(bob_private_key, alice_public_key, a, p)

    # Both should have the same shared secret
    assert alice_shared_secret == bob_shared_secret

    print("Shared Secret:", alice_shared_secret)
