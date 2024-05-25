import galois
# pip install galois

GF = galois.GF(2**8, irreducible_poly=501) # AES pakai 283

def gf_mult(a, b):
    """
    Multiply two numbers in the GF(2^8) finite field defined 
    by the polynomial x^8 + x^4 + x^3 + x + 1.
    """
    # Convert inputs to elements of GF(2^8)
    a_gf = GF(a)
    b_gf = GF(b)
    
    # Perform multiplication in GF(2^8)
    result = a_gf * b_gf
    
    return int(result)

def gf_invert(number):
    """
    Inverts a number in GF(2^8) using the Extended Euclidean Algorithm.
    """
    # Convert input to an element of GF(2^8)
    number_gf = GF(number)
    
    # Find the multiplicative inverse in GF(2^8)
    if number_gf == 0:
        return 0
    else:
        return int(number_gf ** -1)

def circular_left_shift(byte, num):
    return ((byte << num) % (1 << 8)) | (byte >> (8 - num))

def affine_transformation(byte):
    return (
        byte 
        ^ circular_left_shift(byte, 1) 
        ^ circular_left_shift(byte, 2)
        ^ circular_left_shift(byte, 3)
        ^ circular_left_shift(byte, 4)
        ^ 0x63
    )


def generate_s_box():
    s_box = [0] * 256
    for i in range(256):
        inv = gf_invert(i)
        s_box[i] = affine_transformation(int(inv))
    return s_box

def generate_inverse_s_box(s_box):
    result = [0] * 256
    for idx, val in enumerate(s_box):
        result[val] = idx
    return result

def pprint(s_box, hex=False):
    for i in range(16):
        if hex:
            print(', '.join(f'{x:02x}' for x in s_box[i*16:(i+1)*16]), end=",\n")
        else:
            print(', '.join(f'{x:>3}' for x in s_box[i*16:(i+1)*16]), end=",\n")


def main():
    s_box = generate_s_box()
    print("S-BOX")
    pprint(s_box)

    inv_s_box = generate_inverse_s_box(s_box)
    print("INV S-BOX")
    pprint(inv_s_box)



if __name__ == "__main__":
    main()