from utils.constant import S_BOX, INV_S_BOX

def substitute(input_int: int, round_key: int) -> int:
    """
    Substitute half-block
    """
    result = 0
    for i in range(8):  # Process each of the 8 bytes in the 64-bit input
        byte_segment = (input_int >> (8*i)) & 0xFF  # Extract ith byte
        round_key_segment = (round_key >> (8*i)) & 0xFF  # Extract ith byte of round_key
        substituted = S_BOX[byte_segment ^ round_key_segment]
        result |= (substituted << (8*i))  # Place back into the result
    return result

def inv_substitute(input_int: int, round_key: int) -> int:
    """
    Inverse substitute half-block
    """
    result = 0
    for i in range(8):
        byte_segment = (input_int >> (8*i)) & 0xFF  # Extract ith byte
        inv_substituted = INV_S_BOX[byte_segment]
        round_key_segment = (round_key >> (8*i)) & 0xFF  # Extract ith byte of round_key
        result |= ((inv_substituted ^ round_key_segment) << (8*i))  # Place back into the result
    return result

def test():
    print("===== SUBSTITUTION TEST =====")
    input_int = 260603
    input_key = 260603
    print(f"Original   : {input_int:064b}")
    substituted_int = substitute(input_int, input_key)
    print(f"Substituted: {substituted_int:064b}")
    original_int = inv_substitute(substituted_int, input_key)
    print(f"Original   : {original_int:064b}")

if __name__ == "__main__":
    test()