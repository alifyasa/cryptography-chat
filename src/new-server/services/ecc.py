# Elliptic Curve Point Addition
def mod_inverse(k, p):
    """Return the modular inverse of k modulo p."""
    return pow(k, p - 2, p)

def point_addition(p1, p2, a, p):
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 == y2:
        if y1 == 0:  # Case when tangent is vertical, point at infinity
            return None
        # Point doubling
        m = ((3 * x1**2 + a) * mod_inverse(2 * y1, p)) % p
    else:
        if x1 == x2:
            return None  # Point at infinity
        m = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def point_multiplication(k, point, a, p):
    result = None
    addend = point

    while k:
        if k & 1:
            result = point_addition(result, addend, a, p)
        addend = point_addition(addend, addend, a, p)
        k >>= 1

    return result
