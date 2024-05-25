from utils.cipher.feistel import feistel_network
from utils.constant import EULER_NNUMBER
# from feistel import feistel_network

def generate_sub_keys(key: int, round_size: int):
    sub_keys = [0] * round_size
    for i in range(round_size):
        sub_keys[i] = feistel_network(key, EULER_NNUMBER[i * 16: (i + 1) * 16])
    return sub_keys

def test():
    key = 26062003
    print(f"Key           : {key:0128b}")
    sub_keys = generate_sub_keys(key, 16)
    for idx, sub_key in enumerate(sub_keys):
        print(f"Sub-Key {idx:>2d}    : {sub_key:0128b}")

if __name__ == "__main__":
    test()