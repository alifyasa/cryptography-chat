class Keccak:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate
        self.state = [[0] * 5 for _ in range(5)]
        self.output_length = 256  # Default output length

    @staticmethod
    def rotate_left(x, n):
        return ((x << n) | (x >> (64 - n))) & (2**64 - 1)

    def theta(self):
        C = [self.state[x][0] ^ self.state[x][1] ^ self.state[x][2] ^ self.state[x][3] ^ self.state[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ self.rotate_left(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                self.state[x][y] ^= D[x]

    def rho(self):
        r = [[0, 36, 3, 41, 18],
             [1, 44, 10, 45, 2],
             [62, 6, 43, 15, 61],
             [28, 55, 25, 21, 56],
             [27, 20, 39, 8, 14]]
        for x in range(5):
            for y in range(5):
                self.state[x][y] = self.rotate_left(self.state[x][y], r[x][y])

    def pi(self):
        new_state = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                new_state[y][(2 * x + 3 * y) % 5] = self.state[x][y]
        self.state = new_state

    def chi(self):
        new_state = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                new_state[x][y] = self.state[x][y] ^ ((~self.state[(x + 1) % 5][y]) & self.state[(x + 2) % 5][y])
        self.state = new_state

    def iota(self, round_index):
        RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
              0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
              0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
              0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
              0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
              0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
        self.state[0][0] ^= RC[round_index]

    def keccak_f(self):
        for round_index in range(24):
            self.theta()
            self.rho()
            self.pi()
            self.chi()
            self.iota(round_index)

    def absorb(self, data):
        blocks = [data[i:i + self.rate] for i in range(0, len(data), self.rate)]
        for block in blocks:
            block += b'\x01' + b'\x00' * (self.rate - len(block) - 1)
            for i in range(len(block)):
                self.state[i % 5][i // 5] ^= block[i]
            self.keccak_f()

    def squeeze(self):
        output = b''
        while len(output) < self.output_length // 8:
            for i in range(self.rate // 8):
                output += self.state[i % 5][i // 5].to_bytes(8, 'little')
            self.keccak_f()
        return output[:self.output_length // 8]

    def hash(self, data, output_length=256):
        self.output_length = output_length
        data = bytearray(data)
        self.absorb(data)
        return self.squeeze()

def keccak_hash(data, output_length=256):
    keccak = Keccak(2 * 256, 1600 - 2 * 256)
    return keccak.hash(data, output_length)
