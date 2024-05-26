from sympy.ntheory import isprime
from sympy import nextprime
import random

def generate_prime(bits):
    p = nextprime(random.getrandbits(bits))
    while not isprime(p):
        p = nextprime(p)
    return p

def generate_alpha_p_q(bits=256):
    q = generate_prime(bits)
    p = 2*q + 1
    while not isprime(p):
        q = generate_prime(bits)
        p = 2*q + 1
    alpha = pow(random.randint(2, p - 2), 2, p)
    return alpha, p, q

SCHNORR_ALPHA, SCHNORR_P, SCHNORR_Q = generate_alpha_p_q()