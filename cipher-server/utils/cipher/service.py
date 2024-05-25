from utils.cipher.subkey import generate_sub_keys
from utils.cipher.feistel import feistel_network
# from subkey import generate_sub_keys
# from feistel import feistel_network

def encrypt_block(block_plaintext: int, key: int) -> int:
    data_len = len(f"{block_plaintext:08b}")
    assert data_len <= 128, f"Input size {data_len}, expected input size <= 128"
    sub_keys = generate_sub_keys(key, 16)
    ciphertext = feistel_network(block_plaintext, sub_keys)
    return ciphertext

def decrypt_block(block_ciphertext:int, key: int) -> int:
    data_len = len(f"{block_ciphertext:08b}")
    assert data_len <= 128, f"Input size {data_len}, expected input size <= 128"
    key_len = len(f"{key:08b}")
    assert data_len <= 128, f"Key size {key_len}, expected key size <= 128"
    sub_keys = generate_sub_keys(key, 16)
    plaintext = feistel_network(block_ciphertext, sub_keys, decrypt=True)
    return plaintext

def char_string_to_int(char_string: str) -> int:
    return int(''.join(format(ord(char), '08b') for char in char_string), 2)

def int_to_char_string(num: int) -> str:
    binary_str = bin(num)[2:]

    padding_length = 8 - (len(binary_str) % 8)
    padded_binary_str = ('0' * padding_length + binary_str) if padding_length < 8 else binary_str
    
    chars = [chr(int(padded_binary_str[i:i+8], 2)) for i in range(0, len(padded_binary_str), 8)]
    
    return ''.join(chars)

def test():
    plaintext = "najkdnjkandajnsd"
    key = "alifyasa"
    print(f"Char Plaintext : {plaintext}")

    formatted_plaintext = char_string_to_int(plaintext)
    formatted_key = char_string_to_int(key)
    print(f"Bit Plaintext  : {formatted_plaintext:0128b}")
    print(f"Bit Key        : {formatted_key:0128b}")

    ciphertext = encrypt_block(formatted_plaintext, formatted_key)
    print(f"Bit Ciphertext : {ciphertext:0128b}")

    decrypted_ciphertext = decrypt_block(ciphertext, formatted_key)
    print(f"Bit Decrypted  : {decrypted_ciphertext:0128b}")
    print(f"Char Plaintext : {int_to_char_string(decrypted_ciphertext)}")

    print(f"Is Decrypted == Plaintext? {decrypted_ciphertext == formatted_plaintext}")

if __name__ == "__main__":
    test()