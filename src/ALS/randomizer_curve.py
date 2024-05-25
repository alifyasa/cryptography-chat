import random
import os
from Crypto.Util import number

PRIME_NUMBER_SIZE = 256

class RandomizerCurve:
    def __init__(self):
        self.p = self._draw_prime_number()
        self.a, self.b, self.x, self.y = self._draw_parameters(self.p)

    def get_all_parameters(self):
        return self.a, self.b, self.x, self.y, self.p

    def _draw_prime_number(self):
        while True:
            pr = number.getPrime(PRIME_NUMBER_SIZE, os.urandom)
            if pr % 4 == 3:
                return pr

    def _is_delta_valid(self, a, b, p):
        return (4 * a**3 + 27 * b**2) % p != 0

    def _calculate_f(self, a, b, x, p):
        return (x**3 + a * x + b) % p

    def _check_legendre(self, f, p):
        return pow(f, (p - 1) // 2, p) == 1

    def _calculate_y(self, f, p):
        return pow(f, (p + 1) // 4, p)

    def _test_equality(self, y, p, x, a, b):
        y_squared = pow(y, 2, p)
        f_test = (x**3 + a * x + b) % p
        return y_squared == f_test

    def _draw_parameters(self, random_prime):
        while True:
            a = random.randrange(2, random_prime - 1)
            b = random.randrange(2, random_prime - 1)

            if not self._is_delta_valid(a, b, random_prime):
                continue

            x = random.randrange(2, random_prime - 1)
            f = self._calculate_f(a, b, x, random_prime)

            if not self._check_legendre(f, random_prime):
                continue

            y = self._calculate_y(f, random_prime)

            if self._test_equality(y, random_prime, x, a, b):
                return a, b, x, y

if __name__ == "__main__":
    curve = RandomizerCurve()
    a, b, x, y, p = curve.get_all_parameters()
    print(f"Curve parameters:\na: {a}\nb: {b}\nx: {x}\ny: {y}\np: {p}")
