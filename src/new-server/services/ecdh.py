from random import randint
from services.randomizer_curve import RandomizerCurve
from services.ecc import *

# Key generation function
def generate_key(n, G, a, p):
    private_key = randint(1, n - 1)
    public_key = point_multiplication(private_key, G, a, p)
    return private_key, public_key

# Shared secret generation function
def generate_shared_secret(private_key, public_key, a, p):
    shared_secret = point_multiplication(private_key, public_key, a, p)
    return shared_secret[0]  # Return only the x-coordinate as shared secret

# Define curve parameters and generate keys
def get_all_key_ECDH():
    randomizer_curve = RandomizerCurve()
    a, b, gx, gy, p, n = randomizer_curve.get_all_parameters()  # Including the order n
    G = (gx, gy)

    # Alice's side
    alice_private_key, alice_public_key = generate_key(n, G, a, p)

    # Bob's side
    bob_private_key, bob_public_key = generate_key(n, G, a, p)

    # Alice computes shared secret
    alice_shared_secret = generate_shared_secret(alice_private_key, bob_public_key, a, p)

    # Bob computes shared secret
    bob_shared_secret = generate_shared_secret(bob_private_key, alice_public_key, a, p)

    # Both should have the same shared secret
    assert alice_shared_secret == bob_shared_secret

    # Save keys to files
    with open("alice_private_key.ecprv", "w") as f:
        f.write(str(alice_private_key))
    with open("alice_public_key.ecpub", "w") as f:
        f.write(str(alice_public_key))
    with open("bob_private_key.ecprv", "w") as f:
        f.write(str(bob_private_key))
    with open("bob_public_key.ecpub", "w") as f:
        f.write(str(bob_public_key))

    return bob_private_key, bob_public_key, alice_private_key, alice_public_key, alice_shared_secret

if __name__ == "__main__":
    # Initialize curve parameters
    bob_priv_key, bob_pub_key, alice_priv_key, alice_pub_key, shared_key = get_all_key_ECDH()

    print("Bob's private key:", bob_priv_key)
    print("Bob's public key:", bob_pub_key)

    print("Alice's private key:", alice_priv_key)
    print("Alice's public key:", alice_pub_key)

    print("Shared secret:", shared_key)