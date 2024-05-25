from random import randint
from randomizer_curve import RandomizerCurve
from ecc import *

# Key generation function
def generate_key(n, G, a, b, p):
    private_key = randint(1, n - 1)  # Random integer between 1 and n-1
    public_key = point_multiplication(private_key, G, a, b, p)
    return private_key, public_key

# Shared secret generation function
def generate_shared_secret(private_key, public_key, a, b, p):
    shared_secret = point_multiplication(private_key, public_key, a, b, p)
    return shared_secret[0]  # Return only the x-coordinate as shared secret

def getAllKeyECDH():
    randomizerCurve = RandomizerCurve()
    a, b, gx, gy, p, n = randomizerCurve.get_all_parameters()  # Including the order n
    G = (gx, gy)

    # Alice's side
    alice_private_key, alice_public_key = generate_key(n, G, a, b, p)

    # Bob's side
    bob_private_key, bob_public_key = generate_key(n, G, a, b, p)

    # Alice computes shared secret
    alice_shared_secret = generate_shared_secret(alice_private_key, bob_public_key, a, b, p)

    # Bob computes shared secret
    bob_shared_secret = generate_shared_secret(bob_private_key, alice_public_key, a, b, p)

    # Both should have the same shared secret
    assert alice_shared_secret == bob_shared_secret

    return bob_private_key, bob_public_key, alice_private_key, alice_public_key, alice_shared_secret

if __name__ == "__main__":
    # Initialize curve parameters
    bobPrivKey, bobPubKey, alicePrivKey, alicePubKey, sharedKey = getAllKeyECDH()

    print("Bob's private key:", bobPrivKey)
    print("Bob's public key:", bobPubKey)

    print("Alice's private key:", alicePrivKey)
    print("Alice's public key:", alicePubKey)

    print("Shared secret:", sharedKey)
