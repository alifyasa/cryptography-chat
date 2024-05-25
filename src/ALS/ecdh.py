from random import randint

# Elliptic Curve Point Addition
def point_addition(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2

    if p1 == p2:
        m = ((3 * x1 * x1 + a) * pow(2 * y1, -1, p)) % p
    else:
        m = ((y2 - y1) * pow(x2 - x1, -1, p)) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

# Elliptic Curve Point Multiplication
def point_multiplication(k, p):
    result = None
    addend = p
    while k:
        if k & 1:
            result = point_addition(result, addend)
        addend = point_addition(addend, addend)
        k >>= 1
    return result

# Key generation function
def generate_key():
    private_key = randint(1, n-1)  # Random integer between 1 and n-1
    public_key = point_multiplication(private_key, G)
    return private_key, public_key

# Shared secret generation function
def generate_shared_secret(private_key, public_key):
    shared_secret = point_multiplication(private_key, public_key)
    return shared_secret[0]  # Return only the x-coordinate as shared secret

if __name__ == "__main__":
    # Elliptic Curve parameters
    # We'll use a simple curve y^2 = x^3 + ax + b (mod p)
    a = 2
    b = 2
    p = 17  # Prime number
    G = (15, 13)  # Base point (generator point)
    n = 19  # Order of the generator point
    
    # Alice's side
    alice_private_key, alice_public_key = generate_key()

    # Bob's side
    bob_private_key, bob_public_key = generate_key()

    # Alice computes shared secret
    alice_shared_secret = generate_shared_secret(alice_private_key, bob_public_key)

    # Bob computes shared secret
    bob_shared_secret = generate_shared_secret(bob_private_key, alice_public_key)

    # Both should have the same shared secret
    assert alice_shared_secret == bob_shared_secret

    print("Shared Secret:", alice_shared_secret)