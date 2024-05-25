from utils.cipher.substitution import substitute
from utils.cipher.permutation import permutate
# from substitution import substitute
# from permutation import permutate

def round_function(feistel_half: int, round_key: int):
    # block is 128 bit/16 bytes, half is 64 bit/8 bytes

    substituted = substitute(feistel_half, round_key)
    return permutate(substituted)

def feistel_round(left: int, right, round_key: int) -> int:
    """
    Single round of the Feistel network.
    
    Parameters:
    left (int): Left half of the data.
    right (int): Right half of the data.
    round_key (int): Key for this round.
    
    Returns:
    tuple: New left and right halves.
    """
    new_right = left ^ round_function(right, round_key)
    new_left = right
    
    return new_left, new_right

def feistel_network(data: int, sub_keys: int, decrypt=False) -> int:
    """
    Simple Feistel network implementation.
    
    Parameters:
    data (int): Input data to be encrypted/decrypted.
    keys (list): List of keys for each round.
    
    Returns:
    int: Encrypted or decrypted data.
    """

    # Needs 10 - 16 subkeys
    # assert len(sub_keys) >= 10 and len(sub_keys) <= 16

    # Data is 16 bytes or 128 bit
    # 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF 
    left  = data >> 64
    right = data & 0xFFFFFFFFFFFFFFFF

    # If decrypting, reverse the order of the round keys
    if decrypt:
        sub_keys = sub_keys[::-1]
    
    # Perform rounds
    for round_key in sub_keys:
        # print(f"Feistel Key {round_key} - LEFT : {left:064b}")
        # print(f"Feistel Key {round_key} - RIGHT: {right:064b}")
        left, right = feistel_round(left, right, round_key)
    
    # Recombine halves
    return (right << 64) | left

def test():
    data = 26062003
    sub_keys = list(range(16))

    print(f"Data          : {data:0128b}")
    feisteled = feistel_network(data, sub_keys)
    print(f"Feistel Result: {feisteled:0128b}")
    original = feistel_network(feisteled, sub_keys, decrypt=True)
    print(f"Original      : {original:0128b}")

if __name__ == "__main__":
    test()