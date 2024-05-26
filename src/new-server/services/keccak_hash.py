from keccak import Keccak

def keccak_hash(data, output_length=256):
    keccak = Keccak(2 * 256, 1600 - 2 * 256)
    return keccak.hash(data, output_length)

# Contoh penggunaan
if __name__ == "__main__":
    message = b"Pesan untuk di-hash menggunakan Keccak"
    hash_value = keccak_hash(message)
    print("Hash value:", hash_value.hex())