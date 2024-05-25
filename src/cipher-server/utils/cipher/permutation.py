from utils.constant import P_BOX, INV_P_BOX

def permutate(input_int: int) -> int:
    """
    Permutate half-byte
    """
    output_int = 0  # Initialize the output integer
    for input_pos, output_pos in enumerate(P_BOX):
        # Extract the bit at the current input position
        input_bit = (input_int >> input_pos) & 1
        # Set the extracted bit at the corresponding output position
        output_int |= (input_bit << output_pos)
    
    return output_int

def inv_permutate(input_int: int) -> int :
    """
    Inverse permutate half-byte
    """
    output_int = 0  # Initialize the output integer
    for input_pos, output_pos in enumerate(INV_P_BOX):
        # Extract the bit at the current input position
        input_bit = (input_int >> input_pos) & 1
        # Set the extracted bit at the corresponding output position
        output_int |= (input_bit << output_pos)
    
    return output_int

def test():
    print("===== PERMUTATION TEST =====")
    input_int = 260603
    print(f"Original  : {input_int:064b}")
    permutated_int = permutate(input_int)
    print(f"Permutated: {permutated_int:064b}")
    original_int = inv_permutate(permutated_int)
    print(f"Original  : {original_int:064b}")

if __name__ == "__main__":
    test()